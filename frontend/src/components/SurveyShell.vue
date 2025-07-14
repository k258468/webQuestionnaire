<template>
  <form @submit.prevent="submitForm">
    <!-- 共通フィールド -->
    

    <div>
      <label>年齢:</label>
      <input v-model.number="age" type="number" required />
    </div>

    <!-- slot がフォームの中にある！ -->
    <slot></slot>

    <!-- 共通部分 -->
    <div>
      <label>性別(1つ選択):</label>
      <div v-for="opt in genderOptions" :key="opt.value">
        <input
          type="checkbox"
          :value="opt.value"
          :checked="gender === opt.value"
          @change="selectSingleCheckbox(opt.value)"
        />
        {{ opt.label }}
      </div>
    </div>

    <div>
      <label>興味のある分野(複数選択可):</label>
      <div v-for="opt in interestOptions" :key="opt.value">
        <input
          type="checkbox"
          :value="opt.value"
          v-model="interests"
        />
        {{ opt.label }}
      </div>
    </div>

    <button type="submit" :disabled="loading">
      {{ loading ? '送信中...' : '送信' }}
    </button>
  </form>
</template>


<script lang="ts" setup>
import { ref } from 'vue';
import axios from 'axios';

/* ---------------- props / emits ---------------- */
const props = defineProps<{ userType: string }>();
const emit = defineEmits(['submitted']);

/* ---------------- フォーム状態 ---------------- */
const name       = ref('');
const age        = ref<number | null>(null);
const feedback   = ref('');
const gender     = ref<string | null>(null);
const interests  = ref<string[]>([]);
const loading    = ref(false);

/* ---------------- 選択肢 ---------------- */
const genderOptions = [
  { value: 'male',   label: '男性' },
  { value: 'female', label: '女性' },
  { value: 'other',  label: 'その他' },
];

const interestOptions = [
  { value: 'it',     label: 'IT' },
  { value: 'sports', label: 'スポーツ' },
  { value: 'music',  label: '音楽' },
  { value: 'travel', label: '旅行' },
];

/* ---------------- 単一選択制御 ---------------- */
function selectSingleCheckbox(val: string) {
  gender.value = gender.value === val ? null : val;
}

/* ---------------- 送信処理 ---------------- */
const API_BASE = 
  import.meta.env.VITE_API_URL ||
  `${window.location.protocol}//${window.location.hostname}:8000`;

async function submitForm() {
  /* クライアント側バリデーション */
  if (!gender.value) {
    alert('性別を1つ選択してください。');
    return;
  }
  if (interests.value.length === 0) {
    alert('興味のある分野を少なくとも1つ選択してください。');
    return;
  }

  loading.value = true;
  try {
    await axios.post(`${API_BASE}/api/survey`, {
      name:       name.value,
      age:        age.value,
      feedback:   feedback.value,
      userType:   props.userType,
      gender:     gender.value,
      interests:  interests.value,
    });

    /* 成功：フォームリセット & 画面遷移 */
    name.value      = '';
    age.value       = null;
    feedback.value  = '';
    gender.value    = null;
    interests.value = [];
    emit('submitted');
  } catch (err) {
    console.error('送信エラー:', err);
    alert('送信に失敗しました。時間を置いて再度お試しください。');
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 420px;
}

button[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>




