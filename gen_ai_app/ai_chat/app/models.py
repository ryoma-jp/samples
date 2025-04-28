from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

class ConversationThread(db.Model):
    __tablename__ = 'conversation_threads'

    id = Column(Integer, primary_key=True)
    summary = Column(String(255), nullable=False)
    # content = Column(JSON, nullable=False)  # ← 旧設計。不要ならコメントアウトまたは削除
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)

class Message(db.Model):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, db.ForeignKey('conversation_threads.id'), nullable=False)
    sender = Column(String(16), nullable=False)  # 'user' or 'ai'
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    thread = db.relationship('ConversationThread', backref=db.backref('messages', lazy=True, cascade="all, delete-orphan"))
