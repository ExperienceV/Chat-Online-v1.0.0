from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


app = FastAPI()

# Configuración de la base de datos SQLite
Base = declarative_base()
engine = create_engine("sqlite:///./chat.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ChatMessage(Base):
    """
    Modelo de datos para almacenar los mensajes de chat en la base de datos.
    """
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)


