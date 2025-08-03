<!-- src/views/AdminView.vue -->
<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="2">
          <v-card-title class="text-h6 font-weight-bold">
            アンケート結果（{{ tabLabel }}）
          </v-card-title>

          <v-card-text>
            <!-- ─── タブ ─── -->
            <v-tabs v-model="tab" class="mb-4">
              <v-tab value="student">学生</v-tab>
              <v-tab value="teacher">教師</v-tab>
            </v-tabs>

            <!-- ─── エラー表示 ─── -->
            <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
              {{ error }}
            </v-alert>

            <!-- ─── CSV テーブル ─── -->
            <v-data-table
              :headers="headers"
              :items="rows"
              :loading="loading"
              loading-text="読み込み中..."
              density="comfortable"
              class="elevation-1"
            >
              <!-- 画像セルプレビュー -->
              <template #item="{ item, columns }">
                <tr>
                  <td
                    v-for="(col, idx) in columns"
                    :key="`${col.key ?? 'col'}-${idx}`"
                  >
                    <template v-if="isImage(cellValue(item, col.key) as string)">
                      <v-img
                        :src="imageSrc(cellValue(item, col.key) as string)"
                        max-width="128"
                        max-height="128"
                        contain
                      />
                    </template>
                    <template v-else>
                      {{ cellValue(item, col.key) }}
                    </template>
                  </td>
                </tr>
              </template>

              <template #no-data>データがありません</template>
            </v-data-table>

            <!-- ─── 固定グラフ表示 ─── -->
            <v-divider class="my-6" />

            <h3 class="text-subtitle-1 mb-2">集計グラフ</h3>

            <div v-if="chartSrc" class="d-flex justify-center">
              <v-img :src="chartSrc" max-width="640" class="rounded" />
            </div>
            <p v-else class="text-body-2">
              表示するグラフがありません（static/admin に chart_*.png を置いてください）
            </p>

            <!-- ─── static フォルダ画像一覧（任意） ─── -->
            <v-divider class="my-6" />

            <h3 class="text-subtitle-1 mb-2">static フォルダの画像一覧</h3>

            <v-row dense v-if="images.length">
              <v-col v-for="img in images" :key="img" cols="4" sm="3" md="2">
                <v-img :src="imageSrc(img)" aspect-ratio="1" cover class="rounded" />
                <div class="text-caption mt-1 text-truncate">{{ img }}</div>
              </v-col>
            </v-row>
            <p v-else class="text-body-2">画像はありません</p>
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn
              color="primary"
              prepend-icon="mdi-home"
              :to="{ name: 'Home' }"
            >
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

/* ---------- 型 ---------- */
type Tab = 'student' | 'teacher'
type Header = { title: string; key: string }

/* ---------- ルートパラメータ ---------- */
const route = useRoute()
const pwd = (route.query.pwd as string) ?? ''

/* ---------- reactive state ---------- */
const tab = ref<Tab>('student')
const rows = ref<Record<string, unknown>[]>([])
const headers = ref<Header[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

/* static 画像一覧 */
const images = ref<string[]>([])

const tabLabel = computed(() =>
  tab.value === 'student' ? '学生' : '教師',
)

/* ---------- API & static base ---------- */
const API_BASE =
  import.meta.env.VITE_API_URL ??
  `${window.location.protocol}//${window.location.hostname}:8000`

const imageBase = `${API_BASE}/static/`

/* ---------- 画像ヘルパ ---------- */
function isImage(v: string) {
  return /\.(png|jpe?g)$/i.test(v)
}
function imageSrc(name: string) {
  return /^https?:\/\//.test(name) ? name : imageBase + name
}

/* null‑safe でセル値取得 */
function cellValue(
  row: Record<string | number | symbol, unknown>,
  k: string | number | symbol | null,
) {
  return k == null ? '' : row[k]
}

/* ---------- 固定グラフの src を計算 ---------- */
const chartSrc = computed(() => {
  const prefix =
    tab.value === 'student' ? 'admin/chart_student' : 'admin/chart_teacher'
  const file = images.value.find((n) => n.startsWith(`${prefix}`))
  return file ? imageSrc(file) : null
})

/* ---------- CSV 取得 ---------- */
async function load() {
  loading.value = true
  error.value = null
  try {
    const { data } = await axios.get(
      `${API_BASE}/api/results/${tab.value}`,
      { params: { pwd } },
    )
    rows.value = Array.isArray(data) ? data : []
    headers.value = rows.value.length
      ? Object.keys(rows.value[0]).map((key) => ({ title: key, key }))
      : []
  } catch {
    error.value = '認証失敗またはデータ取得失敗'
    rows.value = []
    headers.value = []
  } finally {
    loading.value = false
  }
}

/* ---------- static 画像一覧取得 ---------- */
async function loadImages() {
  try {
    const { data } = await axios.get<string[]>(`${API_BASE}/api/images`)
    images.value = data
  } catch {
    /* エラーは無視（画像なし） */
  }
}

/* ---------- フック ---------- */
onMounted(() => {
  load()
  loadImages()
})
watch(tab, load)
</script>
