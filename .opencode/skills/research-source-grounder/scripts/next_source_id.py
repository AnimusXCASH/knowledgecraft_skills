from pathlib import Path
import re


# Resolve repository root from this script's location:
# repo/.opencode/skills/research-source-grounder/scripts/next_source_id.py
REPO_ROOT = Path(__file__).resolve().parents[4]

GROUNDING_DIR = REPO_ROOT / ".knowledgecraft" / "research" / "grounded"

PATTERN = re.compile(
    r"^SRC-UNREGISTERED-(\d+)-(?:source-card\.md|claim-ledger\.yaml)$"
)


def main():
    GROUNDING_DIR.mkdir(parents=True, exist_ok=True)

    occupied = set()

    for path in GROUNDING_DIR.iterdir():
        if not path.is_file():
            continue

        match = PATTERN.match(path.name)

        if match:
            occupied.add(int(match.group(1)))

    next_number = max(occupied, default=0) + 1

    source_id = f"SRC-UNREGISTERED-{next_number:03d}"

    print(source_id)


if __name__ == "__main__":
    main()