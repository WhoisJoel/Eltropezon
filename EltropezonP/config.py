import os

# Nombre del archivo de la base de datos
DATABASE_NAME = "finances.db"

# Ruta para la base de datos
# Esto asegura que la base de datos se guarde en el mismo directorio que el archivo principal del proyecto,
# sin importar desde dónde se ejecute el script.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DATABASE_NAME)


CATEGORIES = [
    "Materia Prima",
    "Mano de Obra",
    "Gastos Operativos",
    "Salarios Fijos",
    "Publicidad",
    "Mantenimiento",
    "Otros"
]

# Nombres de los tipos de transacción
TRANSACTION_TYPES = ["Ingreso", "Gasto"]

# NOTA: En una aplicación más grande, podrías agregar la configuración de
# la ventana (tamaño, título), rutas de archivos de íconos, o cualquier otra constante
# que deba ser fácilmente modificable.