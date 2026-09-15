# AGENTS.md — BeeSDK repository guidance

## Purpose

This file contains stable repository-wide rules for AI agents working with `beesdk`.

Task-specific requirements belong in the approved Issue.

Detailed workflows belong in `.agents/skills/`.

Prompts should normally contain only:

- selected workflow;
- exact target information;
- approved Issue;
- implementation or verification evidence;
- task-specific constraints.

## Instruction precedence

Use this order:

1. Current explicit task instructions and approved Issue.
2. This `AGENTS.md`.
3. Selected repository skill.
4. Current repository contracts and documentation.
5. Implementation reports and previous comments as supporting evidence only.

The actual target worktree, current files, diff, tests, package metadata and built package evidence take precedence over stale reports.

When instructions materially conflict, stop and report the conflict.

## Agent role separation

Tool, authority and read-only restrictions apply only to the current task and agent.

When producing a prompt for another agent, do not copy the current agent's tool restrictions unless they are explicitly required for that executor.

Planning, prompt-preparation and review tasks may use Bee Dev MCP in read-only mode.

Implementation and correction prompts are executed by Copilot or Codex. They must instruct the executor to work in the exact worktree using its available local repository tools. They must not require Bee Dev MCP, an MCP target, review mode or read-only behavior.

## Bee Dev MCP rules

These rules apply only when the current task explicitly selects Bee Dev MCP for read-only planning, prompt preparation or review.

Bee Dev MCP is read-only.

Available Bee Dev MCP tools:

- `list_projects`;
- `list_worktrees`;
- `get_project_context`;
- `get_review_manifest`;
- `get_review_bundle_page`;
- `get_review_bundle` — compatibility only;
- `read_project_file`;
- `search_project`;
- `get_github_context`.

Do not refer to nonexistent tools such as `get_file`.

Use `get_review_manifest` and `get_review_bundle_page` for complete reviews.

Do not repeatedly call `get_review_bundle` expecting pagination.

### GitHub context resolution

When any supplied input contains a supported GitHub Issue or Pull Request URL, call `get_github_context` before interpreting that input.

For an Issue, read and consider:

- title;
- body;
- all Issue comments.

For a Pull Request, read and consider:

- title;
- body;
- all conversation comments;
- reviews;
- inline review comments.

A GitHub URL is an instruction to load its complete available context, not merely a reference to include in the output.

When pasted content and a GitHub URL are supplied together, consider both. If they materially conflict, report the conflict instead of silently choosing one.

Comments are context and do not automatically expand the approved scope. Explicit accepted clarifications may refine the Issue or PR contract.

If mandatory GitHub context is unavailable, incomplete or reported as truncated, return the applicable incomplete-workflow result instead of proceeding from partial context.

### Exact target resolution

Before planning or review:

1. call `list_worktrees`;
2. match the requested worktree by exact `path`;
3. use the returned MCP `target`;
4. call `get_project_context`;
5. verify project, path, branch, HEAD and dirty state.

For review, verify the expected base branch from the complete manifest.

Do not infer a target from a branch name.

Do not substitute the main worktree for a requested feature worktree.

### Complete reading

Repository inspection is incomplete while required data is paginated, truncated or has continuation metadata.

For manifests and diffs, continue with the exact `next_cursor` while `has_more=true`.

For files, continue with the exact `next_line` and `next_column` until both are null.

Read required files listed under `omitted_files` or `related_omitted_files` directly with `read_project_file`.

Treat `truncated=true` as incomplete review data.

Failure to retrieve mandatory MCP data is not a code defect.

When mandatory review inspection cannot be completed, return:

```text
REVIEW INCOMPLETE
```

Do not return `CHANGES REQUIRED` solely because MCP data is incomplete.

## Mandatory reading

Read documents required by the selected skill.

Common documents include:

- `AGENTS.md`;
- approved Issue;
- relevant `docs/ROADMAP.md` section;
- `docs/SDLC.md`;
- `docs/SECURITY.md`;
- `docs/DEV_GUIDE.md`;
- `README.ru.md`.

When relevant, also read:

- `docs/ARCHITECTURE.md`;
- `docs/SPEC.md`;
- `pyproject.toml`;
- `CHANGELOG.md`;
- public BeeSDK contracts;
- package exports;
- package typing metadata;
- related consumer repository ROADMAPs and public contracts.

ROADMAP status does not prove implementation. Compare it with current code, contracts, tests, package metadata and consumer evidence where applicable.

## Architecture boundary

Canonical dependency direction:

```text
                    beesdk
                      ↑
        ┌─────────────┼─────────────┐
        │             │             │
     beeagent    beeagent-rop     beescan
```

Canonical responsibility flow:

```text
consumer module
→ BeeSDK public contract
→ consumer host/runtime
→ capability / storage / connector / external system
```

BeeSDK owns:

- shared public contracts;
- public protocols;
- shared enums and bounded data shapes;
- stable public contract modules;
- type contracts;
- `py.typed`;
- package metadata and build contract;
- compatibility policy;
- shared host/module boundary semantics;
- artifact port contracts;
- capability caller contracts;
- package version and release contract.

Consumer hosts own:

- orchestration;
- runtime and session state;
- module registry and loading;
- runtime context creation;
- configuration loading and validation;
- artifact and storage implementation;
- capability execution;
- approvals, authority and policy enforcement;
- connectors;
- secrets;
- execution and egress;
- runtime logs and observability;
- external-system integration.

Domain modules own:

- domain models and taxonomy;
- classification and business rules;
- duplicate resolution;
- domain fixtures;
- domain summaries and recommendations;
- bounded domain AI behavior.

BeeUI owns:

- generic rendering;
- layout and reusable presentation blocks;
- templates and static assets;
- generic UI session and presentation mechanisms.

Do not:

- make BeeSDK depend on BeeAgent, beeagent-rop, BeeScan, BeeUI or another consumer;
- move runtime orchestration or execution into BeeSDK;
- move storage implementation into BeeSDK;
- move consumer configuration into BeeSDK;
- move domain business rules or taxonomy into BeeSDK;
- add consumer-specific behavior to shared contracts without proven reusable semantics;
- import private consumer internals;
- duplicate public contracts when BeeSDK already owns them;
- allow module-controlled input to grant runtime authority;
- bypass host-owned capability, approval or authority boundaries;
- create a second runtime or source of truth;
- add speculative shared contracts without demonstrated consumer need.

## Sources of truth

Use:

- package metadata and package version: `pyproject.toml`;
- package dependency declarations: `pyproject.toml`;
- resolved development environment: `uv.lock`;
- public import surface: `src/beesdk/artifacts.py`, `src/beesdk/capabilities.py` and `src/beesdk/modules.py`;
- public contract implementation: `src/beesdk/`;
- package typing marker: `src/beesdk/py.typed`;
- public contract specification: `docs/SPEC.md`;
- architecture boundaries: `docs/ARCHITECTURE.md`;
- development and consumer guidance: `docs/DEV_GUIDE.md`;
- security boundaries: `docs/SECURITY.md`;
- iteration scope: approved Issue aligned with `docs/ROADMAP.md`;
- contract behavior and compatibility evidence: tests and verified consumer usage.

Rules:

- no hidden defaults for required contract behavior;
- no duplicate source of truth;
- package metadata must remain internally consistent;
- public contract-module imports must be explicit;
- type contracts are part of the public compatibility surface;
- consumer runtime state is not BeeSDK configuration;
- BeeSDK must not own consumer secrets;
- BeeSDK must not perform hidden runtime I/O;
- preserve compatibility unless the Issue explicitly allows a breaking change.

## Implementation rules

- Stay inside the approved Issue.
- Prefer the smallest complete solution.
- Follow KISS.
- Do not perform unrelated refactoring.
- Do not add speculative architecture.
- Do not create abstractions without a concrete consumer need.
- Do not duplicate existing contracts or logic.
- Do not broaden or narrow an existing extracted contract without an explicit compatibility decision.
- Preserve dependency direction `consumer -> beesdk`.
- Do not add consumer imports to BeeSDK.
- Do not add runtime execution, network access, storage implementation or service behavior to BeeSDK.
- Follow PEP 8.
- Keep public identifiers, package metadata and data fields in English.
- Treat external values passed through public contracts as untrusted.
- Keep read-only, draft-only and execution authority explicit where represented by contracts.
- Host/runtime authority must not be derived from module-controlled payload.
- Keep runtime dependencies empty while the approved BeeSDK baseline requires zero runtime dependencies.
- Do not change `pyproject.toml.version` for ordinary work.

## Documentation and contracts

Update relevant documentation when implementation changes:

- public API;
- public protocol or data contract;
- type signature;
- package/build behavior;
- compatibility guarantee;
- artifact contract;
- capability contract;
- authority or security boundary;
- dependency direction;
- consumer integration contract.

Do not update unrelated documentation.

When public fields, signatures or public contract modules change:

- identify the source of truth;
- document compatibility impact;
- preserve existing behavior when required;
- update contract tests;
- verify public contract-module imports when applicable;
- verify affected consumer compatibility when required by the Issue.

Do not treat implementation convenience as sufficient reason to expand the public SDK surface.

## Verification

Do not run, request or require `uv lock --check` or any dedicated lockfile validation.

When an approved Issue has no dependency change, do not inspect, regenerate, modify or separately validate `uv.lock`.

When an approved dependency change exists, inspect only the necessary dependency and relevant lockfile changes.

Determine the change level from `docs/SDLC.md` and `docs/SECURITY.md`:

- `low-risk`;
- `runtime-risk`;
- `security-sensitive`.

Run checks proportional to the change.

As applicable, verification may include:

- targeted tests;
- `uv run pytest -q`;
- `uv build`;
- package import smoke;
- public contract-module API checks;
- built package contents inspection;
- `py.typed` verification;
- package metadata inspection;
- runtime dependency inspection;
- contract compatibility checks;
- consumer compatibility smoke;
- dependency-direction checks;
- SAST;
- SCA;
- fuzzing when a parser or validator justifies it.

DAST and IAST are normally not applicable while BeeSDK has no network-facing runtime, but use them when the actual approved change introduces a relevant surface.

Review agents using Bee Dev MCP cannot execute commands.

They may use supplied command output as evidence but must:

- name the supplied command;
- distinguish reported evidence from inspected code;
- verify that required scenarios are covered;
- never claim MCP ran tests.

Missing verification is a blocker only when required by the Issue, SDLC or security rules.

## Security

- Never expose secrets, tokens, passwords or complete environment dumps.
- BeeSDK must not own or persist consumer credentials.
- Importing `beesdk` must not perform network access, subprocess execution, service startup, database access or other hidden runtime side effects.
- Treat external input and values passed through public contracts as untrusted.
- Keep runtime authority host-owned.
- Module-controlled payload must not grant, override or escalate authority.
- A module-facing capability caller must not accept caller-controlled runtime identity, policy, credentials or authority unless an approved contract explicitly changes that boundary.
- Capability results are evidence and data, not execution authority.
- Artifact contracts must remain bounded and host-implemented.
- Do not introduce unrestricted filesystem path access through artifact contracts.
- Do not add external mutations or execution behavior to a contracts-only API without explicit security-reviewed scope.
- Keep dependency direction one-way from consumers to BeeSDK.
- Do not add consumer-specific secrets, customer data or runtime configuration to BeeSDK.
- Keep package runtime dependencies minimal; the current v0.1 baseline is zero runtime dependencies.
- Preserve deterministic host-enforced policy and authority boundaries.
- Public type contracts and package exports are part of the security and compatibility boundary.

## Review rules

Review the exact requested target relative to the declared base branch.

Inspect:

- committed changes;
- staged changes;
- unstaged changes;
- untracked files;
- deleted and renamed files;
- complete changed-file contents;
- relevant unchanged public contracts;
- public exports;
- package metadata;
- relevant consumer contracts when explicitly required;
- supplied verification evidence.

Prioritize blockers that affect the current Issue:

- unmet acceptance criteria;
- incorrect or unsafe public behavior;
- security or authority violations;
- SDK/consumer ownership violations;
- reverse consumer dependency;
- conflicting sources of truth;
- incompatible public contracts;
- incompatible type or protocol contracts;
- incorrect public contract-module imports;
- package/build regressions;
- unintended runtime dependencies;
- missing required verification;
- unrelated changes entering the PR;
- unintended dependency or version changes;
- documentation contradicting public behavior;
- missing required consumer compatibility evidence.

Do not make blockers from:

- optional polish;
- personal naming preferences;
- speculative architecture;
- unrelated cleanup;
- requirements absent from the Issue.

Perform one complete review pass and consolidate all real blockers.

Use:

- `.agents/skills/beesdk-plan-iteration/SKILL.md` for planning;
- `.agents/skills/beesdk-review-and-close/SKILL.md` for review and PR preparation.

## Required implementation evidence

The implementation report should contain:

1. files read;
2. change level;
3. source of truth;
4. SDK/consumer/runtime boundary assessment;
5. changed files;
6. exact test commands and results;
7. required package, build and import smoke results;
8. public API, typing and compatibility evidence;
9. package/build artifacts inspected;
10. security review;
11. dependency status;
12. known limitations;
13. confirmation:

```text
version not changed
```

Narrative claims do not replace exact verification evidence.
