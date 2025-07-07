<template>
  <div>
    <h2>あなたはどちらですか？</h2>
    <button @click="select('teacher')">教師</button>
    <button @click="select('student')">学生</button>
  </div>
</template>

<script lang="ts" setup>
const emit = defineEmits(['selected']);
const select = (type: string) => emit('selected', type);
</script>
