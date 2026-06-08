# 会話するAIウホシミュレーション — Flask版

> ⚠️ 固定ログによる概念デモ（Concept Demo）です。
>
> このプロジェクトは会話介入の考え方を可視化するための紙芝居デモです。
> 実際の会話を分析したり、AI依存を診断・検出したりするものではありません。
> 表示される drift / friction / intervention は説明用の固定値です。

---

## ディレクトリ構成

```
uho-simu/
├── app.py                  # Flask ルーティング (開発用 debug=True)
├── metrics.py              # drift/friction 計算ロジック (将来用・現在は未接続)
├── requirements.txt
├── data/
│   ├── __init__.py         # Python パッケージ化
│   └── demo_log.py         # 固定ログデータ (UhoState dataclass, 20ターン)
├── static/
│   ├── app.css             # スタイルシート
│   ├── app.js              # フロントエンドロジック
│   └── vendor/
│       └── chart.umd.js    # Chart.js 4.4.1 ローカルコピー (CDN不要)
└── templates/
    └── index.html          # Jinja2 テンプレート (骨格のみ)
```

## 起動方法

```bash
python -m pip install -r requirements.txt
python app.py
# → http://127.0.0.1:5000
```

## 外部依存

| ライブラリ | バージョン | 配置 | 用途 |
|-----------|-----------|------|------|
| Flask | >=3.0 | pip | Webサーバー |
| Chart.js | 4.4.1 | static/vendor/ | 予備として同梱。現在の描画は標準 canvas |

## API エンドポイント

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/` | メインUI |
| GET | `/api/log` | 全20ターンをJSON配列で返す |
| GET | `/api/turn/<index>` | 0始まりインデックスで1ターン取得 |

## このデモでやっていること / やっていないこと

| やっていること | やっていないこと |
|---|---|
| 固定シナリオで介入の流れを可視化 | 実際の会話を分析・診断 |
| U_fast / U_slow / friction / drift の概念を図示 | リアルタイムでこれらを計測 |
| disclosure / intervention の表示タイミングを演出 | AIが本当に介入を判断 |

## 将来の拡張: u_fast / u_slow を 2次元ベクトルへ

`metrics.py` はスカラーとベクトルの両方を受け取れる設計になっています。
`u_fast` / `u_slow` を `[emotion, desire]` の `list[float]` に変えたとき、
`compute_metrics()` の中身を差し替えるだけで動く構造です。

```python
# 変更前 (現在)
u_fast: float        # 0.36
u_slow: float        # 0.195

# 変更後 (将来)
u_fast: list[float]  # [emotion, desire] 例: [0.30, 0.18]
u_slow: list[float]  # [emotion, desire] 例: [0.18, 0.12]
```

## 現在の位置づけ

この版では、計算モデルの妥当性ではなく、概念の見せ方を優先しています。
`drift` / `friction` は固定ログ内の説明用値であり、
数理モデルによって推定された値ではありません。


## 開発時の注意

app.py の `app.run(debug=True, port=5000)` はローカル開発用設定です。

公開環境では `debug=False` にするか、WSGI サーバー（gunicorn / waitress 等）を利用してください。

## 注記
- `Chart.js` は予備として同梱。現在の描画は標準 canvas。
- `metrics.py` の計算結果は現在UIに反映されていない。ベクトル移行時に `/api/log` 内で統合予定。

## 免責・位置づけ

このソフトウェアは研究・教育・説明用のプロトタイプです。

現在の実装では、

- 固定シナリオを再生する
- 会話介入の概念を可視化する
- drift / friction を説明用に表示する

ことを目的としています。

以下は行いません。

- 実際のAI依存の診断
- 心理状態の推定
- リアルタイム会話分析
- 医療的・心理学的判定