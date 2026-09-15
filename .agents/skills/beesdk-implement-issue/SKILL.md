---
name: beesdk-implement-issue
description: Implement one approved BeeSDK Issue in the exact target worktree and return complete implementation and verification evidence.
---

# BeeSDK approved Issue implementation workflow

## Purpose

Use this workflow after an Issue has been approved and a dedicated target worktree and branch have been prepared.

This workflow may modify the target repository and run local checks.

Do not:

- work outside the approved Issue;
- perform unrelated refactoring or cleanup;
- create speculative abstractions;
- commit, push, create a PR or merge;
- change package version unless the Issue is explicitly release-related.

## Required inputs

Obtain:

- project;
- exact target worktree;
- expected branch;
- base branch;
- approved Issue or normalized approved task contract;
- Issue source when supplied;
- planning constraints;
- related repository contracts when explicitly supplied.

## Working contract

Before proposing or applying a change, read every declared file completely. Keep a file inventory; when another file becomes necessary, add it to the inventory and read it completely before editing it.

Map the work to the supplied current roadmap iteration and stay inside its approved scope. Before editing, determine `low-risk`, `runtime-risk` or `security-sensitive`, then derive required checks from `docs/SDLC.md` and `docs/SECURITY.md`.

Make the smallest complete KISS change. Do not refactor unrelated code, run formatters over unrelated content, remove an existing check without an explicit task-specific reason, or add first-party production/test comments, explanatory docstrings, `TODO`, `FIXME`, `NOTE` or decorative separators. Preserve required license, provenance and security annotations and unrelated existing comments.

Use proportional tests for acceptance criteria and public behavior. Prefer existing test files and helpers; create a file or helper only when demonstrably necessary. Keep consumer-specific runtime implementation, domain business logic and product-specific behavior out of BeeSDK; report explicitly when a requested change belongs to a consumer repository.

Before reporting completion, inspect the final diff and remove every newly introduced prohibited comment and unrelated formatting change.

## Target safety gate

Before changing files:

1. verify the current working directory;
2. verify the current branch;
3. inspect `git status`;
4. verify that the worktree matches the requested target;
5. identify pre-existing staged, unstaged and untracked changes.

Stop when:

- the path or branch differs from the requested target;
- unrelated pre-existing changes make safe attribution impossible;
- the Issue materially conflicts with `AGENTS.md` or repository contracts.

Do not silently switch branches or substitute another worktree.

## Required reading

Read before implementation:

- `AGENTS.md`;
- the approved Issue or normalized approved task contract;
- the relevant `docs/ROADMAP.md` section;
- `docs/SDLC.md`;
- `docs/SECURITY.md`;
- directly relevant public contracts, package metadata, implementation and tests.

Read related repository files only when required to verify a public contract or consumer compatibility.

Do not modify a related repository unless the Issue explicitly assigns work to it.

## Change classification

Determine the actual change level:

- `low-risk`;
- `runtime-risk`;
- `security-sensitive`.

Use `docs/SDLC.md` and `docs/SECURITY.md` to derive required checks.

If the actual implementation requires a higher change level than the Issue declares, report the mismatch before continuing.

## Implementation

Implement the smallest complete solution satisfying Scope and Acceptance Criteria.

Requirements:

- follow KISS;
- preserve explicit SDK, consumer and host/runtime ownership;
- use existing public contracts and package sources of truth;
- do not introduce hidden defaults for required behavior;
- do not create a second source of truth;
- do not duplicate existing logic or contracts;
- do not hardcode values that belong in an existing contract or package source of truth;
- preserve dependency direction `consumer -> beesdk`;
- do not import consumer projects into BeeSDK;
- do not move runtime implementation into BeeSDK;
- follow PEP 8;
- keep public identifiers, package metadata and data fields in English;
- do not add comments;
- preserve compatibility unless the Issue explicitly permits a breaking change;
- keep `pyproject.toml.version` unchanged for ordinary feature, fix, docs and chore work.

When the approved Issue has no dependency change, do not inspect, regenerate, modify or separately validate `uv.lock`. When it explicitly requires a dependency change, allow only the necessary minimal registry lock update and inspect only that relevant diff. Never run or require `uv lock --check`, and do not treat unrelated lock noise as an independent finding.

## Tests and verification

Add or update only tests proportional to the Issue.

Prefer existing test files and helpers.

Do not create a new test file or helper unless the required behavior cannot be covered cleanly in the existing structure.

Run all checks required by the actual change level, including as applicable:

- targeted tests;
- `uv run pytest -q`;
- `uv build`;
- package import smoke;
- public API verification;
- package contents verification;
- `py.typed` verification;
- consumer compatibility smoke;
- dependency direction verification;
- configuration or metadata validation;
- contract verification;
- SAST;
- SCA;
- DAST;
- IAST;
- fuzzing.

Use `uv run` for Python commands when applicable.

Record exact commands, exit codes, passed, failed, skipped and warnings.

Do not claim a check passed when it was not executed.

## Implementation report

Return one report containing:

1. `Target verification`
2. `Files read`
3. `Change level`
4. `Required checks`
5. `Source of truth`
6. `SDK/consumer/runtime boundary`
7. `Changed files`
8. `Acceptance Criteria coverage`
9. `Tests and commands`
10. `Smoke`
11. `Package/build artifacts`
12. `Public API and compatibility`
13. `Security review`
14. `Dependencies`
15. `Known limitations`
16. `Recommended Conventional Commit`
17. `Version status`

For every substantive correction made during implementation, describe:

- `Файл`
- `Было`
- `Стало`
- `Почему`

Do not include a diff.

End with:

```text
version not changed
```

unless the approved Issue explicitly requires release versioning.