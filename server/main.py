from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from routers import auth, chat
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv('JWT/.env')
app = FastAPI()

class FastServer:
    def __init__(self, routers: list[APIRouter]) -> None:
        """
        Inicializa una instancia de FastServer.

        Este constructor configura los valores iniciales de la instancia
        y ejecuta las funciones necesarias para configurar
        la aplicación FastAPI.

        Args:
            routers (list[APIRouter]): Lista de routers que se agregarán a la aplicación.
        """
        self.set_static()
        self.set_middleware()
        self.set_routers(routers)

    def set_static(self) -> None:
        """
        Configura la ruta para servir archivos estáticos.

        Esta función verifica si el directorio de archivos estáticos existe.
        Si no existe, se lanza un error. Los archivos estáticos se montan
        en la ruta '/static'.
        
        Raises:
            RuntimeError: Si el directorio de archivos estáticos no existe.
        """
        static_dir = Path(__file__).resolve().parent / "../client/static"
        if not static_dir.exists():
            raise RuntimeError(f"Directory '{static_dir}' does not exist")
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

    def set_middleware(self) -> None:
        """
        Configura el middleware CORS para la aplicación.

        Esta función restringe el acceso a recursos de distintos orígenes.
        Por defecto, se permiten todos los orígenes, credenciales, métodos
        y encabezados. Modificar según sea necesario.

        Configuración por defecto:
            - Orígenes: Todos permitidos.
            - Credenciales: Todos permitidos.
            - Métodos: Todos permitidos.
            - Headers: Todos permitidos.
        """
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"], 
            allow_headers=["*"],
        )

    def set_routers(self, routers: list[APIRouter]) -> None:
        """
        Agrega los routers a la aplicación FastAPI.

        Esta función incluye las rutas proporcionadas en el parámetro
        routers a la aplicación.

        Args:
            routers (list[APIRouter]): Lista de routers a agregar a la aplicación.
        """
        for r in routers:
            app.include_router(r)

# Lista de routers.
routers = [auth.auth_rt, chat.chat_rts]

# Objeto FastServer al cual le pasamos la lista de
# routers como parámetro.
server = FastServer(routers)


