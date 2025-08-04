# クイックスタート

1. リポジトリ直下へ
`cd /path/to/webQuestionnaire`

2. バックエンドをビルド（日本語フォント同梱）
`docker compose build --no-cache backend`

3. 起動（バックグラウンド）
`docker compose up -d`


# ブラウザ確認
[フロント](http://localhost:5173)

[バックエンド](http://localhost:8000)

# ディレクトリ構成
```
webQuestionnaire/
├─ frontend/                      # Vite + Vue
│  ├─ public/
│  │  └─ images/overview.png      # 概要図（任意）
│  └─ src/
│     └─ components/ServiceIntro.vue
├─ backend/
│  └─ app/
│     ├─ main.py                  # API 本体
│     ├─ charts.py                # グラフ生成（PNG）
│     ├─ static/
│     │  └─ admin/                # 生成画像の出力先（chart_*.png）
│     └─ data/                    # 回答 CSV 保存先（*.csv）
├─ docker/
│  └─ backend/Dockerfile          # 日本語フォント入りバックエンド用
└─ docker-compose.yml
```
