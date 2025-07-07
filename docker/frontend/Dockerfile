FROM node:20-slim
WORKDIR /src/frontend

COPY package.json ./

# Vue CLI をグローバル導入（Vite を使いたいなら npm i -g create-vite）
RUN npm install -g @vue/cli

ENV NODE_ENV=development

# 開発サーバーを自動起動させる ↓↓↓
CMD ["npm","run","dev","--","--host","0.0.0.0","--port","5173"]