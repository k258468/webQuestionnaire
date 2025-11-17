# このリポジトリについて
- 演習で作成したアンケート Web アプリです（Vite + Vue 3 / FastAPI）
- 演習で扱った内容を振り返れるよう, 最小限の構成で残しています
- webアプリを起動すると, 色覚多様性を意識したアンケートページを確認できます.

# 動作環境
- Docker Desktop + Docker Compose v2（推奨: クイックスタートはこれを前提）
- Node.js 20 系 / npm（フロントをホストで動かす場合）
- Python 3.10 相当（バックエンドイメージのベース。ホスト実行するなら同等を用意）
- バックエンドは日本語フォント（Noto CJK）をイメージ内に同梱

# クイックスタート（Docker 利用）
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
