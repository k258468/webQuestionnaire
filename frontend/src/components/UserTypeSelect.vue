<!-- src/components/RoleSelect.vue -->
<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card elevation="2">
          <v-card-title class="text-h6 font-weight-bold">
            あなたはどちらですか？
          </v-card-title>

          <v-card-text>
            <v-btn
              block
              size="large"
              color="primary"
              class="mb-3"
              prepend-icon="mdi-account-tie"
              @click="select('teacher')"
            >
              教師
            </v-btn>

            <v-btn
              block
              size="large"
              variant="outlined"
              color="secondary"
              prepend-icon="mdi-school-outline"
              @click="select('student')"
            >
              学生
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  (e: 'selected', type: 'teacher' | 'student'): void
}>()

const select = (type: 'teacher' | 'student') => emit('selected', type)
</script>
