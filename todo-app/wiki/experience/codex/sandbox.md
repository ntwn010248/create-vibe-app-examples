# [PITFALL] Sandbox Temp Directory ACL Lock on Windows

## TL;DR
In this sandbox, `tempfile.TemporaryDirectory()` can create directories that later commands cannot access or delete. Use workspace-local deterministic test files instead of temp dirs.

## Context
Project: `todo-app`  
Environment: Windows PowerShell sandbox (`workspace-write`)

## Problem
Tests that used temporary directories (system temp and workspace temp) failed with:
- `PermissionError: [WinError 5] Access is denied`
- cleanup failures in `TemporaryDirectory.cleanup()`

This also left stale folders under `code/tests/.tmp/` that the current sandbox user cannot remove.

## Solution
1. Avoid `TemporaryDirectory()` for this environment.
2. Use a deterministic workspace file path per test run:
   - `code/tests/test-todos.json`
3. Remove the file in `setUp` and `tearDown` for isolation.

Implemented in:
- `code/tests/test_todo_app.py`

## Why This Works
- File ACL behavior is stable for normal workspace files.
- Test isolation is preserved by deleting/recreating the same file.
- No dependency on OS temp directories or sandbox token-specific ACLs.

## Operational Notes
- Existing locked folders under `code/tests/.tmp/` may require cleanup outside this sandbox identity.
- This is an environment cleanup issue, not a blocker for running the current tests.

## Prevention
- In this repo, prefer deterministic workspace test artifacts over OS temp dirs.
- If temp paths are required, validate create/read/delete in a single command context before adopting.
- Keep tests dependency-free (`unittest`) and storage-local when sandbox constraints are unknown.

## Tags
#pitfall #sandbox #windows #acl #python #testing
