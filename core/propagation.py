"""
Propagation modes and interference characters.

Two-level model:

  PropagationMode     — answers: how does a single passage step proceed?
                        Operates at the simplex-actualization level.

  InterferenceCharacter — answers: what does this eddy produce where fields meet?
                          Operates at the eddy (session) level, retrospectively.

Kept in core/ so both extract/ and passage/ can import without circularity.
"""
from enum import Enum


class PropagationMode(Enum):
    """
    How a single step of the passage proceeds.
    Never pure — the distribution across steps is the signal.
    """
    DEDUCTIVE    = "deductive"     # necessary entailment; conservative; no new information
    INDUCTIVE    = "inductive"     # pattern following; generalising; mild compression
    TRANSDUCTIVE = "transductive"  # structural form crosses a domain boundary; genuinely new


class InterferenceCharacter(Enum):
    """
    What the eddy produces at the point of contact between fields.
    Determined retrospectively from the passage as a whole.

    Transverse is the most generative: fields cross without direct
    reinforcement or cancellation, producing vocabulary rotations
    that neither field contained alone.
    """
    CONSTRUCTIVE = "constructive"  # fields reinforce; amplify shared patterns
    DESTRUCTIVE  = "destructive"   # fields cancel or critique; incompatibilities surface
    TRANSVERSE   = "transverse"    # fields cross at an angle; unexpected rotations emerge
    RESONANT     = "resonant"      # fields amplify a shared structural pattern across domains
