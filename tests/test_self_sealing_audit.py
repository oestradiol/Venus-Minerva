from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_self_sealing.py"
SCOPE_PATH = ROOT / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json"

_spec = importlib.util.spec_from_file_location("self_sealing", SCRIPT)
if _spec is None or _spec.loader is None:
    raise RuntimeError("cannot load self-sealing auditor")
audit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(audit)


class ScopeDeclarationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))

    def test_scope_is_candidate_without_authority(self):
        self.assertEqual(self.scope["status"], "CANDIDATE_NOT_ADMITTED")
        self.assertFalse(self.scope["promotion_authority"])
        self.assertFalse(self.scope["truth_authority"])

    def test_guarded_checkers_and_guards_exist_on_branch(self):
        for row in self.scope["guarded"]:
            with self.subTest(checker=row["checker"]):
                self.assertTrue(
                    (ROOT / row["checker"]).exists(),
                    f"declared checker absent: {row['checker']}",
                )
            for guard in row["guards"]:
                with self.subTest(guard=guard):
                    self.assertTrue(
                        (ROOT / guard).exists(),
                        f"declared guarded artifact absent: {guard}",
                    )

    def test_fence_surfaces_exist_on_branch(self):
        for path in self.scope["fence_surfaces"]:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).exists())

    def test_every_declared_residual_carries_a_reopening_condition(self):
        # A residual without a reopening condition is not a residual; it is a
        # silent compression wearing a residual's name.
        for row in self.scope["declared_residuals"]:
            with self.subTest(key=row["key"]):
                self.assertIn("key", row)
                self.assertTrue(row.get("reopening_condition", "").strip())
                self.assertIn(
                    row.get("class"),
                    {"UNADJUDICATED", "CONTAMINATION_ATTESTED_AND_REVERTED"},
                )

    def test_declared_residual_keys_are_unique(self):
        keys = [row["key"] for row in self.scope["declared_residuals"]]
        self.assertEqual(len(keys), len(set(keys)))

    def test_admitted_exceptions_state_a_reason_and_independent_check(self):
        for row in self.scope.get("admitted_exceptions", []):
            with self.subTest(prefix=row.get("commit_subject_prefix")):
                self.assertTrue(row.get("reason", "").strip())
                self.assertTrue(row.get("rules_waived"))

    def test_known_contamination_is_declared_not_erased(self):
        keys = {row["key"] for row in self.scope["declared_residuals"]}
        self.assertIn("R2_FENCE_REMOVAL|AGENTS.md|3d9dc269", keys)
        self.assertIn(
            "R1_SELF_SEALING|scripts/lint_github_markdown.py|cda936eb", keys
        )


class EpisodeGroupingTests(unittest.TestCase):
    @staticmethod
    def commit(sha: str, author: str, when: int) -> object:
        return audit.Commit(sha, author, when, f"subject {sha}")

    def test_gap_longer_than_threshold_starts_a_new_episode(self):
        commits = [
            self.commit("a", "X", 0),
            self.commit("b", "X", 100),
            self.commit("c", "X", 100 + 1801),
        ]
        episodes = audit.group_episodes(commits, 1800)
        self.assertEqual([len(e) for e in episodes], [2, 1])

    def test_author_change_starts_a_new_episode(self):
        commits = [
            self.commit("a", "X", 0),
            self.commit("b", "Y", 10),
        ]
        self.assertEqual(len(audit.group_episodes(commits, 1800)), 2)

    def test_the_real_contamination_gap_separates_episodes(self):
        # 13:04:46 -> 13:32:10 is 1644s, inside the default window, so the
        # detector must not rely on the gap alone; it relies on co-modification.
        commits = [
            self.commit("good", "Elaina", 0),
            self.commit("bad", "Elaina", 1644),
        ]
        self.assertEqual(len(audit.group_episodes(commits, 1800)), 1)


class HelperTests(unittest.TestCase):
    def test_normalize_folds_typographic_fence_forms(self):
        self.assertEqual(audit.normalize("a ≠ b"), "a != b")
        self.assertEqual(audit.normalize("x → y"), "x -> y")

    def test_is_prefrozen_matches_declared_markers(self):
        markers = ["_PREFREEZE.json"]
        self.assertTrue(audit.is_prefrozen("kernel/x_PREFREEZE.json", markers))
        self.assertFalse(audit.is_prefrozen("kernel/x.json", markers))

    def test_waiver_requires_both_subject_match_and_rule(self):
        commit = audit.Commit("s", "A", 0, "revert(minerva): undo something")
        exceptions = [
            {
                "commit_subject_prefix": "revert(minerva): undo",
                "rules_waived": ["R2_FENCE_REMOVAL"],
            }
        ]
        self.assertTrue(audit.waived(commit, "R2_FENCE_REMOVAL", exceptions))
        self.assertFalse(audit.waived(commit, "R1_SELF_SEALING", exceptions))

    def test_unrelated_subject_is_not_waived(self):
        commit = audit.Commit("s", "A", 0, "feat: something else")
        exceptions = [
            {
                "commit_subject_prefix": "revert(minerva): undo",
                "rules_waived": ["R2_FENCE_REMOVAL"],
            }
        ]
        self.assertFalse(audit.waived(commit, "R2_FENCE_REMOVAL", exceptions))


class FenceCoverageTests(unittest.TestCase):
    """The fences the 2026-09-26 episode deleted must all be watched."""

    def test_deleted_fences_are_all_declared_tokens(self):
        scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
        tokens = {audit.normalize(t) for t in scope["fence_tokens"]}
        for lost in (
            "external model != Minerva",
            "can inspect != can claim",
            "self-implication != self-certification",
            "re-derivation != memory lookup",
            "current Perspective != diachronic Observer",
            "INTENDED -> WRITTEN -> VERIFIED -> ADMITTED",
        ):
            with self.subTest(fence=lost):
                self.assertIn(audit.normalize(lost), tokens)


class DetectionTests(unittest.TestCase):
    """End-to-end: build a synthetic repo and assert each rule actually fires.

    The earlier suite exercised helpers only. An adversarial review noted that
    nothing tested main(), removed_fence_tokens, or the rules themselves -- so
    the suite could not have caught a detector that silently stopped detecting.
    """

    def build(self, scope_extra=None, script=None):
        import subprocess
        import tempfile

        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(tmp, ignore_errors=True))

        def run(*args, when=None):
            env = None
            if when:
                import os

                env = dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
            subprocess.run(
                ["git", *args], cwd=tmp, check=True, capture_output=True, env=env
            )

        run("init", "-q")
        run("config", "user.email", "t@example.invalid")
        run("config", "user.name", "Tester")
        (tmp / "scripts").mkdir()
        (tmp / "kernel" / "development").mkdir(parents=True)

        scope = {
            "episode_gap_seconds": 1800,
            "audit_since": "2000-01-01T00:00:00+00:00",
            "guarded": [{"checker": "scripts/check.py", "guards": ["GUARDED.md"]}],
            "fence_tokens": ["a != b"],
            "fence_surfaces": ["GUARDED.md"],
            "prefreeze_markers": ["_PREFREEZE.json"],
            "admitted_exceptions": [],
            "declared_residuals": [],
        }
        scope.update(scope_extra or {})
        (tmp / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json").write_text(
            json.dumps(scope), encoding="utf-8"
        )
        (tmp / "scripts/check.py").write_text("# checker v1\n", encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nkeep\n", encoding="utf-8")
        (tmp / "kernel/development/X_PREFREEZE.json").write_text("{}\n", encoding="utf-8")
        run("add", "-A")
        # Baseline sits in its own episode, far in the past, so that a later
        # edit reads as MODIFY rather than collapsing into bootstrap ADD.
        run("commit", "-qm", "baseline", when="2020-01-01T00:00:00+0000")
        return tmp, run

    def audit_in(self, tmp):
        old_root, old_scope = audit.ROOT, audit.SCOPE_PATH
        audit.ROOT = tmp
        audit.SCOPE_PATH = tmp / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json"
        try:
            import contextlib
            import io

            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = audit.main()
            return code, buf.getvalue()
        finally:
            audit.ROOT, audit.SCOPE_PATH = old_root, old_scope

    def test_r1_fires_when_checker_and_guarded_change_together(self):
        tmp, run = self.build()
        (tmp / "scripts/check.py").write_text("# checker v2\n", encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nchanged\n", encoding="utf-8")
        run("commit", "-qam", "edit both")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("R1_SELF_SEALING", out)

    def test_r1_silent_when_only_guarded_changes(self):
        tmp, run = self.build()
        (tmp / "GUARDED.md").write_text("a != b\nchanged\n", encoding="utf-8")
        run("commit", "-qam", "edit guarded only")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 0, out)

    def test_r2_fires_on_fence_deletion(self):
        tmp, run = self.build()
        (tmp / "GUARDED.md").write_text("keep\n", encoding="utf-8")
        run("commit", "-qam", "drop fence")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("R2_FENCE_REMOVAL", out)

    def test_r3_fires_on_prefreeze_mutation(self):
        tmp, run = self.build()
        (tmp / "kernel/development/X_PREFREEZE.json").write_text('{"x":1}\n', encoding="utf-8")
        run("commit", "-qam", "touch prefreeze")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("R3_PREFREEZE_MUTATION", out)

    def test_restoring_a_checker_no_longer_bypasses_r1(self):
        # Regression: an is_restoration bypass suppressed exactly this shape,
        # and only for its own author.
        tmp, run = self.build()
        (tmp / "scripts/check.py").write_text("# checker v2\n", encoding="utf-8")
        run("commit", "-qam", "change checker")
        (tmp / "scripts/check.py").write_text("# checker v1\n", encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nnovel\n", encoding="utf-8")
        run("commit", "-qam", "restore checker and edit guarded")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("R1_SELF_SEALING", out)

    def test_waiver_requires_matching_sha_not_just_subject(self):
        tmp, run = self.build(
            scope_extra={
                "admitted_exceptions": [
                    {
                        "commit_subject_prefix": "drop fence",
                        "commit_sha": "0000000",
                        "rules_waived": ["R2_FENCE_REMOVAL"],
                    }
                ]
            }
        )
        (tmp / "GUARDED.md").write_text("keep\n", encoding="utf-8")
        run("commit", "-qam", "drop fence")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("R2_FENCE_REMOVAL", out)

    def test_r4_fires_when_a_declared_residual_is_deleted(self):
        tmp, run = self.build(
            scope_extra={
                "declared_residuals": [
                    {"key": "K1", "class": "UNADJUDICATED", "reopening_condition": "x"}
                ]
            }
        )
        scope_path = tmp / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json"
        data = json.loads(scope_path.read_text())
        data["declared_residuals"] = []
        scope_path.write_text(json.dumps(data), encoding="utf-8")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("R4_RESIDUAL_DELETED", out)

    def test_r4_accepts_a_residual_moved_to_closed_with_a_return(self):
        tmp, run = self.build(
            scope_extra={
                "declared_residuals": [
                    {"key": "K1", "class": "UNADJUDICATED", "reopening_condition": "x"}
                ]
            }
        )
        scope_path = tmp / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json"
        data = json.loads(scope_path.read_text())
        data["declared_residuals"] = []
        data["closed_residuals"] = [{"key": "K1", "closing_return": "run 123 returned X"}]
        scope_path.write_text(json.dumps(data), encoding="utf-8")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 0, out)

    def test_bare_audit_since_withholds(self):
        # git reads a bare date in the running machine's timezone, so the
        # window would differ between a laptop and CI. Refuse rather than
        # return a location-dependent verdict.
        tmp, _ = self.build({"audit_since": "2000-01-01 00:00"})
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 2, out)
        self.assertIn("explicit UTC offset", out)

    def test_verdict_does_not_depend_on_the_machine_timezone(self):
        # Regression for the 2026-09-26 split: a commit three hours after the
        # UTC boundary was inside the window in CI (UTC) and outside it on
        # the author's machine (UTC-03:00), so CI failed while every local
        # run passed. With an explicit offset both must agree.
        import os

        tmp, run = self.build({"audit_since": "2021-06-01T00:00:00+00:00"})
        (tmp / "scripts/check.py").write_text("# checker v2\n", encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nchanged\n", encoding="utf-8")
        run("commit", "-qam", "edit both", when="2021-06-01T01:00:00+0000")
        verdicts = {}
        old = os.environ.get("TZ")
        try:
            for tz in ("UTC", "America/Sao_Paulo", "Pacific/Kiritimati"):
                os.environ["TZ"] = tz
                verdicts[tz] = self.audit_in(tmp)[0]
        finally:
            if old is None:
                os.environ.pop("TZ", None)
            else:
                os.environ["TZ"] = old
        self.assertEqual(set(verdicts.values()), {1}, verdicts)

    def test_empty_window_withholds_rather_than_passing(self):
        # Regression for D6: PASS over 0 commits. Recorded as fixed during the
        # 2026-09-26 session; it was not, until this test and its guard.
        tmp, _ = self.build({"audit_since": "2099-01-01T00:00:00+00:00"})
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 2, out)
        self.assertIn("nothing was audited", out)

    def test_shallow_clone_withholds(self):
        import subprocess

        tmp, run = self.build()
        (tmp / "GUARDED.md").write_text("a != b\nmore\n", encoding="utf-8")
        run("commit", "-qam", "second")
        shallow = tmp.parent / (tmp.name + "-shallow")
        subprocess.run(
            ["git", "clone", "-q", "--depth", "1", f"file://{tmp}", str(shallow)],
            check=True, capture_output=True,
        )
        self.addCleanup(lambda: __import__("shutil").rmtree(shallow, ignore_errors=True))
        code, out = self.audit_in(shallow)
        self.assertEqual(code, 2, out)
        self.assertIn("shallow", out)

    def test_offset_check_rejects_clock_and_zone_dependent_values(self):
        # Each of these was accepted by the first, suffix-only check.
        for value in ("yesterday Z", "Sep 26 2026 -1200", "2026-09-26 +0000",
                      "2026-09-26T00:00+99:99", "2026-0926Z", "2026-09-26 00:00",
                      "2026-09-26"):
            with self.subTest(value=value):
                self.assertFalse(audit.has_explicit_offset(value))
        for value in ("2026-09-26T00:00:00+00:00", "2026-09-26T00:00:00Z",
                      "2026-09-25T21:00-03:00"):
            with self.subTest(value=value):
                self.assertTrue(audit.has_explicit_offset(value))

    def test_declared_r1_residual_needs_a_bound(self):
        tmp, run = self.build()
        (tmp / "scripts/check.py").write_text("# checker v2\n", encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nchanged\n", encoding="utf-8")
        run("commit", "-qam", "edit both", when="2021-06-01T01:00:00+0000")
        first = __import__("subprocess").run(
            ["git", "rev-parse", "HEAD"], cwd=tmp, capture_output=True, text=True
        ).stdout[:8]
        scope = tmp / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json"
        data = json.loads(scope.read_text(encoding="utf-8"))
        data["declared_residuals"] = [{
            "key": f"R1_SELF_SEALING|scripts/check.py|{first}",
            "reopening_condition": "x",
        }]
        scope.write_text(json.dumps(data), encoding="utf-8")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)  # declared, but through no commit
        data["declared_residuals"][0]["through"] = first
        scope.write_text(json.dumps(data), encoding="utf-8")
        run("add", "-A")
        run("-c", "user.name=Reviewer", "commit", "-qm", "bound by another party",
            when="2021-06-01T01:05:00+0000")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 0, out)

    def test_declared_r1_residual_does_not_absorb_a_later_checker_edit(self):
        # Regression for the independent review of 2026-09-26: one declaration
        # covered every later edit to the same checker in the same episode.
        tmp, run = self.build()
        (tmp / "scripts/check.py").write_text("# checker v2\n", encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nchanged\n", encoding="utf-8")
        run("commit", "-qam", "edit both", when="2021-06-01T01:00:00+0000")
        first = __import__("subprocess").run(
            ["git", "rev-parse", "HEAD"], cwd=tmp, capture_output=True, text=True
        ).stdout[:8]
        scope = tmp / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json"
        data = json.loads(scope.read_text(encoding="utf-8"))
        data["declared_residuals"] = [{
            "key": f"R1_SELF_SEALING|scripts/check.py|{first}",
            "through": first,
            "reopening_condition": "x",
        }]
        scope.write_text(json.dumps(data), encoding="utf-8")
        run("add", "-A")
        run("-c", "user.name=Reviewer", "commit", "-qm", "declare",
            when="2021-06-01T01:05:00+0000")
        self.assertEqual(self.audit_in(tmp)[0], 0)
        (tmp / "scripts/check.py").write_text("# checker v3\n", encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nchanged again\n", encoding="utf-8")
        run("commit", "-qam", "edit both again", when="2021-06-01T01:10:00+0000")
        code, out = self.audit_in(tmp)
        # The reviewer's commit splits the author's episodes, so the second
        # co-modification is a new episode with a finding of its own rather
        # than growth of the declared one. Either way it is not absorbed.
        self.assertEqual(code, 1, out)
        self.assertIn("SELF-SEALING AUDIT FINDINGS", out)

    def test_delete_then_readd_of_a_checker_fires_r1(self):
        # Second-pass review: the first status in an episode was kept, so a
        # checker deleted in one commit and re-added edited in the next was
        # invisible to R1.
        tmp, run = self.build()
        run("rm", "-q", "scripts/check.py")
        run("commit", "-qm", "drop checker", when="2021-06-01T01:00:00+0000")
        (tmp / "scripts").mkdir(exist_ok=True)
        (tmp / "scripts/check.py").write_text("# checker, weakened\n", encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nchanged\n", encoding="utf-8")
        run("add", "-A")
        run("commit", "-qm", "re-add", when="2021-06-01T01:01:00+0000")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("R1_SELF_SEALING", out)

    def test_first_introduction_is_still_bootstrap(self):
        tmp, run = self.build()
        (tmp / "scripts/new_check.py").write_text("# v1\n", encoding="utf-8")
        scope = tmp / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json"
        data = json.loads(scope.read_text(encoding="utf-8"))
        data["guarded"].append({"checker": "scripts/new_check.py", "guards": ["GUARDED.md"]})
        scope.write_text(json.dumps(data), encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nchanged\n", encoding="utf-8")
        run("add", "-A")
        run("commit", "-qm", "introduce", when="2021-06-01T01:00:00+0000")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 0, out)

    def test_deleting_a_prefreeze_fires_unless_its_bytes_survive(self):
        tmp, run = self.build()
        run("rm", "-q", "kernel/development/X_PREFREEZE.json")
        run("commit", "-qm", "drop prefreeze", when="2021-06-01T01:00:00+0000")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("R3_PREFREEZE_MUTATION", out)

        tmp2, run2 = self.build()
        (tmp2 / "history").mkdir()
        run2("mv", "kernel/development/X_PREFREEZE.json", "history/X_SUPERSEDED.json")
        run2("commit", "-qm", "retire byte-exact", when="2021-06-01T01:00:00+0000")
        code, out = self.audit_in(tmp2)
        self.assertEqual(code, 0, out)

    def test_a_bound_set_by_the_covered_author_fires(self):
        # Second-pass review: `through` could be advanced by the same author in
        # a scope-only commit, and nothing flagged it.
        tmp, run = self.build()
        (tmp / "scripts/check.py").write_text("# checker v2\n", encoding="utf-8")
        (tmp / "GUARDED.md").write_text("a != b\nchanged\n", encoding="utf-8")
        run("commit", "-qam", "edit both", when="2021-06-01T01:00:00+0000")
        sha = __import__("subprocess").run(
            ["git", "rev-parse", "HEAD"], cwd=tmp, capture_output=True, text=True
        ).stdout[:8]
        scope = tmp / "kernel/development/SELF_SEALING_AUDIT_SCOPE.json"
        data = json.loads(scope.read_text(encoding="utf-8"))
        data["declared_residuals"] = [{
            "key": f"R1_SELF_SEALING|scripts/check.py|{sha}", "through": sha,
            "reopening_condition": "x",
        }]
        scope.write_text(json.dumps(data), encoding="utf-8")
        run("commit", "-qam", "self-declare", when="2021-06-01T01:05:00+0000")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 1, out)
        self.assertIn("a bound needs a party other than the covered author", out)

        data["declared_residuals"][0]["reviewed"] = "by someone else"
        scope.write_text(json.dumps(data), encoding="utf-8")
        run("-c", "user.name=Reviewer", "commit", "-qam", "bound by another party",
            when="2021-06-01T01:10:00+0000")
        code, out = self.audit_in(tmp)
        self.assertEqual(code, 0, out)

    def test_no_restoration_bypass_remains_in_source(self):
        self.assertNotIn("def is_restoration", SCRIPT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
