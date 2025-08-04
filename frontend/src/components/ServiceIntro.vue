<!-- src/components/ServiceIntro.vue -->
<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="10" lg="9" xl="8">
        <!-- 事前アンケートの案内（高コントラスト・配慮配色） -->
        <v-alert
          variant="outlined"
          color="primary"
          border="start"
          icon="mdi-information-outline"
          density="comfortable"
          class="a11y-alert mb-4 text-body-1"
          role="note"
          aria-label="事前アンケートの案内"
        >
          このページは、Webサービスを導入する前に実施する
          <strong>事前アンケート</strong>の説明ページです。下記の概要をご確認のうえ、
          内容に同意いただける場合は「次へ」からアンケートに進んでください。
        </v-alert>

        <v-card elevation="2">
          <v-card-title class="text-h5 font-weight-bold">
            WEBアプリの概要
          </v-card-title>

          <v-card-text class="text-body-1">
            <p>
              現在我々は、講義後に実施される学生のアンケート回答文から、定期試験における成績を予測し、
              成績が低下する可能性のある学生を早期に特定・支援することを可能にするWEBアプリを開発しようと考えています。
              本アプリの対象ユーザーは、学生と教員の双方です。
            </p>
            <p class="mt-3">
              学生は、自身のアンケート回答に基づいた予測点数を確認することで、単位取得の見込みを把握できます。
              これにより、必要な学習の見直しや改善につなげることが可能となります。
            </p>
            <p class="mt-3">
              一方、教員にとっては、学生ごとの成績予測を早期に把握することで、講義内容や進行方法の見直しを行い、
              理解度の向上を図ることができます。これにより、より多くの学生が単位を取得できるよう講義の質を高めることが期待されます。
            </p>
            <p class="mt-3">
              本WEBアプリを活用することで、講義の質の向上や、留年者の減少といった教育の改善に貢献できると考えています。
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

<style scoped>
.a11y-alert{
  /* 中立背景＋標準前景色（ライト/ダーク両対応） */
  background: var(--v-theme-surface);
  color: var(--v-theme-on-surface);
  line-height: 1.6;
}
</style>
