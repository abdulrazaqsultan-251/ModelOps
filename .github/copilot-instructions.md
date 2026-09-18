# ModelOps Copilot Instructions

## Project
ModelOps is a Python CLI for inspecting, validating, and comparing AI model metadata.

## Constraints
- Python 3.11+
- Use the src/ project layout.
- Use pytest for tests.
- Keep modules cohesive and responsibilities focused.
- Prefer clear names and small functions.
- Raise specific custom exceptions instead of using bare except.
- Do not add secrets, tokens, credentials, or private course files.
- Keep CLI behavior simple and deterministic.

## Commands
modelops inspect <path>
modelops validate <path>
modelops compare <first> <second>

## Development workflow
1. Understand the requested change.
2. Inspect the existing code before editing.
3. Make the smallest focused change.
4. Review the diff.
5. Run the relevant tests.
6. Run the full test suite before committing.
7. Use Conventional Commit messages.

## Vibe Coding
Before accepting agent-generated code:
- Review the proposed diff.
- Check that it follows these constraints.
- Run tests.
- Reject unnecessary changes.
