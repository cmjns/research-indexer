"""
SimplexExtractor ABC.

An extractor parses a Domain into a SimplexNetwork — it continues an
individuation already underway in the text. Every extractor makes
theoretical commitments that shape what becomes visible in the network.
These commitments are declared formally and tracked by the analysis layer.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from core.domain import Domain
from core.network import SimplexNetwork
from crystallize.state import PropagationMode


@dataclass
class TheoreticalCommitment:
    """
    A machine-readable declaration of what an extractor assumes.

    privileged_dimension : what this commitment makes salient
    suppressed_dimension : what this commitment renders latent
    propagation_bias     : which crystallization mode this tends to favour
    """
    name: str
    formal_expression: str
    privileged_dimension: str
    suppressed_dimension: str
    propagation_bias: PropagationMode


class SimplexExtractor(ABC):
    """
    Parses a Domain into a SimplexNetwork.

    The text is already individuated — already moving. The extractor
    continues the movement; it does not start from zero or map a
    pre-individual field.

    All extractors must declare their theoretical commitments. These
    are used by AnalyzeService.commitment_trace() to attribute features
    of the crystallization to extractor assumptions vs. field properties.
    """

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def commitments(self) -> list[TheoreticalCommitment]: ...

    @abstractmethod
    def extract(self, domain: Domain) -> SimplexNetwork: ...
