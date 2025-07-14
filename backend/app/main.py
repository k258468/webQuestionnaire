from fastapi import FastAPI
from pydantic import BaseModel
import csv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_methods=["POST"],
    allow_headers=["*"],
)

class SurveyData(BaseModel):
    name: str
    age: int
    feedback: str
    userType: str
    gender: str
    interests: list[str]

@app.post("/api/survey")
async def save_survey(data: SurveyData):
    with open('survey_results.csv', mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            data.name,
            data.age,
            data.feedback,
            data.userType,
            data.gender,
            ';'.join(data.interests)
        ])
    return {"message": "success"}
