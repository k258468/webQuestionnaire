<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" sm="10" md="8" lg="6">
        <v-card elevation="2">
          <v-card-title class="text-h6 font-weight-bold">
            アンケート
          </v-card-title>

          <v-card-text>
            <v-form ref="form" @submit.prevent="submitForm">
              <!-- 共通フィールド -->
              <v-text-field
                v-model.number="age"
                label="年齢"
                type="number"
                variant="outlined"
                density="comfortable"
                :rules="[required, isPositiveInt]"
                prepend-icon="mdi-numeric"
                class="mb-4"
                required
              />

              <v-radio-group
                v-model="gender"
                :rules="[required]"
                label="性別（1つ選択）"
                inline
                class="mb-4"
              >
                <v-radio
                  v-for="opt in genderOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </v-radio-group>

              <v-combobox
                v-model="interests"
                :items="interestOptions"
                item-title="label"
                item-value="value"
                :return-object="false"
                label="興味のある分野（複数選択可）"
                multiple
                chips
                closable-chips
                variant="outlined"
                density="comfortable"
                :rules="[minOne]"
                class="mb-6"
              />

              <!-- 学生 / 教師 固有フィールド（子側で描画） -->
              <slot />

              <v-btn
                type="submit"
                color="primary"
                block
                :loading="loading"
                :disabled="loading"
              >
                送信
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import type { VForm } from 'vuetify/components'
import axios, { isAxiosError } from 'axios'

type UserType = 'student' | 'teacher'
type Gender = 'male' | 'female' | 'other'
type Interest = 'it' | 'sports' | 'music' | 'travel'

type StudentPayload = {
  student_id: string
  age: number
  grade: string            // ★ サーバは string を要求
  gender: Gender
  interests: string[]      // ★ 文字列配列
}

type TeacherPayload = {
  age: number
  subject: string
  experience: number       // サーバが experience を期待している想定
  gender: Gender
  interests: string[]
}

const props = defineProps<{
  userType: UserType

  // Student 用（v-model:name / v-model:grade）
  name?: string
  grade?: number | null

  // Teacher 用（v-model:subject / v-model:years）
  subject?: string
  years?: number | null
}>()

const emit = defineEmits<{
  (e: 'submitted'): void
  (e: 'update:name', v: string): void
  (e: 'update:grade', v: number | null): void
  (e: 'update:subject', v: string): void
  (e: 'update:years', v: number | null): void
}>()

/** v-form */
const form = ref<VForm | null>(null)

/** 共通フォーム状態 */
const age = ref<number | null>(null)
const gender = ref<Gender | null>(null)
const interests = ref<(Interest | string)[]>([]) // combobox からは string が返る想定だが保険で union
const loading = ref(false)

/** 選択肢（共通） */
const genderOptions = [
  { value: 'male', label: '男性' },
  { value: 'female', label: '女性' },
  { value: 'other', label: 'その他' }
] as const

const interestOptions = [
  { value: 'it', label: 'IT' },
  { value: 'sports', label: 'スポーツ' },
  { value: 'music', label: '音楽' },
  { value: 'travel', label: '旅行' }
] as const

/** ルール */
const required = (v: unknown) =>
  (v !== null && v !== undefined && v !== '' && !(Array.isArray(v) && v.length === 0)) || '必須項目です'

const minOne = (v: unknown) =>
  (Array.isArray(v) && v.length > 0) || '少なくとも1つ選択してください'

const isPositiveInt = (v: unknown) =>
  (typeof v === 'number' && Number.isInteger(v) && v > 0) || '正の整数を入力してください'

/** API ベース URL */
const API_BASE: string =
  import.meta.env.VITE_API_URL ??
  `${window.location.protocol}//${window.location.hostname}:8000`

async function submitForm(e?: Event) {
  e?.preventDefault()
  console.log('[submit] called')

  const result = await form.value?.validate()
  console.log('[submit] validate:', result)
  if (!result?.valid) return

  // interests を必ず string[] へ
  const interestsForApi = interests.value.map(i => String(i))

  // props の必須値チェック
  if (props.userType === 'student') {
    if (!props.name || props.grade == null) {
      console.warn('[submit] missing student props', { name: props.name, grade: props.grade })
      return
    }
  } else {
    if (!props.subject || props.years == null) {
      console.warn('[submit] missing teacher props', { subject: props.subject, years: props.years })
      return
    }
  }
  if (age.value == null || !gender.value || interestsForApi.length === 0) {
    console.warn('[submit] missing common', { age: age.value, gender: gender.value, interestsForApi })
    return
  }

  loading.value = true
  try {
    let endpoint = ''
    let payload: StudentPayload | TeacherPayload

    if (props.userType === 'student') {
      payload = {
        student_id: props.name!,
        age: age.value!,
        grade: String(props.grade!),              // ★ 文字列化
        gender: gender.value!,
        interests: interestsForApi,
      }
      endpoint = `${API_BASE}/api/survey/student`
    } else {
      payload = {
        age: age.value!,
        subject: props.subject!,
        experience: props.years!,                 // ★ サーバ仕様に合わせる
        gender: gender.value!,
        interests: interestsForApi,
      }
      endpoint = `${API_BASE}/api/survey/teacher`
    }

    console.log('[submit] endpoint:', endpoint)
    console.log('[submit] payload:', payload)

    const res = await axios.post(endpoint, payload)
    console.log('[submit] response:', res.status, res.data)

    form.value?.resetValidation()
    emit('submitted')
  } catch (err) {
    if (isAxiosError(err)) {
      console.error('[submit] axios error status:', err.response?.status)
      console.error('[submit] axios error data  :', err.response?.data)
      const d = err.response?.data as any
      if (d?.detail) console.table(d.detail)
    } else {
      console.error('[submit] error:', err)
    }
  } finally {
    loading.value = false
  }
}

/** userType 切替時に古いバリデーションを消す */
watch(
  () => props.userType,
  () => form.value?.resetValidation()
)
</script>

