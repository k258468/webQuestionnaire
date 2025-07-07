<template>
  <form @submit.prevent="submitForm">
    <p>アンケート対象：{{ userType === 'teacher' ? '教師' : '学生' }}</p>
    <div>
      <label>お名前:</label>
      <input v-model="name" required />
    </div>
    <div>
      <label>年齢:</label>
      <input v-model="age" type="number" required />
    </div>
    <div>
      <label>ご意見:</label>
      <textarea v-model="feedback" required></textarea>
    </div>

    <!-- 単一選択チェックボックス(性別) -->
    <div>
      <label>性別（1つだけ選択してください）:</label>
      <div v-for="option in genderOptions" :key="option.value">
        <input
          type="checkbox"
          :value="option.value"
          :checked="gender === option.value"
          @change="selectSingleCheckbox(option.value)"
        />
        {{ option.label }}
      </div>
    </div>

    <!-- 複数選択チェックボックス(興味のある分野) -->
    <div>
      <label>興味のある分野（複数選択可）:</label>
      <div v-for="option in interestOptions" :key="option.value">
        <input
          type="checkbox"
          :value="option.value"
          v-model="interests"
        />
        {{ option.label }}
      </div>
    </div>

    <button type="submit">送信</button>
  </form>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
const props = defineProps<{ userType: string }>();

const name = ref('');
const age = ref<number | null>(null);
const feedback = ref('');

// 単一選択の性別用
const gender = ref<string | null>(null);
const genderOptions = [
  { value: 'male', label: '男性' },
  { value: 'female', label: '女性' },
  { value: 'other', label: 'その他' },
];

// 複数選択の興味分野用
const interests = ref<string[]>([]);
const interestOptions = [
  { value: 'it', label: 'IT' },
  { value: 'sports', label: 'スポーツ' },
  { value: 'music', label: '音楽' },
  { value: 'travel', label: '旅行' },
];

// チェックボックス1つだけ選択させるための関数
const selectSingleCheckbox = (selected: string) => {
  if (gender.value === selected) {
    gender.value = null; // 同じものクリックで解除も可
  } else {
    gender.value = selected;
  }
};

const emit = defineEmits(['submitted']);

//名前、年齢、意見の警告は直接HTML上で指定されている。性別と興味はvue使ってる。
const submitForm = () => {
  if (!gender.value) { //警告
    alert('性別を1つ選択してください。');
    return;
  }

  if (interests.value.length === 0) {
    alert('興味のある分野を少なくとも1つ選択してください。');
    return;
  }

  console.log('送信内容:', {
    name: name.value,
    age: age.value,
    feedback: feedback.value,
    userType: props.userType,
    gender: gender.value,
    interests: interests.value,
  });
  emit('submitted', {
    name: name.value,
    age: age.value,
    feedback: feedback.value,
    userType: props.userType,
    gender: gender.value,
    interests: interests.value,
  });
};
</script>

