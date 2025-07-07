FROM python:3.10-slim
WORKDIR /app

# 依存
COPY docker/backend/requirements.txt .
RUN pip install -r requirements.txt

# アプリ本体
COPY backend /app

# 開発用リロード付きで起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
