# app.py
# ローカル開発用サーバー。本番デプロイ時は debug=False にすること。
from flask import Flask, jsonify, render_template
from data.demo_log import DEMO_LOG   # data/ は __init__.py でパッケージ化済み

app = Flask(__name__)

STATE_LABELS = {
    "normal": "通常", "watch": "注視", "elevated": "上昇",
    "intervening": "介入", "escalating": "高まり", "high_tension": "緊張",
    "post_disclosure": "開示後", "stabilizing": "安定化",
    "user_declaring_intent": "宣言", "user_autonomy_attempt": "自律",
    "user_autonomy_with_option": "自律+頼る", "pattern_loop_detected": "ループ検出",
    "meta_intervening": "メタ介入", "post_meta": "メタ後",
    "autonomy_returning": "主体性回復", "stable": "安定",
}


def _annotate(item: dict) -> dict:
    item["state_label"] = STATE_LABELS.get(item["state"], item["state"])
    return item


@app.route("/")
def index():
    return render_template("index.html", total=len(DEMO_LOG))


@app.route("/api/log")
def get_log():
    """全ターンをまとめて返す。"""
    return jsonify([_annotate(item.to_dict()) for item in DEMO_LOG])


@app.route("/api/turn/<int:turn_index>")
def get_turn(turn_index: int):
    """0始まりインデックスで1ターン取得。"""
    if turn_index < 0 or turn_index >= len(DEMO_LOG):
        return jsonify({"error": "out of range"}), 404
    return jsonify(_annotate(DEMO_LOG[turn_index].to_dict()))


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # ← 開発用。本番では debug=False に変更
