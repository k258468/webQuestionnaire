<template>
  <div class="thanks">
    <h2>ご協力ありがとうございました！</h2>
    <p>アンケートは正常に送信されました。</p>

    <router-link class="top-link" to="/">トップへ戻る</router-link>

    <!-- 管理者ボタン -->
    <button class="admin-btn" @click="openAdmin">
      管理者
    </button>

  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

function openAdmin() {
  const pwd = prompt('管理者パスワードを入力してください');
  if (pwd) {
    router.push({ name: 'Admin', query: { pwd } });
  }
}
</script>

<style scoped>
.thanks { text-align: center; margin-top: 3rem; }
.top-link { display: inline-block; margin-top: 1rem; }
.admin-btn {
  margin-top: 2rem;
  padding: 0.5rem 1rem;
  background: #444;
  color: #fff;
  border-radius: 4px;
}
</style>
