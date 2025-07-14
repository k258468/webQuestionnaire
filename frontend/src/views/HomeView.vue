<template>
  <div>
    <ServiceIntro v-if="step === 1" @next="step++" />
    <UserTypeSelect v-else-if="step === 2" @selected="onUserSelected" />
    
    <!-- ↓ userType でアンケートを切替 -->
   <TeacherSurveyForm
     v-else-if="step === 3 && userType==='teacher'"
     @submitted="onSubmitted"
   />
   <StudentSurveyForm
     v-else-if="step === 3 && userType==='student'"
     @submitted="onSubmitted"
   />

    <button class="admin-btn" @click="openAdmin">
      管理者
    </button>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import ServiceIntro from '../components/ServiceIntro.vue';
import UserTypeSelect from '../components/UserTypeSelect.vue';
import TeacherSurveyForm from '../components/TeacherSurveyForm.vue';
import StudentSurveyForm from '../components/StudentSurveyForm.vue';


const step = ref(1);
const userType  = ref<'teacher' | 'student' | ''>('');
const router = useRouter();

/* ----- ユーザー種別選択後 ----- */
function onUserSelected(type: 'teacher' | 'student') {
  userType.value = type;
  step.value = 3;
}

/* ----- アンケート送信完了 ----- */
function onSubmitted() {
  router.push({ name: 'Complete' });   // 名前付きルートを利用
}

/* ----- 管理者画面に遷移 ----- */
function openAdmin() {
  const pwd = prompt('管理者パスワードを入力してください');
  if (pwd) {
    router.push({ name: 'Admin', query: { pwd } });
  }
}
</script>

<style scoped>
.home-wrap {
  position: relative;
  padding-bottom: 3rem;          /* ボタンが重ならないよう余白確保 */
}
.admin-btn {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background: #444;
  color: #fff;
  cursor: pointer;
}
</style>


