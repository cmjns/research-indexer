"""Tests for OperativeZero and Eddy construction."""
import pytest
from core.operative_zero import OperativeZero
from core.term import Term
from core.simplex import Role
from passage.eddy import VocabRotation, Eddy, RemainderEntry
from core.propagation import InterferenceCharacter


# ------------------------------------------------------------------
# OperativeZero
# ------------------------------------------------------------------

class TestOperativeZero:

    def test_stationary_sequence(self):
        """Flat sequence → Z is real, at current value."""
        oz = OperativeZero.compute([1.0, 1.0, 1.0, 1.0])
        assert not oz.is_virtual
        assert abs(oz.value - 1.0) < 1e-6
        assert oz.distance_from_current < 1e-6

    def test_oscillating_sequence(self):
        """Alternating sequence → Z is mean, non-virtual."""
        oz = OperativeZero.compute([1.0, 3.0, 1.0, 3.0, 1.0])
        assert not oz.is_virtual
        assert abs(oz.value - 2.0) < 0.5   # mean ≈ 2.0

    def test_diverging_sequence_is_virtual(self):
        """Euthyphro: the cycle never closes — Z is virtual."""
        oz = OperativeZero.compute([1.0, 1.5, 2.2, 3.1, 4.3])
        assert oz.is_virtual
        assert oz.value is None
        assert oz.approach_direction == 1.0   # moving away positively

    def test_converging_sequence(self):
        """Weakly aporetic cycle that will close — Z is real."""
        # geometric: each step halves the gap
        oz = OperativeZero.compute([0.0, 0.5, 0.75, 0.875, 0.9375])
        assert not oz.is_virtual
        # Z should be near 1.0
        assert oz.value is not None
        assert oz.value > 0.9

    def test_too_short(self):
        """Fewer than 2 points → virtual by default."""
        oz = OperativeZero.compute([1.0])
        assert oz.is_virtual

    def test_empty(self):
        oz = OperativeZero.compute([])
        assert oz.is_virtual


# ------------------------------------------------------------------
# VocabRotation
# ------------------------------------------------------------------

class TestVocabRotation:

    def test_creates_correctly(self):
        term = Term(id="piety", label="piety")
        rot = VocabRotation(
            term=term,
            role_from=Role.SOURCE,    field_from="simplex-1",
            role_to=Role.TARGET,      field_to="simplex-2",
        )
        assert rot.term.label == "piety"
        assert rot.role_from == Role.SOURCE
        assert rot.role_to == Role.TARGET


# ------------------------------------------------------------------
# Eddy
# ------------------------------------------------------------------

class TestEddy:

    def _make_eddy(self, char=None, oz=None):
        return Eddy(
            id="test-eddy",
            scale="meso",
            source="directory:test",
            fields_in_rotation=["thought", "argument"],
            vocabulary_rotations=[
                VocabRotation(
                    term=Term(id="piety", label="piety"),
                    role_from=Role.SOURCE, field_from="s1",
                    role_to=Role.TARGET,   field_to="s2",
                )
            ],
            interference_character=char or InterferenceCharacter.TRANSVERSE,
            what_appeared="Transverse interference. 3 steps, 1 role rotation.",
            remainder=[],
            operative_zero=oz or OperativeZero(
                value=None, is_virtual=True,
                approach_direction=1.0, distance_from_current=float("inf")
            ),
            steps=[],
        )

    def test_to_ledger_entry_structure(self):
        eddy = self._make_eddy()
        entry = eddy.to_ledger_entry()

        assert entry["id"] == "test-eddy"
        assert entry["scale"] == "meso"
        assert "fields_in_rotation" in entry
        assert "vocabulary_in_play" in entry
        assert "interference" in entry
        assert "remainder" in entry
        assert "operative_zero" in entry
        assert "structural_pattern" in entry

    def test_to_ledger_flags_unannotated_fields(self):
        eddy = self._make_eddy()
        entry = eddy.to_ledger_entry()
        assert entry["fields_in_rotation"]["dominant_field"] == "_needs_annotation"
        assert "_needs_annotation" in entry["remainder"]["feeds_into"]

    def test_virtual_operative_zero_in_ledger(self):
        oz = OperativeZero(value=None, is_virtual=True,
                           approach_direction=1.0, distance_from_current=float("inf"))
        eddy = self._make_eddy(oz=oz)
        entry = eddy.to_ledger_entry()
        assert "virtual" in entry["operative_zero"]

    def test_interference_character_recorded(self):
        eddy = self._make_eddy(char=InterferenceCharacter.RESONANT)
        entry = eddy.to_ledger_entry()
        assert entry["interference"]["character"] == "resonant"
