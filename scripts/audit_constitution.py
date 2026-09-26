#!/usr/bin/env python3
"""Enforce kernel/CONSTITUTION.json against the tree.

The 2026-09-26 episode broke rules that were all already written down. None of
them were enforceable. Nine of eleven *_role fields in this repository are
referenced by zero executable files: they describe good practice and decline
nothing. That is why nothing could refuse the contaminating compression.

  K1 DENY_LIST_ENFORCED  every must-remain-outside item names an enforcing
                         artifact AND every distinction it cites exists in
                         that artifact, or it is declared enforcement: NONE
  K2 AUTHORITY_TOTALITY  every tracked path classifies, or fails closed to
                         WITHHOLD; every declared routing edge resolves to a
                         tracked path and names a declared class
  K3 NO_PROSE_ONLY_ROLE  a *_role field that claims to govern must name a check
                         referencing it, or be declared descriptive
  K4 LAWS_PRESENT        the permanent noncollapse laws are present, compared
                         with whitespace normalized
  K5 RUNTIME_DISPOSITION every capability-specific runtime module carries a
                         disposition
  K6 MONOGRAPH_GROUNDING every cited monograph quote is present verbatim in the
                         exact git blob it is pinned to, at the line it names;
                         all five monographs are cited; every deny-list item
                         has a ground, and each anchor it cites names that item
  K7 CORE_PINNED         the laws, deny-list items and enforced items pinned in
                         THIS FILE are still declared and enforced, and the
                         protected sections match the digest pinned here

Comparison is whitespace-normalized throughout. An earlier spaced-form check of
these same laws reported 13 of 15 absent when they were present without spaces
around the operator. A presence check weaker than its name is the defect class
this file exists to prevent.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

# Tests point this at a throwaway copy. They previously mutated the live
# tree, so a run killed mid-test left a corrupted constitution behind.
ROOT = Path(os.environ.get("CONSTITUTION_AUDIT_ROOT") or Path(__file__).resolve().parents[1])
CONSTITUTION = ROOT / "kernel/CONSTITUTION.json"

# Enforcement lives in checkers and runtime. Tests VERIFY enforcement; they do
# not constitute it. Scanning tests/ here would mean that merely naming a role
# in a test string counts as governing it -- a check weaker than its name,
# which is the defect class this file exists to prevent. Found by this
# auditor's own negative suite, which mentions three role names and thereby
# made them all look enforced.
CODE_DIRS = ("scripts", "kernel/runtime")
CORPUS_DIRS = ("kernel", "docs", "provenance", "scripts", "tests")
# K4 asks whether the tree carries each law. Two places cannot count:
# tests/, because a test asserting a law is present would satisfy the check it
# tests; and provenance/canonical-extracts/, because vendoring the source text
# the constitution was transcribed from makes every law "present" at once --
# K4 would then compare the constitution with its own origin. Both were found
# by an independent review, the second after it had already let a declared-
# absent law be promoted without its reopening condition being met.
CORPUS_EXCLUDE = ("tests/", "provenance/canonical-extracts/")

# The protected core is pinned HERE, in the checker, not in the JSON it
# checks. Deleting a law or deny-list item, or downgrading an enforced item to
# NONE, then requires editing this file together with the constitution, which
# the self-sealing auditor's R1 rule surfaces. Before this, deleting TRUST_ROOT
# or a law from the JSON alone passed every check. Additions need no edit here.
PINNED_LAWS = (
    "fewer parts != fewer distinctions",
    "CODE_DELETION != INTERNALIZATION",
    "STATE_OWNERSHIP != GENERALIZATION",
    "ABSTRACTION != CAUSAL_USE",
    "CAUSAL_USE != INTERNALIZATION",
    "SOURCE_REMOVAL != INDEPENDENT_EVALUATION",
    "INTERNALIZATION != PROMOTION",
    "INTERNALIZE_COMPETENCE != INTERNALIZE_CORRECTION_SOVEREIGNTY",
    "GENERATE != DIMENSIONALIZE != LATERALIZE != CRYSTALLIZE_F != INTERNALIZE",
    "LEXICAL_GROUNDING != THEATER_BINDING",
    "RELATION_CLASSIFICATION != PARTICIPANT/KFS_RECONSTRUCTION",
    "DISCOURSE_PRESENTATION_ORDER != EVENT/HISTORY_ORDER",
    "NETWORK_MEMORY_CHANGES_LATER_QUERY != USEFUL_RELATIONAL_RECONSTRUCTION",
    "RETURN_SIGN != CAUSAL_CREDIT",
    "CONFIG_UTILITY != GLOBAL_CONFIG_TRUTH",
    "DUPLICATE_EVENT != NEW_EVIDENCE",
    "ABSENCE_OF_RETURN != NEGATIVE_RETURN",
)
PINNED_DENY_ITEMS = (
    "WORLD_OTHER", "FRESH_WORLD_RETURN", "EVIDENCE_IDENTITY", "EVALUATOR_CUSTODY",
    "TRUST_ROOT", "AUTHORIZATION", "JURISDICTION", "CLAIM_BINDING_AUTHORITY", "STOP",
    "WITHHOLD_SAFETY_LAW", "ROLLBACK", "PARENT_CUSTODY",
    "ANTI_MINERVA_CORRECTION_PERMEABILITY", "O_STAR_EXTERNAL_VALIDATION",
    "HARD_SUBSTRATE_CAPABILITY_LIMITS",
)
PINNED_ENFORCED = (
    "WORLD_OTHER", "FRESH_WORLD_RETURN", "EVIDENCE_IDENTITY", "TRUST_ROOT",
    "AUTHORIZATION", "JURISDICTION", "STOP", "WITHHOLD_SAFETY_LAW", "ROLLBACK",
    "PARENT_CUSTODY", "ANTI_MINERVA_CORRECTION_PERMEABILITY",
    "O_STAR_EXTERNAL_VALIDATION", "HARD_SUBSTRATE_CAPABILITY_LIMITS",
)
# Digest of the protected sections; see protected_core().
PINNED_CORE_DIGEST = "5f6ea730619d019e617d4e383c63e2a5ef68b34c3ecf2402139dd42ff8f3c56c"

# Live authority is the most sensitive routing there is, so its edges are
# pinned exactly. A new live surface needs an edit here; a prefix may never
# route into a LIVE class.
PINNED_LIVE_EDGES = frozenset({
    ("kernel/CONSTITUTION.json", "LIVE_CONSTITUTION"),
    ("kernel/CURRENT_STATE.md", "LIVE_STATE"),
    ("AGENTS.md", "LIVE_ROUTING"),
    ("README.md", "LIVE_ROUTING"),
    ("docs/START_HERE.md", "LIVE_ROUTING"),
})
TEXT_EXT = (".json", ".md", ".py", ".yml", ".yaml", ".tex")


def normalize(text: str) -> str:
    text = text.replace("≠", "!=").replace("→", "->")
    return re.sub(r"\s+", "", text).upper()


def read_files(dirs: tuple[str, ...], exclude: frozenset[Path] = frozenset()) -> list[str]:
    """Concatenate the tree's text, excluding named files.

    CONSTITUTION.json must be excluded when checking whether its own laws are
    present in the tree, or the check is self-satisfying: the constitution is
    part of the tree, so every law it declares is trivially found in itself.
    Caught by this auditor's negative suite, which appended a nonexistent law
    and watched K4 pass.

    Files are returned separately. Concatenating them and then stripping
    whitespace let a law match across the boundary between two unrelated
    files: the tail of one and the head of the next.
    """
    chunks: list[str] = []
    for base in dirs:
        for dirpath, _, filenames in os.walk(ROOT / base):
            if "__pycache__" in dirpath:
                continue
            for name in filenames:
                path = Path(dirpath, name)
                if not name.endswith(TEXT_EXT) or path.resolve() in exclude:
                    continue
                rel = path.relative_to(ROOT).as_posix()
                if dirs is CORPUS_DIRS and rel.startswith(CORPUS_EXCLUDE):
                    continue
                try:
                    chunks.append(path.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    continue
    return chunks


def read_corpus(dirs: tuple[str, ...], exclude: frozenset[Path] = frozenset()) -> str:
    return "\n".join(read_files(dirs, exclude))


def tracked_paths() -> list[str]:
    cp = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr.strip())
    return [p for p in cp.stdout.split() if p]


def role_fields() -> dict[str, list[str]]:
    """Every *_role field carrying a prose string, and where it lives."""
    found: dict[str, list[str]] = {}

    def walk(obj, path: str):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key.endswith("_role") and isinstance(value, str):
                    found.setdefault(key, []).append(path)
                else:
                    walk(value, path)
        elif isinstance(obj, list):
            for item in obj:
                walk(item, path)

    # Every tracked JSON file. Scanning only kernel/ and docs/ missed roles in
    # autonomy/ and benchmarks/, so K3 could not see them to refuse them.
    for rel in tracked_paths():
        # The constitution names roles in order to classify them; counting its
        # own keys as role fields inflated the total and classified nothing.
        if not rel.endswith(".json") or rel == "kernel/CONSTITUTION.json":
            continue
        try:
            walk(json.loads((ROOT / rel).read_text(encoding="utf-8")), rel)
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            continue
    return found


def classify(path: str, rules: list[dict]) -> str:
    for rule in rules:
        prefix = rule.get("prefix", "")
        if prefix and path.startswith(prefix):
            return rule["class"]
        exact = rule.get("path", "")
        if exact and path == exact:
            return rule["class"]
    return "WITHHOLD"


def json_strings(obj) -> set[str]:
    """Every string value in a JSON document, for exact-membership checks."""
    out: set[str] = set()
    if isinstance(obj, str):
        out.add(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            out |= json_strings(value)
    elif isinstance(obj, list):
        for value in obj:
            out |= json_strings(value)
    return out


def protected_core(const: dict) -> str:
    """Canonical digest of every section whose silent change weakens a check.

    Pinning individual values left data-only edits open: adding an authority
    class under a non-LIVE name, re-pointing an enforced item at an irrelevant
    distinction, declaring "CAUSAL" an equivalent form of a law, or editing a
    vendored file and its sha256 pin together all passed. The digest covers the
    laws and their equivalent forms, the deny-list, each enforcement row's
    (item, enforcement, enforced_by, distinctions), and the full routing graph
    with its pins. Changing any of it means updating PINNED_CORE_DIGEST in this
    file, which the self-sealing auditor surfaces as R1.
    """
    a = const["block_a_permanent_noncollapse_laws"]
    c = const["block_c_authority_graph"]
    core = {
        "laws": a.get("laws", []),
        "equivalent_forms": a.get("equivalent_forms", {}),
        "must_remain_outside": const["block_b_deny_list"].get("must_remain_outside", []),
        "enforcement": [
            [r.get("item"), r.get("enforcement"), r.get("enforced_by"), r.get("distinctions")]
            for r in const.get("deny_list_enforcement", [])
        ],
        "classes": c.get("classes", []),
        "routing": [
            [r.get("path"), r.get("prefix"), r.get("class"), r.get("sha256")]
            for r in c.get("routing", [])
        ],
    }
    blob = json.dumps(core, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def matrix_ids(path: Path) -> set[str] | None:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    rows = doc.get("distinctions") if isinstance(doc, dict) else None
    if not isinstance(rows, list):
        return None
    return {row["id"] for row in rows if isinstance(row, dict) and "id" in row}


def main() -> int:
    if not CONSTITUTION.exists():
        print("WITHHOLD: kernel/CONSTITUTION.json is absent")
        return 2
    try:
        const = json.loads(CONSTITUTION.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"WITHHOLD: constitution does not parse: {exc}")
        return 2
    if const.get("register") != "LIVE_CONSTITUTION":
        print("WITHHOLD: constitution does not declare register LIVE_CONSTITUTION")
        return 2
    try:
        paths = tracked_paths()
    except RuntimeError as exc:
        print(f"WITHHOLD: cannot list tracked files: {exc}")
        return 2
    tracked = set(paths)

    errors: list[str] = []
    notes: list[str] = []

    # Exclude the constitution from its own evidence corpus (see read_files),
    # and compare each file separately so a law cannot straddle two files.
    # Excluded from their own evidence: the constitution (every law would be
    # found in itself) and this checker, which pins the laws in PINNED_LAWS and
    # so would satisfy K4 for all of them. The second was introduced by the
    # fix that added the pin and caught before commit.
    corpus_files = [
        normalize(text)
        for text in read_files(
            CORPUS_DIRS,
            exclude=frozenset({
                CONSTITUTION.resolve(),
                (ROOT / "scripts/audit_constitution.py").resolve(),
            }),
        )
    ]
    code_corpus = read_corpus(CODE_DIRS)

    def present(forms: list[str]) -> bool:
        wanted = [normalize(f) for f in forms]
        return any(w in text for text in corpus_files for w in wanted)

    # ---- K4: the laws are present -------------------------------------------
    block_a = const["block_a_permanent_noncollapse_laws"]
    declared_absent = {row["law"]: row for row in block_a.get("known_absent", [])}
    equivalents = block_a.get("equivalent_forms", {})
    for law in block_a["laws"]:
        if present([law] + list(equivalents.get(law, []))):
            continue
        row = declared_absent.get(law)
        if row is None:
            errors.append(
                f"K4 LAWS_PRESENT: not in tree, no declared equivalent form, and not "
                f"declared absent: {law}"
            )
        elif not str(row.get("reason", "")).strip():
            errors.append(f"K4 LAWS_PRESENT: {law} declared absent without a reason")
        else:
            notes.append(f"law stated in constitution only, absent from tree: {law}")
    # A law declared absent that HAS since appeared must be promoted out of the
    # absent list, or the list would hide real coverage.
    for law in declared_absent:
        if present([law] + list(equivalents.get(law, []))):
            errors.append(
                f"K4 LAWS_PRESENT: {law} is declared absent but IS present in the tree; "
                f"remove it from known_absent"
            )

    # ---- K1: deny-list is enforced or declared unenforced --------------------
    # The previous version checked only that the named file existed, so
    # pointing enforced_by at README.md passed. Every distinction a row cites
    # must now exist as a row id in the artifact it names.
    block_b = const["block_b_deny_list"]
    enforcement = {row["item"]: row for row in const.get("deny_list_enforcement", [])}
    for item in block_b["must_remain_outside"]:
        row = enforcement.get(item)
        if row is None:
            errors.append(
                f"K1 DENY_LIST_ENFORCED: {item} has no enforcement entry "
                f"(declare a check, or enforcement: NONE with a reason)"
            )
            continue
        mode = row.get("enforcement")
        if mode == "NONE":
            if not str(row.get("reason", "")).strip():
                errors.append(f"K1 DENY_LIST_ENFORCED: {item} declares NONE without a reason")
            else:
                notes.append(f"UNENFORCED by declaration: {item}")
            continue
        ref = row.get("enforced_by", "")
        cited = list(row.get("distinctions", []))
        if not ref:
            errors.append(f"K1 DENY_LIST_ENFORCED: {item} names no enforcing artifact")
            continue
        if not (ROOT / ref).exists():
            errors.append(f"K1 DENY_LIST_ENFORCED: {item} names missing artifact {ref}")
            continue
        if not cited:
            errors.append(
                f"K1 DENY_LIST_ENFORCED: {item} names {ref} but cites no distinction in it"
            )
            continue
        ids = matrix_ids(ROOT / ref)
        if ids is None:
            errors.append(
                f"K1 DENY_LIST_ENFORCED: {item} names {ref}, which carries no "
                f"distinctions list to cite"
            )
            continue
        missing = [d for d in cited if d not in ids]
        if missing:
            errors.append(
                f"K1 DENY_LIST_ENFORCED: {item} cites distinction(s) absent from "
                f"{ref}: {', '.join(missing)}"
            )
            continue
        # A row that self-declares partial coverage is surfaced every run.
        # Previously only NONE rows were visible, so the advertised count of
        # unenforced items silently excluded the partially enforced ones.
        note = str(row.get("note", ""))
        if note.upper().startswith("PARTIAL"):
            notes.append(f"PARTIALLY ENFORCED: {item} — {note.split('.')[0]}")

    # ---- K3: no prose-only governing role ------------------------------------
    # descriptive_roles must give a reason per role. A bare list was a place
    # to park a governing role unexamined, which is the hole K3 closes.
    descriptive = const.get("descriptive_roles", {})
    if not isinstance(descriptive, dict):
        errors.append("K3 NO_PROSE_ONLY_ROLE: descriptive_roles must map each role to a reason")
        descriptive = {}
    for field, reason in descriptive.items():
        if not str(reason).strip():
            errors.append(f"K3 NO_PROSE_ONLY_ROLE: {field} declared descriptive without a reason")
    governing = const.get("governing_roles", {})
    unenforced = {row["role"]: row for row in const.get("governing_roles_unenforced", [])}
    for field, files in sorted(role_fields().items()):
        if field in code_corpus:
            continue
        if field in descriptive:
            continue
        claim = governing.get(field)
        if claim:
            if not (ROOT / claim).exists():
                errors.append(f"K3 NO_PROSE_ONLY_ROLE: {field} names missing check {claim}")
            elif field not in (ROOT / claim).read_text(encoding="utf-8", errors="replace"):
                errors.append(
                    f"K3 NO_PROSE_ONLY_ROLE: {field} names {claim} but that file "
                    f"does not reference it"
                )
            continue
        row = unenforced.get(field)
        if row is not None:
            if not str(row.get("reopening_condition", "")).strip():
                errors.append(
                    f"K3 NO_PROSE_ONLY_ROLE: {field} declared unenforced without a "
                    f"reopening condition"
                )
            else:
                notes.append(f"GOVERNS BUT UNENFORCED: {field} — {row.get('claims', '')}")
            continue
        errors.append(
            f"K3 NO_PROSE_ONLY_ROLE: {field} ({', '.join(files[:2])}) is referenced by no "
            f"executable file and is neither declared descriptive, bound to a check, nor "
            f"declared governing-but-unenforced with a reopening condition"
        )
    for field in sorted(unenforced):
        if field in code_corpus:
            errors.append(
                f"K3 NO_PROSE_ONLY_ROLE: {field} is declared unenforced but IS now "
                f"referenced by code; move it to governing_roles"
            )

    # ---- K2: authority totality ----------------------------------------------
    # The canonical law is a classification default: an unrouted path is
    # WITHHOLD, never authority. It is not a limit on how many files exist.
    # The previous ratchet failed whenever any file was added, including the
    # result files Minerva's own autonomous worker commits, and was stale on
    # the very commit that introduced it (the auditor and its test were
    # counted after the number was recorded). What K2 enforces instead is
    # that the declared graph is real: every edge resolves and names a
    # declared class. The unrouted count is reported every run.
    block_c = const["block_c_authority_graph"]
    rules = block_c.get("routing", [])
    classes = set(block_c.get("classes", []))
    for rule in rules:
        cls = rule.get("class")
        if cls not in classes:
            errors.append(f"K2 AUTHORITY_TOTALITY: routing edge names undeclared class {cls!r}")
        if rule.get("path") and rule["path"] not in tracked:
            errors.append(f"K2 AUTHORITY_TOTALITY: routing edge to untracked path {rule['path']}")
        if rule.get("prefix") and not any(p.startswith(rule["prefix"]) for p in paths):
            errors.append(
                f"K2 AUTHORITY_TOTALITY: routing prefix {rule['prefix']} matches no tracked path"
            )
        # An edge may pin bytes. IMMUTABLE_EVIDENCE that can change silently
        # is not immutable; the pin makes an in-place edit a finding.
        if rule.get("sha256") and rule.get("path") in tracked:
            digest = hashlib.sha256((ROOT / rule["path"]).read_bytes()).hexdigest()
            if digest != rule["sha256"]:
                errors.append(
                    f"K2 AUTHORITY_TOTALITY: {rule['path']} does not match its pinned sha256"
                )
        if not rule.get("path") and not rule.get("prefix"):
            errors.append("K2 AUTHORITY_TOTALITY: routing edge names neither path nor prefix")
    live = {
        (rule.get("path") or rule.get("prefix"), rule.get("class"))
        for rule in rules if str(rule.get("class", "")).startswith("LIVE_")
    }
    for rule in rules:
        if str(rule.get("class", "")).startswith("LIVE_") and rule.get("prefix"):
            errors.append(
                f"K2 AUTHORITY_TOTALITY: prefix {rule['prefix']} routed into "
                f"{rule['class']}; live authority is granted per file, never by location"
            )
    for edge in sorted(live - PINNED_LIVE_EDGES):
        errors.append(f"K2 AUTHORITY_TOTALITY: unpinned live edge {edge[0]} -> {edge[1]}")
    for edge in sorted(PINNED_LIVE_EDGES - live):
        errors.append(f"K2 AUTHORITY_TOTALITY: pinned live edge missing: {edge[0]} -> {edge[1]}")
    # First match wins in classify(), so an earlier edge can silently override
    # a later one. Refuse any edge an earlier edge already covers.
    for i, rule in enumerate(rules):
        target = rule.get("path") or rule.get("prefix") or ""
        for earlier in rules[:i]:
            if earlier.get("prefix") and target.startswith(earlier["prefix"]):
                errors.append(
                    f"K2 AUTHORITY_TOTALITY: edge {target} is shadowed by earlier "
                    f"prefix {earlier['prefix']}"
                )
            elif earlier.get("path") and earlier["path"] == target:
                errors.append(f"K2 AUTHORITY_TOTALITY: duplicate edge {target}")
    withheld = [p for p in paths if classify(p, rules) == "WITHHOLD"]
    notes.append(
        f"{len(withheld)}/{len(paths)} tracked paths unrouted; each fails closed to "
        f"WITHHOLD and carries no authority"
    )

    # ---- K5: runtime disposition ---------------------------------------------
    # Exact match against string values in the plan, recursively. The previous
    # substring test over the serialized plan accepted any path that merely
    # prefixed a longer string, and the glob ignored subdirectories.
    plan_path = ROOT / "kernel/development/VM_INTERNALIZATION_PHASE_PLAN.json"
    if plan_path.exists():
        values = json_strings(json.loads(plan_path.read_text(encoding="utf-8")))
        exempt = set(const.get("runtime_disposition_exempt", []))
        for p in sorted(Path(ROOT, "kernel/runtime").rglob("*.py")):
            rel = p.relative_to(ROOT).as_posix()
            if p.name == "__init__.py" or rel in exempt or "__pycache__" in rel:
                continue
            if rel not in values:
                errors.append(
                    f"K5 RUNTIME_DISPOSITION: {rel} has no disposition in "
                    f"VM_INTERNALIZATION_PHASE_PLAN.json"
                )
    else:
        errors.append("K5 RUNTIME_DISPOSITION: phase plan absent")

    # ---- K6: monograph grounding ----------------------------------------------
    # Quotes are pinned to git blobs, not branch heads: a later edit to a
    # monograph must not silently change what the constitution cites. A blob
    # missing from this clone is a finding, not a skip -- a check that passes
    # because it could not look is the defect class this file exists to catch.
    block_e = const.get("block_e_monograph_grounding")
    if block_e is None:
        errors.append("K6 MONOGRAPH_GROUNDING: block_e_monograph_grounding is absent")
    else:
        monos = block_e.get("monographs", {})
        anchors = block_e.get("anchors", [])
        ids = {a.get("id") for a in anchors}
        texts: dict[str, str | None] = {}
        raw: dict[str, str | None] = {}
        for name, row in monos.items():
            cp = subprocess.run(
                ["git", "cat-file", "-p", row.get("blob", "")], cwd=ROOT,
                capture_output=True, text=True, check=False,
            )
            if cp.returncode != 0:
                texts[name] = None
                errors.append(
                    f"K6 MONOGRAPH_GROUNDING: {name} blob {row.get('blob', '')[:12]} is not "
                    f"in this clone (fetch origin/{row.get('branch')})"
                )
                continue
            texts[name] = re.sub(r"\s+", " ", cp.stdout)
            raw[name] = cp.stdout
            ref = subprocess.run(
                ["git", "rev-parse", "--verify", "--quiet",
                 f"origin/{row.get('branch')}:{row.get('path')}"],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            head = ref.stdout.strip() if ref.returncode == 0 else ""
            if head and head != row.get("blob"):
                notes.append(
                    f"monograph {name} has changed on origin/{row.get('branch')} since it was "
                    f"pinned; citations still verify against the pinned blob"
                )
        for name in block_e.get("required_monographs", []):
            if name not in monos:
                errors.append(f"K6 MONOGRAPH_GROUNDING: required monograph {name} is not declared")
            elif not any(a.get("monograph") == name for a in anchors):
                errors.append(f"K6 MONOGRAPH_GROUNDING: required monograph {name} is never cited")
        for a in anchors:
            text = texts.get(a.get("monograph"))
            if a.get("monograph") not in monos:
                errors.append(f"K6 MONOGRAPH_GROUNDING: {a.get('id')} cites undeclared monograph")
            elif text is not None and re.sub(r"\s+", " ", a.get("quote", "")).strip() not in text:
                errors.append(
                    f"K6 MONOGRAPH_GROUNDING: {a.get('id')} quote is not verbatim in "
                    f"{a.get('monograph')} blob"
                )
            elif raw.get(a.get("monograph")) is not None:
                # The quote must begin on the named line: it is found in the
                # text from that line on, and not in the text from the next.
                lines = raw[a["monograph"]].splitlines()
                n = int(a.get("line", 0))
                q = re.sub(r"\s+", " ", a.get("quote", "")).strip()
                here = re.sub(r"\s+", " ", " ".join(lines[n - 1:n + 7])) if n >= 1 else ""
                after = re.sub(r"\s+", " ", " ".join(lines[n:n + 7])) if n >= 1 else ""
                if not (1 <= n <= len(lines)) or q not in here or q in after:
                    errors.append(
                        f"K6 MONOGRAPH_GROUNDING: {a.get('id')} does not start at "
                        f"{a.get('monograph')} line {n}"
                    )
        for row in const.get("deny_list_enforcement", []):
            grounds = row.get("monograph_grounds", [])
            if not grounds and not str(row.get("no_monograph_ground", "")).strip():
                errors.append(
                    f"K6 MONOGRAPH_GROUNDING: deny-list item {row['item']} has no ground "
                    f"and no stated reason why none exists"
                )
            elif not grounds:
                notes.append(f"NO MONOGRAPH GROUND: {row['item']}")
            by_id = {a.get("id"): a for a in anchors}
            for gid in grounds:
                if gid not in ids:
                    errors.append(
                        f"K6 MONOGRAPH_GROUNDING: {row['item']} cites unknown anchor {gid}"
                    )
                elif not re.search(
                    rf"(?<![A-Z_]){re.escape(row['item'])}(?![A-Z_])",
                    str(by_id[gid].get("grounds", "")),
                ):
                    # A row may only cite an anchor declared to ground that
                    # item. A review found 9 of 15 rows citing anchors whose
                    # own grounds named something else. This is a consistency
                    # check between two fields the same author writes; it
                    # catches drift, not a misreading. Fit is judged by review.
                    errors.append(
                        f"K6 MONOGRAPH_GROUNDING: {row['item']} cites {gid}, whose "
                        f"grounds do not name {row['item']}"
                    )
        for row in const.get("governing_roles_unenforced", []):
            for gid in row.get("monograph_grounds", []):
                if gid not in ids:
                    errors.append(
                        f"K6 MONOGRAPH_GROUNDING: {row['role']} cites unknown anchor {gid}"
                    )

    # ---- K7: pinned core ------------------------------------------------------
    declared_laws = set(block_a["laws"])
    for law in PINNED_LAWS:
        if law not in declared_laws:
            errors.append(f"K7 CORE_PINNED: pinned law removed from the constitution: {law}")
    declared_items = set(block_b["must_remain_outside"])
    for item in PINNED_DENY_ITEMS:
        if item not in declared_items:
            errors.append(f"K7 CORE_PINNED: pinned deny-list item removed: {item}")
    for item in PINNED_ENFORCED:
        row = enforcement.get(item)
        if row is not None and row.get("enforcement") == "NONE":
            errors.append(f"K7 CORE_PINNED: pinned enforced item downgraded to NONE: {item}")
    digest = protected_core(const)
    if digest != PINNED_CORE_DIGEST:
        errors.append(
            f"K7 CORE_PINNED: a protected section changed (digest {digest[:12]}, pinned "
            f"{PINNED_CORE_DIGEST[:12]}). If intended, update PINNED_CORE_DIGEST in this "
            f"file; the self-sealing auditor will surface that edit"
        )

    # Notes print first and always. They were previously printed only on the
    # passing path, so the whole gap report vanished exactly when something
    # failed -- the moment it matters most.
    for note in notes:
        print(f"  note: {note}")
    if errors:
        print()
        print(f"CONSTITUTION AUDIT FINDINGS ({len(errors)})")
        for item in errors:
            print(f"  {item}")
        print()
        print("A rule that names no enforcing check is documentation, not")
        print("constitution. Either bind it to a check, or declare it unenforced")
        print("with a reason so the gap is visible rather than assumed closed.")
        return 1

    print(
        f"CONSTITUTION AUDIT PASS ({len(block_a['laws'])} laws; "
        f"{len(block_b['must_remain_outside'])} deny-list items; "
        f"{len(role_fields())} role fields; {len(paths)} paths; "
        f"{len((block_e or {}).get('anchors', []))} monograph anchors)"
    )
    print("Enforcement is not correctness: PASS means the boundary is declared and")
    print("checked, not that any claim inside it is true.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
