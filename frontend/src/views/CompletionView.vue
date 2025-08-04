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
              @click="dialog = true"
            >
              管理者
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- パスワード入力ダイアログ -->
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title>管理者パスワード入力</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="inputPwd"
            label="パスワード"
            type="password"
            autofocus
            @keyup.enter="checkPwd"
          />
          <v-alert v-if="errorMsg" type="error" dense text>
            {{ errorMsg }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="dialog = false">キャンセル</v-btn>
          <v-btn color="primary" @click="checkPwd">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const dialog = ref(false)
const inputPwd = ref('')
const errorMsg = ref('')
const router = useRouter()

const ADMIN_PASSWORD = '1234'

function checkPwd() {
  if (inputPwd.value === ADMIN_PASSWORD) {
    dialog.value = false
    errorMsg.value = ''
    const pwdToSend = inputPwd.value
    inputPwd.value = ''
    router.push({ name: 'Admin', query: { pwd: pwdToSend } })
  } else {
    errorMsg.value = 'パスワードが違います。'
  }
}
</script>


