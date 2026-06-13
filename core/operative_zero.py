"""
OperativeZero — the virtual fixed point of a germ's cycle.

The asymptotic nonpoint that the passage approaches but cannot occupy
because every return has already missed it. Zero as non-closure, not emptiness.

Computed from the sequence of entry potentials across passage steps.
The germ is constituted by not reaching its operative zero.

Three regimes:
  Converging  → Z is real; the germ is weak; the passage will settle
  Diverging   → Z is virtual; the germ is strong; non-closure is constitutive
  Oscillating → Z is the mean; the passage is a pendulum around its zero
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class OperativeZero:
    value: Optional[float]      # None when Z is virtual (outside the current field)
    is_virtual: bool
    approach_direction: float   # +1 = moving away; -1 = moving toward; 0 = stable/oscillating
    distance_from_current: float

    @classmethod
    def compute(cls, cycle_potentials: list[float]) -> "OperativeZero":
        """
        Estimate Z from the sequence φ(entry_point) at each passage step.

        Converging sequence  → Z is real, extrapolated from geometric progression
        Oscillating sequence → Z is the mean of the oscillation
        Diverging sequence   → Z is virtual; direction indicates which way it fled
        """
        if len(cycle_potentials) < 2:
            return cls(value=None, is_virtual=True,
                       approach_direction=0.0, distance_from_current=float("inf"))

        deltas = [
            cycle_potentials[i + 1] - cycle_potentials[i]
            for i in range(len(cycle_potentials) - 1)
        ]
        avg_delta = sum(deltas) / len(deltas)
        current = cycle_potentials[-1]

        # Stationary
        if abs(avg_delta) < 1e-9:
            return cls(value=current, is_virtual=False,
                       approach_direction=0.0, distance_from_current=0.0)

        # Oscillating: sign changes in more than a third of consecutive deltas
        sign_changes = sum(
            1 for i in range(len(deltas) - 1)
            if deltas[i] * deltas[i + 1] < 0
        )
        if len(deltas) > 1 and sign_changes > len(deltas) / 3:
            z = sum(cycle_potentials) / len(cycle_potentials)
            return cls(value=z, is_virtual=False,
                       approach_direction=0.0,
                       distance_from_current=abs(current - z))

        # Converging: magnitude of deltas shrinking
        if len(deltas) >= 3 and abs(deltas[-1]) < abs(deltas[0]):
            ratio = abs(deltas[-1]) / (abs(deltas[-2]) + 1e-10)
            if 0 < ratio < 1:
                # geometric series extrapolation of remaining distance
                remaining = deltas[-1] / (1 - ratio + 1e-10)
                z = current + remaining
                return cls(value=z, is_virtual=False,
                           approach_direction=-1.0,
                           distance_from_current=abs(remaining))

        # Diverging — Z is virtual
        direction = 1.0 if avg_delta > 0 else -1.0
        return cls(value=None, is_virtual=True,
                   approach_direction=direction,
                   distance_from_current=float("inf"))

    def __str__(self) -> str:
        if self.is_virtual:
            arrow = "→+∞" if self.approach_direction > 0 else "→-∞"
            return f"OperativeZero(virtual, {arrow})"
        return f"OperativeZero({self.value:.4f}, Δ={self.distance_from_current:.4f})"
