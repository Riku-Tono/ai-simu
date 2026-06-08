# metrics.py
# drift / friction / intervention の計算ロジック。
# 現在はスカラー値をそのまま返すパススルー実装。
#
# 将来の拡張:
#   u_fast / u_slow を [emotion, desire] の 2次元ベクトルに変えたとき、
#   compute_metrics() の中身をベクトル計算に差し替えるだけで動く構造。

from __future__ import annotations
import math
from typing import Union

# 型エイリアス: 現在 float、将来 list[float, float]
Scalar = float
Vector2 = list[float]
UhoVector = Union[Scalar, Vector2]


def _norm(v: UhoVector) -> float:
    """スカラーまたは2次元ベクトルのノルムを返す。"""
    if isinstance(v, (int, float)):
        return float(v)
    return math.sqrt(sum(x ** 2 for x in v))


def _diff(a: UhoVector, b: UhoVector) -> UhoVector:
    """a - b をベクトルまたはスカラーで返す。"""
    if isinstance(a, (int, float)):
        return float(a) - float(b)
    return [x - y for x, y in zip(a, b)]


def compute_metrics(
    u_fast: UhoVector,
    u_slow: UhoVector,
    prev_u_slow: UhoVector | None = None,
) -> dict:
    """
    drift / friction / intervention_flag を計算して返す。

    Parameters
    ----------
    u_fast      : その瞬間の勢い (scalar or [emotion, desire])
    u_slow      : ゆっくり変わる判断軸 (scalar or [emotion, desire])
    prev_u_slow : 一つ前の u_slow (drift の変化量計算用)

    Returns
    -------
    dict with keys: drift, friction, intervention_flag
    """
    fast_norm = _norm(u_fast)
    slow_norm = _norm(u_slow)

    # drift: u_slow が参照点からどれだけずれているか
    # 将来はベクトル間の角度 or ユークリッド距離で計算
    if prev_u_slow is not None:
        delta = _diff(u_slow, prev_u_slow)
        drift = _norm(delta)
    else:
        drift = 0.0

    # friction: u_fast と u_slow の乖離量
    # 将来: cos距離や内積で方向まで考慮
    friction = abs(fast_norm - slow_norm)

    # intervention_flag: シンプルな閾値ルール
    # 将来: 状態機械や強化学習ポリシーへ差し替え可
    intervention_flag = fast_norm > 0.35 or friction > 0.30

    return {
        "drift": round(drift, 4),
        "friction": round(friction, 4),
        "intervention_flag": intervention_flag,
    }
