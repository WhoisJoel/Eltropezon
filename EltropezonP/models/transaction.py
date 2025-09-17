from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    """Clase para representar una transacción de ingresos o gastos."""

    # ID de la transacción, útil para la base de datos
    id: int = None

    # Fecha de la transacción en formato YYYY-MM-DD
    date: str = datetime.now().strftime('%Y-%m-%d')

    # Descripción detallada de la transacción
    description: str = ""

    # Monto de la transacción (puede ser un ingreso o un gasto)
    amount: float = 0.0

    # Tipo de transacción: 'Ingreso' o 'Gasto'
    type: str = ""

    # Categoría del gasto (ej. 'Materia Prima', 'Salarios', 'Publicidad')
    category: str = ""

# NOTA: La clase `Transaction` se encargará de validar los datos en un futuro,
# pero por ahora, la dejamos simple para que la base de datos pueda trabajar con ella.