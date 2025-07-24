<template>
  <SurveyShell 
    :userType="'teacher'" 
    :subject="subject" 
    :years="years" 
    @update:subject="val => subject = val" 
    @update:years="val => years = val" 
    @submitted="emit('submitted')"
  >
    <div>
      <label>担当科目:</label>
      <input v-model="subject" required />
    </div>
    <div>
      <label>教歴（年数）:</label>
      <input v-model.number="years" type="number" required />
    </div>
  </SurveyShell>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SurveyShell from './SurveyShell.vue';

const emit = defineEmits(['submitted']);
const subject = ref('');
const years = ref<number | null>(null);
</script>

