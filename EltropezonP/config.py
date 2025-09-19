# config.py

import os
import sys

# Nombre del archivo de la base de datos
DATABASE_NAME = "finances.db"

def get_base_path():
    """
    Determina la ruta base para los datos de la aplicación.
    Si se ejecuta como un ejecutable, usa la carpeta de Documentos del usuario.
    De lo contrario, usa el directorio del script.
    """
    if getattr(sys, 'frozen', False):
        # Estamos en un ejecutable de PyInstaller
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "Documentos", "ElTropezonData")
    else:
        # Estamos en modo de desarrollo (script normal)
        return os.path.dirname(os.path.abspath(__file__))

# Crear la ruta de la base de datos
BASE_PATH = get_base_path()
DB_PATH = os.path.join(BASE_PATH, DATABASE_NAME)

# Asegurarse de que el directorio de la base de datos exista
if not os.path.exists(BASE_PATH):
    os.makedirs(BASE_PATH)

INCOME_CATEGORIES = ["Venta", "Servicio", "Inversión", "Otros Ingresos"]
EXPENSE_CATEGORIES = ["Materia Prima", "Mano de Obra", "Gastos Operativos", "Salarios Fijos", "Publicidad", "Mantenimiento", "Otros Gastos"]

# Nombres de los tipos de transacción
TRANSACTION_TYPES = ["Ingreso", "Gasto"]