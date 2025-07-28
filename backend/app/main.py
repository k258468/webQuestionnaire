from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import csv, os, pathlib

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = pathlib.Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# -------------------------
# モデル定義
# -------------------------
class StudentSurvey(BaseModel):
    q1_use: str
    q2_value: str
    q3_accept: str
    q4_feel: str
    q4_detail: str | None = ''
    q5_motive: str

class TeacherSurvey(BaseModel):
    q1_method:  list[str] = Field(..., description="学習把握方法")
    q2_value:   str       = Field(..., description="早期支援の価値（5段階）")
    q2_notify:  list[str] = Field(..., description="希望する通知情報")
    q3_value:   str       = Field(..., description="講義改善の価値（5段階）")
    q3_feedback:list[str] = Field(..., description="望ましいフィードバック形式")
    q4_concern:list[str] = Field(..., description="導入懸念")
    q5_value:   str       = Field(..., description="総合評価（5段階）")
    q5_free:    str       = Field('', description="自由記述")

# -------------------------
# ファイルパス
# -------------------------
CSV_FILES = {
    "student": DATA_DIR / "student_results.csv",
    "teacher": DATA_DIR / "teacher_results.csv",
}

# -------------------------
# 学生アンケート保存
# -------------------------
@app.post("/api/survey/student")
async def save_student(data: StudentSurvey):
    path = CSV_FILES["student"]
    first = not path.exists()

    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if first:          # ヘッダ行
            w.writerow([
                "q1_use", "q2_value", "q3_accept",
                "q4_feel", "q4_detail", "q5_motive"
            ])
        w.writerow([
            data.q1_use,
            data.q2_value,
            data.q3_accept,
            data.q4_feel,
            data.q4_detail.replace("\n", " "),
            data.q5_motive,
        ])
    return {"message": "student saved"}

# -------------------------
# 教師アンケート保存
# -------------------------
@app.post("/api/survey/teacher")
async def save_teacher(data: TeacherSurvey):
    path = CSV_FILES["teacher"]
    first = not path.exists()

    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if first:
            w.writerow([
                "q1_method", "q2_value", "q2_notify",
                "q3_value", "q3_feedback",
                "q4_concern", "q5_value", "q5_free"
            ])
        w.writerow([
            ";".join(data.q1_method),
            data.q2_value,
            ";".join(data.q2_notify),
            data.q3_value,
            ";".join(data.q3_feedback),
            ";".join(data.q4_concern),
            data.q5_value,
            data.q5_free.replace("\n", " "),
        ])
    return {"message": "teacher saved"}

# -------------------------
# 結果取得（管理者）
# -------------------------
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "secret")

def verify_pwd(pwd: str):
    if pwd != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/api/results/{user_type}")
async def get_results(user_type: str, pwd: str):
    verify_pwd(pwd)
    path = CSV_FILES.get(user_type)
    if not path or not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
