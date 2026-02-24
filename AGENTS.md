## About Project:

This is a generic project template that includes important configs, directory structure and python project best practices.

This template is intended for creating generic projects in python that don't involve big frameworks, like web scrapping scripts, CLI tools and POC (Proof of Concept) type projects.

### Directory Structure:
```
.
├── AGENTS.md # This file
├── mypy.ini # Type checker config
├── pyproject.toml # Config for linters and formatters
├── README.md # Intended for humans
├── requirements/ # project dependencies
├── docs/ # project documentation
├── skills/ # agent skills
├── src/ # source code
└── tests/
```

## Common workflows:
- Run typechecker: `mypy .`
- Run tests using `pytest`
