<!-- ============================================== -->
<!-- src/views/CompletionView.vue                    -->
<!-- emit ベースで親に遷移を委ねても良いですが、       -->
<!-- ここでは単純に RouterLink にしてもOK。           -->
<!-- ============================================== -->
<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card elevation="2" class="text-center py-8">
          <v-card-title class="text-h5 font-weight-bold mb-2">
            ご協力ありがとうございました！
          </v-card-title>

          <v-card-text class="mb-6">
            アンケートは正常に送信されました。
          </v-card-text>

          <v-card-actions class="flex-column gap-3">
            <v-btn
              color="primary"
              block
              prepend-icon="mdi-home"
              :to="{ name: 'Home' }"
            >
              トップへ戻る
            </v-btn>

            <v-btn
              color="secondary"
              variant="tonal"
              block
              prepend-icon="mdi-shield-account"
              @click="onAdmin"
            >
              管理者
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()

function onAdmin() {
  const pwd = window.prompt('管理者パスワードを入力してください')
  if (pwd) {
    router.push({ name: 'Admin', query: { pwd } })
  }
}
</script>
