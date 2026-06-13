# research-indexer — Specification

> Version: 0.1 (initial)  
> Status: Working draft

---

## 1. Purpose

A modular, content-agnostic individuation machine for exploring texts. A text is not
treated as a fixed structure of meaning but as a field of already-moving individuations.
We do not start from zero: we start with simplexes already underway in the text, and
we extend them.

The system supplies a germ — a role rotation in the simplex network, an aporia, a
non-closing movement — and iteratively crystallizes a projection from it, tracking where
differentials converge, diverge, approach limits, or undergo regime change.

**Philosophical grounding**: Simondon (individuation, metastability, transduction),
Serres (the parasite, the triode, noise-as-signal), Deleuze (difference, intensity,
the virtual), Nagarjuna (prasanga, the MMK as field of potentials).

**Mathematical grounding**: thermodynamics, information theory, complexity/chaos theory.

**Epistemic honesty**: this machine runs now, in our historical moment, processing
now-representations of texts. When we model "historical distance" between Nagarjuna
and Candrakīrti, we are constructing a modulating representation — not accessing the
past itself. This construction enters the system explicitly, as metadata on the C-term
of cross-domain simplexes, with analyst-supplied confidence.

---

## 2. Core Model

### 2.1 The Primitive: The Modulated 3-Simplex

The irreducible unit is the **asymmetric, modulated 3-simplex**, after Serres's
triode / parasite model:

```
A ──[C]──► B
```

- **A** (source/emitter): the term from which signification flows
- **B** (target/receiver): the term individuated by the relation
- **C** (modulator): the relation-to-the-relation; modulates gain and direction of A→B
  without being consumed by it
- **Asymmetry**: A→B ≠ B→A; the relation is directional and locally irreversible
- **Role mobility**: any term may be A in one simplex, C in an adjacent simplex;
  roles are local, not essential properties of terms

A simplex carries:
- `intensity`: magnitude of the A→B relation under modulation C
- `asymmetry`: deviation from symmetry in the A↔B exchange; [-1, 1]
- `gain`: degree to which C amplifies or attenuates A→B

### 2.2 We Start Already Moving

The pre-individual cannot be individuated symbolically. Any asymmetric intensity we
can represent is already a simplex. We do not model a prior substrate; we do not
attempt to represent the pre-individual field as such.

The **SimplexNetwork is the primitive**. When we ingest a text, we are not mapping
a pre-individual field — we are extracting already-individuated simplexes from
already-moving language. The ingestion process continues a movement the text has
already begun.

The **PotentialField** is derived from the SimplexNetwork: a scalar projection useful
for thermodynamic measures. It is not prior to the network; it is computed from it.

```
φ(term) = f(intensities of all simplexes in which term participates, weighted by role)
```

### 2.3 The Aporia as Role Rotation

An aporia is not a special entity. It is a **role rotation** in the simplex network:
a cycle in which A and B swap roles under the same or related modulator C, and in
which the return is displaced from the origin.

The Euthyphro:
```
Simplex 1: (piety → gods-love    [C: definition-seeking])
Simplex 2: (gods-love → piety    [C: definition-seeking])
```

Same terms, same modulator, A and B swapped. The cycle appears to close but does not:
the `piety` at the end of the traversal is not the same as at the start — its potential
has been displaced. The loop reveals non-closure *during traversal*, not in advance.

**Necessary condition for germiness**: displacement > 0 after completing the cycle.
This is revealed by the going, not pre-computed.

### 2.4 The Germ

A germ is a detected or analyst-supplied role rotation (aporia) used to initiate
crystallization. It is modeled as a **process** — a traversal operator — not as a
static structure.

The germ is only actualized when enacted on a specific network. The analyst's act
of selection or supply is what is "outside" in Simondon's sense: the externality
is preserved in the recognition, not in the structure.

### 2.5 Crystallization

From the germ, crystallization extends the SimplexNetwork:

1. Inject germ into network at the selected RoleRotation site
2. Each step: actualize new simplexes adjacent to the germ's traversal
3. Classify each propagation event as Deductive / Inductive / Transductive
4. Record the CrystallizationStep: projection state, mode distribution, entropy delta
5. Derive PotentialField from updated network
6. Detect: convergence / divergence / threshold crossing / regime change
7. Iterate until halt condition

**Propagation modes** (never pure — the distribution is the signal):
- **Deductive**: necessary entailment from existing simplexes; conservative; no new
  information; tends toward closure
- **Inductive**: pattern following across multiple simplexes; generalizing; mild
  compression; risks premature closure into a "law"
- **Transductive**: structural form propagates across a domain boundary; lateral;
  genuinely new information; risks instability without inductive support

A shift in mode distribution across steps is itself a signal:
- Predominantly deductive → converging; approaching stability
- Predominantly transductive → generative; domain-jumping; regime change building
- Abrupt shift deductive → transductive: bifurcation event

### 2.6 Thermodynamic Measures

All derived from the PotentialField and PropagationEvents:

| Measure | Meaning |
|---|---|
| S — field entropy | Distribution of φ across the network |
| ΔS — entropy delta per step | Convergence (ΔS < 0) vs. divergence (ΔS > 0) |
| F = U − TS — free energy | Driving force of crystallization |
| I(A;B\|C) — conditional mutual information | Information shared between A and B given C |
| KL(P‖Q) — projection divergence | Distance between two crystallization states |
| λ — local Lyapunov exponent | Sensitivity; onset of chaos / regime change |

### 2.7 Historical Context as Now-Representation

When relating texts separated in time (e.g. MMK and Candrakīrti's Prasannapadā),
temporal/institutional distance is modeled as C-term metadata on cross-domain simplexes.
This is our now-representation of distance — a modulating construction we supply as
analysts, acknowledged as such, not a direct model of the past.

```
Simplex: (MMK → Prasannapadā [C: HistoricalContext{
    temporal_distance: 700yrs,
    institutional_factors: ["Prasangika formation", "Sanskrit→Tibetan translation"],
    medium_noise: 0.3,
    analyst_confidence: 0.6
}])
```

Transductive relations across projections (e.g. what Candrakīrti's crystallization
owes to MMK's structure) are detected by comparing projections, not annotated manually.

---

## 3. Domain Model

A **Domain** is a unit of meaning at a given scale of extension. Domains are
hierarchically nested and user-defined. The system ships with defaults but all levels
are replaceable.

```
Default:    sentence ⊂ thought ⊂ argument ⊂ work ⊂ corpus
Financial:  line_item ⊂ section ⊂ statement ⊂ annual_report ⊂ corpus
Poetic:     line ⊂ stanza ⊂ poem ⊂ collection
```

A **DomainDefinition** specifies a named level and how to segment a parent domain
into instances of this level. Segmentation is theoretically motivated — NLP sentence
boundary detection is the default first implementation, with the explicit commitment
that it privileges surface syntactic structure.

A **Medium** is the carrier of a Domain. It is separate from the domain it carries
and contributes noise and velocity to the modulation. A handwritten manuscript and
a PDF of the same text are not equivalent. Medium is relevant but not primary.

---

## 4. Data Schemas

```python
# core/term.py
@dataclass
class Term:
    id: str
    label: str
    # no potential stored on Term; φ is derived from the network

# core/simplex.py
class Role(Enum):
    SOURCE    = "A"
    TARGET    = "B"
    MODULATOR = "C"

@dataclass
class HistoricalContext:
    """
    Our now-representation of distance between domains.
    Not an objective property of the past — a modulating construction.
    """
    temporal_distance: Optional[float]
    spatial_distance: Optional[float]
    institutional_factors: list[str]
    medium_noise: float
    analyst_confidence: float

@dataclass
class Simplex:
    id: str
    source: Term
    target: Term
    modulator: Term
    intensity: float
    asymmetry: float        # [-1, 1]
    gain: float
    historical_context: Optional[HistoricalContext]  # None for synchronic

# core/network.py
@dataclass
class SimplexNetwork:
    simplexes: dict[str, Simplex]
    # adjacency is derived: simplexes are adjacent if they share a term
    # roles of shared terms may differ across adjacent simplexes (role mobility)

# core/field.py
@dataclass
class PotentialField:
    """Derived from SimplexNetwork. Not prior to it."""
    potentials: dict[str, float]   # term_id → φ

# core/domain.py
@dataclass
class DomainDefinition:
    name: str
    level: int              # ordinal; higher = more extended
    segmenter: str          # reference to a Segmenter implementation

@dataclass
class Medium:
    format: str             # "plaintext", "pdf", "epub", ...
    velocity: float
    noise_coefficient: float
    extraction_cost: float

@dataclass
class Domain:
    id: str
    definition: DomainDefinition
    parent: Optional[str]   # Domain id
    children: list[str]     # Domain ids
    content: str
    medium: Medium

# core/germ.py
@dataclass
class RoleRotation:
    """A cycle where A and B swap roles under same/related C."""
    cycle: list[str]            # ordered Simplex ids
    modulator_stable: bool
    displacement: float         # revealed during traversal; > 0 for true aporia

class GermSource(Enum):
    ANALYST_SUPPLIED = "analyst"
    DETECTED         = "detected"

@dataclass
class Germ:
    id: str
    label: str
    source: GermSource
    pattern: RoleRotation

# crystallize/state.py
class PropagationMode(Enum):
    DEDUCTIVE    = "deductive"
    INDUCTIVE    = "inductive"
    TRANSDUCTIVE = "transductive"

@dataclass
class PropagationEvent:
    mode: PropagationMode
    source_simplex_ids: list[str]
    new_simplex: Simplex
    confidence: float
    domain_jump: Optional[tuple[str, str]]  # Domain ids; non-None only for transductive
    information_gain: float                  # KL(posterior ‖ prior)

@dataclass
class CrystallizationStep:
    index: int
    network: SimplexNetwork
    field: PotentialField           # derived from network at this step
    propagation_events: list[PropagationEvent]
    mode_distribution: dict[str, float]   # PropagationMode.value → proportion
    entropy: float
    entropy_delta: float
    free_energy: float
    new_role_rotations: list[RoleRotation]  # new aporiae that emerged this step
    regime_change: bool
```

---

## 5. Service Interfaces

```python
class DomainService:
    def register_definition(self, defn: DomainDefinition) -> None: ...
    def ingest(self, content: str, medium: Medium,
               definition: str) -> Domain: ...
    def build_hierarchy(self, root: Domain) -> list[Domain]: ...

class ExtractionService:
    """Parses a Domain into a SimplexNetwork using a named extractor."""
    def extract(self, domain: Domain, extractor: str = "nlp") -> SimplexNetwork: ...
    def commitments(self, extractor: str) -> list[dict]: ...

class GermService:
    def detect(self, network: SimplexNetwork,
               min_displacement: float = 0.1) -> list[Germ]: ...
    def supply(self, label: str, cycle: list[str],
               network: SimplexNetwork) -> Germ: ...

class CrystallizeService:
    def new_session(self, network: SimplexNetwork, germ: Germ) -> str: ...
    def step(self, session_id: str) -> CrystallizationStep: ...
    def run(self, session_id: str, max_steps: int,
            halt_on_stable: bool = True) -> list[CrystallizationStep]: ...

class AnalyzeService:
    def differential_map(self, steps: list[CrystallizationStep]) -> dict: ...
    def compare_projections(self, network_a: SimplexNetwork,
                            network_b: SimplexNetwork) -> dict: ...
    def detect_phases(self, steps: list[CrystallizationStep]) -> list[dict]: ...
    def commitment_trace(self, steps: list[CrystallizationStep],
                         commitments: list[dict]) -> dict: ...
    def report(self, steps: list[CrystallizationStep],
               format: str = "json") -> str: ...
```

---

## 6. CLI Commands

```
ri ingest <source>          --medium plaintext|pdf|epub
                            --domain sentence|thought|argument|work|corpus|<custom>
                            [--out network.json]

ri germ detect <network>    [--min-displacement 0.1]
                            [--out germs.json]

ri germ supply <network>    --label "Euthyphro aporia"
                            --cycle <simplex_id> [<simplex_id> ...]
                            [--out germ.json]

ri crystallize <network>    --germ <germ.json>
                            [--steps 100]
                            [--halt-stable]
                            [--out session.json]

ri analyze <session>        [--map]
                            [--phases]
                            [--compare <other_network.json>]
                            [--commitments <extractor>]
                            [--report json|text]

ri session list
ri session show <id>
```

---

## 7. Module Structure

```
research-indexer/
│
├── core/                   # Pure domain model — no I/O, no frameworks
│   ├── term.py
│   ├── simplex.py          # Simplex, Role, HistoricalContext
│   ├── network.py          # SimplexNetwork
│   ├── field.py            # PotentialField (derived)
│   ├── domain.py           # Domain, DomainDefinition, Medium
│   ├── germ.py             # Germ, RoleRotation, GermSource
│   └── thermodynamics.py   # S, F, KL, Lyapunov, mutual information
│
├── extract/                # Text → SimplexNetwork
│   ├── base.py             # SimplexExtractor ABC + TheoreticalCommitment
│   └── nlp.py              # NLPExtractor (subject/predicate/frame → A/B/C)
│
├── crystallize/            # Individuation engine
│   ├── engine.py           # CrystallizationEngine
│   ├── propagate.py        # Deductive / Inductive / Transductive propagators
│   ├── germ_detector.py    # GermDetector — finds RoleRotations
│   └── state.py            # CrystallizationStep, PropagationEvent, PropagationMode
│
├── analyze/                # Post-crystallization analysis
│   ├── differential.py     # Convergence/divergence maps
│   ├── phase.py            # Phase transition detection
│   ├── compare.py          # Projection comparison (transduction detection)
│   ├── commitment.py       # Commitment trace — attribution of extractor biases
│   └── report.py           # Structured output
│
├── services/               # SOA layer — one service class per domain
│   ├── domain_service.py
│   ├── extraction_service.py
│   ├── germ_service.py
│   ├── crystallize_service.py
│   └── analyze_service.py
│
├── ui/
│   └── cli/
│       └── main.py         # Thin wrapper over services; no business logic
│
└── tests/
    ├── core/
    ├── extract/
    ├── crystallize/
    └── analyze/
```

---

## 8. Theoretical Commitments — NLPExtractor

The default extractor makes the following commitments, machine-readable to the system:

| Commitment | Privileged | Suppressed | Propagation bias |
|---|---|---|---|
| intensity ∝ syntactic salience | Surface grammatical role | Rhetorical / prosodic structure | Inductive |
| subject → A | Grammatical agency | Topical vs. grammatical subject distinction | Deductive |
| main predicate/object → B | Predicative content | Performative / illocutionary force | Deductive |
| subordinate clause / frame → C | Sentential context | Extra-sentential modulation | Inductive |

These commitments are tracked through crystallization by the `commitment_trace` analysis.
Any region of convergence or divergence can be attributed — partially or wholly — to
these commitments, allowing the analyst to distinguish field-genuine results from
extractor artifacts.

---

## 9. Roadmap

**Phase 1 — Core domain + skeleton** *(start here)*
- `core/` fully implemented with tests
- `extract/nlp.py` with NLPExtractor (spaCy, basic subject/predicate/frame)
- Service stubs
- CLI skeleton

**Phase 2 — Crystallization engine**
- GermDetector (RoleRotation detection in SimplexNetwork)
- CrystallizationEngine with all three propagation modes
- Thermodynamic measures operational

**Phase 3 — Analysis**
- Differential maps
- Projection comparison (transduction detection)
- Phase transition detection
- Commitment trace
- Report generation

**Phase 4 — Additional extractors**
- ArgumentExtractor (argument-level simplexes)
- CorpusExtractor (multi-work, cross-domain)
- Structured data extractor (financial statements)

**Phase 5 — Service extraction**
- Extract services to network endpoints (gRPC or lightweight HTTP)
- CLI callers unchanged

---

## 10. Key Design Constraints

1. **The simplex is the primitive.** No system component may claim to access or
   represent the pre-individual field as such.

2. **Strict separation of concerns.** No business logic in the CLI. No I/O in `core/`.
   Services mediate between domain and UI.

3. **SOA from the start.** Every capability is callable as a service. The CLI is one
   consumer; future UIs (web, notebook) are equally valid.

4. **Extractor commitments are first-class.** Every SimplexExtractor declares its
   theoretical commitments in machine-readable form. The analysis layer uses these.

5. **Historical context is explicit.** When temporal/institutional distance modulates
   a cross-domain simplex, that context is supplied by the analyst and flagged as a
   now-representation with an explicit confidence value.

6. **Mode distribution is the signal.** The Deductive/Inductive/Transductive proportion
   across crystallization steps is itself a primary output — not a diagnostic but a
   finding.
