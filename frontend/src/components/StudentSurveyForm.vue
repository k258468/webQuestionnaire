<template>
  <SurveyShell @submitted="emit('submitted')" :userType="'student'">
    <!-- ★ ここに学生専用の質問だけを書く -->
    
    <div>
      <label>学籍番号:</label>
      <input v-model="name" required />
    </div>
    
    <div>
      <label>学年:</label>
      <select v-model="grade" required>
        <option value="" disabled selected>選択</option>
        <option value="1">1年</option>
        <option value="2">2年</option>
        <option value="3">3年</option>
        <option value="4">4年</option>
      </select>
    </div>
  </SurveyShell>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SurveyShell from './SurveyShell.vue';

const emit  = defineEmits(['submitted']);
const name  = ref(''); 
const grade = ref('');
</script>
