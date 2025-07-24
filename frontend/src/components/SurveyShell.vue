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

      <hr />

      <!-- Q1-1 複数選択 -->
      <div>
        <label>Q1-1. 学生の学習到達度や理解度の把握方法（複数選択可）:</label>
        <div v-for="opt in q1Options" :key="opt.value">
          <input type="checkbox" :value="opt.value" v-model="q1_1" />
          {{ opt.label }}
        </div>
        <div>
          その他: <input v-model="q1_1_other" placeholder="具体的に" />
        </div>
      </div>

      <!-- Q1-2 自由記述 -->
      <div>
        <label>Q1-2. 単位取得が厳しい学生に関する課題や困難:</label>
        <textarea v-model="q1_2" rows="3" />
      </div>

      <!-- Q2 単一選択 -->
      <div>
        <label>Q2. Webアプリの役立ち度:</label>
        <select v-model="q2" required>
          <option disabled value="">選択してください</option>
          <option value="very_useful">非常に役立つ</option>
          <option value="somewhat_useful">ある程度役立つ</option>
          <option value="neutral">どちらともいえない</option>
          <option value="not_much_useful">あまり役立たない</option>
          <option value="not_useful">全く役立たない</option>
        </select>
      </div>

      <!-- Q3-1 複数選択 -->
      <div>
        <label>Q3-1. 導入懸念（複数選択可）:</label>
        <div v-for="opt in q3Options" :key="opt.value">
          <input type="checkbox" :value="opt.value" v-model="q3_1" />
          {{ opt.label }}
        </div>
        <div>
          その他: <input v-model="q3_1_other" placeholder="具体的に" />
        </div>
      </div>

      <!-- Q4-1 単一選択 -->
      <div>
        <label>Q4-1. 大学全体への貢献度:</label>
        <select v-model="q4_1" required>
          <option disabled value="">選択してください</option>
          <option value="very_contribute">非常に貢献する</option>
          <option value="somewhat_contribute">ある程度貢献する</option>
          <option value="neutral">どちらともいえない</option>
          <option value="not_much_contribute">あまり貢献しない</option>
          <option value="not_contribute">全く貢献しない</option>
        </select>
      </div>

      <!-- Q4-2 自由記述 -->
      <div>
        <label>Q4-2. その他意見・期待:</label>
        <textarea v-model="q4_2" rows="3" />
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

/* 学生用フォーム状態 */
const studentId = ref('');
const grade = ref('');

/* 教師用フォーム状態 */
const subject = ref('');
const experience = ref<number | null>(null);

const q1_1 = ref<string[]>([]);
const q1_1_other = ref('');
const q1_2 = ref('');
const q2 = ref('');
const q3_1 = ref<string[]>([]);
const q3_1_other = ref('');
const q4_1 = ref('');
const q4_2 = ref('');

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
const q1Options = [
  { value: 'test_results', label: '定期試験や小テストの結果' },
  { value: 'questions', label: '授業中の学生からの質問や反応' },
  { value: 'assignments', label: '課題やレポートの内容' },
  { value: 'office_hours', label: 'オフィスアワーでの相談' },
  { value: 'direct_consult', label: '学生からの直接の相談や、学生の様子から判断' },
];
const q3Options = [
  { value: 'accuracy', label: '予測の精度や信頼性への疑問' },
  { value: 'privacy', label: '学生のプライバシー保護やデータ利用に関する懸念' },
  { value: 'workload', label: '教員の業務負担の増加' },
  { value: 'transparency', label: 'データ利用の透明性' },
  { value: 'integration', label: '既存の学内システムやワークフローとの連携' },
];

function selectSingleCheckbox(val: string) {
  gender.value = gender.value === val ? null : val;
}

const API_BASE =
  import.meta.env.VITE_API_URL ||
  `${window.location.protocol}//${window.location.hostname}:8000`;

async function submitForm() {
  // 共通バリデーション
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

  let payload: any;
  let endpoint: string;

  if (props.userType === 'student') {
    if (!studentId.value) {
      alert('学籍番号を入力してください。');
      return;
    }
    if (!grade.value) {
      alert('学年を選択してください。');
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
    // 教師用の追加バリデーション
    if (!subject.value) {
      alert('担当科目を入力してください。');
      return;
    }
    if (experience.value === null) {
      alert('教歴（年数）を入力してください。');
      return;
    }
    if (!q2.value) {
      alert('Q2を選択してください。');
      return;
    }
    if (!q4_1.value) {
      alert('Q4-1を選択してください。');
      return;
    }

    endpoint = `${API_BASE}/api/survey/teacher`;
    payload = {
      age: age.value,
      gender: gender.value,
      interests: interests.value,
      subject: subject.value,
      experience: experience.value,
      q1_1: q1_1.value,
      q1_1_other: q1_1_other.value,
      q1_2: q1_2.value,
      q2: q2.value,
      q3_1: q3_1.value,
      q3_1_other: q3_1_other.value,
      q4_1: q4_1.value,
      q4_2: q4_2.value,
    };
  }

  loading.value = true;

  try {
    await axios.post(endpoint, payload);

    // フォームリセット
    studentId.value = '';
    grade.value = '';
    subject.value = '';
    experience.value = null;
    q1_1.value = [];
    q1_1_other.value = '';
    q1_2.value = '';
    q2.value = '';
    q3_1.value = [];
    q3_1_other.value = '';
    q4_1.value = '';
    q4_2.value = '';
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





