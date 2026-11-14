"""Utilidades de seguridad: hashes MD5 (32 hex) con hashlib + hmac."""
import hashlib
import hmac
import os
import secrets
import string


def _clave():
    return os.getenv("SECRET_KEY", "").encode("utf-8")


def hash_md5(texto):
    """MD5 simple (32 caracteres hexadecimales)."""
    return hashlib.md5(texto.encode("utf-8")).hexdigest()


def hash_password(password):
    """HMAC-MD5 con SECRET_KEY del .env (32 caracteres hexadecimales)."""
    return hmac.new(_clave(), password.encode("utf-8"), hashlib.md5).hexdigest()


def verificar_password(password, hash_guardado):
    """Compara en tiempo constante para evitar timing attacks."""
    return hmac.compare_digest(hash_password(password), hash_guardado)


def generar_password(longitud=8):
    """Contraseña aleatoria de 8 caracteres (RF-02, RF-04)."""
    alfabeto = string.ascii_letters + string.digits
    return "".join(secrets.choice(alfabeto) for _ in range(longitud))


def generar_codigo_grupo(longitud=10):
    """Código alfanumérico de 10 caracteres para grupos (RF-01)."""
    alfabeto = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alfabeto) for _ in range(longitud))
