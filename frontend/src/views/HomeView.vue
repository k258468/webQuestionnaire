<template>
  <v-container class="py-8 home-wrap" style="position: relative;">
    <ServiceIntro v-if="step === 1" @next="step++" />
    <UserTypeSelect v-else-if="step === 2" @selected="onUserSelected" />

    <TeacherSurveyForm
      v-else-if="step === 3 && userType==='teacher'"
      @submitted="onSubmitted"
    />
    <StudentSurveyForm
      v-else-if="step === 3 && userType==='student'"
      @submitted="onSubmitted"
    />

    <v-btn
      class="admin-btn"
      color="secondary"
      variant="tonal"
      prepend-icon="mdi-shield-account"
      @click="dialog = true"
    >
      管理者
    </v-btn>

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

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ServiceIntro from '@/components/ServiceIntro.vue'
import UserTypeSelect from '@/components/UserTypeSelect.vue'
import TeacherSurveyForm from '@/components/TeacherSurveyForm.vue'
import StudentSurveyForm from '@/components/StudentSurveyForm.vue'

const step = ref<1 | 2 | 3>(1)
const userType  = ref<'teacher' | 'student' | ''>('')
const router = useRouter()

const dialog = ref(false)
const inputPwd = ref('')
const errorMsg = ref('')

// 固定パスワード（本来はサーバーで認証）
const ADMIN_PASSWORD = '1234'

function onUserSelected(type: 'teacher' | 'student') {
  userType.value = type
  step.value = 3
}

function onSubmitted() {
  router.push({ name: 'Complete' })
}

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

<style scoped>
.home-wrap {
  padding-bottom: 3rem;
}
.admin-btn {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}
</style>




