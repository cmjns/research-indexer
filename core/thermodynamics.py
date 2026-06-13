"""
Thermodynamic and information-theoretic measures over PotentialFields
and SimplexNetworks.

All measures are derived — they operate on already-individuated structures.
Temperature T is a parameter governing how aggressively the field crystallizes:
high T = diffuse, exploratory; low T = concentrated, conservative.
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.field import PotentialField
    from core.network import SimplexNetwork


def entropy(field: "PotentialField") -> float:
    """
    Shannon entropy of the potential distribution.
    S = -∑ p(φ) log p(φ)

    High entropy: potentials evenly distributed — diffuse, pre-individual.
    Low entropy: potentials concentrated — individuated, crystallized.
    """
    total = field.total()
    if total == 0.0:
        return 0.0
    probs = [v / total for v in field.potentials.values() if v > 0]
    return -sum(p * math.log(p) for p in probs)


def free_energy(field: "PotentialField", temperature: float = 1.0) -> float:
    """
    F = U - TS
    U = total potential (internal energy)
    S = field entropy
    T = crystallization temperature (analyst parameter)

    Decreasing F drives crystallization.
    """
    u = field.total()
    s = entropy(field)
    return u - temperature * s


def kl_divergence(field_p: "PotentialField",
                  field_q: "PotentialField") -> float:
    """
    KL(P ‖ Q) — divergence between two potential fields.
    Measures how much field_p has individuated away from field_q.

    Returns float('inf') if Q has zero mass where P has nonzero mass.
    """
    total_p = field_p.total()
    total_q = field_q.total()
    if total_p == 0.0:
        return 0.0

    result = 0.0
    for term_id, phi_p in field_p.potentials.items():
        p = phi_p / total_p
        phi_q = field_q.potentials.get(term_id, 0.0)
        q = phi_q / total_q if total_q > 0 else 0.0
        if p > 0:
            if q == 0:
                return float("inf")
            result += p * math.log(p / q)
    return result


def mutual_information_given_c(
    network: "SimplexNetwork",
    source_id: str,
    target_id: str,
    modulator_id: str,
) -> float:
    """
    I(A; B | C) — mutual information between source and target
    terms given modulator, approximated from simplex intensities.

    Counts simplexes where source=A, target=B, modulator=C and
    measures the information contributed by their co-occurrence.

    This is an approximation — a full probabilistic model requires
    a richer statistical treatment at Phase 2.
    """
    abc_count = 0
    ac_count = 0
    bc_count = 0
    c_count = 0
    total = len(network.simplexes)

    if total == 0:
        return 0.0

    for s in network.simplexes.values():
        has_a = s.source.id == source_id
        has_b = s.target.id == target_id
        has_c = s.modulator.id == modulator_id

        if has_c:
            c_count += 1
        if has_a and has_c:
            ac_count += 1
        if has_b and has_c:
            bc_count += 1
        if has_a and has_b and has_c:
            abc_count += 1

    if c_count == 0 or ac_count == 0 or bc_count == 0:
        return 0.0

    p_abc = abc_count / total
    p_ac  = ac_count  / total
    p_bc  = bc_count  / total
    p_c   = c_count   / total

    if p_abc == 0:
        return 0.0

    return p_abc * math.log((p_abc * p_c) / (p_ac * p_bc))


def lyapunov_estimate(entropy_series: list[float]) -> float:
    """
    Local Lyapunov exponent estimated from entropy trajectory.
    λ > 0: diverging (chaotic, sensitive); λ < 0: converging (stable).

    Computed as the average log-ratio of successive entropy deltas.
    Requires at least 3 data points.
    """
    if len(entropy_series) < 3:
        return 0.0

    deltas = [abs(entropy_series[i + 1] - entropy_series[i])
              for i in range(len(entropy_series) - 1)]

    log_ratios = []
    for i in range(len(deltas) - 1):
        if deltas[i] > 0 and deltas[i + 1] > 0:
            log_ratios.append(math.log(deltas[i + 1] / deltas[i]))

    return sum(log_ratios) / len(log_ratios) if log_ratios else 0.0
