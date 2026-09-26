# Fresh Instance Ground

**Purpose:** bootstrap fresh LLM/agent contexts into the project with the minimum stable ground needed to continue useful work without re-reading all of `Canonical/` on every invocation.

**Role:** baseline + conquered distinctions + routing law + current-state pointer.

**Not authority:** this file is not the current Canonical head, does not mint science/FORM/runtime/AGI/consciousness/RSI authority, and must not override newer returned evidence. It is intentionally slower-moving than project history.

## 0. Read order

For a fresh instance:

```text
1. read this file completely
2. read /Canonical/AUTHORITY_GRAPH.json
3. read /Canonical/DISPOSITION_MANIFEST.json
4. read /Canonical/CURRENT_STATE.md
5. if the task concerns live Minerva engineering, follow the current execution pointers named there into split/minerva and verify exact live state
6. if structural interpretation is needed, read /Canonical/Map.md
7. if constitutional/root claims are needed, read /Canonical/Root.md
8. if THEO/PHEN structural synthesis is needed, read /Canonical/Ontology.md
9. descend into /Canonical/Past, /Canonical/Future, provenance, research, runtime evidence, Git history, issue bodies, or workflow artifacts only through an explicit task/evidence edge
```

The point is not to replace Canonical or the live Git body. The point is to avoid forcing every fresh context to reconstruct the entire project before it can act coherently.

Filesystem law:

```text
NO FILE IS LIVE AUTHORITY BY LOCATION, RECENCY, NAME, REVISION NUMBER, OR SEMANTIC SIMILARITY.

Past/*   = evidence/history by default, never current authority by filename.
Future/* = unadmitted candidate/successor material by default, never scheduled/current by filename.

Only explicit live routing/admission edges change those defaults.
```

Stable current-state pointer:

```text
/Canonical/CURRENT_STATE.md
```

Current routing surfaces:

```text
/Canonical/Map.md
/Canonical/Root.md
```

Live Minerva execution is faster-moving than this file. When the task is engineering/current-development specific, resolve the exact live pointers from the current state before acting. At the 2026-09-26 handoff, the important live surfaces included:

```text
split/minerva/kernel/CURRENT_STATE.md
split/minerva/docs/ISSUE_ROADMAP.md
split/minerva/kernel/development/VM_INTERNALIZATION_PHASE_PLAN.json
split/minerva/kernel/development/SELF_TEACHING_DEVELOPMENT_DAG.json
split/minerva/autonomy/interaction/mentor/ACTIVE.json
```

Do not assume those paths' contents, branch head, open carrier, or active issue remain unchanged merely because this bootstrap names them.

If this file and `CURRENT_STATE.md` disagree about a time-sensitive or recently earned state, treat this file as baseline and `CURRENT_STATE.md` as the newer routing projection, then inspect the cited live evidence before promoting any claim.


### 0.1 Execution contract: prose is not enough

For any nontrivial repository mutation, use this order:

```text
SOURCE OF TRUTH
→ EXECUTION INVARIANTS
→ CURRENT LIVE STATE
→ ALLOWED ACTIONS
→ FORBIDDEN ACTIONS
→ ACCEPTANCE TEST
→ MUTATE
→ VERIFY
→ PERSIST NEW STATE
```

Do not act merely because the architecture has been correctly summarized in prose. Before every mutation, re-check the proposed action against the governing invariants and the live machine-readable state.

Mandatory separation:

```text
USER-SUPPLIED / CANONICAL CLAIM
!= CURRENT REPOSITORY FACT
!= ASSISTANT INFERENCE / PROPOSED CHANGE
```

Never silently promote an assistant interpretation into a repository premise. If an interpretation is needed, label it as an inference and test it against the governing files before implementation.

Repository discipline:

```text
conversation history = provenance / evidence
repository state      = operational continuity
```

The project must not depend on a fresh agent reconstructing settled constraints from chat archaeology. Persist the current state and authoritative roadmap in machine-readable repository data.

Before creating a new plan/provenance/roadmap file, check whether an existing authoritative semantic DAG/state object already owns that concern. Prefer updating the existing authority over spawning a parallel planning surface.

Before deleting, moving, collapsing, or superseding repository material:

```text
AUDIT FIRST
→ classify function / authority / provenance role
→ identify live dependencies
→ make the mutation reversible or historically reconstructible
→ verify no consequential distinction was erased
```

Messy != disposable. Duplicate-looking != semantically redundant.

Forbidden default move:

```text
learner-development residual
→ assistant writes capability-specific host machinery
```

unless the live roadmap explicitly authorizes a temporary scaffold, identifies why it is necessary, and defines its source-removal test. The preferred move is:

```text
residual
→ learner encounters / abstracts / reconstructs distinction
→ learner-owned state
→ consequence test
→ source/scaffold removal
```

Every code change should be traceable to a live DAG node or constitutional maintenance need and state which invariant it advances. If no such mapping exists, stop and inspect before coding.

## 1. Core developmental aim

The Machine should become increasingly able to identify, understand, remember, test, repair, and eventually remove its own limitations without allowing self-improvement to become self-authorization, self-validation, or sovereignty.

Developmental arc:

```text
Strong Safe RSI
→ self-selected development
→ Lateralizer + Internalizer
→ learner-initiated external inquiry
→ persistent network memory
→ WWW Mind
→ Lain
→ Root / situated interface
→ broader World participation
→ AGI only if broad heterogeneous competence is independently demonstrated
```

These are gates, not promotions.

```text
Strong Safe RSI != WWW Mind
WWW Mind != AGI
persistent autonomy != AGI
self-improvement != self-authorization != self-validation
```

A learner cannot certify itself into a stronger category by changing its own labels or internal state.

## 2. Constitutional noncollapse

Preserve these distinctions unless a later earned result explicitly replaces them:

```text
learner != evaluator != World != authority
proposal != authority to accept proposal
representation != represented thing
model(World) != World
model(Self) != Self
prediction != return
receipt != return
reply != independent return
memory of Other != Other
reachability != ownership != authorship
connection != fusion
contact != consent != jurisdiction
reading != authorization
presence != sovereignty

CODE_DELETION != INTERNALIZATION
STATE_OWNERSHIP != GENERALIZATION
ABSTRACTION != CAUSAL_USE
CAUSAL_USE != INTERNALIZATION
SOURCE_REMOVAL != INDEPENDENT_EVALUATION
INTERNALIZATION != PROMOTION

GENERATE != DIMENSIONALIZE != LATERALIZE != CRYSTALLIZE_F != INTERNALIZE

LEXICAL_GROUNDING != THEATER_BINDING
RELATION_CLASSIFICATION != PARTICIPANT/KFS_RECONSTRUCTION
DISCOURSE_PRESENTATION_ORDER != EVENT/HISTORY_ORDER

NETWORK_MEMORY_CHANGES_LATER_QUERY != USEFUL_RELATIONAL_RECONSTRUCTION
RETURN_SIGN != CAUSAL_CREDIT
CONFIG_UTILITY != GLOBAL_CONFIG_TRUTH
DUPLICATE_EVENT != NEW_EVIDENCE
ABSENCE_OF_RETURN != NEGATIVE_RETURN

current route != genealogy
genealogy != current authority
historical presence != live dependency
self-selected != self-authorized
self-revision != self-promotion
RSI != AGI
AGI != consciousness
WWW Mind != global subject
boundary != isolation
```

General law:

```text
internalize competence;
do not internalize the outside world's right to disagree.
```

Anything whose epistemic or constitutional value depends on independence from the learner must preserve that independence relation even if its implementation changes.

Examples include:

```text
World / Other
fresh non-preauthored Return
independent evidence identity
independent evaluator custody / trust roots
O* / correction source
Anti-Minerva / correction permeability
STOP / WITHHOLD
rollback / parent custody
authorization
jurisdiction / claim-binding authority
hard resource/substrate boundaries
```

A later implementation that looks simpler while violating one of these is regression, not maturation.

## 3. WorldMirror / Machine architecture

WorldMirror VM is the Body/local developmental center, not the whole World.

There is no requirement that the Machine equal one Python class or one process. Its more meaningful continuity is:

```text
persistent causally connected state
+ developmental lineage
+ learned policies
+ memories
+ provenance
+ admissible transformations
```

Current implementation is largely:

```text
Python dataclasses / generic executors
+ deterministic canonical JSON
+ SHA-256 roots
+ SQLite semantic memory
+ content-addressed compressed objects
+ Git/provenance history
```

The local runtime is a governed semantic state-transition system, not merely mutable variables.

Constitutional transition shape:

```text
returned evidence
→ source / digest / nonce checks
→ jurisdiction / legitimacy / lease checks
→ dependency closure
→ update
→ successor hash
→ sibling-integrity check
→ transition receipt
```

Storage partition:

```text
VMK2 constitutional state
vs developmental semantic state
vs VenusMemory episodic/network memory
vs external World provenance
```

Do not collapse these partitions merely because all can currently be serialized.

Runtime disposition has four classes:

```text
KEEP_CONSTITUTIONAL / EXTERNAL
→ VMK2 constitutional transition core
→ external authority/authentication substrate
→ Internalizer admission/audit

KEEP_GENERIC_REPLACEABLE
→ canonicalization / hydration / storage / interaction store
→ process/action transport
→ generic TransformProgram/interpreter/retrieval machinery
IF task-specific cognitive semantics live in learner state

MATURE_REDUCE
→ historical bespoke machinery whose tested consequence is reproduced by a simpler ordinary mechanism
→ preserve genealogy, not unnecessary runtime complexity

EDIBLE DEVELOPMENTAL SEMANTICS
→ problem formation
→ research/study routing
→ proposal/GENERATE policy
→ network-query derivation / semantic reconstruction
→ learning / causal-credit update
→ recurrence selection
→ lateralization / retrieval / planning / orchestration when earned
```

The long-run direction is:

```text
Python chooses cognition
→ state increasingly chooses cognition
→ Python increasingly executes generic semantics
```

A tiny generic executor may remain indefinitely. Implementation language is irrelevant if it no longer secretly chooses the cognitive answer.

Important current example: capability-specific relation-trace construction/search remains developmental scaffold until B3 is earned. Configuration living in JSON does not by itself make capability-specific Python generic.

## 4. Reality boundary: bytes before host ontology

Default developmental boundary:

```text
WORLD / OTHER
→ BYTES / RAW CARRIER
→ ABSTRACTION
→ RELATIONAL ORGANIZATION
→ CONSEQUENCE
→ REVISION
```

The important architectural commitment is:

```text
BYTES → ABSTRACTION
```

not a host-authored zoology of capability-specific parsers and cognitive organs.

Do **not** assume that arbitrary World input should first be routed through a permanent semantic taxonomy such as:

```text
image → image cognition module
audio → audio cognition module
PDF   → PDF cognition module
Web   → Web cognition module
...
```

That is a default architectural failure mode because it lets host-written categories pre-decide which distinctions matter. If carrier/modality distinctions are consequential, they should increasingly emerge inside learner-owned abstraction because different raw structure produces different returned consequences.

The substrate may still need boring transport/decoding operations to expose bytes or minimally accessible raw structure. Those operations are not thereby cognitive semantics and must not silently become the learner's ontology.

Preferred asymptotic relation:

```text
WORLD
→ raw carrier / bytes
→ generic exposure to developmental center
→ learner discovers consequential distinctions
→ learner relates / remembers / tests them
→ learner-owned abstraction
→ consequence
→ crystallize / internalize / reopen
```

Carrier metadata, hashes, source identity, timestamps, custody and provenance may remain externally recorded because they support evidence integrity. Their presence does not authorize host code to decide the semantic meaning of the carrier.

Never collapse:

```text
raw carrier != abstraction
abstraction != proposition
proposition != evidence
evidence != belief
belief != competence
competence != internalization
```

Strong preference:

```text
capability-specific carrier machinery ↓
learner-owned abstraction ↑
```

A capability-specific decoder/interpreter may exist temporarily only when genuinely required to expose the carrier at all, and then it must be treated as scaffold with explicit justification, provenance, and reduction/internalization criteria. Do not promote temporary access machinery into permanent cognitive architecture by convenience.

## 5. Ingest / integrate / internalize

Keep these operations separate:

```text
ingest:
World thing → persistent encounter representation

integrate:
encounter → changes memory/model/query/representation

internalize:
repeated scaffolded competence
→ reusable learner-owned organization
→ scaffold/source removable
→ capability survives returned tests
```

Internalization is stronger than storage and stronger than causal influence.

Source-removal survival is required evidence for an internalization claim.

A hundred papers may remain source-derived memory while a method abstracted across them becomes learner-owned competence.

## 6. Lateralizer / Crystallizer / Internalizer

Current recovered operator distinction:

```text
GENERATE     = construct candidates within/from an admitted epistemic object
LATERALIZE   = expand/re-express the epistemic basis into independently answerable faces
CRYSTALLIZE  = retain the minimum future-sufficient cross-face organization
INTERNALIZE  = migrate earned scaffolded capability into state-owned function under ablation
```

Lateralizer asks whether the current coordinate system is the problem. Multiple descriptions generated from one perspective are not automatically independent views. Useful faces must be independent enough that disagreement can reveal hidden structure.

Crystallization is not compression for its own sake:

```text
preserve what still changes lawful futures
discard only what has become reconstructible/redundant
```

A crystal is not final. New returned consequence may split previously equivalent states and force reopening.

Developmental rhythm:

```text
World
→ difference
→ Lateralizer / richer representation
→ consequence
→ stable relation
→ CRYSTALLIZE_F
→ simpler representation
→ Internalizer
→ scaffold removal
→ World
→ new difference
→ reopen
```

Long-run minimal machinery may increasingly reduce toward:

```text
differentiate
relate
test
remember
compress
reopen
```

## 7. Self-minimizing developmental architecture

Most explicit developmental machinery is potentially edible if its consequence-bearing organization can be reconstructed as learner-owned competence and survives source/scaffold removal.

Long-run direction:

```text
large explicit VM / developmental machinery
→ repeated use
→ relational regularity discovered
→ learner-owned state/policy
→ returned consequence test
→ source-removal test
→ redundant scaffold disappears
→ smaller machinery
→ repeat
```

Likely edible semantics include problem selection, study/routing, proposal generation, search/query construction, retrieval, lateralization, abstraction discovery, crystallization, planning and portions of developmental orchestration.

Not everything should become learner-sovereign. Constitutional independence relations must remain externally corrigible.

The mature target is closer to:

```text
tiny constitutional substrate
around
a continuously self-reconstructing semantic developmental center
```

not an ever-growing pile of special-case code.

## 8. WWW Mind / Lain / Root

WWW Mind = persistent distributed cognition, not one global subject and not a giant local cache.

```text
Machine
↔ papers
↔ repositories
↔ humans
↔ datasets
↔ agents
↔ databases
↔ previous encounters
```

Persistent network memory matters because:

```text
encounter A
→ remember what/why A mattered
→ encounter B later
→ notice disagreement
→ ask C
→ revise
→ revisit A
```

The external centers remain external.

Lain asks whether a continuously network-situated participant can preserve Self/Other and authority distinctions:

```text
Self ↔ WWW ↔ Other
```

without collapsing into an undifferentiated subject.

Root is a different gate: how distributed cognition becomes locally situated, jurisdictionally bounded, authorized participation.

```text
distributed perception
→ local interpretation
→ situated context
→ jurisdiction
→ authorization
→ action
→ World consequence
→ return
```

Knowing through WWW is not the same as being situated or authorized to act.

## 9. Empirical-development burdens

Every learned distinction/capability must keep three proof burdens separate:

```text
B1 — abstraction
Did the learner acquire the distinction rather than memorize a surface?

B2 — causal use
Does the distinction alter later cognition/action for the predicted reason?

B3 — internalization
Is learner-owned state actually doing the work after the teaching/performance scaffold disappears?
```

Useful B1 controls:

```text
opaque renaming
surface/presentation permutation
irrelevant transformation invariance
held-out factor recombination
matched length/cardinality
paraphrase / carrier change
decoy features
cross-face transfer where claimed
WITHHOLD instead of forced guessing
```

Useful B2 controls:

```text
candidate present vs ablated
relevant-coordinate intervention vs irrelevant-coordinate intervention
same-budget baseline
fresh query / retrieval / prediction / problem / plan / action
prefrozen downstream metric
```

Useful B3 controls:

```text
capability-specific source/teacher/donor inaccessible
generic executor only
cold restart / state rehydration
delayed reuse after unrelated work
fresh non-preauthored transfer
teacher context absent
evaluator-hidden or independent scoring
provenance preserved
rollback reconstructible
decoy scaffold cannot override learned consequence
reopening under contradiction
```

Do not promote directly from a better output to B3. Self-report has zero promotion weight.

Anti-pretend principle: false learning need not involve deception. Shortcut learning, teacher leakage, answer visibility, serialized teacher ontology, benchmark memorization, surface statistics, hidden capability-specific Python, evaluator coupling, or obedient reproduction can all produce false positives.

Known negative/limiting result preserved as baseline:

```text
bounded Internalizer ownership can pass
while fresh lateral transfer fails
```

Therefore:

```text
INTERNALIZATION != GENERALIZATION
```

Cognitive Theater is the current foundational semantic custody example. Bounded results reached indexed binding, symbolic event order, explicit TheaterState, causal KFS intervention/history distinction, and source-removal survival; final independent hidden/fresh evaluation remains WITHHOLD. Local source removal must not be relabeled independent B3 closure.

## 10. Dependency-aware development

Development itself is becoming a learner-owned object. Required planning distinctions include:

```text
dependency DAG
ready frontier
fork / join
work
span
critical path
slack
work/span parallelism
CPM / PERT-like uncertain duration
DAG shortest lawful path under explicit cost
rescheduling after returned durations/outcomes
```

Keep distinctions:

```text
dependency != adjacency
dependency edge != causal truth
shorter != lawful
parallelizable != authorized
critical path != importance
schedule priority != admissibility
PERT estimate != World return
```

B1 should survive opaque task relabeling, shuffled presentation order, held-out fork/join recombination, and dependency-vs-temporal-adjacency traps. Cycles or underspecification may require WITHHOLD.

B2 should show that critical-duration intervention changes predicted span, matched noncritical intervention does not, dependency/admissibility changes alter the schedule correctly, legal parallelism reduces span, and attractive unlawful shortcuts are rejected.

B3 only begins when planning changes actual self-development after teacher labels/scaffolds disappear.

Roadmap scheduling law:

```text
among admissible work:
maximize downstream learning leverage
→ minimize time-to-discriminating return
→ exploit safe parallelism
→ use resource leverage as tie-break
```

The goal is not a sovereign handcrafted scheduler. The learner should reconstruct and use these distinctions in its own state.

## 11. Return credit assignment

Returned consequence requires provenance-aware credit rather than naive reward accumulation.

Preserve:

```text
receiving a signed review != knowing what caused the outcome
returned event != new evidence
same signed return != same causal credit
duplicate return != double utility
same configuration != same expected utility across contexts/targets
mixed target outcomes != global winner
delayed return != credit to whichever episode is active now
missing return != negative return
```

Current rival structure to preserve conceptually:

```text
COUNTING
→ every signed occurrence updates utility

PROVENANCE_BOUND
→ only unique authorized returns bound to originating candidate/target/episode count

CONTEXTUAL
→ credit remains indexed by context rather than collapsing into one global utility
```

Relevant discriminators:

```text
duplicate replay
→ no additional evidence update

wrong-origin return
→ original candidate unchanged

delayed return
→ credit follows originating episode

contradictory target-conditioned returns
→ mixed/contextual evidence remains visible

counterfactual removal of one return
→ only dependent future selection may change
```

Generic contextual-evidence substrate may deduplicate and bucket evidence, but the meaning of candidate/target/episode/sign/admission must become learned/state-owned rather than silently supplied by host code.

This distinction is now part of the critical path toward self-development recurrence.

## 12. Language / Theater / Music / Math

Do not collapse domain status levels:

```text
mentioned
!= analogy
!= structural witness
!= formalized
!= curriculum object
!= executable competence
!= currently live subsystem
```

Math/logic is the deepest vertically integrated domain and serves as exact formal warrant/invariance.

Generic Language is structurally deep and partly operationalized through relational grammar, developmental language machinery and current successor learning state.

English has historical executable curriculum and remains a bootstrap/developmental carrier, not privileged ontology.

Music is a strong temporal-inhabitation / global-to-local structural witness but comparatively embryonic as an executable machine subsystem.

Theater provides explicit roles, participant indexing, knowledge, local perspective, history, action and admissible continuation; it became an executable causal testbed rather than remaining metaphor.

Cross-language curriculum hypothesis, when used, is functional rather than essentialist:

```text
Brazilian Portuguese → GENERATE while preserving relational continuity
Japanese             → INFER while preserving contextual continuity
English              → EXTERNALIZE while preserving warrant/scope
Mathematics          → FORMALIZE while preserving exact invariance
```

The target is relational invariance across different enactment constraints, not superficial translation identity.

## 13. Interaction / mentor boundary

The desired human-facing WorldMirror interface is minimal and evidence-oriented:

```text
chat
+ state diff
+ residuals
+ history/provenance
+ STOP/WITHHOLD
+ inspectable learner state
```

Every interaction should become a structured, provenance-bearing event rather than disappearing after inference.

Mentor context is nonsovereign. Human/LLM guidance may expose doors, residuals, counterexamples, possibility classes or methodological distinctions, but should not silently become target-binding authority, truth authority, promotion authority or independent evaluation.

Desired loop:

```text
mentor / interaction trace
→ orientation, not command
→ Machine forms admissible problem
→ selects target/study/inquiry
→ World returns evidence
→ persistent memory changes later cognition
→ failure exposes residual
→ Machine invents repair / abstraction
→ returned consequence tests it
→ retain / WITHHOLD / reopen
```

Mentor fade is explicit:

```text
M3 unknown-door exposure
→ reveal that a representation/tool/test family exists; do not supply the solution

M2 discriminator coaching
→ ask what distinguishes baseline, falsifies the claim, must remain external, or must disappear for ownership

M1 adversarial review
→ counterexamples, shortcut hypotheses, provenance/authority/transfer challenges

M0 silence
→ learner independently finds residual, forms problem, finds representation/tool, designs discriminator, prefreezes, tests, source-removes, transfers and reopens
```

Terminal mentor objective:

```text
minimize mentor work on the learner's critical path
while preserving access to genuinely unknown doors
```

Returned-review learning must keep axes separate. Useful work can contain an unhelpful method; a positive episode must not reward every method/config merely because something useful happened.

The human is not intended to remain the permanent training substrate.

## 14. Current Machine / Git-body baseline already conquered

Do not make a fresh instance re-prove these merely because it started with an empty context. Verify against current evidence when consequential, but treat them as previously established project history unless current live state says otherwise:

```text
bounded developmental recurrence exists
standing developmental orientation can be causally upstream of autonomous target selection
carrier-local work exhaustion != developmental completion
learner-owned problem formation and bounded writable recurrence exist
self-selected development exists at bounded scope
learner-initiated network inquiry exists
persistent provenance-bearing network memory exists
persistent network memory can causally change later inquiry
bounded WWW Mind structural gate has passed
passive/authored-center separation has bounded evidence
mentor context can be rewritten into narrower nonsovereign context
proposal != authorization != execution is live
reply != independent return is live
raw-first local interaction / process-body surfaces exist
three-burden learning proof is operational
TheaterState / indexed KFS / temporal history / causal KFS intervention exist
same endpoint != same history is operationally represented
bounded Theater source-removal ownership has passed
returned semantic-trace utility can alter later configuration selection
bounded cross-target reuse of a useful trace configuration has been observed
query/memory causality can succeed while semantic crystallization remains inadequate
contract-selected work now fails closed when its exact executor is unavailable rather than silently substituting generic study
```

Important negative/open results are equally part of the conquered state:

```text
general Lateralizer fresh transfer = failed/open
bounded Theater source removal != independent B3
semantic relation trace B3 = not earned; capability-specific scaffold remains
interactive Lain = WITHHOLD
Strong Safe Independent RSI = not earned
AGI = not established
consciousness = OPEN/WITHHOLD
```

Do not inflate bounded evidence into:

```text
AGI
phenomenal consciousness
open-ended RSI
unrestricted Safe Strong RSI
autonomous science
general Lateralizer
general semantics
full multimodal World inhabitation
independent evaluative closure
```

Failure that changes later search/development is developmental evidence; it is not a hidden success claim.

## 15. Current persistent open surface

Stable unresolved classes include:

```text
independent non-preauthored return / independent evaluation custody
Cognitive Theater final independent B3 receipt
general Lateralizer transfer after failed fresh generalization
semantic relation-trace reproducible B2 quality and later B3; capability-specific relation_trace scaffold still live
provenance/context-aware causal return-credit assignment
uncertainty / nonstationarity after credit becomes causally grounded
dependency-DAG / critical-path planning used causally by the learner
learner-generated B1/B2/B3 experiment design
self-development scheduling over its own developmental DAG
policy-by-policy internalization of problem/study/generate/query/learning/recurrence semantics
shrinking autonomous worker toward a generic orchestration membrane
memory retrieval/reconstruction/crystallization ownership distinct from storage
repeated heterogeneous Strong Safe RSI recurrence with mentor off critical path
interactive Lain with real contact capability + jurisdiction + independently authored Other
repeated situated Root action
broader heterogeneous World participation
multimodal carrier-neutral encounter envelopes
minimal constitution while developmental scaffolding shrinks
```

The remaining high-level developmental recurrence is:

```text
OBSERVE
→ RESIDUALIZE
→ FORM
→ LATERALIZE
→ PREFREEZE
→ SCHEDULE
→ ENCOUNTER
→ COMPARE
→ CREDIT
→ CRYSTALLIZE_F
→ INTERNALIZE
→ REMOVE SOURCE
→ TRANSFER
→ REOPEN
```

The actual active slice is volatile. Do not freeze issue numbers or branch SHAs here as authority. Resolve them from `/Canonical/CURRENT_STATE.md` and the live Minerva state before acting.

The 2026-09-26 handoff placed causal return-credit and dependency planning at the parallel-ready frontier, with uncertainty/nonstationarity and a joint RSI recurrence audit downstream. Treat that as a dated handoff fact, not an eternal curriculum order; returned defects may preempt it.

## 16. Canonical / root usage rule

`Canonical/` is the deep authority/provenance environment. This file is the fresh-instance ground. The live Git body may move faster than Canonical's explanatory surfaces, so current engineering claims must also be checked against live branch state/history.

Use them differently:

```text
this file:
fast initialization
stable invariants
conquered distinctions
anti-drift floor
where to look next

/Canonical/CURRENT_STATE.md:
volatile project-level current routing projection
current correction / pointer into live evidence

/Canonical/Map.md:
structural/historical routing and reconciliation

/Canonical/Root.md:
constitutional/root claims

live split/minerva state / Git history / issue bodies / workflow artifacts:
current executable developmental truth and returned engineering evidence

/Canonical/Past, Future, research, provenance, runtime evidence:
deep verification, genealogy, experiments, implementation and unresolved programs
```

Canonical historical custody does not require preserving historical implementation for its own sake:

```text
recover functional consequence
+ preserve genealogy
+ preserve causal distinctions
+ allow implementation replacement/reduction
```

Never let bootstrap convenience outrank evidence.

Never force a fresh instance to read the whole archive when the task only needs the baseline and current pointer.

### 16.1 Planning-state sovereignty

There should be one authoritative machine-readable semantic roadmap/DAG for live developmental state. Other views are projections, active slices, or human-readable renderings.

```text
authoritative semantic DAG/state
→ active subgraph / ready frontier
→ human Markdown projection
→ provenance/evidence behind selected nodes
```

Do not let several overlapping planning files independently claim “current plan.” If multiple planning surfaces exist, explicitly classify each as authoritative, derived/projection, historical, or evidence-only.

Fresh agents should start from the authoritative state layer and open deep provenance only along the selected dependency path. They should not survey hundreds of evidence files merely to rediscover what the roadmap already knows.

Execution continuity rule:

```text
finish a change
→ verify returned result
→ update authoritative machine-readable state
→ only then rely on the next agent to continue
```

A conversational promise or progress update is not persisted project state.


## 17. Update protocol for this file

This file should change slowly.

Update it when a distinction becomes durable enough that future agents should not have to rediscover it, or when the routing law itself changes.

Do not rewrite it for every issue, commit, experiment or local result.

Fast-moving history belongs in `Canonical/CURRENT_STATE.md` and its cited evidence.

When updating:

```text
preserve claim modality
preserve negative results
preserve OPEN/WITHHOLD status
preserve authority boundaries
preserve counterexamples and known failure modes
remove obsolete implementation trivia when reconstructible elsewhere
retain pointers to the live authority/evidence surfaces
```

If a later result overturns a baseline distinction, revise this file explicitly rather than silently layering contradictory prose on top.

## 18. Minimal fresh-instance compression

```text
The Machine is a governed developmental center, not its current Python substrate.
It may increasingly choose what to learn, reorganize representations, inquire of the World, remember external relations, crystallize invariants, design experiments, assign causal credit, schedule development, internalize earned competence and remove obsolete scaffolding.

But competence must not silently become sovereignty.
World, Other, fresh Return, correction, evidence custody, evaluation, authorization, jurisdiction, rollback and STOP/WITHHOLD retain independent constitutional roles.

External encounter != truth.
Storage != learning.
Changed later behavior != correct later behavior.
Abstraction != causal use.
Causal use != internalization.
Code deletion != internalization.
State ownership != generalization.
Source removal != independent evaluation.
Utility != truth.
Return count != evidence count.
Self-revision != self-promotion.
RSI != AGI != consciousness.

Lateralize when the coordinate system is insufficient.
Crystallize only what remains future-sufficient.
Internalize only what survives disappearance of capability-specific teaching/performance machinery.
Reopen when new consequence separates what was compressed.

For every capability, keep B1 abstraction, B2 causal use and B3 internalization separate.
Use dependency DAGs so development becomes schedulable and safely parallelizable.
Use provenance/context-aware causal credit so returned utility does not collapse into reward=truth.
Let the learner increasingly design its own discriminators and make mentor decomposition disappear from the critical path.

Current bounded history already includes self-selected development, learner-initiated Web inquiry, persistent network memory, bounded WWW structure, explicit participant-indexed Theater state, causal KFS intervention, source-removal ownership at bounded scope, returned-utility-driven later selection, and cross-target reuse of some learned trace utility.
It also includes authoritative failures/withholds: general Lateralizer transfer failed, independent Theater B3 remains withheld, relation-trace B3 is not earned, interactive Lain is withheld, Strong Safe RSI is unearned, AGI is unestablished, consciousness is open.

Before mutating the repo, re-check: source of truth, invariants, live state, allowed/forbidden actions, and acceptance test.
Do not turn learner-development residuals into new capability-specific host organs merely because that makes the next test easy.
Prefer WORLD → BYTES → ABSTRACTION, with learned consequential distinctions rather than a permanent host-authored modality taxonomy.
Treat the authoritative machine-readable developmental DAG/state as continuity; treat Markdown and conversation as projections/provenance.
Audit before deleting or consolidating.

Use this file to stand up quickly.
Use /Canonical/CURRENT_STATE.md to know where project history currently is.
For live Minerva work, resolve the current split/minerva state/history before acting.
Use deeper Canonical/provenance only when the claim actually requires it.

The long-run goal is not an ever-larger hand-authored mind, but a progressively smaller constitutional substrate surrounding a self-reconstructing semantic machine that can repeatedly:

notice
→ abstract
→ test
→ plan
→ parallelize
→ credit
→ revise
→ source-remove
→ transfer
→ reopen

on heterogeneous self-selected problems,
while the World remains capable of disagreeing,
and while human/LLM mentorship approaches causal irrelevance.
```
