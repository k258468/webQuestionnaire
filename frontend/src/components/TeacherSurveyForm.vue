<!-- src/components/TeacherSurveyForm.vue -->
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
              <!-- 授業理解度を確認しているか -->
              <div class="field-frame" :class="{ invalid: showInvalidQ1 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">
                    中間・期末試験やレポート以外で、生徒の授業理解度を確認していますか？
                  </h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>
                <v-radio-group v-model="q1_check" inline hide-details>
                  <v-radio label="している" value="している" />
                  <v-radio label="していない" value="していない" />
                </v-radio-group>
              </div>

              <!-- 把握手段（複数） -->
              <div v-if="q1_check === 'している'" class="field-frame" :class="{ invalid: showInvalidQ11 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">どのような方法で把握していますか?（複数選択可）</h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>

                <v-checkbox
                  v-for="opt in q11_how_opts"
                  :key="opt.value"
                  v-model="q11_how"
                  :label="opt.label"
                  :value="opt.value"
                  hide-details
                />
                <v-text-field
                  v-if="q11_how.includes('other')"
                  v-model="q11_how_other"
                  label="その他（具体的に）"
                  density="comfortable"
                  variant="outlined"
                  hide-details
                />
              </div>

              <!-- 活用方法（複数） -->
              <div v-if="q1_check === 'している'" class="field-frame" :class="{ invalid: showInvalidQ12 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">把握した授業理解度をどのように活用していますか？（複数選択可）</h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>

                <v-checkbox
                  v-for="opt in q12_use_opts"
                  :key="opt.value"
                  v-model="q12_use"
                  :label="opt.label"
                  :value="opt.value"
                  hide-details
                />
                <v-text-field
                  v-if="q12_use.includes('other')"
                  v-model="q12_use_other"
                  label="その他（具体的に）"
                  density="comfortable"
                  variant="outlined"
                  hide-details
                  class="mb-2"
                />
              </div>

              <!-- 確認したいか -->
              <div v-else-if="q1_check === 'していない'" class="field-frame" :class="{ invalid: showInvalidQ21 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">できれば、生徒の授業理解度を確認したいですか？</h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>
                <v-radio-group v-model="q21_want" inline hide-details>
                  <v-radio label="したい" value="したい" />
                  <v-radio label="したくない" value="したくない" />
                </v-radio-group>
              </div>

              <!-- したい：理由（複数） -->
              <div v-if="q1_check === 'していない' && q21_want === 'したい'" class="field-frame" :class="{ invalid: showInvalidQ211 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">現状確認していない理由を教えてください（複数選択）</h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>

                <v-checkbox
                  v-for="opt in q211_reason_opts"
                  :key="opt.value"
                  v-model="q211_reason"
                  :label="opt.label"
                  :value="opt.value"
                  hide-details
                />
                <v-text-field
                  v-if="q211_reason.includes('other')"
                  v-model="q211_reason_other"
                  label="その他（具体的に）"
                  density="comfortable"
                  variant="outlined"
                  hide-details
                />
              </div>

              <!-- したくない：自由記述（任意） -->
              <div v-if="q1_check === 'していない' && q21_want === 'したくない'" class="field-frame">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">よろしければ、なぜしたくないのか教えてください（自由記述・任意）</h3>
                </div>
                <v-textarea
                  v-model="q212_reason_free"
                  rows="3"
                  variant="outlined"
                  density="comfortable"
                  hide-details
                />
              </div>

              <!-- 説明文（1問目の直後に表示） -->
              <p class="text-subtitle-1 font-weight-bold mt-2 mb-6">
                私たちは講義終了後の感想アンケートから、その人の定期テスト点を予測する
                Webアプリを作成しようと考えています。
              </p>

              <!-- Webアプリの利点 -->
              <div class="field-frame" :class="{ invalid: showInvalidQ2 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">上記のWebアプリを使う利点を教えてください（複数選択）</h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>

                <v-checkbox
                  v-for="opt in q2_advantage_opts"
                  :key="opt.value"
                  v-model="q2_advantage"
                  :label="opt.label"
                  :value="opt.value"
                  hide-details
                />
                <v-text-field
                  v-if="q2_advantage.includes('other')"
                  v-model="q2_advantage_other"
                  label="その他（具体的に）"
                  density="comfortable"
                  variant="outlined"
                  hide-details
                />
              </div>

              <!-- 懸念点 -->
              <div class="field-frame" :class="{ invalid: showInvalidQ3 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">上記のWebアプリを利用する際の懸念点を教えてください（複数選択）</h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>

                <v-checkbox
                  v-for="opt in q3_concern_opts"
                  :key="opt.value"
                  v-model="q3_concern"
                  :label="opt.label"
                  :value="opt.value"
                  hide-details
                />
                <v-text-field
                  v-if="q3_concern.includes('other')"
                  v-model="q3_concern_other"
                  label="その他（具体的に）"
                  density="comfortable"
                  variant="outlined"
                  hide-details
                />
              </div>

              <!-- 使いたい？ -->
              <div class="field-frame" :class="{ invalid: showInvalidQ4 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">
                    上記のWebアプリを実際に使用したいと思いますか？
                  </h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>

                <v-radio-group v-model="q4_use" inline hide-details>
                  <v-radio label="思う" value="思う" />
                  <v-radio label="思わない" value="思わない" />
                </v-radio-group>
              </div>

              <!-- 思わない理由（任意） -->
              <div v-if="q4_use === '思わない'" class="field-frame">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">よろしければ、思わない理由を教えてください（自由記述・任意）</h3>
                </div>
                <v-textarea
                  v-model="q4_use_reason"
                  rows="3"
                  variant="outlined"
                  density="comfortable"
                  hide-details
                />
              </div>

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
import { ref, watch, computed } from 'vue'
import type { VForm } from 'vuetify/components'
import axios from 'axios'

const form = ref<VForm | null>(null)
const loading = ref(false)
const emit = defineEmits<{ (e: 'submitted'): void }>()

/** Q state */
const q1_check = ref<'している' | 'していない' | ''>('')
const q11_how = ref<string[]>([])
const q11_how_other = ref('')
const q12_use = ref<string[]>([])
const q12_use_other = ref('')

const q21_want = ref<'したい' | 'したくない' | ''>('')
const q211_reason = ref<string[]>([])
const q211_reason_other = ref('')
const q212_reason_free = ref('')

const q2_advantage = ref<string[]>([])
const q2_advantage_other = ref('')

const q3_concern = ref<string[]>([])
const q3_concern_other = ref('')

const q4_use = ref<'思う' | '思わない' | ''>('')
const q4_use_reason = ref('')

/** 送信時のみエラー枠を出す */
const showErrors = ref(false)

/** “その他”のテキストは未入力でもOK（任意）なので、単に保持だけ */
watch(q11_how, v => { if (!v.includes('other')) q11_how_other.value = '' })
watch(q12_use, v => { if (!v.includes('other')) q12_use_other.value = '' })
watch(q211_reason, v => { if (!v.includes('other')) q211_reason_other.value = '' })
watch(q2_advantage, v => { if (!v.includes('other')) q2_advantage_other.value = '' })
watch(q3_concern, v => { if (!v.includes('other')) q3_concern_other.value = '' })
watch(q4_use, v => { if (v !== '思わない') q4_use_reason.value = '' })

/** options */
const q11_how_opts = [
  { value: 'quiz',   label: '小テストの実施' },
  { value: 'react',  label: '授業中の学生からの質問や反応' },
  { value: 'report', label: '課題やレポート' },
  { value: 'office', label: 'オフィスアワーでの相談' },
  { value: 'direct', label: '学生からの直接相談・様子から判断' },
  { value: 'other',  label: 'その他' },
] as const

const q12_use_opts = [
  { value: 'material', label: '講義の方針立てや資料の改善' },
  { value: 'exam',     label: '期末テストの難易度調整' },
  { value: 'assign',   label: '課題の量や難易度の調整' },
  { value: 'office',   label: 'オフィスアワーでの活用' },
  { value: 'other',    label: 'その他' },
] as const

const q211_reason_opts = [
  { value: 'no_method', label: '確認する手段がない' },
  { value: 'no_time',   label: '小テスト作成や採点の時間がない' },
  { value: 'too_many',  label: '受講者数が多すぎる' },
  { value: 'other',     label: 'その他' },
] as const

const q2_advantage_opts = [
  { value: 'no_test',       label: 'テストやレポート作成なしで確認できる' },
  { value: 'many_overview', label: '受講者が多くても一目で把握できる' },
  { value: 'paperless',     label: '紙媒体の必要がない' },
  { value: 'quality',       label: '講義の質がわかる' },
  { value: 'everytime',     label: '毎講義理解度確認ができる' },
  { value: 'other',         label: 'その他' },
] as const

const q3_concern_opts = [
  { value: 'accuracy',     label: '予測の精度や信頼性' },
  { value: 'privacy',      label: '学生のプライバシー・データ利用' },
  { value: 'workload',     label: '教員の業務負担の増加' },
  { value: 'transparency', label: 'データ利用の透明性' },
  { value: 'integration',  label: '既存システム・ワークフローとの連携' },
  { value: 'other',        label: 'その他' },
] as const

/** その他テキストは任意：other はそのまま保持、テキストがあれば other:xxx に変換 */
function normalize(list: string[], otherText: string) {
  const hasOther = list.includes('other')
  const filtered = list.filter(v => v !== 'other')
  if (hasOther && otherText.trim()) {
    filtered.push(`other:${otherText.trim()}`)
  } else if (hasOther) {
    filtered.push('other')
  }
  return filtered
}

/** --- 必須チェック（可視の設問のみ） --- */
const invalidQ1   = computed(() => q1_check.value === '')
const invalidQ11  = computed(() => q1_check.value === 'している'   && q11_how.value.length === 0)
const invalidQ12  = computed(() => q1_check.value === 'している'   && q12_use.value.length === 0)
const invalidQ21  = computed(() => q1_check.value === 'していない' && q21_want.value === '')
const invalidQ211 = computed(() => q1_check.value === 'していない' && q21_want.value === 'したい' && q211_reason.value.length === 0)
const invalidQ2   = computed(() => q2_advantage.value.length === 0)
const invalidQ3   = computed(() => q3_concern.value.length === 0)
const invalidQ4   = computed(() => q4_use.value === '')

/** 表示用（送信後のみ赤枠） */
const showInvalidQ1   = computed(() => showErrors.value && invalidQ1.value)
const showInvalidQ11  = computed(() => showErrors.value && invalidQ11.value)
const showInvalidQ12  = computed(() => showErrors.value && invalidQ12.value)
const showInvalidQ21  = computed(() => showErrors.value && invalidQ21.value)
const showInvalidQ211 = computed(() => showErrors.value && invalidQ211.value)
const showInvalidQ2   = computed(() => showErrors.value && invalidQ2.value)
const showInvalidQ3   = computed(() => showErrors.value && invalidQ3.value)
const showInvalidQ4   = computed(() => showErrors.value && invalidQ4.value)

/** API base */
const API = import.meta.env.VITE_API_URL ?? `${location.protocol}//${location.hostname}:8000`

async function submitForm() {
  showErrors.value = true

  const anyInvalid =
    invalidQ1.value || invalidQ11.value || invalidQ12.value ||
    invalidQ21.value || invalidQ211.value ||
    invalidQ2.value || invalidQ3.value || invalidQ4.value

  if (anyInvalid) {
    alert('未回答の必須項目があります。赤枠のセクションを確認してください。')
    return
  }

  loading.value = true
  try {
    await axios.post(`${API}/api/survey/teacher`, {
      q1_check: q1_check.value,
      q11_how: normalize(q11_how.value, q11_how_other.value),
      q12_use: normalize(q12_use.value, q12_use_other.value),

      q21_want: q21_want.value || null,
      q211_reason: q21_want.value === 'したい' ? normalize(q211_reason.value, q211_reason_other.value) : [],
      q212_reason_free: q21_want.value === 'したくない' ? q212_reason_free.value : '',  // 任意

      q2_advantage: normalize(q2_advantage.value, q2_advantage_other.value),
      q3_concern: normalize(q3_concern.value, q3_concern_other.value),

      q4_use: q4_use.value,
      q4_use_reason: q4_use.value === '思わない' ? q4_use_reason.value : '',          // 任意
    })
    emit('submitted')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.req-chip { display: inline-block; margin-left: .5rem; }

/* セクション枠（通常） */
.field-frame{
  padding: 12px;
  border-radius: 12px;
  transition: border-color .2s, box-shadow .2s, background-color .2s;
}

/* セクション枠（未回答のとき赤枠＋淡い背景） */
.field-frame.invalid{
  border: 2px solid var(--v-theme-error);
  background: rgba(244, 67, 54, 0.06);
}

/* Vuetify のエラーフィールドの枠を少し太く（テキスト系のとき） */
:deep(.v-field--error .v-field__outline){
  border-width: 2px;
}
</style>