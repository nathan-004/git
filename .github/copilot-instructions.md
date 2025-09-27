# Copilot Instructions for AI Coding Agents

## Project Overview
This project is a Python implementation of basic Git functionality. The codebase is organized to mimic Git's internal architecture, with clear separation between core logic, object management, and utility functions.

## Key Components
- `main.py`: Entry point for the application. Orchestrates high-level operations.
- `git/`: Core logic for Git operations.
  - `init_git.py`: Handles repository initialization.
  - `head.py`: Manages HEAD references.
  - `logger.py`: Project-specific logging utilities.
  - `utils.py`: Shared utility functions.
  - `objects/`: Implements Git object types and operations.
    - `blobs.py`, `commits.py`, `branches.py`, `tree.py`, `object.py`, `read.py`: Each file represents a distinct Git object or operation, following Git's internal model.

## Developer Workflows
- **Run the project:**
  - Use `python main.py` from the project root.
- **Debugging:**
  - Logging is handled via `git/logger.py`. Check this file for custom logging patterns.
- **Testing:**
  - No formal test suite detected. Use example files in `example/` for manual testing.

## Project-Specific Patterns
- **Object-Oriented Design:**
  - Each Git object (blob, commit, branch, tree) is implemented as a separate module in `git/objects/`.
- **Initialization:**
  - Repository setup logic is in `git/init_git.py`.
- **HEAD Management:**
  - HEAD reference logic is in `git/head.py`.
- **Utilities:**
  - Common helpers are in `git/utils.py`.
- **Logging:**
  - Use the custom logger in `git/logger.py` for all output.

## Integration Points
- No external dependencies detected; project is pure Python.
- Example files in `example/` are used for manual validation.

## Conventions
- Module-level separation for each Git concept.
- All core logic is under the `git/` directory.
- Example/test files are under `example/`.

## Quick Reference
- **Initialize repo:** See `git/init_git.py`.
- **Manage HEAD:** See `git/head.py`.
- **Work with objects:** See `git/objects/`.
- **Log output:** Use `git/logger.py`.

---
For questions or unclear patterns, review the relevant module or ask for clarification.
