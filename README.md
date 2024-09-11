# 💬 Chat Online v1.1.0

¡Bienvenido, visitante! 👋

A continuación, te explico brevemente cómo ejecutar este programa. Pero antes, necesitamos realizar algunos pasos previos. 🛠️

## 🚀 Configuración Inicial

Una vez hayas clonado este proyecto en tu PC, te recomiendo usar **Visual Studio Code** como editor de código. Sin embargo, si ya tienes un IDE de preferencia, ¡no hay problema! 😊

### 🐍 Creando el Entorno Virtual

Para comenzar, necesitamos crear un entorno virtual de Python. Aquí te muestro la forma que suelo utilizar:

#### Step 1️⃣: Abre la terminal (cmd de preferencia)
Asegúrate de estar en el directorio del proyecto:
```bash
/Chat-Online-v1.1.0
```
#### Step 2️⃣: Crear el entorno virtual
Ingresa el siguiente comando en la terminal:
```bash
python -m venv env
```
Espera unos segundos (o minutos 😅) y luego procederemos a activar el entorno virtual.

#### Step 3️⃣: Activar el entorno virtual
Navega hasta el archivo ejecutable activate dentro de la carpeta env. Si seguiste los pasos correctamente, solo deberás ejecutar este comando:
```bash
env\Scripts\activate
```

🎉 ¡Felicidades, el entorno virtual está activado!

#### Step 4️⃣: Instalar dependencias
Ahora que el entorno virtual está activo, instala las dependencias del proyecto ejecutando:
```bash
pip install -r requirements.txt
```

En solo 4 pasos, habrás configurado tu entorno virtual e instalado todas las dependencias. ¡Fácil, ¿verdad?! 😎

#### 📦 Crear la Base de Datos
Con las dependencias instaladas, solo falta un paso más antes de poner el proyecto en marcha. Dirígete al siguiente archivo:
```bash
server/database/create_tables.py
```
Ejecuta este archivo para crear la base de datos, que registrará a los usuarios y sus mensajes. 🗂️

#### 🖥️ Ejecutar el Servidor
¡Ya casi terminamos! 🚀

Abre la terminal y cambia el directorio de trabajo a la carpeta server:
```bash
cd server
```
Ejecuta el servidor FastAPI con el siguiente comando:
```bash
uvicorn main:app --reload
```
¡Y listo! 🎉 Ahora puedes acceder a las distintas rutas del proyecto.
--------------------------------------------------------------------------------------------

Espero que esta breve guía te haya sido útil. ¡Hasta la próxima! 👋

