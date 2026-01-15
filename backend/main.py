from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import random

from database import engine, Base, SessionLocal
from models import Quiz, Score
<<<<<<< HEAD
=======
from fastapi import HTTPException
>>>>>>> fc83315 (commit)

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
<<<<<<< HEAD
=======
# 管理API
# --------------------
@app.get("/api/admin/quizzes")
def get_quizzes(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).all()
    return [
        {
            "id": q.id,
            "question": q.question,
            "type": q.type,
            "choice_a": q.choice_a,
            "choice_b": q.choice_b,
            "choice_c": q.choice_c,
            "choice_d": q.choice_d,
            "correct": q.correct,
        }
        for q in quizzes
    ]


@app.post("/api/admin/quizzes")
def create_quiz(
    question: str,
    type: str,
    choice_a: str,
    choice_b: str,
    choice_c: str,
    choice_d: str,
    correct: str,
    db: Session = Depends(get_db)
):
    quiz = Quiz(
        question=question,
        type=type,
        choice_a=choice_a,
        choice_b=choice_b,
        choice_c=choice_c,
        choice_d=choice_d,
        correct=correct,
    )
    db.add(quiz)
    db.commit()
    return {"result": "ok"}


@app.delete("/api/admin/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    db.delete(quiz)
    db.commit()
    return {"result": "ok"}


@app.put("/api/admin/quizzes/{quiz_id}")
def update_quiz(
    quiz_id: int,
    question: str,
    type: str,
    choice_a: str,
    choice_b: str,
    choice_c: str,
    choice_d: str,
    correct: str,
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).get(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz.question = question
    quiz.type = type
    quiz.choice_a = choice_a
    quiz.choice_b = choice_b
    quiz.choice_c = choice_c
    quiz.choice_d = choice_d
    quiz.correct = correct

    db.commit()
    return {"result": "ok"}

# --------------------
>>>>>>> fc83315 (commit)
# フロント配信
# --------------------
app.mount("/", StaticFiles(directory="/frontend", html=True), name="frontend")
