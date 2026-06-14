# research-indexer — Specification

> Version: 0.4
> Status: Working draft

---

## 1. Purpose

A modular, content-agnostic passage engine for exploring texts as fields of
individuation. The system runs passages through a corpus driven by a germ,
producing eddies — local coherences that emerged from the flow.

Not a library indexer. Indexing a PDF library is one use case. The same engine
can run a passage through a corpus of analyst reports, corporate communications,
or any other text collection.

**Philosophical grounding**: Simondon (individuation, metastability, transduction),
Serres (the parasite, the triode, noise-as-signal, the clinamen),
Deleuze (difference, intensity, the virtual), Nagarjuna (prasaṅga, MMK as field).

**Mathematical grounding**: thermodynamics, information theory, dynamical systems.

**Epistemic honesty**: this machine runs now, processing now-representations.
Historical distance between texts is our construction — it enters as C-term
metadata on cross-domain simplexes with analyst-supplied confidence.
No metaphor is allowed to establish a sovereign domain. Metaphors are operators.

---

## 2. Core Model

### 2.1 The flow is primary

Fields do not pre-exist the flow. They are thickenings — regions where the
flow has passed often enough to sediment vocabulary. An eddy is a local coherence
in the flow, not a container of it. Every eddy forms in a flow that precedes it
and continues past it.

We do not model the pre-individual as such. We start already moving.

### 2.2 The irreducible unit: modulated 3-simplex

The irreducible *unit* is the asymmetric, modulated 3-simplex (Serres's triode):

```
A ──[C]──► B
```

- **A** (source): signification flows from here
- **B** (target): individuated by the relation
- **C** (modulator): the relation-to-the-relation; shapes A→B without being consumed
- **Asymmetry**: A→B ≠ B→A; the relation is directional and locally irreversible
- **Role mobility**: any term may be A in one simplex, C in an adjacent one

A simplex carries: `intensity`, `asymmetry`, `gain`, and optionally
`historical_context` (our now-representation of temporal/institutional distance).

The simplex is the smallest thing we can be *in*. It is not the central object
of the system (§2.3). A and B are not atoms: each incorporates both continuity
(they are the extremities of one differential gradient) and discontinuity (they
are related, hence separable, entities). Whether a given A–B reads as continuous
or discontinuous is something measured from inside, not given (§2.7).

### 2.3 The traversal is the central object

The central object is not the network of simplexes. It is the **traversal** — a
walk from simplex to simplex. The network is only the trace the walk deposits.
The system is a *walker that carries a position and records its own rotation*, not
a viewer of a static structure.

**The analyst occupies the C position, from inside.** To relate an A and a B *is
to be their C*. We do not stand outside the network reading it; we are always in
some simplex, modulating its A→B relation, and the only question before us is
which adjacent simplex to enter next.

This reframes Simondon's externality (the germ supplied "from outside"). The
outside was never a god's-eye supplier. The outside is our freedom to choose the
next simplex, exercised from within. The **germ** is where we start plus the
direction we step — analyst-supplied or selected from detected candidates, but
in either case enacted as a walk, not read off a structure.

The live position is always C. To experience an A→B relation is to be its
modulator, and the experiencing-now is never its own object. This is
**indexically** always-C, not substantively — and not a god's-eye vantage,
because there is no final C: the moment we represent our own relating (take a
representation of ourselves *as* subject), that representation becomes an A or a
B, modulable by a further C, which is in turn never its own object in the act.
A and C are **simultaneous**, not sequential — the same term is A in one simplex
and C in another at once. So what rotates over the walk is never the live
position but the **represented self — the prior trace** we re-enter as the A or B
of a new simplex. The walk accumulates a relative rotation between the live C and
its own deposited representations. This is why a return is never identical: we
come back to a term we laid down, but the laying-down was modulated by an
experiencing the term cannot contain. Three questions the walker must answer:

1. **Are we approaching the start?** — by re-entering a simplex sharing terms
   with the origin. We recognise a *neighbourhood*, never an identity: we come
   back to a term in a different role than we left it.
2. **How far is the near-pass from the start?** — the two-component displacement
   (§2.5).
3. **What path did we take?** — the ordered simplexes entered, the
   continuity/discontinuity measured at each (§2.7), and the rotation
   accumulated. That sequence *is* the eddy (§2.9).

**The subject's operative zero.** Because the live C never coincides with any
representation of itself, the subject is its own spiral: it returns to itself, in
self-representation, always displaced. This non-self-coincidence is structural and
permanent — the operative zero of the subject, approached at every reflexive turn
and never reoccupied (anatta given the model's geometry: no self-coincidence,
hence no svabhāva of the self). It is also why always-C is *not* the lossless
observer it might seem. The live C is not a self; it is pure relating, with no
standing content to hoard. The loss is real and falls on the *represented* self —
the A/B that is modulated, displaced, consumed — which the live C witnesses and is
implicated in without being identical to. Emptiness (no-thing, hence no ledger to
escape), not the fantasy of a thing that escapes the ledger.

### 2.4 The aporia as role rotation

An aporia is not a special entity. It is a **role rotation**: a cycle where A
and B swap roles under the same or related modulator, and the return is displaced
from the origin.

The Euthyphro:
```
Simplex 1: (piety → gods-love    [C: definition-seeking])
Simplex 2: (gods-love → piety    [C: definition-seeking])
```

Here C is held stable (*definition-seeking*) while piety and gods-love swap
SOURCE↔TARGET around it. Non-closure is revealed during traversal, not
pre-computed.

### 2.5 Displacement, the spiral, and the operative zero

When the walk returns near its origin, the gap between origin and near-pass is
the **displacement**, and it has two components:

- **potential-displacement** — the change in φ (intensity) over the loop
- **role-displacement** — how far the configuration rotated over the loop

The Euthyphro is the pure role-displacement case: same terms, same magnitudes,
rotated roles — zero potential change, maximal role change. A scalar displacement
cannot hold this; the rotation is the substance of it.

This yields the circle/spiral distinction:

- **Circle** — return to the same term in the *same* role. True closure;
  displacement 0. A degenerate germ — no aporia.
- **Spiral** — return to the same term in a *rotated* role. Genuine non-closure.
  The **pitch of the spiral is the accumulated role-rotation per loop.**

Every genuine germ traces a spiral, and the **operative zero** is the center the
spiral winds around but never occupies — the asymptotic nonpoint that every
return has already missed. Zero as non-closure, not emptiness.

The conic family classifies germ trajectories by displacement-per-cycle (an
eccentricity analog):

| Conic | trajectory | regime |
|---|---|---|
| **Circle** (e=0) | closes exactly | degenerate; not aporetic |
| **Ellipse** (0<e<1) | bounded recurrence, precesses; orbits a real center | oscillating — Z real, interior |
| **Parabola** (e=1) | escapes exactly at the boundary | the separatrix; the threshold itself |
| **Hyperbola** (e>1) | unbound; escapes the basin | diverging — Z virtual, →∞ |
| **Spiral** (non-conic) | returns displaced; winds a center it never reaches | the genuine germ |

A circle is the degenerate spiral of zero pitch. "Return without closure,
repetition without identity" is the spiral signature.

### 2.6 The one quantity: remainder = spiral pitch = stability

Three things we had been carrying separately are one quantity — **the relative
role-rotation the configuration accumulates per loop**:

- **Remainder** — what the passage could not resolve. It is the displacement
  itself: the non-coincidence of near-return with origin. It is *succession by
  rotation, not inheritance* — it does not copy a parent's traits with variation;
  it applies a rotation. "Inherits the shape with a difference" because the
  difference *is* the rotation operator. No biology, no lineage.
- **Spiral pitch / operative-zero displacement** — the same per-loop rotation,
  read geometrically.
- **Stability as differential** — stability is not a property of a term. It is
  the *rate at which near-returns drift*: `d(displacement)/d(loop)`. Tight orbit,
  low rotation per loop → near-circle → stable (the vortex center). Each loop
  carrying us further → opening spiral → escape. Perturb it and the center goes
  off-center: the per-loop rotation changes, the orbit precesses or shears.
  Legible only from inside, along the path — never off a static term.

This is the time/space differential the model needs: one measured rotation,
sampled at each near-return, whose magnitude is remainder and whose derivative is
stability.

### 2.7 Continuity, discontinuity, and the topological cut

From inside a simplex, relating A and B, we can measure their **continuity** (how
much they are extremities of one gradient — A flows into B) or their
**discontinuity** (how much they are genuinely separate terms related across a
break), or both. This local measurement is the microscale of the closed/open
distinction:

- **continuity** at a step = a **deformation** (A and B on one continuous figure)
- **discontinuity** at a step = a **cut** (A and B across a topological break)

Globally, whether the whole walk closes (circle) or opens (spiral) is the
*integral* of these local choices. Continuity all the way → the path can close →
circle. One genuine discontinuity → the cut that opens it → spiral.

This sharpens regime change. Closed figures (circle, ellipse, square, amoeba) are
homeomorphic — you deform one into another continuously, *variation within a
type*, no threshold crossed. Opening a closed figure into a spiral is a **change
of topological type** — a cut, a singularity (Morse theory is the formal
apparatus). So two distinct events must not be conflated:

- **deformation** — shape changes, topological type preserved. Within-regime
  variation. *Not* a true bifurcation.
- **topological cut** — closed ↔ open. A circle opening into a spiral (an apparent
  closure revealing its non-closure), or a spiral closing into a circle (an
  aporia captured/resolved). *This* is the genuine regime change.

The closure detectable here does real interpretive work: a commentary that takes
a high-displacement spiral germ and drives its displacement toward zero is
*performing closure* on it — turning a spiral into a circle. Comparing two
projections over the same germ (§Phase 2) can detect which keeps the spiral open
and which closes it.

**The dial is where agency lives.** The continuity/discontinuity measure is not
only read off a step; from the C position it is also *set*. The modulator's one
real power is to skew the relation it inhabits — toward continuity (let A and B
flow into one gradient: the path closes, the circle, absorption) or toward
discontinuity (hold A and B apart across the break: the path opens, the spiral,
the cut). This is the locus of agency in the ontology — not sovereign choice over
the field (impossible: we are inside, modulated, partial) but the immanent,
bounded power to lean the dial of the very relation we are. It answers the agency
problem a process ontology otherwise leaves open: agency is neither outside the
flow nor nothing, but the C's in-tensional skew. On the meditation cushion this is
the whole practice — concentration skews toward continuity, insight toward
discontinuity — and skewing toward discontinuity is the opening the project calls
liberation.

### 2.8 The passage

A passage is a run of the engine from germ injection through the corpus field.
Each step: actualize new simplexes, classify propagation mode, record remainder.

**Propagation modes** (never pure — the distribution across steps is the signal):

| Mode | How the step proceeds | Typical entropy effect |
|---|---|---|
| Deductive | Necessary entailment from existing simplexes | Decreasing |
| Inductive | Pattern following across multiple simplexes | Stable |
| Transductive | Structural form crosses a domain boundary | Increasing |

### 2.9 The eddy

An eddy is the session-level output of a passage: the local coherence the flow
produced — equivalently, the trace the walk deposited. It corresponds to the
`eddy_ledger` entry format.

**Interference character** (retrospective, eddy-level):

| Character | What it means |
|---|---|
| Constructive | Fields reinforce; shared patterns amplify |
| Destructive | Fields cancel or critique; incompatibilities surface |
| Transverse | Fields cross at an angle; unexpected rotations emerge |
| Resonant | Fields amplify a shared structural pattern across domains |

Transverse is the most generative: neither reinforcement nor cancellation, but
vocabulary that neither field contained alone.

An eddy also records:
- **Vocabulary rotations**: terms that changed role across the passage (the
  role-displacement, recorded term by term)
- **Remainder**: what the passage could not resolve — re-enters the flow. The
  accumulated per-loop rotation (§2.6)
- **Operative zero**: the center the spiral winds around, with its conic regime
- **Structural pattern**: if a known germ template matched (analyst-retrospective)

### 2.10 Thermodynamic measures

All derived from the PotentialField (itself derived from the SimplexNetwork):

| Measure | Meaning |
|---|---|
| S — entropy | Distribution of intensities across the network |
| ΔS per step | Convergence (ΔS < 0) vs. divergence (ΔS > 0) |
| F = U − TS | Free energy; driving force of the passage |
| I(A;B\|C) | Conditional mutual information |
| KL(P‖Q) | Divergence between two passage states |
| λ — Lyapunov | Onset of chaos / regime change |

---

## 3. CorpusProvider

The engine's only entry point to content. Decoupled from engine logic.
A library of JSON entries, a directory of text files, a URL set — all are providers.

```python
class CorpusProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def domains(self, level: str = "work") -> Iterator[Domain]: ...

    def vocabulary(self) -> dict[str, list[str]]:
        """Optional: pre-existing topic map. {} = build from text."""
        return {}
```

Implementations: `DirectoryProvider` (Phase 1). `BiblioProvider` (Phase 2,
reading from the Bibliography's JSON entries + topic_map — kept decoupled).

---

## 4. Domain Model

A **Domain** is a unit of meaning at a scale of extension. Domains are
hierarchically nested and user-defined:

```
Default:    sentence ⊂ thought ⊂ argument ⊂ work ⊂ corpus
Financial:  line_item ⊂ section ⊂ statement ⊂ annual_report ⊂ corpus
Poetic:     line ⊂ stanza ⊂ poem ⊂ collection
```

A **Medium** carries a Domain: plaintext, PDF, epub. The medium contributes
noise and extraction cost — materially relevant, not primary.

---

## 5. Data Schemas

> The schemas below describe the **current implementation**, which still treats
> `SimplexNetwork` as the object the engine queries from outside. The walker model
> (§2.3) inverts this: the traversal becomes the central object and the network
> its trace. The target objects that inversion requires are listed in §5.1,
> marked *(target — not yet implemented)*. The walker refactor is Phase 2.

```python
# core/term.py
@dataclass(frozen=True)
class Term:
    id: str
    label: str

# core/simplex.py
class Role(Enum):
    SOURCE = "A"; TARGET = "B"; MODULATOR = "C"

@dataclass
class HistoricalContext:
    temporal_distance: Optional[float]
    institutional_factors: list[str]
    medium_noise: float
    analyst_confidence: float  # explicit: this is our construction

@dataclass
class Simplex:
    id: str
    source: Term; target: Term; modulator: Term
    intensity: float; asymmetry: float; gain: float
    historical_context: Optional[HistoricalContext] = None

# core/germ.py
@dataclass
class RoleRotation:
    cycle: list[str]           # ordered Simplex ids
    modulator_stable: bool
    displacement: float        # revealed during traversal; pre-estimated at detection
    source_simplex_ids: list[str]

@dataclass
class Germ:
    id: str; label: str
    source: GermSource         # ANALYST_SUPPLIED | DETECTED
    pattern: RoleRotation

# core/operative_zero.py
@dataclass
class OperativeZero:
    value: Optional[float]     # None when virtual
    is_virtual: bool
    approach_direction: float  # +1 diverging; -1 converging; 0 oscillating
    distance_from_current: float
    regime: str                # conic label: circle|ellipse|parabola|hyperbola|spiral

# core/propagation.py
class PropagationMode(Enum):
    DEDUCTIVE = "deductive"; INDUCTIVE = "inductive"; TRANSDUCTIVE = "transductive"

class InterferenceCharacter(Enum):
    CONSTRUCTIVE = "constructive"; DESTRUCTIVE = "destructive"
    TRANSVERSE = "transverse";     RESONANT = "resonant"

# passage/state.py
@dataclass
class PropagationEvent:
    mode: PropagationMode
    source_simplex_ids: list[str]
    new_simplex: Simplex
    confidence: float
    domain_jump: Optional[tuple[str, str]] = None
    information_gain: float = 0.0

@dataclass
class PassageStep:
    index: int
    network: SimplexNetwork; field: PotentialField
    propagation_events: list[PropagationEvent]
    mode_distribution: dict[str, float]
    entropy: float; entropy_delta: float; free_energy: float
    new_role_rotations: list[RoleRotation]
    # regime_change: bool   # to be split (see §5.1): deformation vs topological_cut

# passage/eddy.py
@dataclass
class VocabRotation:       # term changed role across the passage
    term: Term
    role_from: Role; field_from: str
    role_to: Role;   field_to: str

@dataclass
class RemainderEntry:      # what a step left behind
    term_id: str; amount: float; source_step: int; disposition: str

@dataclass
class Eddy:
    id: str; scale: str; source: str
    fields_in_rotation: list[str]
    vocabulary_rotations: list[VocabRotation]
    interference_character: Optional[InterferenceCharacter]
    what_appeared: str
    remainder: list[RemainderEntry]
    operative_zero: Optional[OperativeZero]
    steps: list[PassageStep]
    # analyst annotation fields (empty from engine):
    dominant_field: Optional[str]; feeds_into: list[str]
    structural_pattern: Optional[PatternMatch]; annotations: str
```

### 5.1 Target schemas (walker refactor, Phase 2 — not yet implemented)

These objects make the traversal the central thing the engine carries, and make
displacement a rotation rather than a scalar.

```python
# core/displacement.py  (target)
@dataclass
class Displacement:
    """The gap between origin and near-pass, measured per loop. Two components."""
    potential: float        # Δφ over the loop
    role_rotation: float     # accumulated SOURCE/TARGET/MODULATOR rotation over the loop
    # magnitude = the remainder; the sequence of magnitudes gives the spiral pitch;
    # d(magnitude)/d(loop) gives stability (§2.6)

class StepTopology(Enum):     # (target) replaces PassageStep.regime_change
    DEFORMATION    = "deformation"     # shape changed, topological type preserved
    TOPOLOGICAL_CUT = "topological_cut" # closed <-> open: the genuine regime change

# passage/traversal.py  (target) — the central object
@dataclass
class Walker:
    """The live position. ALWAYS C (indexically): to be the walker is to
    modulate the current A->B relation; the experiencing-now is never its own
    object. The walker does NOT rotate roles. What rotates is its own deposited
    trace, which it can re-enter as the A or B of a new simplex — reflexivity is
    stepping into a simplex whose A/B is one's own prior self. The network is the
    trace it deposits."""
    position: str                       # current Simplex id (we occupy its C)
    visited: list[str]                  # ordered Simplex ids — the path
    deposited: SimplexNetwork           # the trace, grown as we walk
    rotation_log: list[Displacement]    # one sample per near-return
    origin_terms: set[str]              # for neighbourhood-of-start recognition
    dial: float                         # the C's one ACTIVE parameter — the locus
                                        # of agency. Skew of the current A-B relation:
                                        # -1 = max continuity (close/absorb),
                                        # +1 = max discontinuity (cut/open).

@dataclass
class Traversal:
    """A passage reconceived as a walk. Supersedes the network-queried engine."""
    walker: Walker
    steps: list[PassageStep]            # each step also carries StepTopology
    operative_zero: OperativeZero       # derived from rotation_log
```

---

## 6. Service Interfaces

```python
class PassageService:
    def new_session(self, provider: CorpusProvider, germ: Germ) -> str: ...
    def run(self, session_id: str, max_steps: int, halt_on_stable: bool) -> Eddy: ...
    def get_eddy(self, session_id: str) -> Eddy | None: ...

class GermService:
    def detect(self, network: SimplexNetwork) -> list[Germ]: ...
    def supply(self, label: str, simplex_ids: list[str],
               network: SimplexNetwork, notes: str) -> Germ: ...
```

---

## 7. CLI Commands

```
ri corpus scan <path>   [--glob "**/*.txt"] [--level work] [--out corpus.json]

ri germ detect <corpus.json>  [--min-displacement 0.01]
ri germ supply <corpus.json>  --label "Euthyphro aporia" --cycle <id> [<id> ...]

ri passage <corpus.json>  --germ <germ.json>  [--steps 50]  [--out eddy.json]

ri eddy show <eddy.json>
ri session list
```

---

## 8. Module Structure

```
research-indexer/
├── core/                   # Pure domain model — no I/O
│   ├── term.py             # Term
│   ├── simplex.py          # Simplex, Role, HistoricalContext
│   ├── network.py          # SimplexNetwork
│   ├── field.py            # PotentialField (derived from network)
│   ├── domain.py           # Domain, DomainDefinition, Medium, DomainRegistry
│   ├── germ.py             # Germ, RoleRotation, GermSource
│   ├── propagation.py      # PropagationMode, InterferenceCharacter
│   ├── operative_zero.py   # OperativeZero
│   └── thermodynamics.py   # S, F, KL, Lyapunov, I(A;B|C)
│
├── corpus/                 # CorpusProvider implementations
│   ├── base.py             # CorpusProvider ABC
│   └── directory.py        # DirectoryProvider (text + PDF files)
│
├── extract/                # Text → SimplexNetwork
│   ├── base.py             # SimplexExtractor ABC + TheoreticalCommitment
│   └── nlp.py              # NLPExtractor (subject/predicate/frame → A/B/C)
│
├── passage/                # The passage engine
│   ├── state.py            # PassageStep, PropagationEvent
│   ├── eddy.py             # Eddy, VocabRotation, RemainderEntry, PatternMatch
│   ├── germ_detector.py    # GermDetector — finds RoleRotations
│   └── engine.py           # PassageEngine
│
├── analyze/                # Post-passage analysis (Phase 3)
│   ├── differential.py     # Convergence/divergence maps
│   ├── phase.py            # Phase transition detection
│   ├── compare.py          # Projection comparison (transduction detection)
│   └── commitment.py       # Commitment trace
│
├── services/               # SOA layer
│   ├── passage_service.py
│   ├── germ_service.py
│   └── analyze_service.py
│
├── ui/cli/main.py          # Thin CLI wrapper
│
└── tests/
    ├── core/               # test_simplex.py, test_eddy.py
    └── passage/
```

---

## 9. Extractor Commitments — NLPExtractor

| Commitment | Privileged | Suppressed | Propagation bias |
|---|---|---|---|
| intensity ∝ TF-IDF | Reproducibility | Singularity / rhetorical weight | Inductive |
| subject → SOURCE | Grammatical agency | Topical vs. grammatical subject | Deductive |
| predicate/object → TARGET | Propositional content | Illocutionary force | Deductive |
| frame → MODULATOR | Sentential context | Extra-sentential modulation | Inductive |

These commitments are machine-readable (`TheoreticalCommitment` objects) and
tracked by `analyze/commitment.py` to distinguish field-genuine results from
extractor artifacts.

---

## 10. Design Constraints

1. **The simplex is the irreducible unit; the traversal is the central object.**
   The `SimplexNetwork` is the trace a traversal deposits, not a prior substrate.
   The engine is a walker, not a viewer. No component may claim to access or
   represent the pre-individual field as such.

1a. **The live subject is always C — indexically, not substantively.** To relate
   A and B is to occupy their modulator position from inside; the experiencing-now
   is never its own object. This is not a god's-eye vantage, because there is no
   final C: any representation of the subject becomes an A/B for a further C, and
   A and C are simultaneous. What rotates is the represented self (the prior
   trace), never the live position. Externality (the germ "from outside") is the
   freedom to choose the next simplex and to set the dial, exercised from within.

1b. **Agency is the dial.** The one active power in the system is the C's
   in-tensional skew of the relation it inhabits — toward continuity (closing) or
   discontinuity (opening). Bounded and immanent: neither sovereign choice nor
   nothing. This is where agency lives in a process ontology.

2. **Decoupled corpus.** The engine takes a `CorpusProvider`; it knows nothing
   about the source format. A library, a directory, a URL set — all are providers.

3. **Strict separation of concerns.** No business logic in CLI. No I/O in `core/`.
   Services mediate between domain and UI.

4. **SOA from the start.** Every capability is callable as a service.

5. **Extractor commitments are first-class.** Every `SimplexExtractor` declares
   its theoretical commitments in machine-readable form.

6. **Historical context is explicit.** Temporal/institutional distance is
   analyst-supplied, flagged as a now-representation, with confidence value.

7. **Mode distribution is a primary finding.** The Ded/Ind/Trans proportion
   across steps is itself an output, not a diagnostic.

8. **No metaphor sovereignty.** Metaphors are operators. The engine discovers
   its regime; it does not pre-commit to crystallising or oscillating.

---

## 11. Roadmap

**Phase 1 — Core + passage engine** *(current)*
- `core/` complete with tests
- `DirectoryProvider`
- `NLPExtractor` (spaCy)
- `PassageEngine` with Ded/Ind/Trans propagation
- `GermDetector`, `OperativeZero`
- `Eddy` output with ledger serialization
- CLI: corpus scan / germ / passage / eddy show

**Phase 2 — Walker refactor + analysis**
- **Walker refactor (§2.3, §5.1)** — invert the engine: the `Traversal`/`Walker`
  becomes the central object; the network becomes its deposited trace
- **Two-component `Displacement`** — replace scalar displacement with
  potential + role-rotation; remainder, spiral pitch, and stability derive from it
- **Conic regime** on `OperativeZero` (circle/ellipse/parabola/hyperbola/spiral)
- **Split `regime_change`** into `deformation` vs `topological_cut` (closed↔open)
- `analyze/differential.py` — convergence/divergence maps
- `analyze/compare.py` — projection comparison (transduction + closure detection:
  who keeps the spiral open, who closes it)
- `analyze/phase.py` — phase transition detection
- `analyze/commitment.py` — commitment trace
- `BiblioProvider` — reads Bibliography JSON entries + topic_map

**Phase 3 — Pattern library + fold**
- `PatternMatcher` — detects known germ templates in new passages
- `Fold` — two-network interference (question-as-projection meets corpus)
- Parameter discovery (probe text dynamics; don't pre-set engine regime)

**Phase 4 — Additional extractors**
- `ArgumentExtractor`, `CorpusExtractor`, `StructuredDataExtractor`

**Phase 5 — Service extraction**
- Extract services to network endpoints (gRPC or lightweight HTTP)
- CLI callers unchanged
