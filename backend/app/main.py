from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv, os, pathlib, json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = pathlib.Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

class SurveyData(BaseModel):
    name: str
    age: int
    feedback: str
    userType: str  # "student" or "teacher"
    gender: str
    interests: list[str]

CSV_FILES = {
    "student": DATA_DIR / "student_results.csv",
    "teacher": DATA_DIR / "teacher_results.csv",
}

# ---- 1. 送信保存 ----
@app.post("/api/survey")
async def save_survey(data: SurveyData):
    csv_path = CSV_FILES.get(data.userType)
    if not csv_path:
        raise HTTPException(status_code=400, detail="Invalid userType")
    first_write = not csv_path.exists()

    with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if first_write:
            writer.writerow(["name", "age", "feedback", "gender", "interests"])
        writer.writerow([
            data.name, data.age, data.feedback, data.gender, ";".join(data.interests)
        ])
    return {"message": "success"}

# ---- 2. CSV → JSON 出力（管理者用） ----
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "secret")

def verify_pwd(pwd: str):
    if pwd != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/api/results/{user_type}")
async def get_results(user_type: str, pwd: str):
    verify_pwd(pwd)
    csv_path = CSV_FILES.get(user_type)
    if not csv_path or not csv_path.exists():
        return []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

