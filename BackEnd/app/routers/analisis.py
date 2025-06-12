from fpdf import FPDF
from fastapi import APIRouter, Form, Depends, HTTPException, Header
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime
import os
import time

from openai import OpenAI
from database import get_db
from models.historial import Historial
from models.usuarios import Usuario
from models.usuarios_historial import UsuarioHistorial

router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

client = OpenAI(api_key=OPENAI_API_KEY)

def generar_pdf(texto: str, nombre_archivo: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for linea in texto.split("\n"):
        pdf.multi_cell(0, 10, linea)
    pdf.output(nombre_archivo)

def obtener_usuario_desde_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/analizar")
def analizar_texto(
    texto: str = Form(...),
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        # Extraer el usuario desde el token
        token = authorization.split(" ")[1]
        username = obtener_usuario_desde_token(token)

        usuario = db.query(Usuario).filter(Usuario.usuario == username).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Crear thread en OpenAI
        thread = client.beta.threads.create()
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=texto
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "failed":
                raise RuntimeError("El asistente falló al procesar la solicitud.")
            time.sleep(1)

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        respuesta = messages.data[0].content[0].text.value

        # Guardar historial
        nuevo = Historial(
            pedido=texto,
            respuesta=respuesta,
            fecha=datetime.utcnow()
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)

        # Relacionar usuario ↔ historial
        relacion = UsuarioHistorial(
            id_usuario=usuario.id,
            id_historial=nuevo.id
        )
        db.add(relacion)
        db.commit()

        # Crear y guardar PDF
        nombre_archivo = f"resultado_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta_archivo = f"/app/resultados/{nombre_archivo}"
        generar_pdf(respuesta, ruta_archivo)

        url_pdf = f"http://TU_IP_PUBLICA:8000/pdf/{nombre_archivo}"

        return {
            "resultado": respuesta,
            "archivo_pdf": nombre_archivo,
            "url_descarga": url_pdf
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pdf/{nombre_archivo}")
def descargar_pdf(nombre_archivo: str):
    ruta = f"/app/resultados/{nombre_archivo}"
    if not os.path.exists(ruta):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(path=ruta, media_type='application/pdf', filename=nombre_archivo)

