from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from routers import auth, chat
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv('JWT/.env')
app = FastAPI()


static_dir = Path(__file__).resolve().parent / "../client/static"

if not static_dir.exists():
    raise RuntimeError(f"Directory '{static_dir}' does not exist")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir los orígenes especificados
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permaitir todos los encabezados
)

app.include_router(auth.auth_rt)
app.include_router(chat.chat_rts)

app.get("/")
async def home():
    return "Whe tienes kaka"

