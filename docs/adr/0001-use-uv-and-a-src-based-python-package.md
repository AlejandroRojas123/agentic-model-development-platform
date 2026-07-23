# ADR 0001: Use uv and a src-based Python package

* **Status:** Accepted
* **Date:** 2026-07-20
* **Decision owners:** Alejandro Rojas

## Context

The Agentic Model Development Platform requires a reproducible Python development environment and an installable package structure.

The project will eventually include data ingestion, data validation, feature engineering, model development, evaluation, monitoring, reporting, and AI-assisted workflows. Its foundation therefore needs to support:

* Reproducible dependency resolution
* Explicit Python-version management
* Separation of production and development dependencies
* Reliable package imports during testing
* Automated testing
* Straightforward setup for contributors and automated workflows
* A structure that can grow without prematurely creating unnecessary subsystems

Several separate tools could be combined to provide these capabilities, including Python installers, `venv`, `pip`, requirements files, and packaging utilities. However, using multiple overlapping tools would add setup and maintenance complexity without providing a clear benefit at this stage.

## Decision

The project will use:

* Python 3.12 as its initial supported Python version
* `uv` for Python installation, virtual-environment creation, dependency resolution, dependency locking, and command execution
* `pyproject.toml` as the central Python project and tooling configuration file
* Hatchling as the initial package build backend
* A `src/`-based package layout
* `amdp` as the Python import-package name
* `pytest` as the initial testing framework
* `uv.lock` as the committed dependency lockfile

The initial package structure is:

```text
src/
└── amdp/
    └── __init__.py
```

Tests are maintained separately:

```text
tests/
└── test_package.py
```

Project commands will generally be executed through `uv`, for example:

```shell
uv sync
uv run python --version
uv run pytest
```

Runtime dependencies and development dependencies will be declared separately in `pyproject.toml`.

Directories for future components will be added only when the corresponding components are implemented. The project will not create speculative empty directories for anticipated agents, models, monitoring systems, APIs, or reporting features.

## Alternatives considered

### Standard library `venv` with `pip` and requirements files

This approach is widely understood and would minimize reliance on newer tooling.

It was not selected because Python installation, virtual-environment management, dependency declaration, dependency locking, and command execution would require multiple separate conventions or tools. This would increase setup complexity and provide weaker project-level reproducibility.

### Poetry

Poetry offers dependency management, virtual environments, packaging, and lockfiles through an integrated workflow.

It was not selected because the project does not currently require Poetry-specific abstractions. `uv` provides the needed environment and dependency-management capabilities while retaining standards-based configuration in `pyproject.toml`.

### Conda

Conda provides environment and package management and can manage non-Python dependencies.

It was not selected as the project standard because the initial application does not require Conda-managed system libraries. Using a standard Python package structure also makes the repository easier to use in common Python build, test, container, and continuous-integration environments.

### Flat repository layout

A flat layout could place the `amdp` package directly in the repository root.

It was not selected because a `src/` layout more clearly separates importable source code from repository-level files and helps tests exercise the installed package rather than importing source files accidentally from the working directory.

### Longer Python package name

The package could use `agentic_model_development_platform` as its import name.

It was not selected because it would make imports unnecessarily verbose. The concise `amdp` name is used for Python imports while the full project name remains the public repository and product name.

## Consequences

### Positive consequences

* A new environment can be created with a small number of commands.
* Python and dependency versions can be reproduced across machines.
* The package can be imported consistently by tests, scripts, and future applications.
* Development dependencies remain distinct from runtime dependencies.
* The project can grow within a conventional Python package structure.
* The committed lockfile provides a reproducible record of resolved dependencies.
* The chosen structure is suitable for future continuous integration and containerization.

### Negative consequences

* Contributors must install or otherwise obtain `uv`.
* The project depends on a tool that may be less familiar than `pip` and `venv`.
* Some contributors may need to adjust existing Conda-, Poetry-, or pip-based workflows.
* Hatchling introduces an additional build-system dependency.
* Python 3.12 excludes environments restricted to earlier Python versions.

### Risks and mitigations

**Risk:** `uv` changes substantially or becomes unsuitable for the project.

**Mitigation:** Core project metadata remains in the standards-based `pyproject.toml` format, reducing migration costs.

**Risk:** The abbreviated package name `amdp` may conflict with another installed package.

**Mitigation:** The project will use an isolated virtual environment, and the package name can be reconsidered before public distribution if an actual conflict arises.

**Risk:** Restricting the project to Python 3.12 may reduce compatibility.

**Mitigation:** The initial restriction favors reproducibility during early development. Support for additional Python versions can be evaluated after the foundation stabilizes.

## Validation

The decision was validated locally on Windows by successfully:

1. Installing Python 3.12 through `uv`
2. Creating and synchronizing the project virtual environment
3. Building and installing the local project package
4. Importing `amdp` from Python
5. Running the initial pytest suite

The initial smoke test completed successfully with one passing test.

## Review conditions

This decision should be reconsidered if:

* The project requires non-Python dependencies that are impractical to manage through the chosen workflow
* Deployment constraints require a different packaging standard
* `uv` no longer supports required project capabilities
* The application needs to support additional Python versions
* The project is prepared for distribution through a public package index