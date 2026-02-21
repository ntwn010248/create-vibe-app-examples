# Vibe Coding Project

This repository is designed for agent-based development with strict phase routing.

## AI Execution Contract (MUST)

1. Invoke specialized agents as sub-agents (never do full workflow in main agent context).
2. Keep main agent context minimal:
   - Main agent only routes, tracks phase status, and aggregates outputs.
   - Sub-agents do detailed reading/writing for their phase.
3. Record learning in `wiki/experience/` after implementation tasks.
4. Do not skip required phases for medium/complex work.

## Sub-Agent Invocation Protocol (MUST)

When a phase is needed, call a sub-agent with:

- `agent`: one of `requirement-manager`, `design-manager`, `implementation-executor`, `experience-depositor`
- `goal`: exact phase objective
- `inputs`: only required file paths and user request
- `expected_output`: concrete artifact path(s)
- `done_criteria`: checklist for that phase


Main agent responsibilities:

1. Determine required phases.
2. Invoke sub-agent for each phase.
3. Validate artifact existence and completion.
4. Continue to next phase.
5. Return concise final summary.

### Invocation Command Format
```
codex exec "{Necessary Prompts}"
```
## Phase Routing Rules

### Task

Examples: new module/system, cross-domain architecture.

Required phases:
1. `requirement-manager` + user confirmation
2. `design-manager` + user confirmation
3. `implementation-executor` in incremental slices
4. `experience-depositor`

## Implement Code Definition (MUST)

Implementation is considered complete only if all are done:

1. Read relevant requirement + design docs.
2. Modify/create code under `code/` (or declared source root).
3. ALWAYS DO TEST DRIVEN DEVELOPMENT
4. Run validation available in environment (tests, lint, syntax check, or manual verification notes).
5. Perform self-review (`skill/code-review` guidance).
6. Provide implementation summary with changed files.

If step 3 cannot run, explicitly state what was not runnable and why.

## Done Definition (Project-Level)

A medium/complex feature is only DONE when all artifacts exist:

- Requirement artifact in `requirement/`
- Design artifact in `wiki/design/`
- Code changes in `code/` (or declared source root)
- Learning note in `wiki/experience/`

## Directory Guide

| Directory | Purpose |
|---|---|
| `.agents/` | Agent role definitions |
| `skill/` | Reusable workflow skills |
| `wiki/` | Project knowledge base |
| `requirement/` | Task tracking |
| `mcp/` | External tool configs |
| `code/` | Source code |
| `reference/` | Reference implementations |
