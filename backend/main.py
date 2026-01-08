from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import random

from database import engine, Base, SessionLocal
from models import Quiz, Score

# DB初期化
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------
# クイズAPI
# --------------------
@app.get("/api/quiz/random")
def random_quiz(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).all()
    if not quizzes:
        return {}

    q = random.choice(quizzes)

    return {
        "id": q.id,
        "question": q.question,
        "choices": {
            "A": q.choice_a,
            "B": q.choice_b,
            "C": q.choice_c,
            "D": q.choice_d
        }
    }

# ★ 総問題数取得
@app.get("/api/quiz/count")
def quiz_count(db: Session = Depends(get_db)):
    return {"count": db.query(Quiz).count()}

# ★ 正誤判定
@app.post("/api/quiz/answer/{quiz_id}")
def answer_quiz(quiz_id: int, answer: str, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).get(quiz_id)
    if not quiz:
        return {"correct": False}

    return {"correct": quiz.correct == answer}

# --------------------
# スコアAPI
# --------------------
@app.post("/api/score")
def save_score(player_name: str, score: int, db: Session = Depends(get_db)):
    s = Score(player_name=player_name, score=score)
    db.add(s)
    db.commit()
    return {"result": "ok"}

@app.get("/api/score/ranking")
def ranking(db: Session = Depends(get_db)):
    scores = (
        db.query(Score)
        .order_by(Score.score.desc())
        .limit(10)
        .all()
    )
    return [
        {"player_name": s.player_name, "score": s.score}
        for s in scores
    ]

# --------------------
# フロント配信
# --------------------
app.mount("/", StaticFiles(directory="/frontend", html=True), name="frontend")
