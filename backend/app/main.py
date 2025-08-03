# app/main.py
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Literal
import csv, os, pathlib

app = FastAPI()

# ───────────── CORS ─────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────── Static 配信 ───────────
BASE_DIR   = pathlib.Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ─────────── CSV 保存先 ───────────
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_FILES = {
    "student": DATA_DIR / "student_results.csv",
    "teacher": DATA_DIR / "teacher_results.csv",
}

# ★ 新しい日本語ヘッダー（列順も固定）
STUDENT_HEADERS = ["学年", "活用意向", "懸念（複数）", "対策の受容"]
TEACHER_HEADERS = [
    "把握の有無","把握手段","活用方法","確認意向",
    "確認したい理由","確認したくない理由",
    "利点","懸念","導入意向","導入しない理由",
]

# ───────── 起動時に旧CSVを削除 ─────────
# @app.on_event("startup")
# def _reset_csv_on_start():
#     # 必要に応じてコメントアウトしてください
#     for p in CSV_FILES.values():
#         if p.exists():
#             p.unlink()

# ─────────── リクエストモデル ───────────
class StudentSurvey(BaseModel):
    grade: Literal['B1','B2','B3','B4','M1','M2','D1','D2','D3']
    s1_want_check: Literal['思う', '思わない']
    s2_concern:    List[str]
    s3_happy:      Literal['はい', 'いいえ']

class TeacherSurvey(BaseModel):
    q1_check: Literal['している', 'していない']
    q11_how: List[str] = []
    q12_use: List[str] = []
    q21_want: Literal['したい', 'したくない', ''] | None = None
    q211_reason: List[str] = []
    q212_reason_free: str = ''
    q2_advantage: List[str]
    q3_concern:   List[str]
    q4_use:       Literal['思う', '思わない']
    q4_use_reason: str = ''

# ─────────── 学生 保存 ───────────
@app.post("/api/survey/student")
async def save_student(data: StudentSurvey):
    path = CSV_FILES["student"]
    first = not path.exists()
    row = {
        "学年":         data.grade,
        "活用意向":     data.s1_want_check,
        "懸念（複数）": ";".join(data.s2_concern),
        "対策の受容":   data.s3_happy,
    }
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if first:
            w.writerow(STUDENT_HEADERS)
        w.writerow([row[h] for h in STUDENT_HEADERS])
    return {"message": "student saved"}

# ─────────── 教員 保存 ───────────
@app.post("/api/survey/teacher")
async def save_teacher(data: TeacherSurvey):
    path = CSV_FILES["teacher"]
    first = not path.exists()
    row = {
        "把握の有無":         data.q1_check,
        "把握手段":           ";".join(data.q11_how or []),
        "活用方法":           ";".join(data.q12_use or []),
        "確認意向":           (data.q21_want or ""),
        "確認したい理由":     ";".join(data.q211_reason or []),
        "確認したくない理由": (data.q212_reason_free or "").replace("\n", " "),
        "利点":               ";".join(data.q2_advantage),
        "懸念":               ";".join(data.q3_concern),
        "導入意向":           data.q4_use,
        "導入しない理由":     (data.q4_use_reason or "").replace("\n", " "),
    }
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if first:
            w.writerow(TEACHER_HEADERS)
        w.writerow([row[h] for h in TEACHER_HEADERS])
    return {"message": "teacher saved"}

# ─────────── 管理取得（ヘッダー認証）───────────
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "secret")

def verify_pwd(pwd: str):
    if (pwd or "").strip() != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/api/results/{user_type}")
async def get_results(
    user_type: str,
    x_admin_pwd: str = Header(..., alias="X-Admin-Pwd")
):
    verify_pwd(x_admin_pwd)
    path = CSV_FILES.get(user_type)
    if not path or not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

# ─────────── 画像一覧（任意）───────────
@app.get("/api/images", response_model=List[str])
async def list_images() -> List[str]:
    exts = {".png", ".jpg", ".jpeg"}
    images: List[str] = [
        str(f.relative_to(STATIC_DIR)).replace("\\", "/")
        for f in STATIC_DIR.rglob("*")
        if f.is_file() and f.suffix.lower() in exts
    ]
    return images