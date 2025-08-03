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
              <!-- 学年（大学/大学院） -->
              <div class="field-frame" :class="{ invalid: showInvalidGrade }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">
                    あなたの学年を教えてください（大学/大学院）
                  </h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>
                <v-select
                  v-model="grade"
                  :items="gradeOptions"
                  item-title="label"
                  item-value="value"
                  variant="outlined"
                  hide-details
                />
              </div>

              <!-- 質問1 -->
              <div class="field-frame" :class="{ invalid: showInvalidS1 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">
                    授業終わりに自分の理解度を確認したいと思いますか？
                  </h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>
                <v-radio-group v-model="s1_want_check" inline hide-details>
                  <v-radio label="思う" value="思う" />
                  <v-radio label="思わない" value="思わない" />
                </v-radio-group>
              </div>

              <!-- 説明文（1問目の直後に表示） -->
              <p class="text-subtitle-1 font-weight-bold mt-2 mb-6">
                私たちは講義終了後の感想アンケートから、その人の定期テスト点を予測する
                Webアプリを作成しようと考えています。
              </p>

              <!-- 質問2 -->
              <div class="field-frame" :class="{ invalid: showInvalidS2 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">
                    教師が講義で上記のWebアプリを導入する場合、どのような懸念点がありますか？（複数選択）
                  </h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>
                <v-checkbox
                  v-for="opt in s2_concern_opts"
                  :key="opt.value"
                  v-model="s2_concern"
                  :label="opt.label"
                  :value="opt.value"
                  hide-details
                />
                <v-text-field
                  v-if="s2_concern.includes('other')"
                  v-model="s2_concern_other"
                  :error="showErrors && invalidS2Other"
                  label="その他（具体的に）"
                  variant="outlined"
                  hide-details
                />
              </div>

              <!-- 質問3 -->
              <div class="field-frame" :class="{ invalid: showInvalidS3 }">
                <div class="d-flex align-center mb-2">
                  <h3 class="text-subtitle-1 font-weight-bold mb-0">
                    教師が理解度が足りない場合に対策をしてくれたら嬉しいですか？
                  </h3>
                  <v-chip class="req-chip" color="error" size="x-small" variant="tonal">必須</v-chip>
                </div>
                <v-radio-group v-model="s3_happy" inline hide-details>
                  <v-radio label="はい" value="はい" />
                  <v-radio label="いいえ" value="いいえ" />
                </v-radio-group>
              </div>

              <v-btn color="primary" block type="submit">送信</v-btn>
            </v-form>
          </v-card-text>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { VForm } from 'vuetify/components'
import axios from 'axios'

/* 学年オプション（学部/修士/博士） */
const gradeOptions = [
  { value: 'B1', label: '学部1年' },
  { value: 'B2', label: '学部2年' },
  { value: 'B3', label: '学部3年' },
  { value: 'B4', label: '学部4年' },
  { value: 'M1', label: '修士1年' },
  { value: 'M2', label: '修士2年' },
  { value: 'D1', label: '博士1年' },
  { value: 'D2', label: '博士2年' },
  { value: 'D3', label: '博士3年' },
] as const

const s2_concern_opts = [
  { value: 'accuracy',     label: '予測の精度や信頼性' },
  { value: 'privacy',      label: '学生のプライバシー保護・データ利用' },
  { value: 'workload',     label: '教員の業務負担の増加' },
  { value: 'transparency', label: 'データ利用の透明性' },
  { value: 'integration',  label: '学内システム・ワークフローとの連携' },
  { value: 'other',        label: 'その他' },
] as const

const form = ref<VForm | null>(null)
const loading = ref(false)
const emit = defineEmits<{ (e: 'submitted'): void }>()

/* state */
const grade = ref<string>('')                      // ★ 追加
const s1_want_check = ref<'思う' | '思わない' | ''>('')
const s2_concern = ref<string[]>([])
const s2_concern_other = ref('')
const s3_happy = ref<'はい' | 'いいえ' | ''>('')

/* エラー表示トグル：初期は false → 送信時 true */
const showErrors = ref(false)

watch(s2_concern, v => { if (!v.includes('other')) s2_concern_other.value = '' })

/* バリデーション */
const invalidGrade = computed(() => grade.value === '')                 // ★ 追加
const invalidS1    = computed(() => s1_want_check.value === '')
const invalidS2Other = computed(() =>
  s2_concern.value.includes('other') && !s2_concern_other.value.trim()
)
const invalidS2    = computed(() =>
  s2_concern.value.length === 0 || invalidS2Other.value
)
const invalidS3    = computed(() => s3_happy.value === '')

/* 表示用（赤枠は送信試行後のみ） */
const showInvalidGrade = computed(() => showErrors.value && invalidGrade.value) // ★ 追加
const showInvalidS1    = computed(() => showErrors.value && invalidS1.value)
const showInvalidS2    = computed(() => showErrors.value && invalidS2.value)
const showInvalidS3    = computed(() => showErrors.value && invalidS3.value)

/* API */
const API = import.meta.env.VITE_API_URL ?? `${location.protocol}//${location.hostname}:8000`

async function submitForm() {
  showErrors.value = true

  if (invalidGrade.value || invalidS1.value || invalidS2.value || invalidS3.value) {
    alert('未回答の必須項目があります。赤枠のセクションを確認してください。')
    return
  }

  loading.value = true
  try {
    await axios.post(`${API}/api/survey/student`, {
      grade:         grade.value,                              // ★ 追加
      s1_want_check: s1_want_check.value,
      s2_concern:    normalize(s2_concern.value, s2_concern_other.value),
      s3_happy:      s3_happy.value,
    })
    emit('submitted')
  } finally {
    loading.value = false
  }
}

/* ヘルパー：その他の正規化 */
function normalize(list: string[], otherText: string) {
  const set = new Set(list)
  set.delete('other')
  if (list.includes('other') && otherText.trim()) set.add(`other:${otherText.trim()}`)
  return Array.from(set)
}
</script>

<style scoped>
.req-chip{ display:inline-block; margin-left:.5rem; }

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

/* テキストフィールドは error=true で赤枠に。厚めにしたい場合は上書き */
:deep(.v-field--error .v-field__outline){
  border-width: 2px;
}
</style>

