FROM python:3.10-slim
ENV MPLBACKEND=Agg

# 日本語フォントと fontconfig を入れる
RUN apt-get update \
 && apt-get install -y --no-install-recommends fontconfig fonts-noto-cjk \
 && fc-cache -f \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ← ここを修正：ビルドコンテキスト（プロジェクトルート）から backend/requirements.txt をコピー
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# アプリ本体
COPY backend /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
