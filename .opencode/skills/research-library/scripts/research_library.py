from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

REGISTRY_VERSION = 2

LIFECYCLE = [
    "new",
    "extracted",
    "grounded",
    "ideas_created",
    "series_planned",
    "drafted",
    "qa_approved",
    "scheduled",
    "published",
]

EXCEPTIONAL_STATES = {"failed", "ignored"}
VALID = set(LIFECYCLE) | EXCEPTIONAL_STATES


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _new_registry() -> dict[str, Any]:
    return {
        "version": REGISTRY_VERSION,
        "updated_at": now(),
        "sources": {},
    }


def _as_path_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(x) for x in value if x]
    return []


def migrate_registry(data: dict[str, Any]) -> dict[str, Any]:
    """
    Upgrade older registry records in memory while preserving existing data.
    The migration is intentionally additive.
    """
    if not isinstance(data, dict):
        raise ValueError("Registry root must be a JSON object.")

    data.setdefault("sources", {})
    data.setdefault("updated_at", now())

    for source_id, record in data["sources"].items():
        if not isinstance(record, dict):
            raise ValueError(f"Invalid source record for {source_id}")

        record.setdefault("source_id", source_id)
        record.setdefault("paths", _as_path_list(record.get("primary_path")))
        record["paths"] = sorted(set(_as_path_list(record.get("paths"))))

        record.setdefault("active_paths", list(record["paths"]))
        record.setdefault("missing_paths", [])
        record.setdefault("stale_paths", [])

        artifacts = record.get("artifacts")
        if not isinstance(artifacts, dict):
            artifacts = {}
        normalized_artifacts: dict[str, list[str]] = {}
        for stage, values in artifacts.items():
            normalized_artifacts[str(stage)] = sorted(set(_as_path_list(values)))
        record["artifacts"] = normalized_artifacts

        record.setdefault("history", [])
        record.setdefault("error", None)
        record.setdefault("revision_of", None)
        record.setdefault("revised_by", [])
        record.setdefault("revision_root", None)
        record.setdefault("revision_number", 1)

        if record.get("revision_of") and not record.get("revision_root"):
            parent = data["sources"].get(record["revision_of"], {})
            record["revision_root"] = (
                parent.get("revision_root")
                or parent.get("revision_of")
                or record["revision_of"]
            )

        record["revised_by"] = sorted(set(_as_path_list(record.get("revised_by"))))

    data["version"] = REGISTRY_VERSION
    return data


def load(path: str | Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        return _new_registry()

    data = json.loads(path.read_text(encoding="utf-8"))
    return migrate_registry(data)


def save(path: str | Path, data: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data["version"] = REGISTRY_VERSION
    data["updated_at"] = now()

    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


def allocate_source_id(
    registry: dict[str, Any],
    digest: str,
    min_prefix: int = 12,
) -> str:
    """
    Return a deterministic collision-safe source ID.

    Same full hash -> same source ID.
    Different hashes that share the initial prefix -> extend the prefix
    until the candidate is unique.
    """
    sources = registry.get("sources", {})

    for source_id, record in sources.items():
        if record.get("sha256") == digest:
            return source_id

    min_prefix = max(1, min(min_prefix, len(digest)))

    for length in range(min_prefix, len(digest) + 1):
        candidate = f"SRC-{digest[:length]}"
        existing = sources.get(candidate)

        if existing is None:
            return candidate

        if existing.get("sha256") == digest:
            return candidate

    # Reaching this point would require an impossible registry inconsistency:
    # the full digest ID exists but belongs to a different digest.
    raise RuntimeError(
        "Unable to allocate collision-safe source ID for digest "
        f"{digest}. Registry may be inconsistent."
    )


def _record_paths(record: dict[str, Any]) -> list[str]:
    paths = set(_as_path_list(record.get("paths")))
    primary = record.get("primary_path")
    if primary:
        paths.add(str(primary))
    return sorted(paths)


def _choose_primary(record: dict[str, Any]) -> str | None:
    stale = set(_as_path_list(record.get("stale_paths")))
    candidates = [
        p
        for p in _record_paths(record)
        if p not in stale and Path(p).exists()
    ]
    return sorted(candidates)[0] if candidates else None


def refresh_path_state(record: dict[str, Any]) -> bool:
    """
    Refresh existence-based path state.

    `stale_paths` means a scan has observed that the path now contains
    different content. Existing-but-unscanned paths are not rehashed here.
    Extraction performs full hash verification before reading a source.
    """
    changed = False
    paths = _record_paths(record)
    stale = set(_as_path_list(record.get("stale_paths")))

    active = sorted(p for p in paths if p not in stale and Path(p).exists())
    missing = sorted(p for p in paths if not Path(p).exists())

    if record.get("paths") != paths:
        record["paths"] = paths
        changed = True

    if record.get("active_paths") != active:
        record["active_paths"] = active
        changed = True

    if record.get("missing_paths") != missing:
        record["missing_paths"] = missing
        changed = True

    primary = record.get("primary_path")
    if not primary or primary in stale or not Path(primary).exists():
        new_primary = active[0] if active else None
        if new_primary != primary:
            record["primary_path"] = new_primary
            record.setdefault("history", []).append(
                {
                    "at": now(),
                    "event": "primary_path_changed",
                    "from": primary,
                    "to": new_primary,
                }
            )
            changed = True

    return changed


def resolve_source_path(record: dict[str, Any]) -> Path:
    """
    Resolve a content-valid path for extraction.

    Every existing candidate is hash-verified against the registered SHA-256.
    If the current primary is stale or missing, another registered copy is
    selected and promoted to primary_path.
    """
    expected = record.get("sha256")
    if not expected:
        raise RuntimeError("Source record is missing sha256.")

    candidates: list[str] = []
    primary = record.get("primary_path")
    if primary:
        candidates.append(str(primary))

    for p in _record_paths(record):
        if p not in candidates:
            candidates.append(p)

    active: list[str] = []
    missing: list[str] = []
    stale: list[str] = []

    for value in candidates:
        path = Path(value)
        if not path.exists():
            missing.append(str(path))
            continue
        if not path.is_file():
            stale.append(str(path))
            continue

        try:
            digest = sha256(path)
        except OSError:
            stale.append(str(path))
            continue

        if digest == expected:
            active.append(str(path.resolve()))
        else:
            stale.append(str(path.resolve()))

    record["active_paths"] = sorted(set(active))
    record["missing_paths"] = sorted(set(missing))
    record["stale_paths"] = sorted(set(stale))

    if not active:
        old_primary = record.get("primary_path")
        record["primary_path"] = None
        if old_primary is not None:
            record.setdefault("history", []).append(
                {
                    "at": now(),
                    "event": "primary_path_changed",
                    "from": old_primary,
                    "to": None,
                }
            )
        raise RuntimeError(
            "No registered path currently contains the source's registered content."
        )

    selected = active[0]
    old_primary = record.get("primary_path")

    if old_primary not in active:
        record["primary_path"] = selected
        record.setdefault("history", []).append(
            {
                "at": now(),
                "event": "primary_path_changed",
                "from": old_primary,
                "to": selected,
            }
        )
    else:
        selected = old_primary

    return Path(selected)


def _source_timestamp(record: dict[str, Any]) -> str:
    return str(record.get("discovered_at") or "")


def prior_same_path(
    registry: dict[str, Any],
    path: str | Path,
    digest: str,
) -> str | None:
    target = str(Path(path).resolve())
    candidates: list[tuple[str, int, str]] = []

    for source_id, record in registry.get("sources", {}).items():
        if record.get("sha256") == digest:
            continue

        known = set(_record_paths(record))
        if target not in known:
            continue

        candidates.append(
            (
                _source_timestamp(record),
                int(record.get("revision_number") or 1),
                source_id,
            )
        )

    if not candidates:
        return None

    return sorted(candidates, reverse=True)[0][2]


def _mark_path_reassigned(
    registry: dict[str, Any],
    path: str | Path,
    new_source_id: str,
) -> None:
    target = str(Path(path).resolve())

    for source_id, record in registry.get("sources", {}).items():
        if source_id == new_source_id:
            continue

        if target not in set(_record_paths(record)):
            continue

        stale = set(_as_path_list(record.get("stale_paths")))
        if target not in stale:
            stale.add(target)
            record["stale_paths"] = sorted(stale)
            record.setdefault("history", []).append(
                {
                    "at": now(),
                    "event": "path_reassigned",
                    "path": target,
                    "to_source_id": new_source_id,
                }
            )

        refresh_path_state(record)


def _link_revision(
    registry: dict[str, Any],
    source_id: str,
    revision_of: str | None,
) -> None:
    if not revision_of:
        return

    source = registry["sources"][source_id]
    parent = registry["sources"].get(revision_of)
    if not parent:
        return

    source["revision_of"] = revision_of
    source["revision_root"] = (
        parent.get("revision_root")
        or parent.get("revision_of")
        or revision_of
    )
    source["revision_number"] = int(parent.get("revision_number") or 1) + 1

    revised_by = set(_as_path_list(parent.get("revised_by")))
    revised_by.add(source_id)
    parent["revised_by"] = sorted(revised_by)
    parent.setdefault("history", []).append(
        {
            "at": now(),
            "event": "revision_created",
            "revision_source_id": source_id,
        }
    )


def pdf(path: str | Path) -> str:
    try:
        import fitz

        doc = fitz.open(path)
        return "\n\n".join(page.get_text("text") for page in doc)
    except Exception:
        pass

    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception:
        pass

    exe = shutil.which("pdftotext")
    if exe:
        proc = subprocess.run(
            [exe, "-layout", str(path), "-"],
            capture_output=True,
        )
        if proc.returncode == 0:
            return proc.stdout.decode("utf-8", errors="replace")

    raise RuntimeError(
        "No PDF extractor available. Install pymupdf or pypdf, or pdftotext."
    )


def docx(path: str | Path) -> str:
    try:
        from docx import Document
    except Exception as exc:
        raise RuntimeError(
            "DOCX extraction requires python-docx."
        ) from exc

    return "\n\n".join(
        paragraph.text
        for paragraph in Document(str(path)).paragraphs
        if paragraph.text.strip()
    )


def extract_text(path: str | Path) -> str:
    path = Path(path)
    extension = path.suffix.lower()

    if extension == ".pdf":
        return pdf(path)

    if extension == ".docx":
        return docx(path)

    if extension in {".md", ".txt", ".html", ".htm"}:
        return path.read_text(encoding="utf-8", errors="replace")

    raise RuntimeError(f"Unsupported file type: {extension}")


def _write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def transition_allowed(current: str, target: str) -> bool:
    if current == target:
        return True

    if current not in VALID or target not in VALID:
        return False

    if target == "failed":
        return current not in {"published", "ignored"}

    if target == "ignored":
        return current != "published"

    if current == "failed":
        return target == "new"

    if current == "ignored":
        return False

    if current in LIFECYCLE and target in LIFECYCLE:
        current_index = LIFECYCLE.index(current)
        return (
            current_index + 1 < len(LIFECYCLE)
            and LIFECYCLE[current_index + 1] == target
        )

    return False


def add_artifacts(
    record: dict[str, Any],
    stage: str,
    artifact_paths: Iterable[str | Path],
) -> list[str]:
    artifacts = record.setdefault("artifacts", {})
    existing = set(_as_path_list(artifacts.get(stage)))
    added: list[str] = []

    for value in artifact_paths:
        path = Path(value).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Artifact does not exist: {path}")

        resolved = str(path)
        if resolved not in existing:
            existing.add(resolved)
            added.append(resolved)

    artifacts[stage] = sorted(existing)

    for resolved in added:
        record.setdefault("history", []).append(
            {
                "at": now(),
                "event": "artifact_added",
                "stage": stage,
                "path": resolved,
            }
        )

    return added


def set_status(
    record: dict[str, Any],
    target: str,
    *,
    force: bool = False,
) -> bool:
    if target not in VALID:
        raise ValueError(f"Invalid status: {target}")

    current = str(record.get("status") or "new")

    if current == target:
        return False

    if not force and not transition_allowed(current, target):
        raise ValueError(
            f"Invalid lifecycle transition: {current} -> {target}. "
            "Use --force only when an explicit override is intended."
        )

    record["status"] = target
    record.setdefault("history", []).append(
        {
            "at": now(),
            "event": "status",
            "from": current,
            "to": target,
            "forced": bool(force),
        }
    )
    return True


def scan(args: argparse.Namespace) -> None:
    registry_path = Path(args.registry).resolve()
    registry = load(registry_path)

    by_hash = {
        record.get("sha256"): source_id
        for source_id, record in registry["sources"].items()
        if record.get("sha256")
    }

    extensions = {
        value.strip().lower()
        for value in args.extensions.split(",")
        if value.strip()
    }

    added = 0
    seen = 0
    duplicates = 0
    revisions = 0

    for raw_root in args.roots:
        root = Path(raw_root).expanduser().resolve()

        if not root.exists():
            print(f"WARNING missing root: {root}", file=sys.stderr)
            continue

        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in extensions:
                continue

            seen += 1
            resolved = str(path.resolve())
            digest = sha256(path)

            if digest in by_hash:
                source_id = by_hash[digest]
                record = registry["sources"][source_id]

                known_paths = set(_record_paths(record))
                was_known = resolved in known_paths
                known_paths.add(resolved)
                record["paths"] = sorted(known_paths)

                stale = set(_as_path_list(record.get("stale_paths")))
                stale.discard(resolved)
                record["stale_paths"] = sorted(stale)

                record["last_seen_at"] = now()

                _mark_path_reassigned(registry, path, source_id)
                refresh_path_state(record)

                if not was_known:
                    record.setdefault("history", []).append(
                        {
                            "at": now(),
                            "event": "path_added",
                            "path": resolved,
                        }
                    )

                duplicates += 1
                continue

            source_id = allocate_source_id(registry, digest)
            stat = path.stat()
            revision_of = prior_same_path(registry, path, digest)

            record = {
                "source_id": source_id,
                "sha256": digest,
                "filename": path.name,
                "primary_path": resolved,
                "paths": [resolved],
                "active_paths": [resolved],
                "missing_paths": [],
                "stale_paths": [],
                "extension": path.suffix.lower(),
                "size_bytes": stat.st_size,
                "discovered_at": now(),
                "last_seen_at": now(),
                "status": "new",
                "revision_of": revision_of,
                "revision_root": None,
                "revision_number": 1,
                "revised_by": [],
                "extracted_path": None,
                "artifacts": {},
                "history": [
                    {
                        "at": now(),
                        "event": "discovered",
                        "path": resolved,
                    }
                ],
                "error": None,
            }

            registry["sources"][source_id] = record
            by_hash[digest] = source_id
            _link_revision(registry, source_id, revision_of)
            _mark_path_reassigned(registry, path, source_id)

            if revision_of:
                revisions += 1

            added += 1

    for record in registry["sources"].values():
        refresh_path_state(record)

    save(registry_path, registry)

    print(
        f"Files seen: {seen}; new content: {added}; "
        f"existing content: {duplicates}; revisions: {revisions}"
    )


def extract(args: argparse.Namespace) -> None:
    registry_path = Path(args.registry).resolve()
    registry = load(registry_path)
    out = Path(args.out).resolve()

    if args.pending:
        targets = [
            source_id
            for source_id, record in registry["sources"].items()
            if record.get("status") in {"new", "failed"}
        ]
    else:
        if not args.source_id:
            raise SystemExit(
                "Provide SOURCE_ID or use --pending."
            )
        targets = [args.source_id]

    for source_id in targets:
        if source_id not in registry["sources"]:
            print(f"Unknown source: {source_id}", file=sys.stderr)
            continue

        record = registry["sources"][source_id]
        previous_status = str(record.get("status") or "new")

        try:
            source_path = resolve_source_path(record)
            text = extract_text(source_path)

            if not text.strip():
                raise RuntimeError("Extraction returned empty text.")

            output_path = out / f"{source_id}.md"
            body = (
                f"# Extracted source: {record.get('filename') or source_path.name}\n\n"
                f"- source_id: `{source_id}`\n"
                f"- sha256: `{record['sha256']}`\n"
                f"- original_path: `{source_path}`\n\n"
                "---\n\n"
                + text
            )
            _write_text_atomic(output_path, body)

            old_status = str(record.get("status") or "new")
            record["extracted_path"] = str(output_path)
            record["error"] = None

            if old_status in {"new", "failed"}:
                record["status"] = "extracted"
                record.setdefault("history", []).append(
                    {
                        "at": now(),
                        "event": "status",
                        "from": old_status,
                        "to": "extracted",
                        "forced": False,
                        "via": "extract",
                    }
                )
            elif old_status in LIFECYCLE and LIFECYCLE.index(old_status) >= LIFECYCLE.index("extracted"):
                # Re-extraction is allowed for an already processed source, but it
                # must never downgrade lifecycle state such as grounded -> extracted.
                record.setdefault("history", []).append(
                    {
                        "at": now(),
                        "event": "extraction_refreshed",
                        "status_preserved": old_status,
                        "path": str(output_path),
                    }
                )
            else:
                raise RuntimeError(
                    f"Cannot extract source while status is {old_status!r}. "
                    "Move it back into the active lifecycle explicitly before extraction."
                )

            print(f"Extracted {source_id}")

        except Exception as exc:
            record["status"] = "failed"
            record["error"] = str(exc)
            record.setdefault("history", []).append(
                {
                    "at": now(),
                    "event": "failed",
                    "from": previous_status,
                    "to": "failed",
                    "value": str(exc),
                }
            )
            print(f"FAILED {source_id}: {exc}", file=sys.stderr)

    save(registry_path, registry)


def status(args: argparse.Namespace) -> None:
    registry = load(Path(args.registry).resolve())

    counts: dict[str, int] = {}
    for record in registry["sources"].values():
        state = record.get("status", "unknown")
        counts[state] = counts.get(state, 0) + 1

    print(f"Total: {len(registry['sources'])}")
    for state in sorted(counts):
        print(f"{state:16} {counts[state]}")

    for source_id, record in sorted(registry["sources"].items()):
        active = len(_as_path_list(record.get("active_paths")))
        missing = len(_as_path_list(record.get("missing_paths")))
        stale = len(_as_path_list(record.get("stale_paths")))
        revision = int(record.get("revision_number") or 1)

        print(
            f"{source_id}  "
            f"{record.get('status', '?'):16}  "
            f"rev={revision:<3} "
            f"active={active:<2} missing={missing:<2} stale={stale:<2} "
            f"{record.get('filename', '')}"
        )


def mark(args: argparse.Namespace) -> None:
    if args.status not in VALID:
        raise SystemExit(f"Invalid status: {args.status}")

    registry_path = Path(args.registry).resolve()
    registry = load(registry_path)

    if args.source_id not in registry["sources"]:
        raise SystemExit(f"Unknown source: {args.source_id}")

    record = registry["sources"][args.source_id]

    try:
        if args.artifact:
            add_artifacts(record, args.status, args.artifact)

        changed = set_status(
            record,
            args.status,
            force=bool(args.force),
        )
    except (ValueError, FileNotFoundError) as exc:
        raise SystemExit(str(exc)) from exc

    save(registry_path, registry)

    if changed:
        suffix = " (forced)" if args.force else ""
        print(f"{args.source_id} -> {args.status}{suffix}")
    else:
        print(f"{args.source_id} already at {args.status}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deterministic KnowledgeCraft research source registry."
    )
    parser.add_argument(
        "--registry",
        default=".knowledgecraft/research/registry.json",
    )

    subparsers = parser.add_subparsers(
        dest="cmd",
        required=True,
    )

    scan_parser = subparsers.add_parser("scan")
    scan_parser.add_argument("roots", nargs="+")
    scan_parser.add_argument(
        "--extensions",
        default=".pdf,.docx,.md,.txt,.html,.htm",
    )
    scan_parser.set_defaults(fn=scan)

    extract_parser = subparsers.add_parser("extract")
    extract_parser.add_argument("source_id", nargs="?")
    extract_parser.add_argument("--pending", action="store_true")
    extract_parser.add_argument(
        "--out",
        default=".knowledgecraft/research/extracted",
    )
    extract_parser.set_defaults(fn=extract)

    status_parser = subparsers.add_parser("status")
    status_parser.set_defaults(fn=status)

    mark_parser = subparsers.add_parser("mark")
    mark_parser.add_argument("source_id")
    mark_parser.add_argument("status")
    mark_parser.add_argument(
        "--artifact",
        action="append",
        help="Artifact path. Repeat --artifact to register multiple artifacts.",
    )
    mark_parser.add_argument(
        "--force",
        action="store_true",
        help="Override lifecycle transition validation explicitly.",
    )
    mark_parser.set_defaults(fn=mark)

    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
