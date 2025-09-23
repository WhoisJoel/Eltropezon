import sqlite3
from typing import List, Optional
from models.transaction import Transaction
from config import DB_PATH


class DBManager:
    def __init__(self):
        self.conn = None
        self.connect()
        self._initialize_database()

    def connect(self):
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.conn.row_factory = sqlite3.Row  # Acceso a columnas por nombre
        except sqlite3.Error as e:
            print(f"Error al conectar con la base de datos: {e}")

    def _initialize_database(self):
        """
        Crea la tabla si no existe.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    type TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            ''')
            self.conn.commit()
            print("Tabla de transacciones verificada/creada.")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def add_transaction(self, transaction: Transaction):
        """Añade una nueva transacción a la base de datos."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (date, description, amount, type, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (transaction.date, transaction.description, transaction.amount,
                  transaction.type, transaction.category))
            self.conn.commit()
            print(f"Transacción '{transaction.description}' añadida correctamente.")
        except sqlite3.Error as e:
            print(f"Error al añadir la transacción: {e}")

    def get_all_transactions(self) -> List[Transaction]:
        """Obtiene todas las transacciones de la base de datos, ordenadas por fecha."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
            rows = cursor.fetchall()
            return [Transaction(
                        id=row['id'],
                        date=row['date'],
                        description=row['description'],
                        amount=row['amount'],
                        type=row['type'],
                        category=row['category']
                    ) for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener las transacciones: {e}")
            return []

    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Obtiene una transacción por su ID."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
            row = cursor.fetchone()
            if row:
                return Transaction(
                    id=row['id'],
                    date=row['date'],
                    description=row['description'],
                    amount=row['amount'],
                    type=row['type'],
                    category=row['category']
                )
            return None
        except sqlite3.Error as e:
            print(f"Error al obtener la transacción por ID: {e}")
            return None

    def update_transaction(self, transaction: Transaction):
        """Actualiza una transacción existente en la base de datos."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE transactions
                SET date = ?, description = ?, amount = ?, type = ?, category = ?
                WHERE id = ?
            ''', (transaction.date, transaction.description, transaction.amount,
                  transaction.type, transaction.category, transaction.id))
            self.conn.commit()
            print(f"Transacción ID {transaction.id} actualizada correctamente.")
        except sqlite3.Error as e:
            print(f"Error al actualizar la transacción: {e}")

    def delete_transaction(self, transaction_id: int):
        """Borra una transacción de la base de datos por su ID."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            self.conn.commit()
            print(f"Transacción ID {transaction_id} borrada correctamente.")
        except sqlite3.Error as e:
            print(f"Error al borrar la transacción: {e}")

    def get_transaction_by_description(self, description: str) -> Optional[Transaction]:
        """Obtiene la transacción más reciente por su descripción."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM transactions WHERE description = ? ORDER BY date DESC LIMIT 1",
                (description,))
            row = cursor.fetchone()
            if row:
                return Transaction(
                    id=row['id'],
                    date=row['date'],
                    description=row['description'],
                    amount=row['amount'],
                    type=row['type'],
                    category=row['category']
                )
            return None
        except sqlite3.Error as e:
            print(f"Error al obtener la transacción por descripción: {e}")
            return None

    def get_all_unique_descriptions(self) -> list:
        """Obtiene todas las descripciones únicas de la base de datos, ordenadas alfabéticamente."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT description FROM transactions ORDER BY description ASC")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            print(f"Error al obtener las descripciones: {e}")
            return []

    def close(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")
