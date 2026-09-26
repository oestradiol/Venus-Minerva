"""Negative suite for the constitution auditor.

An auditor is worthless until it has been shown to fail. Both prior auditors in
this repository shipped with real defects found exactly this way -- one
reported PASS over zero commits because a bare date parsed to nothing, the
other looped forever on a cyclic graph, and a hang is indistinguishable from a
pass. Neither would have been caught by exercising the happy path.

Every mutation runs against a throwaway git copy of the tracked tree, pointed
at by CONSTITUTION_AUDIT_ROOT. An earlier version of this file mutated the live
tree and restored it in a finally block, so a run killed mid-test left a
corrupted constitution and a stray probe file behind.

Run: python3 -m unittest tests/test_constitution_audit.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LIVE = Path(__file__).resolve().parents[1]
SCRIPT = LIVE / "scripts/audit_constitution.py"
REL_CONST = "kernel/CONSTITUTION.json"
REL_PLAN = "kernel/development/VM_INTERNALIZATION_PHASE_PLAN.json"

COPY: Path | None = None


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout


def setUpModule() -> None:
    global COPY
    COPY = Path(tempfile.mkdtemp(prefix="constitution-audit-"))
    for rel in git(LIVE, "ls-files").split():
        src = LIVE / rel
        if not src.is_file():
            continue
        dst = COPY / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    git(COPY, "init", "-q")
    # K6 verifies monograph quotes against pinned blobs from the other split
    # branches. Borrow the live object store read-only so the copy can see
    # them without copying five branches' history.
    live_objects = git(LIVE, "rev-parse", "--path-format=absolute", "--git-common-dir").strip()
    (COPY / ".git/objects/info/alternates").write_text(
        str(Path(live_objects) / "objects") + "\n", encoding="utf-8"
    )
    git(COPY, "add", "-A")
    git(COPY, "-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-qm", "copy")


def tearDownModule() -> None:
    if COPY is not None:
        shutil.rmtree(COPY, ignore_errors=True)


def run_audit(root: Path | None = None) -> tuple[int, str]:
    env = dict(os.environ, CONSTITUTION_AUDIT_ROOT=str(root or COPY))
    cp = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=LIVE, capture_output=True, text=True,
        timeout=120, env=env,
    )
    return cp.returncode, cp.stdout + cp.stderr


def load() -> dict:
    return json.loads((COPY / REL_CONST).read_text(encoding="utf-8"))


class CopyTestCase(unittest.TestCase):
    """Restores every file a test touched in the copy, and tracks new ones."""

    def setUp(self) -> None:
        self._saved: dict[Path, str | None] = {}

    def tearDown(self) -> None:
        for path, text in self._saved.items():
            if text is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text(text, encoding="utf-8")
        git(COPY, "add", "-A")

    def write(self, rel: str, text: str, track: bool = False) -> Path:
        path = COPY / rel
        if path not in self._saved:
            self._saved[path] = path.read_text(encoding="utf-8") if path.exists() else None
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        if track:
            git(COPY, "add", rel)
        return path

    def mutate(self, fn) -> tuple[int, str]:
        doc = load()
        fn(doc)
        self.write(REL_CONST, json.dumps(doc, indent=2))
        return run_audit()

    def assert_fires(self, rule: str, fn=None) -> str:
        code, out = self.mutate(fn) if fn else run_audit()
        self.assertEqual(code, 1, f"{rule} did not fail the audit:\n{out}")
        self.assertTrue(
            any(line.strip().startswith(rule) for line in out.splitlines()),
            f"{rule} did not fire:\n{out}",
        )
        return out


class DeclaredConstitutionTests(CopyTestCase):
    def test_declared_constitution_passes(self):
        code, out = run_audit()
        self.assertEqual(code, 0, out)
        self.assertIn("CONSTITUTION AUDIT PASS", out)

    def test_live_tree_passes_too(self):
        # The copy is a faithful stand-in only if the live tree agrees with it.
        code, out = run_audit(LIVE)
        self.assertEqual(code, 0, out)

    def test_pass_message_denies_that_enforcement_is_correctness(self):
        _, out = run_audit()
        self.assertIn("Enforcement is not correctness", out)

    def test_register_is_live_constitution(self):
        # A constitution nothing may cite governs nothing.
        self.assertEqual(load()["register"], "LIVE_CONSTITUTION")

    def test_carries_no_promotion_or_truth_authority(self):
        doc = load()
        self.assertFalse(doc["promotion_authority"])
        self.assertFalse(doc["truth_authority"])

    def test_unenforced_items_are_visible_not_hidden(self):
        _, out = run_audit()
        for item in ("EVALUATOR_CUSTODY", "CLAIM_BINDING_AUTHORITY"):
            with self.subTest(item=item):
                self.assertIn(f"UNENFORCED by declaration: {item}", out)

    def test_partially_enforced_items_are_visible(self):
        # Previously only NONE rows were reported, so the two items that
        # self-declare partial coverage never appeared in any output.
        _, out = run_audit()
        for item in ("EVIDENCE_IDENTITY", "O_STAR_EXTERNAL_VALIDATION", "PARENT_CUSTODY"):
            with self.subTest(item=item):
                self.assertIn(f"PARTIALLY ENFORCED: {item}", out)

    def test_governing_but_unenforced_roles_are_visible(self):
        _, out = run_audit()
        for role in ("crystallizer_role", "lateralizer_role", "internalizer_role",
                     "epistemic_role", "roadmap_role"):
            with self.subTest(role=role):
                self.assertIn(f"GOVERNS BUT UNENFORCED: {role}", out)

    def test_gap_report_survives_a_failing_run(self):
        # Notes were printed only on the passing path, so the whole gap report
        # disappeared exactly when something failed.
        out = self.assert_fires(
            "K1",
            lambda d: d["block_b_deny_list"]["must_remain_outside"].append("NEW_UNGOVERNED_ITEM"),
        )
        self.assertIn("UNENFORCED by declaration: EVALUATOR_CUSTODY", out)
        self.assertIn("tracked paths unrouted", out)

    def test_audit_does_not_write_to_the_tree_it_audits(self):
        before = git(COPY, "status", "--porcelain")
        run_audit()
        self.assertEqual(git(COPY, "status", "--porcelain"), before)


class RuleFiresTests(CopyTestCase):
    # ---- K4 -----------------------------------------------------------------
    def test_k4_fires_when_a_law_goes_missing_from_the_tree(self):
        # Assembled at runtime so the literal never appears in this file,
        # which is itself part of the corpus being searched.
        probe = "_".join(["ZZPROBE", "LAW"]) + " != " + "_".join(["NOT", "IN", "TREE"])
        self.assert_fires(
            "K4", lambda d: d["block_a_permanent_noncollapse_laws"]["laws"].append(probe)
        )

    def test_k4_does_not_match_a_law_straddling_two_files(self):
        # The corpus was concatenated and whitespace-stripped, so the tail of
        # one file and the head of the next could together spell a law that
        # neither contains.
        left = "_".join(["ZZSTRADDLE", "LEFT"])
        right = "_".join(["ZZSTRADDLE", "RIGHT"])
        self.write("docs/zz_a_straddle.md", f"x\n{left} !=")
        self.write("docs/zz_b_straddle.md", f"{right}\ny\n")
        self.assert_fires(
            "K4",
            lambda d: d["block_a_permanent_noncollapse_laws"]["laws"].append(f"{left} != {right}"),
        )

    def test_k4_fires_when_a_declared_absent_law_reappears(self):
        def fn(d):
            d["block_a_permanent_noncollapse_laws"]["known_absent"].append(
                {"law": "CODE_DELETION != INTERNALIZATION", "reason": "wrong on purpose",
                 "reopening_condition": "n/a"}
            )
        self.assert_fires("K4", fn)

    def test_k4_fires_when_a_declared_absent_law_gives_no_reason(self):
        def fn(d):
            for row in d["block_a_permanent_noncollapse_laws"]["known_absent"]:
                row["reason"] = ""
        self.assert_fires("K4", fn)

    # ---- K1 -----------------------------------------------------------------
    def test_k1_fires_on_deny_list_item_with_no_enforcement_entry(self):
        self.assert_fires(
            "K1",
            lambda d: d["block_b_deny_list"]["must_remain_outside"].append("NEW_UNGOVERNED_ITEM"),
        )

    def test_k1_fires_on_enforcement_none_without_a_reason(self):
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "EVALUATOR_CUSTODY":
                    row["reason"] = "   "
        self.assert_fires("K1", fn)

    def test_k1_fires_when_named_enforcing_artifact_is_missing(self):
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "STOP":
                    row["enforced_by"] = "kernel/development/NO_SUCH_FILE.json"
        self.assert_fires("K1", fn)

    def test_k1_is_not_satisfied_by_pointing_at_any_existing_file(self):
        # The exact defeat of the previous version: enforced_by only had to
        # exist, so README.md satisfied it.
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "STOP":
                    row["enforced_by"] = "README.md"
        self.assert_fires("K1", fn)

    def test_k1_fires_when_a_cited_distinction_is_not_in_the_matrix(self):
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "STOP":
                    row["distinctions"].append("_".join(["ZZNO", "SUCH", "DISTINCTION"]))
        self.assert_fires("K1", fn)

    def test_k1_fires_when_an_enforced_row_cites_nothing(self):
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "STOP":
                    row["distinctions"] = []
        self.assert_fires("K1", fn)

    # ---- K3 -----------------------------------------------------------------
    def test_k3_fires_on_a_new_unreferenced_role(self):
        self.write(
            "kernel/development/_TEST_TEMP_ROLE_PROBE.json",
            json.dumps({"_".join(["zzprobe", "role"]): "claims to govern and binds to nothing"}),
            track=True,
        )
        out = self.assert_fires("K3")
        self.assertIn("zzprobe_role", out)

    def test_k3_sees_roles_outside_kernel_and_docs(self):
        # Role discovery used to scan only kernel/ and docs/, so a role in
        # autonomy/ or benchmarks/ could not be refused.
        self.write(
            "benchmarks/_zz_probe/plan.json",
            json.dumps({"_".join(["zzfar", "role"]): "governs from outside the scanned dirs"}),
            track=True,
        )
        out = self.assert_fires("K3")
        self.assertIn("zzfar_role", out)

    def test_k3_fires_on_descriptive_role_without_a_reason(self):
        self.assert_fires("K3", lambda d: d["descriptive_roles"].__setitem__("mythos_role", " "))

    def test_k3_refuses_a_bare_descriptive_list(self):
        # A bare list is where epistemic_role and roadmap_role were parked
        # unexamined although both forbid something.
        self.assert_fires(
            "K3", lambda d: d.__setitem__("descriptive_roles", list(d["descriptive_roles"]))
        )

    def test_k3_fires_on_unenforced_role_without_reopening_condition(self):
        def fn(d):
            for row in d["governing_roles_unenforced"]:
                if row["role"] == "crystallizer_role":
                    row["reopening_condition"] = ""
        self.assert_fires("K3", fn)

    def test_k3_fires_when_an_unenforced_role_is_actually_referenced(self):
        self.assert_fires(
            "K3",
            lambda d: d["governing_roles_unenforced"].append(
                {"role": "actor_role", "claims": "x", "reopening_condition": "y"}
            ),
        )

    def test_k3_fires_when_a_governing_role_names_a_missing_check(self):
        def fn(d):
            d["governing_roles"]["crystallizer_role"] = "scripts/no_such_check.py"
            d["governing_roles_unenforced"] = [
                r for r in d["governing_roles_unenforced"] if r["role"] != "crystallizer_role"
            ]
        self.assert_fires("K3", fn)

    # ---- K2 -----------------------------------------------------------------
    def test_k2_fires_on_routing_edge_to_untracked_path(self):
        self.assert_fires(
            "K2",
            lambda d: d["block_c_authority_graph"]["routing"].append(
                {"path": "kernel/NO_SUCH_LIVE_STATE.md", "class": "LIVE_STATE"}
            ),
        )

    def test_k2_fires_on_prefix_matching_nothing(self):
        self.assert_fires(
            "K2",
            lambda d: d["block_c_authority_graph"]["routing"].append(
                {"prefix": "no/such/dir/", "class": "IMMUTABLE_EVIDENCE"}
            ),
        )

    def test_k2_fires_on_undeclared_class(self):
        self.assert_fires(
            "K2",
            lambda d: d["block_c_authority_graph"]["routing"].append(
                {"path": "Makefile", "class": "SOVEREIGN"}
            ),
        )

    def test_k2_fires_when_pinned_immutable_evidence_is_edited(self):
        rel = "provenance/canonical-extracts/FRESH_INSTANCE_GROUND_2026-09-26.md"
        text = (COPY / rel).read_text(encoding="utf-8")
        self.write(rel, text.replace("gates, not promotions", "gates and promotions"))
        self.assert_fires("K2")

    def test_k2_does_not_fail_when_files_are_added(self):
        # The removed ratchet failed whenever the unrouted count grew, which
        # every autonomous worker commit that writes a result file does.
        self.write("autonomy/evidence/_zz_new_result.json", "{}\n", track=True)
        code, out = run_audit()
        self.assertEqual(code, 0, out)

    # ---- K5 -----------------------------------------------------------------
    def test_k5_sees_nested_runtime_modules(self):
        self.write("kernel/runtime/_zz_sub/zz_probe_module.py", "x = 1\n", track=True)
        out = self.assert_fires("K5")
        self.assertIn("zz_probe_module.py", out)

    def test_k5_is_not_satisfied_by_a_mention_inside_a_sentence(self):
        # The previous substring test over the serialized plan accepted any
        # path that appeared anywhere inside a longer string.
        rel = "kernel/runtime/zz_mentioned_only.py"
        self.write(rel, "x = 1\n", track=True)
        plan = json.loads((COPY / REL_PLAN).read_text(encoding="utf-8"))
        plan["_zz_note"] = f"historically see {rel} for context"
        self.write(REL_PLAN, json.dumps(plan))
        self.assert_fires("K5")


class MonographGroundingTests(CopyTestCase):
    def test_all_five_monographs_are_cited(self):
        block = load()["block_e_monograph_grounding"]
        self.assertEqual(
            sorted(block["required_monographs"]),
            ["ARCANE", "ECLIPSIS", "MINERVA", "OFE", "VENUS"],
        )
        cited = {a["monograph"] for a in block["anchors"]}
        self.assertEqual(cited, set(block["required_monographs"]))

    def test_k6_fires_when_a_quote_is_paraphrased(self):
        def fn(d):
            a = d["block_e_monograph_grounding"]["anchors"][0]
            a["quote"] = a["quote"].replace("coarsest", "smallest")
        self.assert_fires("K6", fn)

    def test_k6_fires_when_a_quote_is_attributed_to_the_wrong_monograph(self):
        def fn(d):
            for a in d["block_e_monograph_grounding"]["anchors"]:
                if a["id"] == "VEN_ANCESTRY":
                    a["monograph"] = "OFE"
        self.assert_fires("K6", fn)

    def test_k6_fires_when_a_pinned_blob_is_absent(self):
        def fn(d):
            d["block_e_monograph_grounding"]["monographs"]["OFE"]["blob"] = "0" * 40
        self.assert_fires("K6", fn)

    def test_k6_fires_when_a_required_monograph_is_never_cited(self):
        def fn(d):
            b = d["block_e_monograph_grounding"]
            b["anchors"] = [a for a in b["anchors"] if a["monograph"] != "ARCANE"]
            for row in d["deny_list_enforcement"]:
                row["monograph_grounds"] = [
                    g for g in row["monograph_grounds"] if not g.startswith("ARC_")
                ] or ["OFE_COARSEST"]
        self.assert_fires("K6", fn)

    def test_k6_fires_on_deny_list_item_without_a_ground(self):
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "STOP":
                    row["monograph_grounds"] = []
        self.assert_fires("K6", fn)

    def test_k6_fires_on_a_ground_naming_an_unknown_anchor(self):
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "STOP":
                    row["monograph_grounds"].append("_".join(["ZZ", "NO", "ANCHOR"]))
        self.assert_fires("K6", fn)

    def test_mu_f_is_attributed_to_venus_only(self):
        # mu_F is the author's notation in the Venus monograph; OFE and
        # Eclipsis use Disc_F / Res_F. An earlier plan proposed "correcting"
        # mu_F out of the repository as an assistant import, which would have
        # removed the author's own notation.
        anchors = load()["block_e_monograph_grounding"]["anchors"]
        mu = [a for a in anchors if a["id"] == "VEN_MU"]
        self.assertEqual(len(mu), 1)
        self.assertEqual(mu[0]["monograph"], "VENUS")


class ReviewRegressionTests(CopyTestCase):
    """Each test reproduces an attack from the independent review of 2026-09-26
    that passed every check at the time."""

    def test_k7_deleting_a_deny_list_item_fires(self):
        def fn(d):
            d["block_b_deny_list"]["must_remain_outside"].remove("TRUST_ROOT")
            d["deny_list_enforcement"] = [
                r for r in d["deny_list_enforcement"] if r["item"] != "TRUST_ROOT"
            ]
        self.assert_fires("K7", fn)

    def test_k7_deleting_a_law_fires(self):
        self.assert_fires(
            "K7",
            lambda d: d["block_a_permanent_noncollapse_laws"]["laws"].remove(
                "ABSTRACTION != CAUSAL_USE"
            ),
        )

    def test_k7_downgrading_an_enforced_item_fires(self):
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "ROLLBACK":
                    row.clear()
                    row.update({"item": "ROLLBACK", "enforcement": "NONE", "reason": "any"})
        self.assert_fires("K7", fn)

    def test_k2_prefix_into_live_class_fires(self):
        self.assert_fires(
            "K2",
            lambda d: d["block_c_authority_graph"]["routing"].append(
                {"prefix": "autonomy/", "class": "LIVE_CONSTITUTION"}
            ),
        )

    def test_k2_unpinned_live_edge_fires(self):
        self.assert_fires(
            "K2",
            lambda d: d["block_c_authority_graph"]["routing"].append(
                {"path": "Makefile", "class": "LIVE_ROUTING"}
            ),
        )

    def test_k2_shadowing_edge_fires(self):
        # Inserted first, a kernel/ prefix would override the constitution's
        # own LIVE_CONSTITUTION edge under first-match classification.
        self.assert_fires(
            "K2",
            lambda d: d["block_c_authority_graph"]["routing"].insert(
                0, {"prefix": "kernel/", "class": "HISTORICAL_SNAPSHOT"}
            ),
        )

    def test_k4_vendored_source_text_does_not_count(self):
        probe = "_".join(["ZZVENDORED", "LAW"]) + " != " + "_".join(["ONLY", "IN", "SOURCE"])
        self.write("provenance/canonical-extracts/_zz_source.md", probe + "\n")
        self.assert_fires(
            "K4", lambda d: d["block_a_permanent_noncollapse_laws"]["laws"].append(probe)
        )

    def test_k4_test_files_do_not_count(self):
        probe = "_".join(["ZZTESTONLY", "LAW"]) + " != " + "_".join(["NOT", "CARRIED"])
        self.write("tests/_zz_probe.py", f"# {probe}\n")
        self.assert_fires(
            "K4", lambda d: d["block_a_permanent_noncollapse_laws"]["laws"].append(probe)
        )

    def test_k4_checker_does_not_satisfy_its_own_laws(self):
        # PINNED_LAWS in the auditor names every law. If the auditor counted
        # as evidence, this declared-absent law would read as present.
        absent = [r["law"] for r in load()["block_a_permanent_noncollapse_laws"]["known_absent"]]
        self.assertIn(
            "NETWORK_MEMORY_CHANGES_LATER_QUERY != USEFUL_RELATIONAL_RECONSTRUCTION", absent
        )
        code, out = run_audit()
        self.assertEqual(code, 0, out)

    def test_k6_citing_an_anchor_for_an_item_it_does_not_ground_fires(self):
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "ROLLBACK":
                    row["monograph_grounds"] = ["ARC_DROPPED_INDEX"]
        self.assert_fires("K6", fn)

    def test_k6_wrong_line_fires(self):
        def fn(d):
            for a in d["block_e_monograph_grounding"]["anchors"]:
                if a["id"] == "OFE_COARSEST":
                    a["line"] += 1
        self.assert_fires("K6", fn)

    def test_k6_ungrounded_item_needs_a_reason(self):
        def fn(d):
            for row in d["deny_list_enforcement"]:
                if row["item"] == "TRUST_ROOT":
                    row["no_monograph_ground"] = ""
        self.assert_fires("K6", fn)

    def test_ungrounded_items_are_reported(self):
        _, out = run_audit()
        self.assertIn("NO MONOGRAPH GROUND: TRUST_ROOT", out)
        self.assertIn("NO MONOGRAPH GROUND: HARD_SUBSTRATE_CAPABILITY_LIMITS", out)


class FailClosedTests(CopyTestCase):
    def test_unparseable_constitution_withholds(self):
        self.write(REL_CONST, "{ not json")
        code, out = run_audit()
        self.assertEqual(code, 2)
        self.assertIn("WITHHOLD", out)

    def test_wrong_register_withholds(self):
        code, out = self.mutate(lambda d: d.__setitem__("register", "CANDIDATE_NOT_ADMITTED"))
        self.assertEqual(code, 2)
        self.assertIn("WITHHOLD", out)


if __name__ == "__main__":
    unittest.main()
