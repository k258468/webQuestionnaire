<!-- ============================================== -->
<!-- src/views/HomeView.vue                         -->
<!-- 親：emit を拾って /complete へ遷移               -->
<!-- ============================================== -->
<template>
  <v-container class="py-8 home-wrap">
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
      @click="openAdmin"
    >
      管理者
    </v-btn>
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

function onUserSelected(type: 'teacher' | 'student') {
  userType.value = type
  step.value = 3
}

function onSubmitted() {
  console.log('[Home] submitted -> go Complete')
  router.push({ name: 'Complete' })
}

function openAdmin() {
  const pwd = prompt('管理者パスワードを入力してください')
  if (pwd) {
    router.push({ name: 'Admin', query: { pwd } })
  }
}
</script>

<style scoped>
.home-wrap {
  position: relative;
  padding-bottom: 3rem;
}
.admin-btn {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}
</style>



