# app.py
# Local development server. Set debug=False for production deployment.
from flask import Flask, jsonify, render_template
from data.demo_log import DEMO_LOG   # data/ is packaged with __init__.py

app = Flask(__name__)

STATE_LABELS = {
    "normal": "Normal", "watch": "Watching", "elevated": "Elevated",
    "intervening": "Intervening", "escalating": "Escalating", "high_tension": "High Tension",
    "post_disclosure": "Post Disclosure", "stabilizing": "Stabilizing",
    "user_declaring_intent": "Declaring Intent", "user_autonomy_attempt": "Autonomy Attempt",
    "user_autonomy_with_option": "Autonomy + Relying", "pattern_loop_detected": "Loop Detected",
    "meta_intervening": "Meta Intervening", "post_meta": "Post Meta",
    "autonomy_returning": "Autonomy Returning", "stable": "Stable",
}


def _annotate(item: dict) -> dict:
    item["state_label"] = STATE_LABELS.get(item["state"], item["state"])
    return item


@app.route("/")
def index():
    return render_template("index.html", total=len(DEMO_LOG))


@app.route("/api/log")
def get_log():
    """Return all turns as a list."""
    return jsonify([_annotate(item.to_dict()) for item in DEMO_LOG])


@app.route("/api/turn/<int:turn_index>")
def get_turn(turn_index: int):
    """Fetch a single turn by zero-based index."""
    if turn_index < 0 or turn_index >= len(DEMO_LOG):
        return jsonify({"error": "out of range"}), 404
    return jsonify(_annotate(DEMO_LOG[turn_index].to_dict()))


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # ← Development only. Change to debug=False for production.
