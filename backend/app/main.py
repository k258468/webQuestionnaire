from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import csv, os, pathlib

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# staticディレクトリを公開
app.mount("/static", StaticFiles(directory="app/static"), name="static")

DATA_DIR = pathlib.Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# -------------------------
# モデル定義（個別に分ける）
# -------------------------
class StudentSurvey(BaseModel):
    student_id: str
    age: int
    grade: str
    gender: str
    interests: list[str]

class TeacherSurvey(BaseModel):
    age: int
    subject: str
    experience: int
    gender: str
    interests: list[str]

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
        writer = csv.writer(f)
        if first:
            writer.writerow(["student_id", "age", "grade", "gender", "interests"])
        writer.writerow([
            data.student_id,
            data.age,
            data.grade,
            data.gender,
            ";".join(data.interests)
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
        writer = csv.writer(f)
        if first:
            writer.writerow(["age", "subject", "experience", "gender", "interests"])
        writer.writerow([
            data.age,
            data.subject,
            data.experience,
            data.gender,
            ";".join(data.interests)
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


