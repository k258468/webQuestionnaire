<!-- ============================================== -->
<!-- src/views/AdminView.vue                         -->
<!-- Vuetify での閲覧画面（タブ + data-table）        -->
<!-- ============================================== -->
<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="2">
          <v-card-title class="text-h6 font-weight-bold">
            アンケート結果（{{ tabLabel }}）
          </v-card-title>

          <v-card-text>
            <v-tabs v-model="tab" class="mb-4">
              <v-tab value="student">学生</v-tab>
              <v-tab value="teacher">教師</v-tab>
            </v-tabs>

            <v-alert
              v-if="error"
              type="error"
              variant="tonal"
              class="mb-4"
            >
              認証失敗またはデータ取得失敗
            </v-alert>

            <v-data-table
              :headers="headers"
              :items="rows"
              :loading="loading"
              loading-text="読み込み中..."
              class="elevation-1"
              density="comfortable"
            >
              <template #no-data>
                データがありません
              </template>
            </v-data-table>
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" prepend-icon="mdi-home" :to="{ name: 'Home' }">
              トップへ戻る
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

type Tab = 'student' | 'teacher'
type Header = { title: string; key: string }

const route = useRoute()
const pwd = (route.query.pwd as string) || ''

const tab = ref<Tab>('student')
const rows = ref<Record<string, unknown>[]>([])
const headers = ref<Header[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const tabLabel = computed(() => (tab.value === 'student' ? '学生' : '教師'))

const API_BASE: string =
  import.meta.env.VITE_API_URL ??
  `${window.location.protocol}//${window.location.hostname}:8000`

async function load() {
  loading.value = true
  error.value = null
  try {
    const { data } = await axios.get(
      `${API_BASE}/api/results/${tab.value}`,
      { params: { pwd } }
    )

    rows.value = Array.isArray(data) ? data : []
    headers.value = rows.value.length
      ? Object.keys(rows.value[0]).map((k) => ({ title: k, key: k }))
      : []
  } catch (e) {
    error.value = 'fetch_failed'
    rows.value = []
    headers.value = []
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(tab, load)
</script>
