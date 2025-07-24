<template>
  <form @submit.prevent="submitForm">
    <!-- 共通フィールド -->
    <div>
      <label>年齢:</label>
      <input v-model.number="age" type="number" required />
    </div>

    <!-- 学生用の質問 -->
    <div v-if="userType === 'student'">
      <div>
        <label>学籍番号:</label>
        <input v-model="studentId" required />
      </div>
      <div>
        <label>学年:</label>
        <select v-model="grade" required>
          <option value="" disabled>選択してください</option>
          <option value="1">1年</option>
          <option value="2">2年</option>
          <option value="3">3年</option>
          <option value="4">4年</option>
        </select>
      </div>
    </div>

    <!-- 教師用の質問 -->
    <div v-else-if="userType === 'teacher'">
      <div>
        <label>担当科目:</label>
        <input v-model="subject" required />
      </div>
      <div>
        <label>教歴（年数）:</label>
        <input v-model.number="experience" type="number" required />
      </div>
    </div>

    <!-- 性別 -->
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

    <!-- 興味のある分野 -->
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

const props = defineProps<{ userType: 'student' | 'teacher' }>();
const emit = defineEmits(['submitted']);

/* 共通フォーム状態 */
const age = ref<number | null>(null);
const gender = ref<string | null>(null);
const interests = ref<string[]>([]);
const loading = ref(false);

/* 個別フォーム状態 */
const studentId = ref('');
const grade = ref('');
const subject = ref('');
const experience = ref<number | null>(null);

/* 選択肢 */
const genderOptions = [
  { value: 'male', label: '男性' },
  { value: 'female', label: '女性' },
  { value: 'other', label: 'その他' },
];
const interestOptions = [
  { value: 'it', label: 'IT' },
  { value: 'sports', label: 'スポーツ' },
  { value: 'music', label: '音楽' },
  { value: 'travel', label: '旅行' },
];

function selectSingleCheckbox(val: string) {
  gender.value = gender.value === val ? null : val;
}

const API_BASE =
  import.meta.env.VITE_API_URL ||
  `${window.location.protocol}//${window.location.hostname}:8000`;

async function submitForm() {
  if (age.value === null) {
    alert('年齢を入力してください。');
    return;
  }
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
    let payload: any;
    let endpoint: string;

    if (props.userType === 'student') {
      if (!studentId.value) {
        alert('学籍番号を入力してください。');
        loading.value = false;
        return;
      }
      if (!grade.value) {
        alert('学年を選択してください。');
        loading.value = false;
        return;
      }

      endpoint = `${API_BASE}/api/survey/student`;
      payload = {
        student_id: studentId.value,
        age: age.value,
        grade: grade.value,
        gender: gender.value,
        interests: interests.value,
      };
    } else {
      // teacher
      if (!subject.value) {
        alert('担当科目を入力してください。');
        loading.value = false;
        return;
      }
      if (experience.value === null) {
        alert('教歴（年数）を入力してください。');
        loading.value = false;
        return;
      }

      endpoint = `${API_BASE}/api/survey/teacher`;
      payload = {
        age: age.value,
        subject: subject.value,
        experience: experience.value,
        gender: gender.value,
        interests: interests.value,
      };
    }

    await axios.post(endpoint, payload);

    // フォームリセット
    studentId.value = '';
    grade.value = '';
    subject.value = '';
    experience.value = null;
    age.value = null;
    gender.value = null;
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




