# Repository Discovery

## Objective

Identify the real application structure and trace the affected behavior
without assuming a specific stack.

## Start with repository guidance

Read relevant instructions and architecture documents, including any
CLAUDE.md files, READMEs, contribution guidance, service documentation,
API contracts and schema documentation.

Inspect the working tree before considering changes. Preserve all existing
user edits and untracked files.

## Discover the stack

Use repository files to identify applicable technologies, for example:

- package.json and lockfiles
- pyproject.toml, requirements files and Python project configuration
- pom.xml, Gradle files and JVM build configuration
- go.mod
- Cargo.toml
- .NET project and solution files
- Dockerfiles and deployment manifests
- Infrastructure-as-code and CI/CD configuration
- ORM models, SQL schemas and migration directories

These are examples, not required files. Do not infer the stack from a
filename mentioned in a ticket.

## Locate the execution path

Search for:

- User-facing labels and error messages
- API routes and endpoint definitions
- Request/response models and validation
- Domain services and business rules
- Database repositories and query definitions
- Events, jobs, queues and consumers
- Feature flags and configuration
- Existing tests and fixtures

Follow calls from the entry point through relevant functions and
dependencies. Read surrounding code rather than interpreting a search
match in isolation.

## Evidence requirements

For each proposed code finding, record:

- Exact repository-relative path
- Function, class, component or query
- Line range, if the inspected tool supports reliable line numbers
- Observed behavior in the code
- Connection between that behavior and the ticket symptom
- Existing test coverage or missing test coverage

Do not fabricate paths, symbols or line numbers.

## Multiple repositories

If the system spans repositories, inspect only repositories available in
the current session or explicitly provided by the user. Record which
repositories were available and which were not.

Do not assume that the current repository contains the frontend, backend,
database migrations or infrastructure for every affected service.

## Git history

If useful and permitted, inspect recent commits and blame information for
the relevant code. Treat temporal correlation as a clue, not proof of
causation.

Never reset, checkout over, discard, or rewrite user changes as part of
read-only investigation.

## Completion criteria

The assistant should understand the relevant execution path, identify
candidate files and tests, and know which required dependencies or
repositories remain inaccessible.