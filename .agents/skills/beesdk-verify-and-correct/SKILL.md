---
name: beesdk-verify-and-correct
description: Independently verify an implemented BeeSDK Issue, apply only necessary in-scope corrections, and return final evidence for read-only review.
---

# BeeSDK verification and correction workflow

## Purpose

Use this workflow after initial implementation or after a read-only review has returned blocking findings.

The executor may inspect files, modify the exact target worktree and run local checks.

Use this workflow once for independent post-implementation verification. Reuse it only to address explicit blocking findings returned by a completed final review.

Do not:

- expand the approved Issue;
- add optional polish;
- create speculative architecture;
- perform unrelated cleanup;
- create preventive closing patches without a demonstrated blocker;
- commit, push, create a PR or merge;
- change package version unless the Issue is explicitly release-related.

## Required inputs

For every run obtain:

- project;
- exact target worktree;
- expected branch;
- base branch;
- related repository contracts when explicitly supplied.

For initial independent verification also obtain:

- approved Issue or normalized approved task contract;
- planning constraints.

For a correction run also obtain:

- explicit blocking findings from the completed final review.

Do not require an implementation report or previous verification report.

## Working contract

Before proposing or applying a change, read every declared file completely. Keep a file inventory; when another file becomes necessary, add it to the inventory and read it completely before editing it.

For initial verification, map the work to the supplied roadmap context and approved task contract.

For a correction run, treat the supplied final-review blockers as the complete correction scope. Do not require the full Issue or planning context and do not reopen already reviewed scope.

Before editing, determine `low-risk`, `runtime-risk` or `security-sensitive`, then derive required checks from `docs/SDLC.md` and `docs/SECURITY.md`.

Make the smallest complete KISS change. Do not refactor unrelated code, run formatters over unrelated content, remove an existing check without an explicit task-specific reason, or add first-party production/test comments, explanatory docstrings, `TODO`, `FIXME`, `NOTE` or decorative separators. Preserve required license, provenance and security annotations and unrelated existing comments.

Use proportional tests for acceptance criteria and public behavior. Prefer existing test files and helpers; create a file or helper only when demonstrably necessary. Keep consumer-specific runtime implementation, domain business logic and product-specific behavior out of BeeSDK; report explicitly when a requested change belongs to a consumer repository.

Before reporting completion, inspect the final diff and remove every newly introduced prohibited comment and unrelated formatting change.

## Target safety gate

Before verification:

1. verify the current working directory;
2. verify the current branch;
3. inspect `git status`;
4. inventory committed, staged, unstaged and untracked changes relative to the base branch;
5. distinguish current-Issue changes from unrelated changes.

Stop when:

- the path or branch differs from the requested target;
- unrelated changes prevent safe verification;
- mandatory target information is missing;
- the approved task contract is missing for initial verification;
- explicit final-review blockers are missing for a correction run.

Do not silently switch branches or replace the requested worktree.

## Required reading

Read for every run:

- `AGENTS.md`;
- `docs/SDLC.md`;
- `docs/SECURITY.md`;
- all changed and untracked files;
- directly related public contracts, exports, package metadata, consumers and tests.

For initial independent verification also read:

- the approved Issue or normalized approved task contract;
- the relevant roadmap section;
- supplied planning constraints.

For a correction run also read:

- every supplied final-review blocker;
- the directly related current files, contracts and tests.

Do not request or depend on an implementation report or previous verification report.

The current target worktree, diff, tests, package outputs and consumer compatibility evidence are authoritative.

## Verification

For initial verification, evaluate every Acceptance Criterion as:

- satisfied;
- partially satisfied;
- not satisfied;
- not verifiable;
- not applicable.

For a correction run, verify:

- every supplied blocking finding;
- every affected Acceptance Criterion explicitly named in those findings;
- regressions in the behavior touched by the corrections.

Verify as applicable:

- source of truth;
- SDK, consumer and runtime ownership;
- public contracts;
- top-level exports;
- type/protocol compatibility;
- backward compatibility;
- package metadata;
- package build behavior;
- independent package importability;
- `py.typed`;
- dependency direction;
- runtime dependency surface;
- consumer compatibility;
- dependency and version status;
- security and authority boundaries;
- required tests and checks.

Determine the actual change level from `docs/SDLC.md` and `docs/SECURITY.md`.

When the approved Issue has no dependency change, do not inspect, regenerate, modify or separately validate `uv.lock`. When it explicitly requires a dependency change, allow only the necessary minimal registry lock update and inspect only that relevant diff. Never run or require `uv lock --check`, and do not treat unrelated lock noise as an independent finding.

Do not report the following syntax as a finding solely because it lacks additional parentheses:

```python
except json_mod.JSONDecodeError, OSError:
```

## Corrections

Apply corrections only when required by:

- an unsatisfied Acceptance Criterion;
- incorrect or unsafe current-Issue behavior;
- an architecture or source-of-truth violation;
- a public-contract incompatibility;
- a type/protocol incompatibility;
- a package/build incompatibility;
- missing required verification;
- a supplied valid review blocker.

Corrections must be:

- limited to the current Issue;
- minimal and complete;
- consistent with existing public contracts and package sources of truth;
- free of duplicated logic or contracts;
- free of unnecessary defaults and hardcoding;
- compatible with dependency direction `consumer -> beesdk`;
- free of consumer runtime implementation inside BeeSDK;
- PEP 8 compliant;
- free of new comments.

If a new function or class is necessary, identify its exact insertion location in the report.

Do not introduce a new requirement merely because it might be useful later.

## Tests and checks

Run all checks required by the actual change level.

Include as applicable:

- targeted regression tests;
- `uv run pytest -q`;
- `uv build`;
- package import smoke;
- top-level public API verification;
- built package contents inspection;
- `py.typed` verification;
- consumer compatibility smoke;
- dependency direction checks;
- package metadata and contract checks;
- SAST;
- SCA;
- DAST;
- IAST;
- fuzzing.

Use existing tests and helpers when practical.

Do not create new test files or helpers without a concrete need.

Record exact commands, exit codes, passed, failed, skipped and warnings.

## Final report

Return one consolidated report containing:

1. `Target verification`
2. `Actual changed-file inventory`
3. `Acceptance Criteria coverage`
4. `Blocking findings received`
5. `Corrections made`
6. `Change level`
7. `Required checks`
8. `Tests and commands`
9. `Smoke`
10. `Public API and compatibility`
11. `Package/build artifacts`
12. `Security review`
13. `Dependencies`
14. `Unrelated-file check`
15. `Known limitations`
16. `Recommended Conventional Commit`
17. `Final readiness`
18. `Version status`

Describe every correction in this format:

```text
Файл:
`path/to/file`

Было:
<previous incorrect behavior>

Стало:
<implemented required behavior>

Почему:
<current-Issue requirement and verification evidence>
```

Do not include a diff.

When no correction was required, state:

```text
Правки не потребовались.
```

End with:

```text
version not changed
```

unless the approved Issue explicitly requires release versioning.