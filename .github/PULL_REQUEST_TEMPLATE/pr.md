### Summary

What was done in this PR.

Include short, concrete statements:

- what behavior / contract changed;
- what files/modules were touched;
- what was intentionally not changed.

### Related issue

Closes #

If relevant, also reference:

- ROADMAP iteration:
- related docs:
- affected consumer:
- follow-up issues:

### Iteration

- Iteration:
- Goal:
- Change level:
  - [ ] low-risk
  - [ ] runtime-risk
  - [ ] security-sensitive

> Use the current iteration from `docs/ROADMAP.md`.
> Change level should match `docs/SDLC.md` / `docs/SECURITY.md`.

### Scope

What is included / excluded.

**Included**

- ...
- ...

**Excluded**

- ...
- ...

### Changes

- ...
- ...
- ...

### Package / Public API / Contract impact

Mark what changed:

- [ ] no package, public API or contract changes
- [ ] public contract-module imports changed
- [ ] module contract changed
- [ ] artifact port contract changed
- [ ] capability contract changed
- [ ] package metadata / build behavior changed
- [ ] runtime dependency surface changed
- [ ] backward compatibility / migration behavior changed
- [ ] docs updated

If applicable, specify:

**New / changed public exports**

- `...`

**New / changed contracts**

- `...`

**New / changed package metadata**

- `...`

**Compatibility / migration impact**

- `...`

### Verification level

Required checks for this PR:

**Base checks**

- [ ] `uv run pytest -q`
- [ ] `uv build` when package/build behavior is affected
- [ ] package import smoke completed
- [ ] public API / contract behavior checked

**Compatibility checks**

- [ ] package works without consumer projects installed
- [ ] dependency direction remains consumer -> `beesdk`
- [ ] affected consumer compatibility smoke completed when required

**Quality / security checks**

Mark only what is required for this PR:

- [ ] SAST completed
- [ ] SCA completed
- [ ] DAST completed
- [ ] IAST completed
- [ ] fuzzing completed
- [ ] not applicable (explained in Notes)

> Only mark checks that are required for this change level.
> Use `docs/SDLC.md` and `docs/SECURITY.md` as source of truth.

#### Test details

Commands / scenarios used:

- `...`
- `...`

Include automated and compatibility verification when relevant.

#### Manual scenarios checked

- ...
- ...
- ...

### Artifacts

What was created or verified:

- ...
- ...
- ...

If applicable, list exact files, for example:

- `tests/...`
- `src/beesdk/...`
- `README.ru.md`
- `CHANGELOG.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE.md`
- `docs/SPEC.md`
- `pyproject.toml`
- `uv.lock`
- built wheel / source distribution

### Security review

Fill only if relevant for this PR:

- public API / compatibility boundary affected:
- module / capability authority boundary affected:
- artifact boundary affected:
- runtime dependency surface changed:
- serialization / parsing changed:
- external or untrusted payload affected:
- consumer migration required:

### Checklist

#### SDLC / scope

- [ ] change stays within current iteration / declared standalone scope
- [ ] issue, code, tests, docs, and PR are aligned
- [ ] `docs/ROADMAP.md` updated if roadmap status or planned contract changed
- [ ] related docs updated if needed (`DEV_GUIDE`, `README.ru.md`, `SPEC`, `SDLC`, `SECURITY`, `ARCHITECTURE`)

#### Package / public API / contracts

- [ ] public contracts are imported through explicit BeeSDK contract modules
- [ ] no consumer-specific implementation was added to BeeSDK
- [ ] dependency direction remains consumer -> `beesdk`
- [ ] backward compatibility is preserved or migration is documented
- [ ] module / artifact / capability boundaries remain explicit
- [ ] runtime dependencies remain unchanged unless explicitly approved
- [ ] package builds and imports as expected

#### Security

- [ ] no secrets or consumer-specific private data committed
- [ ] no unsafe execution / egress behavior introduced
- [ ] dependency changes were reviewed
- [ ] authority remains host-owned where applicable
- [ ] security checks required for this PR were completed

#### Code quality

- [ ] change follows KISS
- [ ] no unnecessary abstraction / refactor was added
- [ ] public API remains minimal
- [ ] project style respected

#### Version / release

- [ ] no version change required
- [ ] version / changelog change is intentional and release-related
- [ ] breaking compatibility impact is explicitly documented if applicable

### Limitations / follow-ups

Anything intentionally left out of scope:

- ...
- ...

### Notes

Anything important for reviewer.

Examples:

- why some checks are marked not applicable;
- known limitations;
- compatibility notes;
- migration / deprecation notes;
- what to inspect first during review.
