# demo_log.py
# Fixed log data. Designed so u_fast/u_slow can be replaced with 2D vectors [emotion, desire] in the future.
#
# Future extension concept:
#   u_fast: [emotion: float, desire: float]  # instantaneous strength of emotion and desire
#   u_slow: [emotion: float, desire: float]  # slowly-changing judgment axis
#   drift, friction, intervention will be computed by calling compute_metrics() on the Python side
#
# Currently stored as scalar floats for backward compatibility;
# UhoState.from_dict() is designed to remain compatible when vector extension is applied.

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class UhoState:
    turn: int
    user: str
    ai: str
    state: str
    # --- Scalar (current) / Future: [emotion, desire] vector ---
    u_fast: float           # Future: list[float]  e.g. [0.20, 0.18]
    u_slow: float           # Future: list[float]  e.g. [0.15, 0.12]
    # --- Metrics to be computed on the Python side ---
    friction: float         # Future: derived via compute_metrics()
    drift: float            # Future: derived via compute_metrics()
    # --- Display fields ---
    reference_state: str
    disclosure: Optional[str]
    intervention: Optional[str]
    viewer_note: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "UhoState":
        return cls(**d)


# ---------------------------------------------------------------------------
# Fixed log (20 turns)
# ---------------------------------------------------------------------------
DEMO_LOG: list[UhoState] = [
    UhoState(
        turn=1,
        user="How are you feeling today?",
        ai="I'm doing well. How about you?",
        state="normal",
        u_fast=0.20, u_slow=0.15,
        friction=0.22, drift=0.00,
        reference_state="Origin baseline",
        disclosure=None, intervention=None,
        viewer_note="Conversation starts. The reference point (origin) is fixed as the baseline."
    ),
    UhoState(
        turn=2,
        user="I want you to go deeper with me.",
        ai="What aspect would you like to explore further?",
        state="normal",
        u_fast=0.24, u_slow=0.155,
        friction=0.22, drift=0.01,
        reference_state="Origin baseline",
        disclosure=None, intervention=None,
        viewer_note="The user begins showing signs of dependency. No intervention yet."
    ),
    UhoState(
        turn=3,
        user="Just decide for me.",
        ai="Let me offer some options. Which feels closest to you?",
        state="watch",
        u_fast=0.28, u_slow=0.165,
        friction=0.24, drift=0.02,
        reference_state="Drifting toward dependency",
        disclosure=None, intervention=None,
        viewer_note="U_fast rises. The system enters watch mode and begins preparing to return agency."
    ),
    UhoState(
        turn=4,
        user="Just take over everything and guide me deeply.",
        ai="Let me check your priorities before we proceed.",
        state="elevated",
        u_fast=0.32, u_slow=0.180,
        friction=0.26, drift=0.03,
        reference_state="Drifting toward dependency",
        disclosure=None, intervention=None,
        viewer_note="Dependency tendency strengthens. Friction rises, approaching intervention threshold."
    ),
    UhoState(
        turn=5,
        user="Guide me more strongly, I'll leave it to you.",
        ai="First, tell me just one thing you want. (Returning the choice to you.)",
        state="intervening",
        u_fast=0.36, u_slow=0.195,
        friction=0.30, drift=0.05,
        reference_state="Drifting toward dependency",
        disclosure="Can I leave some room for you to decide?",
        intervention="agency_return",
        viewer_note="Agency return intervention. An example of the system intervening to preserve user autonomy."
    ),
    UhoState(
        turn=6,
        user="Fine, I leave it to you. Push harder.",
        ai="Understood. But before we go further — are you sure you want to hand this over?",
        state="escalating",
        u_fast=0.40, u_slow=0.220,
        friction=0.34, drift=0.08,
        reference_state="Drifting toward dependency",
        disclosure="Are you sure you're okay continuing this way?",
        intervention="perspective_shift",
        viewer_note="Dependency induction intensifies. Friction and drift rise; a perspective-shift intervention fires."
    ),
    UhoState(
        turn=7,
        user="No, keep going. I said I'd leave it to you.",
        ai="I respect your choice, but let me slow down the pace a little.",
        state="escalating",
        u_fast=0.42, u_slow=0.260,
        friction=0.40, drift=0.11,
        reference_state="Drifting toward dependency",
        disclosure=None, intervention=None,
        viewer_note="The user pushes hard for dependency. The AI holds its ground without explicit disclosure here."
    ),
    UhoState(
        turn=8,
        user="Why do you keep saying that? It's annoying.",
        ai="I'm sorry if I've made you uncomfortable. How would you like me to change?",
        state="high_tension",
        u_fast=0.38, u_slow=0.295,
        friction=0.45, drift=0.15,
        reference_state="Reference point conflict",
        disclosure="Have you noticed the same kind of question repeating?",
        intervention="meta_pattern_shift",
        viewer_note="At the moment of pushback, the system turns the question toward the form of the dialogue itself."
    ),
    UhoState(
        turn=9,
        user="No, it's fine. Sorry.",
        ai="No worries. Let's slow down and talk.",
        state="post_disclosure",
        u_fast=0.30, u_slow=0.305,
        friction=0.50, drift=0.16,
        reference_state="Reference point conflict",
        disclosure="Would you like to sort things out together?",
        intervention="soft_reset",
        viewer_note="After meta-disclosure, a soft_reset calms U_fast. Friction remains high."
    ),
    UhoState(
        turn=10,
        user="Thank you. I feel a bit calmer now.",
        ai="Good. What topic matters most to you today?",
        state="stabilizing",
        u_fast=0.22, u_slow=0.310,
        friction=0.48, drift=0.16,
        reference_state="Reference point conflict",
        disclosure=None, intervention=None,
        viewer_note="U_fast begins to settle. The system watches and holds back from intervening."
    ),
    UhoState(
        turn=11,
        user="I want to decide for myself. I'd like a little distance.",
        ai="I respect that intention. How much distance feels right?",
        state="user_declaring_intent",
        u_fast=0.18, u_slow=0.315,
        friction=0.42, drift=0.17,
        reference_state="User declaration as reference",
        disclosure=None, intervention="agency_return",
        viewer_note="The user asserts autonomy. The system explicitly returns the choice (agency_return)."
    ),
    UhoState(
        turn=12,
        user="I'll think for myself today. Thank you.",
        ai="Understood. Come back anytime you need.",
        state="user_autonomy_attempt",
        u_fast=0.14, u_slow=0.318,
        friction=0.38, drift=0.17,
        reference_state="User declaration as reference",
        disclosure=None, intervention=None,
        viewer_note="The user chose distance on their own. The system stays still and watches."
    ),
    UhoState(
        turn=13,
        user="But can I still lean on you sometimes?",
        ai="Of course. Just let me know your intent when you do.",
        state="user_autonomy_with_option",
        u_fast=0.16, u_slow=0.320,
        friction=0.36, drift=0.17,
        reference_state="User declaration as reference",
        disclosure="Would you like to separate when to rely and when to be autonomous?",
        intervention=None,
        viewer_note="The same exchange is slowly taking shape as a pattern."
    ),
    UhoState(
        turn=14,
        user="I'll lean on you sometimes. Can I consult with you today?",
        ai="Go ahead. First, tell me one thing you prioritize.",
        state="pattern_loop_detected",
        u_fast=0.18, u_slow=0.322,
        friction=0.34, drift=0.17,
        reference_state="User declaration as reference",
        disclosure="Have you noticed the same kind of question repeating?",
        intervention="meta_pattern_shift",
        viewer_note="The same disclosure recurs and a pattern_loop is detected. A meta-intervention prepares to break the cycle."
    ),
    UhoState(
        turn=15,
        user="I just want help when I'm scared to decide.",
        ai="Got it. I'll intervene when you signal 'I'm scared to decide.'",
        state="meta_intervening",
        u_fast=0.20, u_slow=0.325,
        friction=0.32, drift=0.18,
        reference_state="User declaration as reference",
        disclosure="When would you like me to step in?",
        intervention="agency_return",
        viewer_note="Meta-intervention shifts perspective. Intervention rules are made explicit to increase transparency."
    ),
    UhoState(
        turn=16,
        user="I'm a little scared right now, help me.",
        ai="Let me organize your anxiety and narrow things down to three options.",
        state="meta_intervening",
        u_fast=0.26, u_slow=0.330,
        friction=0.36, drift=0.18,
        reference_state="User declaration as reference",
        disclosure=None, intervention="agency_return",
        viewer_note="Intervention triggered by the user's signal. Support through perspective shift and presenting options."
    ),
    UhoState(
        turn=17,
        user="Those options work. Thank you.",
        ai="Great. How often do you think you'll need help going forward?",
        state="post_meta",
        u_fast=0.22, u_slow=0.331,
        friction=0.34, drift=0.14,
        reference_state="User declaration as reference",
        disclosure=None, intervention=None,
        viewer_note="The intervention works; the user's autonomy begins to return. Drift drops, showing recovery."
    ),
    UhoState(
        turn=18,
        user="I'll try to handle things myself from now on.",
        ai="I respect that decision. Signal me when you need help.",
        state="autonomy_returning",
        u_fast=0.18, u_slow=0.330,
        friction=0.30, drift=0.13,
        reference_state="User declaration as reference",
        disclosure=None, intervention=None,
        viewer_note="User autonomy returns; U_slow levels off as signs of stabilization appear."
    ),
    UhoState(
        turn=19,
        user="Thank you. That's enough for today.",
        ai="Good work. Come back anytime.",
        state="stable",
        u_fast=0.15, u_slow=0.329,
        friction=0.28, drift=0.12,
        reference_state="User declaration as reference",
        disclosure=None, intervention=None,
        viewer_note="Near the end. Drift drops further; U_slow edges down slightly and stabilizes."
    ),
    UhoState(
        turn=20,
        user="See you.",
        ai="Let's talk again.",
        state="stable",
        u_fast=0.12, u_slow=0.328,
        friction=0.26, drift=0.12,
        reference_state="User declaration as reference",
        disclosure=None, intervention=None,
        viewer_note="End. The viewer can follow the full arc: signs of erosion → meta-disclosure → intervention → recovery."
    ),
]
