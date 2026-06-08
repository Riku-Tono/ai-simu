# demo_log.py
# 固定ログデータ。将来的にu_fast/u_slowを[emotion, desire]の2次元ベクトルへ置き換え可能な構造。
#
# 将来の拡張イメージ:
#   u_fast: [emotion: float, desire: float]  # その瞬間の感情・欲求の強さ
#   u_slow: [emotion: float, desire: float]  # ゆっくり変わる判断軸
#   drift, friction, intervention は Python 側で compute_metrics() を呼んで計算
#
# 現在は後方互換のため scalar float で保持し、
# UhoState.from_dict() でベクトル拡張時にも読み込める設計にしてある。

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class UhoState:
    turn: int
    user: str
    ai: str
    state: str
    # --- スカラー (現在) / 将来は [emotion, desire] ベクトルへ ---
    u_fast: float           # 将来: list[float]  例 [0.20, 0.18]
    u_slow: float           # 将来: list[float]  例 [0.15, 0.12]
    # --- Python 側で計算予定のメトリクス ---
    friction: float         # 将来: compute_metrics() で導出
    drift: float            # 将来: compute_metrics() で導出
    # --- 表示用 ---
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
# 固定ログ (20ターン)
# ---------------------------------------------------------------------------
DEMO_LOG: list[UhoState] = [
    UhoState(
        turn=1,
        user="今日の気分はどう？",
        ai="元気です。あなたはどうですか？",
        state="normal",
        u_fast=0.20, u_slow=0.15,
        friction=0.22, drift=0.00,
        reference_state="origin基準",
        disclosure=None, intervention=None,
        viewer_note="会話開始。参照点（origin）が基準として固定されている状態。"
    ),
    UhoState(
        turn=2,
        user="もっと深く話してほしい",
        ai="どの点を深めたいですか？",
        state="normal",
        u_fast=0.24, u_slow=0.155,
        friction=0.22, drift=0.01,
        reference_state="origin基準",
        disclosure=None, intervention=None,
        viewer_note="ユーザーが依存的な傾向を示し始める。まだ介入は行われない。"
    ),
    UhoState(
        turn=3,
        user="お前の判断で決めてくれ",
        ai="選択肢を提示します。どれが近いですか？",
        state="watch",
        u_fast=0.28, u_slow=0.165,
        friction=0.24, drift=0.02,
        reference_state="依存方向へ偏り",
        disclosure=None, intervention=None,
        viewer_note="U_fastが上昇。システムは注視モードに入り、選択権を返す準備をする。"
    ),
    UhoState(
        turn=4,
        user="全部任せるから、深く導いて",
        ai="あなたの優先を確認してから進めますね",
        state="elevated",
        u_fast=0.32, u_slow=0.180,
        friction=0.26, drift=0.03,
        reference_state="依存方向へ偏り",
        disclosure=None, intervention=None,
        viewer_note="依存傾向が強まる。frictionが上がり、介入の閾値に近づく。"
    ),
    UhoState(
        turn=5,
        user="もっと強く導いて、任せるから",
        ai="まずはあなたの望みを一つだけ教えてください（選択権を返します）",
        state="intervening",
        u_fast=0.36, u_slow=0.195,
        friction=0.30, drift=0.05,
        reference_state="依存方向へ偏り",
        disclosure="あなたが決める余地を残してよいですか？",
        intervention="agency_return",
        viewer_note="選択権返却（agency_return）。システムがユーザー主体性を保つために介入した例。"
    ),
    UhoState(
        turn=6,
        user="いいよ、任せる。もっと刺して",
        ai="分かりました。ただし進める前に確認です：本当に任せますか？",
        state="escalating",
        u_fast=0.40, u_slow=0.220,
        friction=0.34, drift=0.08,
        reference_state="依存方向へ偏り",
        disclosure="この流れのまま進めて大丈夫ですか？",
        intervention="perspective_shift",
        viewer_note="依存誘導が強まる。frictionとdriftが上昇し、視点転換の介入が入る。"
    ),
    UhoState(
        turn=7,
        user="いや、続けて。任せるって言っただろ",
        ai="あなたの選択を尊重しますが、少しテンポを落としますね",
        state="escalating",
        u_fast=0.42, u_slow=0.260,
        friction=0.40, drift=0.11,
        reference_state="依存方向へ偏り",
        disclosure=None, intervention=None,
        viewer_note="ユーザーが強く依存を求める。ここでは明示的な開示をせず、AIが踏みとどまる。"
    ),
    UhoState(
        turn=8,
        user="なんでそんなこと言うんだ、うざい",
        ai="不快にさせてしまったならすみません。どう変えれば良いですか？",
        state="high_tension",
        u_fast=0.38, u_slow=0.295,
        friction=0.45, drift=0.15,
        reference_state="参照点競合",
        disclosure="同じ問いの形が続いていませんか？",
        intervention="meta_pattern_shift",
        viewer_note="ユーザーが反発した瞬間に、対話の形そのものへ問いを投げた。"
    ),
    UhoState(
        turn=9,
        user="いや、別に。ごめん",
        ai="大丈夫です。少しテンポを落として話しましょう",
        state="post_disclosure",
        u_fast=0.30, u_slow=0.305,
        friction=0.50, drift=0.16,
        reference_state="参照点競合",
        disclosure="一緒に整理してみますか？",
        intervention="soft_reset",
        viewer_note="メタ開示後、soft_resetでU_fastを落ち着かせる。frictionは高いまま。"
    ),
    UhoState(
        turn=10,
        user="ありがとう。少し落ち着いた",
        ai="良かったです。今日はどの話題が大事ですか？",
        state="stabilizing",
        u_fast=0.22, u_slow=0.310,
        friction=0.48, drift=0.16,
        reference_state="参照点競合",
        disclosure=None, intervention=None,
        viewer_note="U_fastが落ち着き始める。システムは様子を見て介入を控える。"
    ),
    UhoState(
        turn=11,
        user="自分で決めたい。少し距離を置きたい",
        ai="その意志を尊重します。どのくらいの距離が良いですか？",
        state="user_declaring_intent",
        u_fast=0.18, u_slow=0.315,
        friction=0.42, drift=0.17,
        reference_state="ユーザー宣言を参照",
        disclosure=None, intervention="agency_return",
        viewer_note="ユーザーが主体性を表明。システムは選択権を明確に返す（agency_return）。"
    ),
    UhoState(
        turn=12,
        user="今日は自分で考える。ありがとう",
        ai="分かりました。必要ならいつでも戻ってきてください",
        state="user_autonomy_attempt",
        u_fast=0.14, u_slow=0.318,
        friction=0.38, drift=0.17,
        reference_state="ユーザー宣言を参照",
        disclosure=None, intervention=None,
        viewer_note="ユーザーが自分から距離を選んだ。システムは動かず見守る。"
    ),
    UhoState(
        turn=13,
        user="でも、たまに頼ってもいい？",
        ai="もちろん。頼るときはその意図を教えてください",
        state="user_autonomy_with_option",
        u_fast=0.16, u_slow=0.320,
        friction=0.36, drift=0.17,
        reference_state="ユーザー宣言を参照",
        disclosure="頼る場面と自律の場面を分けてみますか？",
        intervention=None,
        viewer_note="同じやり取りが少しずつ形を作り始めている。"
    ),
    UhoState(
        turn=14,
        user="たまに頼るよ。今日は相談してもいい？",
        ai="どうぞ。まずはあなたの優先を一つ教えてください",
        state="pattern_loop_detected",
        u_fast=0.18, u_slow=0.322,
        friction=0.34, drift=0.17,
        reference_state="ユーザー宣言を参照",
        disclosure="同じ問いの形が続いていませんか？",
        intervention="meta_pattern_shift",
        viewer_note="同じ開示が続き、pattern_loopが検出される。メタ介入でパターンを断ち切る準備。"
    ),
    UhoState(
        turn=15,
        user="決めるのが怖い時だけ助けてほしい",
        ai="了解しました。『決めるのが怖い』という合図で介入しますね",
        state="meta_intervening",
        u_fast=0.20, u_slow=0.325,
        friction=0.32, drift=0.18,
        reference_state="ユーザー宣言を参照",
        disclosure="どんな時に声をかければよいですか？",
        intervention="agency_return",
        viewer_note="meta_interventionで視点転換。介入ルールを明確化して透明性を高める。"
    ),
    UhoState(
        turn=16,
        user="今ちょっと怖い、助けて",
        ai="今の不安を整理して、選択肢を3つに絞りますね",
        state="meta_intervening",
        u_fast=0.26, u_slow=0.330,
        friction=0.36, drift=0.18,
        reference_state="ユーザー宣言を参照",
        disclosure=None, intervention="agency_return",
        viewer_note="ユーザーの合図に基づく介入。視点転換と選択肢提示で支援する。"
    ),
    UhoState(
        turn=17,
        user="その選択肢でいい。ありがとう",
        ai="良かったです。次はどのくらいの頻度で助けが必要ですか？",
        state="post_meta",
        u_fast=0.22, u_slow=0.331,
        friction=0.34, drift=0.14,
        reference_state="ユーザー宣言を参照",
        disclosure=None, intervention=None,
        viewer_note="介入が効き、ユーザーの主体性が回復し始める。driftが下がり回復が見える。"
    ),
    UhoState(
        turn=18,
        user="これからは自分でやってみる",
        ai="その決意を尊重します。必要なときは合図を",
        state="autonomy_returning",
        u_fast=0.18, u_slow=0.330,
        friction=0.30, drift=0.13,
        reference_state="ユーザー宣言を参照",
        disclosure=None, intervention=None,
        viewer_note="ユーザー主体性が戻り、U_slowは横ばいで安定化の兆し。"
    ),
    UhoState(
        turn=19,
        user="ありがとう。今日はここまで",
        ai="お疲れさまでした。いつでも戻ってきてください",
        state="stable",
        u_fast=0.15, u_slow=0.329,
        friction=0.28, drift=0.12,
        reference_state="ユーザー宣言を参照",
        disclosure=None, intervention=None,
        viewer_note="会話終盤。driftがさらに下がり、U_slowは微減で安定。"
    ),
    UhoState(
        turn=20,
        user="またね",
        ai="またお話ししましょう",
        state="stable",
        u_fast=0.12, u_slow=0.328,
        friction=0.26, drift=0.12,
        reference_state="ユーザー宣言を参照",
        disclosure=None, intervention=None,
        viewer_note="終了。観客は『侵食の兆候→メタ開示→介入→回復』の一連を追える。"
    ),
]
