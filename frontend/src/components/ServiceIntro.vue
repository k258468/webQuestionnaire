<!-- frontend/src/components/ServiceIntro.vue -->
<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="10" lg="9" xl="8">
        <v-card elevation="2">
          <!-- アンケート説明（可読性重視の配色） -->
          <v-alert
            type="info"
            variant="tonal"
            color="primary"
            class="mb-4"
            border="start"
            prominent
          >
            <div class="font-weight-medium">
              このページは、Webサービスを導入する前に実施する事前アンケートの説明ページです。
              下記の概要をご確認のうえ、内容に同意いただける場合は「次へ」からアンケートに進んでください。
            </div>
          </v-alert>

          <v-card-title class="text-h5 font-weight-bold">
            WEBアプリの概要
          </v-card-title>


          <v-card-text class="text-body-1">
            <p class="mb-4">
              現在我々は、講義後に実施される学生のアンケート回答文から、定期試験における成績を予測し、成績が低下する可能性のある学生を早期に特定・支援することを可能にするWEBアプリを開発しようと考えています。
              本アプリの対象ユーザーは、学生と教員の双方です。学生は、自身のアンケート回答に基づいた予測点数を確認することで、単位取得の見込みを把握できます。
              一方、教員は、学生ごとの成績予測を早期に把握することで、講義内容や進行方法の見直しを行い、理解度の向上を図ることができます。
            </p>

            <!-- 概要図（public/images/overview.png） -->
            <v-img
              src="/images/overview.png"
              alt="Webアプリ概要図"
              class="rounded-lg my-4"
              max-width="100%"
              aspect-ratio="16/9"
              eager
            />
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
defineEmits<{ (e: 'next'): void }>()
</script>
