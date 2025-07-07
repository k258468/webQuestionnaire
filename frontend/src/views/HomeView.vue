<template>
  <div>
    <ServiceIntro v-if="step === 1" @next="step++" />
    <UserTypeSelect v-else-if="step === 2" @selected="onUserSelected" />
    <SurveyForm v-else-if="step === 3" :userType="userType" @submitted="onSubmitted" />
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import ServiceIntro from '../components/ServiceIntro.vue';
import UserTypeSelect from '../components/UserTypeSelect.vue';
import SurveyForm from '../components/SurveyForm.vue';

const step = ref(1);
const userType = ref('');
const router = useRouter();

const onUserSelected = (type: string) => {
  userType.value = type;
  step.value++;
};

const onSubmitted = (data: any) => {
  console.log('アンケート結果:', data);
  router.push('/complete');
};
</script>


