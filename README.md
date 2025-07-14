# プロジェクトのルートへ移動
cd /path/to/webQuestionnaire

# 1) フロントエンド依存
`cd /path/to/webQuestionnairefrontend`
`npm install`

# 2) バックエンド依存
`cd /path/to/webQuestionnaire/backend`
`pip install -r requirements.txt`

# 1) まだコンテナが動いていなければ起動
`docker compose up` --前面実行（ログを見ながら開発するならこちら）
# ─ または ─
`docker compose up -d` --バックグラウンド実行

# 2) ブラウザ確認
[フロント](http://localhost:5173)

[バックエンド](http://localhost:8000)