from sqlalchemy import Column, Integer, String, Text
from database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    type = Column(String(20), nullable=False)

    choice_a = Column(Text, nullable=False)
    choice_b = Column(Text, nullable=False)
    choice_c = Column(Text, nullable=False)
    choice_d = Column(Text, nullable=False)

    correct = Column(String(1), nullable=False)  # A/B/C/D

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)
    player_name = Column(String(50), nullable=False)
    score = Column(Integer, nullable=False)
