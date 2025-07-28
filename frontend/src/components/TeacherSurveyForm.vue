<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card elevation="2">
          <v-card-title class="text-h6 font-weight-bold">
            教員向けアンケート
          </v-card-title>

          <v-card-text>
            <v-form ref="form" @submit.prevent="submitForm">
              <!-- ───── 1. 学習状況把握 ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                1. 学生の学習状況把握に関する現状と課題
              </h3>

              <p class="mb-1">
                学習到達度や理解度を把握する方法（該当するものを全て選択）
              </p>

              <v-checkbox
                v-for="opt in q1aOptions"
                :key="opt.value"
                v-model="q1a"
                :label="opt.label"
                :value="opt.value"
              />

              <v-text-field
                v-if="q1a.includes('other')"
                v-model="q1aOther"
                label="その他の具体的な方法"
                density="comfortable"
                class="mb-6"
              />

              <!-- ───── 2. 早期検知・支援 ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                2. 早期検知・早期支援の価値
              </h3>

              <v-radio-group
                v-model="q2a"
                :rules="[required]"
                label="どれくらい役立つか"
                inline
                class="mb-2"
              >
                <v-radio v-for="opt in likert5" :key="opt" :label="opt" :value="opt" />
              </v-radio-group>

              <p class="mb-1">希望する情報・通知（複数選択可）</p>

              <v-checkbox
                v-for="opt in q2bOptions"
                :key="opt.value"
                v-model="q2b"
                :label="opt.label"
                :value="opt.value"
              />

              <v-text-field
                v-if="q2b.includes('other')"
                v-model="q2bOther"
                label="その他 具体的に"
                density="comfortable"
                class="mb-6"
              />

              <!-- ───── 3. 講義改善 ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                3. 講義内容改善への貢献
              </h3>

              <v-radio-group
                v-model="q3a"
                :rules="[required]"
                label="どれくらい役立つか"
                inline
                class="mb-2"
              >
                <v-radio v-for="opt in likert5" :key="opt" :label="opt" :value="opt" />
              </v-radio-group>

              <p class="mb-1">望ましいフィードバック形式（複数選択可）</p>

              <v-checkbox
                v-for="opt in q3bOptions"
                :key="opt.value"
                v-model="q3b"
                :label="opt.label"
                :value="opt.value"
              />

              <v-text-field
                v-if="q3b.includes('other')"
                v-model="q3bOther"
                label="その他 具体的に"
                density="comfortable"
                class="mb-6"
              />

              <!-- ───── 4. 導入懸念 ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                4. 導入と運用に関する懸念
              </h3>

              <v-checkbox
                v-for="opt in q4Options"
                :key="opt.value"
                v-model="q4"
                :label="opt.label"
                :value="opt.value"
              />

              <v-text-field
                v-if="q4.includes('other')"
                v-model="q4Other"
                label="その他 具体的に"
                density="comfortable"
                class="mb-6"
              />

              <!-- ───── 5. 総合評価 ───── -->
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                5. 総合的な評価と今後の期待
              </h3>

              <v-radio-group
                v-model="q5a"
                :rules="[required]"
                label="大学全体への貢献度"
                inline
                class="mb-2"
              >
                <v-radio v-for="opt in likert5" :key="opt" :label="opt" :value="opt" />
              </v-radio-group>

              <v-textarea
                v-model="q5b"
                label="自由記述：期待・意見"
                rows="3"
                variant="outlined"
                density="comfortable"
                class="mb-6"
              />

              <!-- 送信 -->
              <v-btn color="primary" block type="submit" :loading="loading">
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
import { ref, watch } from 'vue'
import type { VForm } from 'vuetify/components'
import axios from 'axios'

/* emit */
const emit = defineEmits<{ (e: 'submitted'): void }>()

/* v-form & loading */
const form    = ref<VForm | null>(null)
const loading = ref(false)

/* 質問 state */
const q1a = ref<string[]>([]); const q1aOther = ref('')
const q2a = ref('');           const q2b = ref<string[]>([]); const q2bOther = ref('')
const q3a = ref('');           const q3b = ref<string[]>([]); const q3bOther = ref('')
const q4  = ref<string[]>([]); const q4Other = ref('')
const q5a = ref('');           const q5b = ref('')

/* “その他” を外したら自由記述をクリア */
watch(q1a, val => { if (!val.includes('other')) q1aOther.value = '' })
watch(q2b, val => { if (!val.includes('other')) q2bOther.value = '' })
watch(q3b, val => { if (!val.includes('other')) q3bOther.value = '' })
watch(q4,  val => { if (!val.includes('other')) q4Other.value = '' })

/* 定数・ルール */
const required = (v: unknown) => (v !== null && v !== '' && !(Array.isArray(v)&&!v.length)) || '必須'
const likert5 = ['非常に役立つ','ある程度役立つ','どちらともいえない','あまり役立たない','全く役立たない'] as const

const q1aOptions = [
  { value:'test',        label:'定期試験結果' },
  { value:'reaction',    label:'授業中の反応' },
  { value:'report',      label:'課題・レポート' },
  { value:'office',      label:'オフィスアワー' },
  { value:'direct',      label:'直接相談や様子' },
  { value:'other',       label:'その他' }
] as const

const q2bOptions = [
  { value:'name_score',    label:'氏名と成績傾向' },
  { value:'answer_excerpt',label:'回答文抜粋' },
  { value:'term_under',    label:'専門用語理解不足など' },
  { value:'learning_style',label:'学習方法傾向' },
  { value:'support_advice',label:'サポート策提案' },
  { value:'other',         label:'その他' }
] as const

const q3bOptions = [
  { value:'low_rate_topic', label:'理解度低い講義回' },
  { value:'term_list',      label:'用語リスト' },
  { value:'excerpt',        label:'回答文抜粋' },
  { value:'overall_tendency',label:'学習傾向分析' },
  { value:'material_advice',label:'資料改善提案' },
  { value:'other',          label:'その他' }
] as const

const q4Options = [
  { value:'accuracy',    label:'予測精度' },
  { value:'privacy',     label:'プライバシー' },
  { value:'workload',    label:'業務負担' },
  { value:'transparency',label:'データ透明性' },
  { value:'system_link', label:'システム連携' },
  { value:'other',       label:'その他' }
] as const

/* API */
const API = import.meta.env.VITE_API_URL ??
            `${location.protocol}//${location.hostname}:8000`

/* ヘルパー：選択肢を整形（other を除去し other:内容 だけ残す） */
function normalize(list: string[], otherText: string) {
  const set = new Set(list)
  set.delete('other')
  if (list.includes('other') && otherText.trim()) {
    set.add(`other:${otherText.trim()}`)
  }
  return Array.from(set)
}

async function submitForm() {
  const { valid } = await form.value?.validate() ?? { valid: false }
  if (!valid) return

  loading.value = true
  try {
    await axios.post(`${API}/api/survey/teacher`, {
      q1_method:   normalize(q1a.value, q1aOther.value),
      q2_value:    q2a.value,
      q2_notify:   normalize(q2b.value, q2bOther.value),
      q3_value:    q3a.value,
      q3_feedback: normalize(q3b.value, q3bOther.value),
      q4_concern:  normalize(q4.value,  q4Other.value),
      q5_value:    q5a.value,
      q5_free:     q5b.value,
    })
    emit('submitted')
  } finally {
    loading.value = false
  }
}
</script>