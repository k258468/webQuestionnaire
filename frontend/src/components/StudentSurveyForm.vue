<!-- src/components/StudentSurveyForm.vue -->
<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card elevation="2">
          <v-card-title class="text-h6 font-weight-bold">
            学生アンケート
          </v-card-title>

          <v-card-text>
            <v-form ref="form" @submit.prevent="submitForm">
              <!-- ───── 1. 早期検知・支援の活用意向 ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                1. 早期検知・早期支援の必要性と効果
              </h3>

              <v-radio-group
                v-model="q1"
                :rules="[required]"
                label="活用意向"
                inline
                class="mb-6"
              >
                <v-radio v-for="opt in fiveUse" :key="opt" :label="opt" :value="opt" />
              </v-radio-group>

              <!-- ───── 2. パーソナライズド・フィードバック ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                2. パーソナライズされたフィードバックの価値
              </h3>

              <v-radio-group
                v-model="q2"
                :rules="[required]"
                label="学習改善への役立ち度"
                inline
                class="mb-6"
              >
                <v-radio v-for="opt in fiveValue" :key="opt" :label="opt" :value="opt" />
              </v-radio-group>

              <!-- ───── 3. 講義改善への受容性 ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                3. 講義改善への貢献への受容性
              </h3>

              <v-radio-group
                v-model="q3"
                :rules="[required]"
                label="データ活用への印象"
                inline
                class="mb-6"
              >
                <v-radio v-for="opt in fiveGood" :key="opt" :label="opt" :value="opt" />
              </v-radio-group>

              <!-- ───── 4. プライバシー懸念 ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                4. プライバシーとデータ利用への懸念
              </h3>

              <v-radio-group
                v-model="q4"
                :rules="[required]"
                label="プライバシー懸念の度合い"
                inline
              >
                <v-radio v-for="opt in fiveFeel" :key="opt" :label="opt" :value="opt" />
              </v-radio-group>

              <v-textarea
                v-if="q4DetailNeeded"
                v-model="q4Detail"
                :rules="[required]"
                label="懸念点を具体的に"
                rows="3"
                variant="outlined"
                density="comfortable"
                class="mb-6"
              />

              <!-- ───── 5. 学習モチベーション ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                5. 学習モチベーションへの影響
              </h3>

              <v-radio-group
                v-model="q5"
                :rules="[required]"
                label="モチベーションの変化"
                inline
                class="mb-6"
              >
                <v-radio v-for="opt in fiveMotivation" :key="opt" :label="opt" :value="opt" />
              </v-radio-group>

              <!-- 送信 -->
              <v-btn color="primary" block :loading="loading" type="submit">
                送信
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { VForm } from 'vuetify/components'
import axios from 'axios'

/* emit */
const emit = defineEmits<{ (e: 'submitted'): void }>()

/* v-form & loading */
const form    = ref<VForm | null>(null)
const loading = ref(false)

/* 質問 state */
const q1 = ref('')
const q2 = ref('')
const q3 = ref('')
const q4 = ref('')
const q4Detail = ref('')
const q5 = ref('')

const q4DetailNeeded = computed(() => ['非常に感じる','ある程度感じる'].includes(q4.value))

/* 定数・ルール */
const required = (v: unknown) => (v !== null && v !== '' && !(Array.isArray(v)&&!v.length)) || '必須'

const fiveUse        = ['積極的に活用したい','どちらかといえば活用したい','どちらともいえない','あまり活用したくない','全く活用したくない'] as const
const fiveValue      = ['非常に役立つ','ある程度役立つ','どちらともいえない','あまり役立たない','全く役立たない'] as const
const fiveGood       = ['非常に良いと思う','良いと思う','どちらともいえない','あまり良くないと思う','全く良くないと思う'] as const
const fiveFeel       = ['非常に感じる','ある程度感じる','どちらともいえない','あまり感じない','全く感じない'] as const
const fiveMotivation = ['非常に向上する','ある程度向上する','どちらともいえない','あまり向上しない','全く向上しない'] as const

/* API */
const API = import.meta.env.VITE_API_URL ??
            `${location.protocol}//${location.hostname}:8000`

async function submitForm() {
  if (q4DetailNeeded.value && !q4Detail.value.trim()) {
    alert('プライバシー懸念の具体的内容を記入してください')
    return
  }

  const { valid } = await form.value?.validate() ?? { valid:false }
  if (!valid) return

  loading.value = true
  try {
    await axios.post(`${API}/api/survey/student`, {
      q1_use:     q1.value,
      q2_value:   q2.value,
      q3_accept:  q3.value,
      q4_feel:    q4.value,
      q4_detail:  q4Detail.value,
      q5_motive:  q5.value,
    })
    emit('submitted')
  } finally { loading.value = false }
}
</script>
