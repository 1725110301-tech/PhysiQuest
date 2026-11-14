"""Configuración global: carga .env y logger hacia aplicacion.log."""
import logging
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "aplicacion.log")

logger = logging.getLogger("laboratorio")
logger.setLevel(logging.INFO)

if not logger.handlers:
    _formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    _archivo = logging.FileHandler(LOG_FILE, encoding="utf-8")
    _archivo.setFormatter(_formato)
    logger.addHandler(_archivo)

    _consola = logging.StreamHandler()
    _consola.setFormatter(_formato)
    logger.addHandler(_consola)
