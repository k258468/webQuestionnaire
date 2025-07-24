<template>
  <SurveyShell
    userType="teacher"
    v-model:subject="subject"
    v-model:years="years"
    @submitted="emit('submitted')"
  >
    <div>
      <v-text-field
        v-model="subject"
        label="担当科目"
        variant="outlined"
        density="comfortable"
        prepend-icon="mdi-book-open-variant"
        :rules="[required]"
        required
        class="mb-4"
      />

      <v-text-field
        v-model.number="years"
        label="教歴（年数）"
        type="number"
        variant="outlined"
        density="comfortable"
        prepend-icon="mdi-teach"
        :rules="[required]"
        required
      />
    </div>
  </SurveyShell>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SurveyShell from './SurveyShell.vue'

const emit = defineEmits<{ (e: 'submitted'): void }>()

const subject = ref<string>('')
const years = ref<number | null>(null)

const required = (v: unknown) =>
  (v !== null && v !== undefined && v !== '' && !(Array.isArray(v) && v.length === 0)) || '必須項目です'
</script>
