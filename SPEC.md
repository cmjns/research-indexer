# research-indexer — Specification

> Version: 0.2
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

We do not model the pre-individual as such. We start already moving. The
SimplexNetwork is the primitive — it is what we have when we begin.

### 2.2 The primitive: modulated 3-simplex

The irreducible unit is the asymmetric, modulated 3-simplex (Serres's triode):

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

### 2.3 The aporia as role rotation

An aporia is not a special entity. It is a **role rotation**: a cycle where A
and B swap roles under the same or related modulator, and the return is displaced
from the origin.

The Euthyphro:
```
Simplex 1: (piety → gods-love    [C: definition-seeking])
Simplex 2: (gods-love → piety    [C: definition-seeking])
```

Non-closure is revealed during traversal, not pre-computed. Displacement > 0
after completing the cycle is the necessary condition for germiness.

### 2.4 The germ and the operative zero

A **germ** is a detected or analyst-supplied role rotation used to initiate a
passage. It is a process — a traversal operator — not a static structure.
Externality is preserved in the analyst's act of selection.

Every genuine germ has an **operative zero**: the virtual fixed point the cycle
approaches asymptotically but cannot occupy because every return has already
missed it. Zero as non-closure, not emptiness.

```
Z such that φ_C(Z) = Z    [the fixed point of the potential composition around C]
```

Three regimes for Z:
- **Virtual** (diverging potentials): strong germ; constitutive non-closure
- **Real, distant** (converging): weak germ; the passage will settle
- **Oscillatory** (alternating): the germ is a pendulum around its zero

### 2.5 The passage

A passage is a run of the engine from germ injection through the corpus field.
Each step: actualize new simplexes, classify propagation mode, record remainder.

**Propagation modes** (never pure — the distribution across steps is the signal):

| Mode | How the step proceeds | Typical entropy effect |
|---|---|---|
| Deductive | Necessary entailment from existing simplexes | Decreasing |
| Inductive | Pattern following across multiple simplexes | Stable |
| Transductive | Structural form crosses a domain boundary | Increasing |

### 2.6 The eddy

An eddy is the session-level output of a passage: the local coherence the flow
produced. It corresponds to the `eddy_ledger` entry format.

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
- **Vocabulary rotations**: terms that changed role across the passage
- **Remainder**: what the passage could not resolve — re-enters the flow
- **Operative zero**: the virtual fixed point of the germ's cycle
- **Structural pattern**: if a known germ template matched (analyst-retrospective)

### 2.7 Thermodynamic measures

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
    regime_change: bool

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

1. **The simplex is the primitive.** No component may claim to access or
   represent the pre-individual field as such.

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

**Phase 2 — Analysis**
- `analyze/differential.py` — convergence/divergence maps
- `analyze/compare.py` — projection comparison (transduction detection)
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
