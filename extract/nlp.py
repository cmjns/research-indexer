"""
NLPExtractor — the default first implementation.

Maps syntactic structure to simplex roles:
    subject            → A (source)
    main predicate/obj → B (target)
    subordinate/frame  → C (modulator)

Theoretical commitments:
    - intensity ∝ syntactic salience (TF-IDF weighted)
    - grammatical subject → SOURCE  (privileges grammatical agency)
    - predicative content → TARGET  (privileges propositional content)
    - sentential frame    → MODULATOR (privileges local context)

What is suppressed: rhetorical structure, prosodic weight, illocutionary
force, extra-sentential modulation, argument-level structure.

Propagation bias: predominantly INDUCTIVE (syntax is pattern-governed)
with DEDUCTIVE moments at the sentence level.

Requires: spaCy with a language model installed.
    pip install spacy
    python -m spacy download en_core_web_sm
"""
from __future__ import annotations

import uuid
from collections import Counter

from core.domain import Domain
from core.network import SimplexNetwork
from core.simplex import Simplex, Role
from core.term import Term
from crystallize.state import PropagationMode
from extract.base import SimplexExtractor, TheoreticalCommitment


class NLPExtractor(SimplexExtractor):

    COMMITMENTS: list[TheoreticalCommitment] = [
        TheoreticalCommitment(
            name="intensity_as_frequency",
            formal_expression="φ(t) ∝ TF-IDF(t)",
            privileged_dimension="reproducibility / statistical salience",
            suppressed_dimension="singularity / rhetorical weight",
            propagation_bias=PropagationMode.INDUCTIVE,
        ),
        TheoreticalCommitment(
            name="subject_as_source",
            formal_expression="nsubj(token) → Role.SOURCE",
            privileged_dimension="grammatical agency",
            suppressed_dimension="topical vs. grammatical subject distinction",
            propagation_bias=PropagationMode.DEDUCTIVE,
        ),
        TheoreticalCommitment(
            name="predicate_as_target",
            formal_expression="ROOT/dobj(token) → Role.TARGET",
            privileged_dimension="predicative / propositional content",
            suppressed_dimension="performative / illocutionary force",
            propagation_bias=PropagationMode.DEDUCTIVE,
        ),
        TheoreticalCommitment(
            name="frame_as_modulator",
            formal_expression="advcl/mark/prep(token) → Role.MODULATOR",
            privileged_dimension="sentential context",
            suppressed_dimension="extra-sentential / inter-textual modulation",
            propagation_bias=PropagationMode.INDUCTIVE,
        ),
    ]

    def __init__(self, model: str = "en_core_web_sm") -> None:
        try:
            import spacy
            self._nlp = spacy.load(model)
        except ImportError:
            raise ImportError(
                "spaCy is required for NLPExtractor. "
                "Install: pip install spacy && python -m spacy download en_core_web_sm"
            )
        except OSError:
            raise OSError(
                f"spaCy model {model!r} not found. "
                f"Install: python -m spacy download {model}"
            )

    @property
    def name(self) -> str:
        return "nlp"

    @property
    def commitments(self) -> list[TheoreticalCommitment]:
        return self.COMMITMENTS

    def extract(self, domain: Domain) -> SimplexNetwork:
        doc = self._nlp(domain.content)
        term_freq = self._term_frequencies(doc)
        network = SimplexNetwork()

        for sent in doc.sents:
            simplex = self._extract_simplex(sent, term_freq, domain.id)
            if simplex is not None:
                network.add(simplex)

        return network

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _term_frequencies(self, doc) -> Counter:
        """TF-IDF approximation: raw lemma frequency over the document."""
        return Counter(
            token.lemma_.lower()
            for token in doc
            if not token.is_stop and not token.is_punct and token.is_alpha
        )

    def _extract_simplex(self, sent, term_freq: Counter, domain_id: str):
        """
        Extract one simplex from a sentence.

        A  (source)   : grammatical subject (nsubj)
        B  (target)   : root verb + direct object, or root noun
        C  (modulator): adverbial clause, prepositional phrase, or frame

        Falls back to pronoun subjects, existential constructions, etc.
        Returns None if no viable (A, B, C) triple can be found.
        """
        source_token = None
        target_token = None
        modulator_token = None

        root = [t for t in sent if t.dep_ == "ROOT"]
        if not root:
            return None
        root = root[0]

        for token in sent:
            if token.dep_ in ("nsubj", "nsubjpass") and token.head == root:
                source_token = token
            elif token.dep_ in ("dobj", "attr", "acomp") and token.head == root:
                target_token = token
            elif token.dep_ in ("advcl", "prep", "mark", "advmod") and modulator_token is None:
                modulator_token = token

        # fallback: use root as target if no object found
        if source_token is None or (target_token is None and root.pos_ not in ("VERB", "AUX")):
            return None

        if target_token is None:
            target_token = root

        if modulator_token is None:
            # use the document/domain as a null modulator
            modulator_token = root  # degenerate: modulator = predicate

        def make_term(token) -> Term:
            lemma = token.lemma_.lower()
            return Term(id=f"{domain_id}::{lemma}", label=lemma)

        source   = make_term(source_token)
        target   = make_term(target_token)
        modulator = make_term(modulator_token)

        # intensity: average TF of source and target lemmas
        total = sum(term_freq.values()) or 1
        phi_a = term_freq[source.label] / total
        phi_b = term_freq[target.label] / total
        intensity = (phi_a + phi_b) / 2.0

        # asymmetry: difference in salience between source and target
        asymmetry = max(-1.0, min(1.0, phi_a - phi_b))

        # gain: salience of modulator
        gain = term_freq[modulator.label] / total

        return Simplex(
            id=str(uuid.uuid4()),
            source=source,
            target=target,
            modulator=modulator,
            intensity=intensity,
            asymmetry=asymmetry,
            gain=gain,
        )
