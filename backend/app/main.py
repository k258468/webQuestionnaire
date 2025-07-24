from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import csv, os, pathlib
from typing import List, Optional

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

# 学生アンケートモデル
class StudentSurvey(BaseModel):
    student_id: str
    age: int
    grade: str
    gender: str
    interests: List[str]

# 教師アンケートモデル（拡張版）
class TeacherSurvey(BaseModel):
    age: int
    subject: str
    experience: int
    gender: str
    interests: List[str]

    q1_1: List[str]
    q1_1_other: Optional[str] = ""
    q1_2: Optional[str] = ""
    q2: str
    q3_1: List[str]
    q3_1_other: Optional[str] = ""
    q4_1: str
    q4_2: Optional[str] = ""

CSV_FILES = {
    "student": DATA_DIR / "student_results.csv",
    "teacher": DATA_DIR / "teacher_results.csv",
}

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

@app.post("/api/survey/teacher")
async def save_teacher(data: TeacherSurvey):
    path = CSV_FILES["teacher"]
    first = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if first:
            writer.writerow([
                "age", "subject", "experience", "gender", "interests",
                "Q1-1", "Q1-1-other", "Q1-2", "Q2",
                "Q3-1", "Q3-1-other", "Q4-1", "Q4-2"
            ])
        writer.writerow([
            data.age,
            data.subject,
            data.experience,
            data.gender,
            ";".join(data.interests),
            ";".join(data.q1_1),
            data.q1_1_other or "",
            data.q1_2 or "",
            data.q2,
            ";".join(data.q3_1),
            data.q3_1_other or "",
            data.q4_1,
            data.q4_2 or "",
        ])
    return {"message": "teacher saved"}

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



