from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# --- クイズAPI ---
@app.get("/api/quiz/random")
def random_quiz(db: Session = Depends(get_db)):
    quizzes = db.query(Quiz).all()
    if not quizzes:
        return {}
    q = random.choice(quizzes)
    return {
        "id": q.id,
        "question": q.question,
        "choices": {"A": q.choice_a, "B": q.choice_b, "C": q.choice_c, "D": q.choice_d},
        "explanation": q.explanation
    }

@app.get("/api/quiz/count")
def quiz_count(db: Session = Depends(get_db)):
    return {"count": db.query(Quiz).count()}

@app.post("/api/quiz/answer/{quiz_id}")
def answer_quiz(quiz_id: int, answer: str, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).get(quiz_id)
    if not quiz:
        return {"correct": False}
    return {"correct": quiz.correct == answer, "correct_answer": quiz.correct, "explanation": quiz.explanation}

# --- スコアAPI ---
@app.post("/api/score")
def save_score(player_name: str, score: int, db: Session = Depends(get_db)):
    s = Score(player_name=player_name, score=score)
    db.add(s)
    db.commit()
    return {"result": "ok"}

@app.get("/api/score/ranking")
def ranking(db: Session = Depends(get_db)):
    scores = db.query(Score).order_by(Score.score.desc()).limit(10).all()
    return [{"player_name": s.player_name, "score": s.score} for s in scores]

# --- 管理API ---
@app.get("/api/admin/quizzes")
def get_quizzes(db: Session = Depends(get_db)):
    return db.query(Quiz).all()

@app.post("/api/admin/quizzes")
def create_quiz(
    question: str, type: str, choice_a: str, choice_b: str, choice_c: str, choice_d: str, 
    correct: str, explanation: str = None, db: Session = Depends(get_db)
):
    quiz = Quiz(
        question=question, type=type, choice_a=choice_a, choice_b=choice_b, 
        choice_c=choice_c, choice_d=choice_d, correct=correct, explanation=explanation
    )
    db.add(quiz)
    db.commit()
    return {"result": "ok"}

@app.put("/api/admin/quizzes/{quiz_id}")
def update_quiz(
    quiz_id: int, question: str, type: str, choice_a: str, choice_b: str, choice_c: str, choice_d: str, 
    correct: str, explanation: str = None, db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).get(quiz_id)
    if not quiz: raise HTTPException(status_code=404, detail="Not found")
    quiz.question, quiz.type, quiz.correct, quiz.explanation = question, type, correct, explanation
    quiz.choice_a, quiz.choice_b, quiz.choice_c, quiz.choice_d = choice_a, choice_b, choice_c, choice_d
    db.commit()
    return {"result": "ok"}

@app.delete("/api/admin/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).get(quiz_id)
    if quiz:
        db.delete(quiz)
        db.commit()
    return {"result": "ok"}

app.mount("/", StaticFiles(directory="/frontend", html=True), name="frontend")