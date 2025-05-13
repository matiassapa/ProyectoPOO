import hashlib
from sqlalchemy.orm import Session
from models.users import User
from datetime import datetime, date
import re
import secrets, string


def check_consecutive_numbers(password: str) -> bool:
    """
    Verifica si la contraseña contiene más de dos números consecutivos.
    Retorna True si hay números consecutivos, de lo contrario False.
    """
    for i in range(len(password) - 2):
        if (
            int(password[i + 1]) == int(password[i]) + 1
            and int(password[i + 2]) == int(password[i + 1]) + 1
        ):
            return True
    return False

def get_user_name_by_login(db: Session, login: str):
    """
    Consulta en la tabla sec_users por el login y devuelve un nombre y apellido concatenados.
    """
    user = db.query(User.nombre, User.apellido).filter(User.login == login).first()
    if user:
        return f"{user.nombre} {user.apellido}"  # Usamos f-string para concatenar
    return ""



def parse_date(date_value):
    """
    Valida y devuelve una fecha en formato 'YYYY-MM-DD'.
    Puede manejar objetos date, datetime o cadenas en formato 'YYYY-MM-DD' y 'DD/MM/YYYY'.
    Si no es válida, devuelve una cadena vacía.
    """
    if isinstance(date_value, (date, datetime)):
        return date_value.strftime("%Y-%m-%d")
    elif isinstance(date_value, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(date_value, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
    return ""



def calculate_age(birthdate: str) -> int:
    """Calcula la edad a partir de una fecha de nacimiento en formato 'YYYY-MM-DD'."""
    if not birthdate:
        return 0  # Si no hay fecha, devuelve 0
    try:
        birthdate_date = datetime.strptime(birthdate, "%Y-%m-%d").date()
        today = datetime.now().date()
        age = today.year - birthdate_date.year - ((today.month, today.day) < (birthdate_date.month, birthdate_date.day))
        return age
    except ValueError:
        return 0  # Si la fecha no tiene el formato correcto, devuelve 0
    

def validar_correo(correo: str) -> bool:
    # Expresión regular básica para validar correos electrónicos
    patron = r"(^[\w\.\-]+@[\w\-]+\.[\w\.\-]+$)"
    return re.match(patron, correo) is not None


def generar_codigo_para_link(length: int = 10) -> str:
    """Genera un código alfanumérico aleatorio de la longitud especificada."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))