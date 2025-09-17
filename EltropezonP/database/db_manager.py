import sqlite3
import os
from models.transaction import Transaction
from config import DB_PATH

class DBManager:
    """Clase para gestionar la conexión y operaciones con la base de datos SQLite."""

    def __init__(self):
        self.db_path = DB_PATH
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establece la conexión con la base de datos."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def create_tables(self):
        """Crea las tablas de la base de datos si no existen."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    description TEXT,
                    amount REAL NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")

    def add_transaction(self, transaction: Transaction):
        """Agrega una nueva transacción a la base de datos."""
        sql = """
            INSERT INTO transactions (date, description, amount, type, category)
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(sql, (
                transaction.date,
                transaction.description,
                transaction.amount,
                transaction.type,
                transaction.category
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al agregar transacción: {e}")
            return False

    def get_all_transactions(self):
        """Devuelve todas las transacciones de la base de datos."""
        sql = "SELECT id, date, description, amount, type, category FROM transactions ORDER BY date DESC"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        # Convierte las filas de la base de datos en objetos Transaction
        return [Transaction(id=row[0], date=row[1], description=row[2], amount=row[3], type=row[4], category=row[5]) for
                row in rows]

    def get_total_by_category(self, start_date=None, end_date=None):
        """
        Calcula el total de ingresos y gastos por categoría en un rango de fechas.
        Retorna un diccionario con los totales.
        """
        # Consulta para sumar los montos por categoría y tipo
        sql = """
            SELECT type, category, SUM(amount)
            FROM transactions
            WHERE date BETWEEN ? AND ?
            GROUP BY type, category
        """
        if not start_date or not end_date:
            # Si no se especifican fechas, calcula para todos los registros
            sql = "SELECT type, category, SUM(amount) FROM transactions GROUP BY type, category"
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, (start_date, end_date))

        return self.cursor.fetchall()

    def close(self):
        """Cierra la conexión con la base de datos."""
        if self.conn:
            self.conn.close()


# Ejemplo de uso:
if __name__ == "__main__":
    db = DBManager()

    # Creando una instancia de transacción
    new_expense = Transaction(
        description="Compra de maíz",
        amount=50.0,
        type="Gasto",
        category="Materia Prima"
    )

    # Agregando la transacción a la base de datos
    db.add_transaction(new_expense)
    print("Transacción agregada con éxito.")

    # Obteniendo y mostrando todas las transacciones
    transactions = db.get_all_transactions()
    print("\n--- Todas las transacciones ---")
    for t in transactions:
        print(
            f"ID: {t.id}, Fecha: {t.date}, Descripción: {t.description}, Monto: {t.amount}, Tipo: {t.type}, Categoría: {t.category}")

    db.close()