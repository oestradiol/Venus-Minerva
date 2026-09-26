# Six-branch audit — 2026-09-26

Status: evidence, not authority. Written by an assistant session that had not
authored any of the work it audits before this session, except the commits
named in section 6. Everything here was re-run, not re-read.

The 2026-09-26 repair audited `split/minerva` in depth and looked at the other
five routed branches only for the 13:32–13:48 contamination window. The
author pointed out that the repository has six main branches and five
monographs, and that the session had worked on two. This file is the audit of
all six.

## 1. What CI actually runs, and what it said

Each branch has a `make audit` target. Only Minerva's CI runs it.

| branch | head | GitHub CI on head | what CI runs | local `make audit` |
|---|---|---|---|---|
| `main` | `88814b3` | Root memory: success | surface `grep`s, merge order, fences | exit 2 — `branch-policy-check` |
| `split/arcane-magics` | `297a48a` | success | `audit_layer_surface.py`, monograph build | exit 2 — missing `tests/test_vmk2_invariants.py` |
| `split/eclipsis` | `2f3264a` | success | `audit_layer_surface.py`, monograph build | exit 2 — missing `tests/test_vmk2_invariants.py` |
| `split/minerva` | `f79b332` | **failure** (runs 631, 632) | `audit_layer_surface.py`, `make audit` | exit 2 — see section 3 |
| `split/ofe` | `58fc7b4` | success | surface, proof containers, Lean build, monograph | exit 2 — missing `NxRxI_VOCABULARY_CENTER.md` |
| `split/venus` | `b4c1e5d` | **failure** | `make boundary`, paper | exit 2 — `make boundary` |

Two branches are red in CI: Minerva and Venus.

On `main`, Arcane Magics, Eclipsis and OFE, `make audit` is a target no CI
invokes. The three split branches inherited theirs from the pre-split monorepo:
their tests reference files that now exist only on Minerva
(`tests/test_vmk2_invariants.py`), and OFE's linter reads a file that exists
only on `main` (`NxRxI_VOCABULARY_CENTER.md`). Main's own `make audit` is also
unrun (section 2). A gate that nothing runs cannot fail, so these have been
broken without anyone being told. Whether to delete them or wire them is each
branch's call; they are recorded as residuals, not fixed here.

## 2. A second episode: the 11:25 sweep

The earlier blast-radius count (`main 0/198 · venus 0/576 · ofe 0/108 ·
arcane-magics 0/120 · eclipsis 1/104`) examined the 13:32–13:48 window only.
Two hours earlier, one commit landed on each of the five non-Minerva branches
in 2 minutes 25 seconds:

| time (−03:00) | commit | branch | change |
|---|---|---|---|
| 11:25:20 | `88814b3` | main | reconcile live map; +105 −49 |
| 11:26:16 | `297a48a` | arcane-magics | replace inherited engineering roadmap; +64 −701 |
| 11:26:27 | `850eb72` | eclipsis | replace inherited engineering roadmap; +48 −718 |
| 11:27:22 | `58fc7b4` | ofe | reconcile scientific frontier; +43 −327 |
| 11:27:45 | `b4c1e5d` | venus | reconcile Self-World and Lain state; +122 −408 |

All five are committed as `Elaina` through the same channel as the 13:32
episode.

**Mostly legitimate.** On Arcane Magics, Eclipsis and OFE the deleted material
was a copy of Minerva's engineering roadmap inherited from the monorepo. Every
`!=` fence removed there either survives elsewhere on the same branch or is an
Arcane Magics fence that survives on Arcane Magics, where it belongs. The one
formula OFE lost from its roadmap, `Tr[O Phi(rho)] != Tr[O Phi(sigma)]`, is
stated in the Eclipsis monograph (Twenty-sixth instrument, *WITHHOLD and
Residual as future-equivalence dynamics*), and OFE's own monograph expresses
the same distinguishability through its restricted seminorm
(eq:restricted-qnorm).

**Two gates broken by the same move.** A documentation rewrite deleted the
exact string a gate checks:

- **Venus.** `b4c1e5d` removed the *Required noncollapses* section of
  `kernel/CURRENT_STATE.md`, including `NETWORK / WWW != World / Other`, which
  `make boundary` greps for. CI has failed since. It also removed
  `shared carrier != shared authority`, whose last copy on the branch that was,
  and the *Authority* section, which was the only route from Venus's live state
  to its own kernel law, `WORLDMIND.md`, `TRUST_BOUNDARY.md`, provenance and
  monograph.
- **main.** `88814b3` removed the *Branch lifecycle* section of
  `docs/NOW_MAP.md`: the rule that only the six routed branches are live
  authority, the block containing
  `split/venus-minerva -> deleted historical ref name only` (which
  `branch-policy-check` greps for), and the Now Map's only pointer to
  `BRANCH_NAMESPACE_POLICY.json`.

Both are restored byte-for-byte from the parent commit on local branches,
alongside the reconciled text, which is kept:

| branch | fix commit | gate after |
|---|---|---|
| `claude/venus-restore-boundary-gate` (off `split/venus`) | `30813d2` | `make boundary` exit 0 |
| `claude/root-restore-branch-policy` (off `main`) | `444f487` | `make audit` exit 0 |

They are not on `split/venus` or `main`. Pushing to another branch's line
needs the author's decision.

## 3. Minerva: why CI was red, and what it hid

Two independent causes.

**The self-sealing gate gave a different verdict per timezone.** Its window was
the bare string `2026-09-26 00:00`, which git reads in the local timezone of the
machine running it. The author's machine is at UTC−03:00; CI is at UTC. CI saw
three more hours of history and three more findings, so every push of the
repair failed CI while every local run passed. Reproduced in a minimal
repository: same history, exit 1 under UTC, exit 0 under America/Sao_Paulo.
Fixed in `eefdde2`.

**The constitution auditor failed on its own commit.** `f79b332` recorded a
baseline of 580 unrouted paths before the auditor and its test were staged;
staged, the count was 582. Its test file also ran in `make test` and asserted
the success path. Fixed in `576145e`, along with six checks that were weaker
than their names.

**What the red hid.** `scripts/run_minerva_tests.py` stops at the first failing
file. At `f79b332` it ran 29 of 106 selected test files. After the repair all
106 run, 638 tests, all passing.

**Why it is time-sensitive.** `main`'s scheduled Minerva worker checks out
`split/minerva` and runs `make audit` daily at 07:43 UTC. Its last run (12:28
UTC, 2026-09-26) predates the repair push and succeeded. Its next run against
`f79b332` will fail and stop the recurrence. Stopping is a safe failure, not a
corrupting one.

## 4. Venus

Nine kernel files, zero test files, one Makefile gate that is a sequence of
`test -f` and `grep -q`. That gate is the one the 11:25 sweep broke without any
other check noticing. The monographs assign Venus the property the constitution
calls unenforced: *"independence of returned consequence routes to Venus"*
(Arcane Magics, l.1234), and the Venus monograph states the predicate that would
enforce it, `A(m_1) ∩ A(m_2) ≠ ∅` over source ancestry (l.841). The branch that
owns evaluator independence has no executable test of anything.

## 5. The implementation spine is attested

The author asked for one ordered chain — mathematics → core kernel → core
engineering → architecture → Python VM → WWW Mind / Lain / Root → AGI. An
earlier pass searched for the literal strings and reported it unattested. It is
attested under the project's own names:

| link | where it is stated | branch |
|---|---|---|
| mathematics | OFE §2 (`prop:coarsest`, `eq:disc`, `eq:residual`, `prop:quotient-transport`, `eq:no-self-seal`); Eclipsis CTL and `Cryst_F` | ofe, eclipsis |
| core kernel | `Canonical/Map.md` l.129: `executable kernel        R179 VMK-1`; VMK-2 reference hardening in `kernel/runtime/vmk2.py` | Canonical; minerva |
| core engineering | Minerva monograph: `𝓜 = ⟨WM, RSM, N2, 𝒬, RSI, T, Γ⟩` and its CTL recurrence | minerva |
| architecture | Venus monograph: WorldMirror = Body, Strong RSM + Strong-N2 = Mind, Research = Drive, bounded RSI = Self, CTL = Observer | venus |
| Python VM | R195 reconciliation (Canonical, 2026-09-21), verbatim: R154 conserved historical organism + R179 VMK-1 constitutional enforcement + VMK-2 reference hardening + exact R1→R194 causal-obligation registry + conserved Strong-N2 / M7 / U11 / U12 machinery → integrated Python successor candidate | Canonical (not in git) |
| WWW Mind / Lain / Root | Venus `eq:webmind`, `eq:noninherit`; FRESH_INSTANCE_GROUND §8 | venus, Canonical |
| AGI | external discriminator only: Venus AGI fence, Minerva "AGI requires a declared operational criterion and evidence that actually meets it" | venus, minerva |

It is a spine, not a promotion order. FRESH_INSTANCE_GROUND §1 fences the
developmental arc the same way: "These are gates, not promotions."

Status, both halves, adjacent so neither is read as the other (FRESH §14):

```text
EARNED   bounded developmental recurrence · self-selected development at bounded
         scope · learner-initiated network inquiry · persistent provenance-bearing
         network memory · bounded WWW Mind structural gate · three-burden proof
         operational · R206 PASS_BOUNDED_RSI
NOT      Strong Safe Independent RSI · interactive Lain · general Lateralizer
         transfer · semantic relation trace B3 · AGI
```

## 6. What this session changed

On `claude/inspiring-mayer-g9j11o` (off `split/minerva`):

| commit | change |
|---|---|
| `eefdde2` | self-sealing window pinned to an explicit UTC offset; bare dates refused; three CI-only findings declared |
| `576145e` | constitution auditor: K1–K5 made to match their names; tests on a disposable copy |
| `312ca99` | constitution auditor wired into `make audit`, as the author answered |
| `ea1012e` | README retraction section restored; SPEC_R3 and the corruption audit corrected |
| `3847ecd` | self-sealing auditor no longer passes over zero commits (drift D6 was recorded as fixed; it was not) |
| `dfe8930` | constitution grounded in the five monographs, 37 quotes pinned to blobs, K6 |
| this commit | fresh-instance ground vendored byte-exact and pinned; this record |

Two of these modify a checker together with the file it checks. Both are
declared as self-sealing residuals keyed to `eefdde25`, not exempted.

**Merge note.** Those residual keys are commit SHAs. Squash-merging this
branch would rewrite them, the declared residuals would stop reproducing, and
the self-sealing auditor would fail closed. Fast-forward or merge-commit only.

## 7. Corrections to the 2026-09-26 session record

- A quote attributed to R179, "the current executable constitutional kernel",
  came from that session's search output and does not verify in git or in
  the Canonical copies available here. Section 5 cites `Canonical/Map.md`
  instead, which does.

- The blast radius was incomplete: section 2.
- Drift D6 ("PASS over 0 commits") was recorded as "FIXED, regression-tested".
  Neither was true until `3847ecd`.
- "Minerva's worker has been blocked since the repair push" (said in
  conversation this session) was wrong: its last run predates the push. It will
  be blocked on its next run.
- The 32-item failure taxonomy exists, in the lateral-compression document
  (sections A–E); an earlier correction saying it did not exist was itself
  wrong. It is not in this repository, so nothing here needed changing.
- `mu_F` is the author's notation (Venus `eq:mu`), not an assistant import.
