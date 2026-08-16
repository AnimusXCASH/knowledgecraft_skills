# Research Paper Input Folder

Put local research papers/reports here when using KnowledgeCraft in this repository as a working environment.

Example:

```text
papers/
├── paper-1.pdf
├── paper-2.pdf
└── report.docx
```

Then start OpenCode from the repository root and ask:

```text
Process ./papers/paper-1.pdf for my research knowledge base.
```

or:

```text
/research-batch

Process all new and unfinished research in ./papers through ideas_created.
```

You may also use sources located elsewhere by providing their explicit paths.

This folder is **input**.

Generated KnowledgeCraft state belongs under:

```text
.knowledgecraft/
```

The `.gitignore` in this folder ignores local research files by default so papers are not accidentally committed to the public repository.

Do not remove that protection unless you intentionally want to version specific source files and have the rights to do so.
