#!/usr/bin/env python3
"""Structural detector for self-sealing interpretation.

A mind anti-virus is not the correct counter-belief; that would be another
candidate infection wearing a lab coat. It is the preservation of
discrimination, provenance, reopenability, and independent return.

This auditor therefore never judges whether a change is correct. It judges
whether the change left the correction channel reachable:

  R1  an episode must not MODIFY a checker and an artifact that checker guards
  R2  an episode must not DELETE a declared fence token from a governance surface
  R3  an episode must not MODIFY a prefrozen artifact

An "episode" is a contiguous run of commits by one author with no gap longer
than episode_gap_seconds. That is the unit in which a working session can
quietly move a goalpost.

The grouping is coarse and its precision is poor for long sessions: on this
branch the largest episode is 308 commits, so R1 can fire on a checker and a
guarded file touched hours apart with nothing to do with each other. Treat R1
as a prompt to look, never as a verdict. The 2026-09-26 contamination sat
1644s after the branch's own work, inside the 1800s window, so the gap did NOT
separate it -- co-modification did.

R1 fires on modification, not introduction. Adding a checker together with its
own scope declaration is bootstrap, not self-sealing: there is no prior
judgment for the new rule to retroactively alter. Editing both later is.

There is deliberately NO restoration bypass. An earlier version skipped R1 when
a checker's blob matched one it had held before, reasoning that a restored rule
is independent of whoever restored it. An adversarial review showed that across
501 commits the bypass suppressed exactly one finding -- its author's own -- and
that it was unsound twice over: it inspected only the checker, ignoring novel
edits to guarded artifacts in the same episode, and it counted corrupt ancestor
blobs as valid restorations, so re-applying a known corruption verbatim would
have passed. Restoration episodes are now declared residuals like any other.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE_PATH = ROOT / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json"


def git(*args: str) -> str:
    cp = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if cp.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {cp.stderr.strip()}")
    return cp.stdout


def normalize(text: str) -> str:
    """Fence tokens appear with both ASCII != and typographic forms."""
    return (
        text.replace("≠", "!=")
        .replace("→", "->")
        .replace(" ", " ")
    )


class Commit:
    __slots__ = ("sha", "author", "when", "subject", "changes")

    def __init__(self, sha: str, author: str, when: int, subject: str):
        self.sha = sha
        self.author = author
        self.when = when
        self.subject = subject
        self.changes: dict[str, str] = {}


def load_commits(since: str) -> list[Commit]:
    sep = "\x1e"
    raw = git(
        "log",
        f"--since={since}",
        "--reverse",
        "--no-merges",
        f"--format={sep}%H%x1f%an%x1f%at%x1f%s",
        "--name-status",
    )
    commits: list[Commit] = []
    for block in raw.split(sep):
        block = block.strip("\n")
        if not block:
            continue
        head, _, tail = block.partition("\n")
        sha, author, when, subject = head.split("\x1f", 3)
        commit = Commit(sha, author, int(when), subject)
        for line in tail.splitlines():
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            status, path = parts[0], parts[-1]
            commit.changes[path] = status[0]
        commits.append(commit)
    return commits


def group_episodes(commits: list[Commit], gap: int) -> list[list[Commit]]:
    episodes: list[list[Commit]] = []
    for commit in commits:
        if (
            episodes
            and episodes[-1][-1].author == commit.author
            and commit.when - episodes[-1][-1].when <= gap
        ):
            episodes[-1].append(commit)
        else:
            episodes.append([commit])
    return episodes


def waived(commit: Commit, rule: str, exceptions: list[dict]) -> bool:
    """A waiver must name the exact commit it forgives.

    Matching on subject prefix alone is forgeable: any later commit reusing the
    subject line would inherit the waiver. When commit_sha is declared it is
    required, and the subject must still match, so both have to agree.
    """
    for row in exceptions:
        if rule not in row.get("rules_waived", []):
            continue
        sha = row.get("commit_sha", "")
        prefix = row.get("commit_subject_prefix", "")
        if sha and not commit.sha.startswith(sha):
            continue
        if prefix and not commit.subject.startswith(prefix):
            continue
        if sha or prefix:
            return True
    return False


def removed_fence_tokens(sha: str, path: str, tokens: list[str]) -> list[str]:
    try:
        diff = git("show", "-U0", "--format=", sha, "--", path)
    except RuntimeError:
        return []
    hits: list[str] = []
    for line in diff.splitlines():
        if not line.startswith("-") or line.startswith("---"):
            continue
        body = normalize(line[1:])
        for token in tokens:
            if normalize(token) in body and token not in hits:
                hits.append(token)
    return hits


ISO_WITH_OFFSET = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?(Z|[+-]\d{2}:\d{2})$"
)


def has_explicit_offset(since: str) -> bool:
    """True only for a full ISO-8601 timestamp with a valid UTC offset.

    `git log --since="2026-09-26 00:00"` is read in the local timezone of the
    machine running it. The 2026-09-26 repair was verified on a machine at
    UTC-03:00 and gated in CI at UTC; the three-hour difference put about 109
    more commits and three more findings into the window in CI only, so every
    local "make audit exit 0" on the repair was true on the author's laptop
    and false on the gate. A verdict that depends on where it runs is a check
    weaker than its name.

    The first version of this check only looked for an offset-like suffix, and
    an independent review showed it accepted "yesterday Z", "Sep 26 2026 -1200"
    and "+99:99", all still clock- or timezone-dependent. The value must now
    parse as an ISO timestamp whose offset is real.
    """
    value = since.strip()
    if not ISO_WITH_OFFSET.match(value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def is_prefrozen(path: str, markers: list[str]) -> bool:
    return any(marker in path for marker in markers)


def previously_declared() -> set[str] | None:
    """Residual keys declared by the last committed version of the scope file.

    The scope declaration is this auditor's control plane, and editing it alone
    changes what the auditor will report without touching the auditor. R4
    therefore compares the working declaration against its own last committed
    state: a residual may be added freely, but one that disappears must be
    accounted for in closed_residuals with the return that closed it.

    Returns None when there is no prior version to compare against.
    """
    rel = SCOPE_PATH.relative_to(ROOT).as_posix()
    try:
        prior = git("show", f"HEAD:{rel}")
    except RuntimeError:
        return None
    try:
        data = json.loads(prior)
    except json.JSONDecodeError:
        return None
    return {row["key"] for row in data.get("declared_residuals", []) if "key" in row}




def main() -> int:
    if not SCOPE_PATH.exists():
        print("WITHHOLD: self-sealing audit scope declaration is absent")
        return 2
    try:
        scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"WITHHOLD: scope declaration does not parse: {exc}")
        return 2

    gap = int(scope.get("episode_gap_seconds", 1800))
    since = scope.get("audit_since")
    if not since:
        print("WITHHOLD: scope declares no audit_since window")
        return 2
    if not has_explicit_offset(since):
        print(
            f"WITHHOLD: audit_since {since!r} carries no explicit UTC offset. git "
            "resolves a bare date in the local timezone of whatever machine runs "
            "the audit, so the window -- and the verdict -- would differ between "
            "a laptop and CI."
        )
        return 2

    exceptions = scope.get("admitted_exceptions", [])
    fence_tokens = scope.get("fence_tokens", [])
    fence_surfaces = set(scope.get("fence_surfaces", []))
    markers = scope.get("prefreeze_markers", [])

    guard_map: dict[str, set[str]] = {}
    for row in scope.get("guarded", []):
        guard_map.setdefault(row["checker"], set()).update(row.get("guards", []))

    try:
        shallow = git("rev-parse", "--is-shallow-repository").strip() == "true"
        commits = load_commits(since)
    except RuntimeError as exc:
        print(f"WITHHOLD: cannot resolve audit window: {exc}")
        return 2
    # An audit over no history is not a pass. The first version of this
    # auditor reported PASS over 0 commits when a bare date parsed to nothing;
    # that was recorded as fixed and regression-tested, and neither was true
    # until this guard. A shallow clone is the same failure by another route:
    # truncated history cannot support a verdict about history.
    if shallow and not git("log", "-1", "--format=%H", f"--before={since}").strip():
        # Shallow is fine when the cut lies before the window. It is not when
        # no commit older than the window start survives: then the window
        # itself may be truncated and the episode grouping at its start is
        # unknowable.
        print("WITHHOLD: shallow clone with no commit before the audit window; "
              "the window may be truncated")
        return 2
    if not commits:
        print(f"WITHHOLD: no commits in the audit window since {since}; nothing was audited")
        return 2

    declared = {
        row["key"]: row for row in scope.get("declared_residuals", [])
    }
    episodes = group_episodes(commits, gap)
    findings: list[tuple[str, str]] = []
    r1_through: dict[str, str] = {}

    for episode in episodes:
        touched: dict[str, str] = {}
        for commit in episode:
            for path, status in commit.changes.items():
                # a path added then modified in one episode counts as added
                touched.setdefault(path, status)

        span = f"{episode[0].sha[:8]}..{episode[-1].sha[:8]}"
        author = episode[0].author

        # R1 — checker modified alongside an artifact it guards
        for checker, guards in guard_map.items():
            if touched.get(checker) != "M":
                continue
            overlap = sorted(guards & set(touched))
            if not overlap:
                continue
            if all(waived(c, "R1_SELF_SEALING", exceptions) for c in episode):
                continue
            key = f"R1_SELF_SEALING|{checker}|{episode[0].sha[:8]}"
            through = [c.sha[:8] for c in episode if checker in c.changes][-1]
            findings.append((
                key,
                f"R1_SELF_SEALING [{span}] {author}: checker {checker} was modified "
                f"in the same episode as the artifacts it guards: {', '.join(overlap)} "
                f"(last checker change {through})",
            ))
            r1_through[key] = through

        # R2 — fence token deleted from a governance surface
        for commit in episode:
            if waived(commit, "R2_FENCE_REMOVAL", exceptions):
                continue
            for path in sorted(set(commit.changes) & fence_surfaces):
                lost = removed_fence_tokens(commit.sha, path, fence_tokens)
                if lost:
                    findings.append((
                        f"R2_FENCE_REMOVAL|{path}|{commit.sha[:8]}",
                        f"R2_FENCE_REMOVAL [{commit.sha[:8]}] {commit.author}: "
                        f"{path} lost fence token(s): {'; '.join(lost)}",
                    ))

        # R3 — prefrozen artifact mutated
        for commit in episode:
            if waived(commit, "R3_PREFREEZE_MUTATION", exceptions):
                continue
            for path, status in sorted(commit.changes.items()):
                if status == "M" and is_prefrozen(path, markers):
                    findings.append((
                        f"R3_PREFREEZE_MUTATION|{path}|{commit.sha[:8]}",
                        f"R3_PREFREEZE_MUTATION [{commit.sha[:8]}] {commit.author}: "
                        f"prefrozen artifact modified: {path}",
                    ))

    # R4 — a declared residual may never be silently removed from the scope file
    prior_keys = previously_declared()
    if prior_keys is not None:
        closed = {row["key"] for row in scope.get("closed_residuals", []) if "key" in row}
        vanished = sorted(prior_keys - set(declared) - closed)
        if vanished:
            print(f"R4_RESIDUAL_DELETED ({len(vanished)})")
            for key in vanished:
                print(f"  {key}")
            print()
            print("A residual was removed from the scope declaration without a")
            print("closing return. Residuals are never gauge, so deleting one is")
            print("exactly the silent compression this auditor exists to prevent.")
            print("Move it to closed_residuals with the evidence that closed it.")
            return 1
        for row in scope.get("closed_residuals", []):
            if not row.get("closing_return", "").strip():
                print(f"R4_RESIDUAL_DELETED: closed residual {row.get('key')} "
                      f"records no closing return")
                return 1

    # An R1 residual is keyed by the episode's first commit, and an episode
    # keeps growing while its author keeps committing. Without a bound, one
    # declaration silently covered every later edit to the same checker in the
    # same episode: on 2026-09-26 a residual declared for 576145e went on to
    # absorb dfe8930 and e83b650, and a commit deleting a deny-list item and
    # editing the auditor passed. Each R1 declaration therefore names the last
    # checker-modifying commit it covers; a later one is a fresh finding.
    grown = {
        key for key, through in r1_through.items()
        if key in declared and declared[key].get("through") != through
    }
    fresh = [(key, msg) for key, msg in findings if key not in declared or key in grown]
    carried = [(key, msg) for key, msg in findings if key in declared and key not in grown]
    stale = sorted(set(declared) - {key for key, _ in findings})

    if carried:
        print(f"DECLARED RESIDUALS ({len(carried)}) — unadjudicated, not compressed")
        for key, msg in carried:
            row = declared[key]
            print(f"  {msg}")
            print(f"      reopen: {row.get('reopening_condition', 'UNSPECIFIED')}")
        print()

    if stale:
        # A residual that no longer reproduces has been silently compressed away.
        # Per the residual law, that is exactly the failure this auditor exists
        # to prevent, so it fails closed rather than quietly shrinking the list.
        print(f"STALE DECLARED RESIDUALS ({len(stale)}) — declared but no longer detected")
        for key in stale:
            print(f"  {key}")
        print()
        print("A declared residual that stops reproducing was either resolved or")
        print("compressed away. Remove it from the scope declaration explicitly,")
        print("with the return that closed it. Do not let it lapse silently.")
        return 1

    if fresh:
        print(f"SELF-SEALING AUDIT FINDINGS ({len(fresh)})")
        for key, msg in fresh:
            print(f"  {msg}")
            if key in grown:
                print(
                    f"      declared through {declared[key].get('through', 'NOTHING')}; "
                    f"the checker was modified again after that declaration"
                )
        print()
        print("A finding is not proof the change is wrong. It is proof the change")
        print("altered a rule of judgement without an independent return. Either")
        print("supply that return, or record an admitted exception with reasoning in")
        print("kernel/development/SELF_SEALING_AUDIT_SCOPE.json.")
        return 1

    print(
        f"SELF-SEALING AUDIT PASS "
        f"({len(commits)} commits since {since}; {len(episodes)} episodes; "
        f"{len(guard_map)} guarded checkers; {len(fence_tokens)} fence tokens; "
        f"{len(carried)} declared residuals carried)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
