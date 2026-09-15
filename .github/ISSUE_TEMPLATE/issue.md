---
name: Issue
about: "Use title prefixes: Feature:, Fix:, Docs:, Chore:, Idea:"
title: "Feature: <short title>"
labels: []
assignees: []
---

### Summary

One sentence: what needs to be done (or explored).

### Type

Select one primary type:

- [ ] Feature
- [ ] Fix
- [ ] Docs
- [ ] Chore
- [ ] Idea

### Roadmap / iteration

- Iteration:
- Stage:
- Goal from `docs/ROADMAP.md`:

If this is not tied to a roadmap iteration, explain why.

### Context

Why this matters. Links, references, consumer evidence.

Include:

- current problem / limitation;
- why now;
- related issue / PR / roadmap item if any;
- affected consumer project if relevant (`beeagent`, `beeagent-rop`, `beescan`, etc.).

### Scope

What is included / excluded.

**Included**

- ...
- ...

**Excluded**

- ...
- ...

### Deliverable

What should exist when this is done.

Examples:

- new or updated public contract;
- new public export;
- updated module contract;
- updated artifact port contract;
- updated capability contract;
- compatibility fix;
- package/build metadata update;
- documentation update.

### Acceptance Criteria

What must be true for this task to be considered done.

- ...
- ...
- ...

Keep criteria observable and testable.

### Change level

Choose one:

- [ ] low-risk
- [ ] runtime-risk
- [ ] security-sensitive

> Use `docs/SDLC.md` / `docs/SECURITY.md` to classify the task.

### Package / Public API / Contract impact

Mark what is expected:

- [ ] no package, public API or contract change expected
- [ ] public contract-module imports may change
- [ ] module contract may change
- [ ] artifact port contract may change
- [ ] capability contract may change
- [ ] package metadata / build behavior may change
- [ ] runtime dependency surface may change
- [ ] backward compatibility / migration impact expected
- [ ] docs update likely required

If known already, list affected files / exports / contracts:

- `...`
- `...`

### Tests

What must be checked:

**Automated**

- [ ] unit / contract tests
- [ ] `uv run pytest -q`

**Package / compatibility**

- [ ] `uv build`
- [ ] package import smoke
- [ ] public contract-module API verification
- [ ] consumer compatibility smoke if applicable

**Quality / security**

Mark what is expected for this task:

- [ ] SAST
- [ ] SCA
- [ ] DAST
- [ ] IAST
- [ ] fuzzing
- [ ] some checks are not applicable

Describe the required scenarios briefly:

- ...
- ...
- ...

### Artifacts

What files / outputs should appear or be updated in tests, docs, package metadata, or build outputs.

Examples:

- `tests/...`
- `src/beesdk/...`
- `README.ru.md`
- `CHANGELOG.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE.md`
- `docs/SDLC.md`
- `docs/SECURITY.md`
- `docs/SPEC.md`
- `pyproject.toml`
- `uv.lock` if an approved dependency change requires it
- built wheel / source distribution when package verification is required

### Security notes

Fill if relevant:

- public API / compatibility boundary involved:
- module / capability authority boundary involved:
- artifact boundary involved:
- runtime dependency changes involved:
- serialization / parsing involved:
- external or untrusted payload involved:
- consumer migration involved:

### Definition of Done

Task is done when:

- [ ] behavior / contract is implemented within the declared scope
- [ ] public API remains explicit and documented
- [ ] backward compatibility is preserved or migration is explicitly documented
- [ ] tests are green
- [ ] package builds successfully when package behavior is affected
- [ ] package imports successfully without consumer projects installed
- [ ] no unintended dependency from `beesdk` to consumer projects was introduced
- [ ] runtime dependencies remain unchanged unless explicitly approved
- [ ] no secrets or consumer-specific data are committed
- [ ] checks required for this task by `docs/SDLC.md` / `docs/SECURITY.md` are completed
- [ ] docs are updated if public contract / compatibility / package behavior changed
- [ ] changelog / version decision is recorded when applicable
- [ ] result is ready to be closed through PR

### Notes

Constraints, assumptions, extra links.

Use this section for:

- follow-up ideas;
- explicit non-goals;
- migration notes;
- reviewer hints;
- consumer compatibility notes;
- implementation constraints.
