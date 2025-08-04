<template>
  <v-container class="py-8">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="2">
          <!-- タイトル + 再生成ボタン + パスワード入力 -->
          <v-card-title class="d-flex align-center justify-space-between">
            <span class="text-h6 font-weight-bold">
              アンケート結果（{{ tabLabel }}）
            </span>

            <div class="d-flex align-center ga-2">
              
              <!-- グラフ再生成ボタン -->
              <v-btn
                size="small"
                color="primary"
                prepend-icon="mdi-cog-refresh"
                :loading="rebuilding"
                @click="rebuildCharts"
              >
                グラフ再生成
              </v-btn>
            </div>
          </v-card-title>

          <v-card-text>
            <!-- タブ -->
            <v-tabs v-model="tab" class="mb-4">
              <v-tab value="student">学生</v-tab>
              <v-tab value="teacher">教師</v-tab>
            </v-tabs>

            <!-- エラー/完了メッセージ -->
            <v-alert v-if="error" type="error" variant="tonal" class="mb-4">
              {{ error }}
            </v-alert>
            <v-alert
              v-if="notice"
              type="success"
              variant="tonal"
              class="mb-4"
              @click="notice = null"
            >
              {{ notice }}
            </v-alert>

            <!-- グラフ一覧 -->
            <div v-for="def in chartDefsForTab" :key="def.pattern" class="mb-10">
              <h3 class="text-subtitle-1 font-weight-bold mb-2">
                {{ def.label }}
              </h3>

              <div class="d-flex justify-center">
                <v-img
                  v-if="getChartSrc(def)"
                  :src="getChartSrc(def)"
                  max-width="960"
                  width="100%"
                  class="rounded elevation-1"
                  :alt="def.label"
                />
                <div v-else class="text-body-2 text-medium-emphasis">
                  グラフ画像が見つかりません（「グラフ再生成」を押してください）
                </div>
              </div>
            </div>
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
type ChartDef = { pattern: string; label: string }

const API_BASE =
  import.meta.env.VITE_API_URL ??
  `${window.location.protocol}//${window.location.hostname}:8000`
const imageBase = `${API_BASE}/static/`

const tab = ref<Tab>('student')
const error = ref<string | null>(null)
const notice = ref<string | null>(null)
const rebuilding = ref(false)
const images = ref<string[]>([])
const loadingImages = ref(false)
const pwd = ref('')
const cacheBuster = ref<number>(Date.now())

const studentDefs: ChartDef[] = [
  { pattern: 'admin/chart_student_grade', label: 'あなたの学年を教えてください（大学/大学院）' },
  { pattern: 'admin/chart_student_q1', label: '授業終わりに自分の理解度を確認したいと思いますか？' },
  { pattern: 'admin/chart_student_q2', label: '教師が講義で上記のWebアプリを導入する場合、どのような懸念点がありますか？（複数選択）' },
  { pattern: 'admin/chart_student_q3', label: '教師が理解度が足りない場合に対策をしてくれたら嬉しいですか？' },
]
const teacherDefs: ChartDef[] = [
  { pattern: 'admin/chart_teacher_q1_check', label: '中間・期末試験やレポート以外で、生徒の授業理解度を確認していますか？' },
  { pattern: 'admin/chart_teacher_q11_how', label: 'どのような方法で把握していますか？（複数選択）' },
  { pattern: 'admin/chart_teacher_q12_use', label: '把握した授業理解度をどのように活用していますか？（複数選択）' },
  { pattern: 'admin/chart_teacher_q21_want', label: 'できれば、生徒の授業理解度を確認したいですか？' },
  { pattern: 'admin/chart_teacher_q211_reason', label: '現状確認していない理由（複数選択）' },
  { pattern: 'admin/chart_teacher_q2_advantage', label: '上記のWebアプリを使う利点（複数選択）' },
  { pattern: 'admin/chart_teacher_q3_concern', label: '上記のWebアプリを利用する際の懸念点（複数選択）' },
  { pattern: 'admin/chart_teacher_q4_use', label: '上記のWebアプリを実際に使用したいと思いますか？' },
]

const chartDefsForTab = computed(() =>
  tab.value === 'student' ? studentDefs : teacherDefs,
)

function imageSrc(name: string) {
  return /^https?:\/\//.test(name) ? name : imageBase + name
}
function getChartSrc(def: ChartDef): string | undefined {
  const hit = images.value.find(n => n.startsWith(def.pattern))
  return hit ? `${imageSrc(hit)}?t=${cacheBuster.value}` : undefined
}

async function loadImages() {
  loadingImages.value = true
  error.value = null
  try {
    const { data } = await axios.get<string[]>(`${API_BASE}/api/images`)
    images.value = Array.isArray(data) ? data : []
  } catch (e) {
    error.value = '画像一覧の取得に失敗しました'
    images.value = []
  } finally {
    loadingImages.value = false
  }
}

async function rebuildCharts() {
  rebuilding.value = true
  error.value = null
  notice.value = null
  try {
    await axios.post(
      `${API_BASE}/api/charts/rebuild`,
      {},
      { headers: { 'X-Admin-Pwd': pwd.value } },
    )
    cacheBuster.value = Date.now()
    await loadImages()
    notice.value = 'グラフ画像を再生成しました'
  } catch (e) {
    error.value = 'グラフ再生成に失敗しました（認証エラーまたはサーバーエラー）'
  } finally {
    rebuilding.value = false
  }
}

const route = useRoute()
onMounted(() => {
  const p = route.query.pwd
  if (typeof p === 'string') {
    pwd.value = p
  }
  loadImages()
})
watch(tab, () => loadImages())

const tabLabel = computed(() => (tab.value === 'student' ? '学生' : '教師'))
</script>



