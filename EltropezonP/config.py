# config.py

import os
import sys

# Nombre del archivo de la base de datos
DATABASE_NAME = "finances.db"


def get_base_path():
    """Devuelve la ruta base donde se almacenará la base de datos."""
    home_dir = os.path.expanduser("~")

    # Si estamos ejecutando un .exe congelado
    if getattr(sys, 'frozen', False):
        base_path = os.path.join(home_dir, "Documentos", "ElTropezonData")
    else:
        # Si estamos en modo desarrollo, se puede usar la carpeta fija también
        base_path = os.path.join(home_dir, "Documentos", "ElTropezonData")

    # Crear carpeta si no existe
    if not os.path.exists(base_path):
        os.makedirs(base_path, exist_ok=True)

    return base_path


BASE_PATH = get_base_path()
DB_PATH = os.path.join(BASE_PATH, DATABASE_NAME)

# Categorías de ejemplo
INCOME_CATEGORIES = ["Venta", "Servicio", "Inversión", "Otros Ingresos"]
EXPENSE_CATEGORIES = ["Materia Prima", "Mano de Obra", "Gastos Operativos", "Salarios Fijos", "Publicidad",
                      "Mantenimiento", "Otros Gastos"]

# Tipos de transacción
TRANSACTION_TYPES = ["Ingreso", "Gasto"]
