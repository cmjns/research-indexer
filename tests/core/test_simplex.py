import pytest
from core.term import Term
from core.simplex import Simplex, Role
from core.network import SimplexNetwork
from core.field import PotentialField
from core.germ import RoleRotation


def make_simplex(a_label, b_label, c_label, intensity=1.0, asymmetry=0.5, gain=0.1):
    a = Term(id=a_label, label=a_label)
    b = Term(id=b_label, label=b_label)
    c = Term(id=c_label, label=c_label)
    return Simplex(
        id=f"{a_label}-{b_label}",
        source=a, target=b, modulator=c,
        intensity=intensity, asymmetry=asymmetry, gain=gain,
    )


def test_simplex_roles():
    s = make_simplex("piety", "gods-love", "definition-seeking")
    roles = s.roles()
    assert roles[Role.SOURCE].label == "piety"
    assert roles[Role.TARGET].label == "gods-love"
    assert roles[Role.MODULATOR].label == "definition-seeking"


def test_simplex_terms():
    s = make_simplex("piety", "gods-love", "definition-seeking")
    assert len(s.terms()) == 3


def test_network_adjacency():
    s1 = make_simplex("piety", "gods-love", "definition-seeking")
    s2 = make_simplex("gods-love", "piety", "definition-seeking")
    network = SimplexNetwork()
    network.add(s1)
    network.add(s2)

    adj = network.adjacency()
    assert s2.id in adj[s1.id]
    assert s1.id in adj[s2.id]


def test_role_shifts_detects_aporia():
    """The Euthyphro: piety and gods-love swap roles — a role shift."""
    s1 = make_simplex("piety", "gods-love", "definition-seeking")
    s2 = make_simplex("gods-love", "piety", "definition-seeking")
    network = SimplexNetwork()
    network.add(s1)
    network.add(s2)

    shifts = network.role_shifts()
    shifted_labels = {t.label for t, *_ in shifts}
    assert "piety" in shifted_labels or "gods-love" in shifted_labels


def test_potential_field_derived_from_network():
    s = make_simplex("piety", "gods-love", "definition-seeking", intensity=2.0)
    network = SimplexNetwork()
    network.add(s)

    field = PotentialField.from_network(network)
    assert field.phi(s.source) > 0
    assert field.phi(s.target) > 0
    assert field.total() > 0


def test_role_rotation_genuine():
    rotation = RoleRotation(cycle=["s1", "s2"], displacement=0.5)
    assert rotation.is_genuine(threshold=0.1)

    flat = RoleRotation(cycle=["s1", "s2"], displacement=0.0)
    assert not flat.is_genuine(threshold=0.0)
