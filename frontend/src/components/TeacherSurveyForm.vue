<template>
  <SurveyShell @submitted="emit('submitted')" :userType="'teacher'">
    <!-- 教師専用質問 -->
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

    <div>
      <label>Q1-2. 単位取得が厳しい学生に関する課題や困難（自由記述）:</label>
      <textarea v-model="q1_2"></textarea>
    </div>

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

    <div>
      <label>Q4-2. その他意見・期待:</label>
      <textarea v-model="q4_2"></textarea>
    </div>
  </SurveyShell>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SurveyShell from './SurveyShell.vue';

const emit = defineEmits(['submitted']);

// Q1-1 選択肢
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

const q1_1 = ref<string[]>([]);
const q1_1_other = ref('');
const q1_2 = ref('');
const q2 = ref('');
const q3_1 = ref<string[]>([]);
const q3_1_other = ref('');
const q4_1 = ref('');
const q4_2 = ref('');
</script>


