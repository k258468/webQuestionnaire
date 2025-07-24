<!-- src/components/ServiceIntro.vue -->
<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="10" lg="9" xl="8">
        <v-card elevation="2">
          <v-card-title class="text-h5 font-weight-bold">
            サービスの概要
          </v-card-title>

          <v-card-text class="text-body-1">
            <p>
              このアンケートは「講義終了後の感想アンケートから、その人の定期テスト点を予測する
              webアプリ」の社会的価値が適切か否かを客観的に把握することを目的としています。
            </p>
          </v-card-text>

          <v-card-actions class="justify-end">
          <v-spacer />
            <v-btn
              color="primary"
              prepend-icon="mdi-arrow-right"
              @click="$emit('next')"
            >
              次へ
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  (e: 'next'): void
}>()
</script>
