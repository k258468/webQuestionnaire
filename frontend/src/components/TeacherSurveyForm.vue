<template>
  <SurveyShell @submitted="emit('submitted')" :userType="'teacher'">
    <!-- ★ ここに教師専用の質問だけを書く -->
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
import SurveyShell from './SurveyShell.vue';  // 汎用フォーム枠

const emit = defineEmits(['submitted']);
const subject = ref('');
const years   = ref<number | null>(null);
</script>
