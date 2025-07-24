<!-- 例: App.vue (またはページレイアウト用コンポーネント) -->
<template>
  <RouterView
    v-slot="{ Component }"
    @submitted="goComplete"
    @goTop="router.push({ name: 'Home' })"
    @admin="goAdmin"
  >
    <component :is="Component" />
  </RouterView>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()

function goComplete() {
  router.push({ name: 'Complete' })
}

function goAdmin(pwd: string | null) {
  if (!pwd) return        // キャンセル時は何もしない
  router.push({ name: 'Admin', query: { pwd } })
}
</script>

