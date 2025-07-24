<template>
  <SurveyShell
    userType="student"
    v-model:name="studentId"
    v-model:grade="grade"
    @submitted="emit('submitted')"
  >
    <div>
      <v-text-field
        v-model="studentId"
        label="学籍番号"
        variant="outlined"
        density="comfortable"
        prepend-icon="mdi-card-account-details-outline"
        :rules="[required]"
        required
        class="mb-4"
      />

      <v-select
        v-model.number="grade"
        :items="grades"
        item-title="title"
        item-value="value"
        label="学年"
        variant="outlined"
        density="comfortable"
        prepend-icon="mdi-school-outline"
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

const studentId = ref<string>('')
const grade = ref<number | null>(null)

const grades = [
  { title: '1年', value: 1 },
  { title: '2年', value: 2 },
  { title: '3年', value: 3 },
  { title: '4年', value: 4 },
] as const

const required = (v: unknown) =>
  (v !== null && v !== undefined && v !== '' && !(Array.isArray(v) && v.length === 0)) || '必須項目です'
</script>
