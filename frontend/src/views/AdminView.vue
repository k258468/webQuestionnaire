<template>
  <div>
    <h2>アンケート結果（{{ tabLabel }}）</h2>

    <select v-model="tab" @change="load">
      <option value="student">学生</option>
      <option value="teacher">教師</option>
    </select>

     <!-- グラフ画像の表示 -->
    <div style="margin: 1rem 0;">
      <img :src="chartImageUrl" alt="アンケートグラフ" width="600" v-if="chartImageUrl" />
    </div>

    <table v-if="rows.length">
      <thead>
        <tr><th v-for="h in headers" :key="h">{{ h }}</th></tr>
      </thead>
      <tbody>
        <tr v-for="(r,i) in rows" :key="i">
          <td v-for="h in headers" :key="h">{{ r[h] }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>データがありません</p>
    <router-link to="/">トップへ戻る</router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const pwd = route.query.pwd as string || '';

const tab = ref<'student'|'teacher'>('student');
const rows = ref<any[]>([]);
const headers = ref<string[]>([]);

const tabLabel = computed(() => tab.value === 'student' ? '学生' : '教師');

// 画像URL（タブに応じて切り替える）
const chartImageUrl = computed(() => {
  return `http://localhost:8000/static/admin/chart_${tab.value}.png?${Date.now()}`;
});

async function load() {
  try {
    const { data } = await axios.get(`http://localhost:8000/api/results/${tab.value}`, {
      params: { pwd },
    });
    rows.value = data;
    headers.value = data.length ? Object.keys(data[0]) : [];
  } catch (e) {
    alert('認証失敗またはデータ取得失敗');
    rows.value = [];
  }
}

onMounted(load);
watch(tab, load);
</script>
