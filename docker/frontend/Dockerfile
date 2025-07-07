FROM node:20-slim

WORKDIR /app

ENV NODE_ENV=development

COPY package.json ./

RUN npm install

COPY . .

# 開発サーバーを自動起動させる ↓↓↓
CMD ["npm","run","dev","--","--host","0.0.0.0","--port","5173"]