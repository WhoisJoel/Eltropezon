from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton,
    QMessageBox, QDateEdit, QLabel, QGroupBox
)
from PyQt6.QtCore import pyqtSignal, QDate, Qt
from models.transaction import Transaction
from database.db_manager import DBManager
from config import CATEGORIES, TRANSACTION_TYPES  # Importar categorías y tipos de config


class TransactionFormWidget(QWidget):
    transaction_saved = pyqtSignal()

    def __init__(self, db_manager: DBManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Ajustar márgenes

        form_group = QGroupBox("INGRESAR NUEVA TRANSACCIÓN")
        form_group.setStyleSheet(
            "QGroupBox { background-color: #3A3A3A; border: none; } QGroupBox::title { background-color: transparent; }")  # Override groupbox style
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)  # Espacio entre filas

        # Campos del formulario con estilos mejorados
        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Descripción de la transacción")

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        self.amount_input.setValidator(QDoubleValidator(0.0, 1000000.0, 2))  # Validar solo números flotantes

        self.type_input = QComboBox()
        self.type_input.addItems(TRANSACTION_TYPES)

        self.category_input = QComboBox()
        self.category_input.addItems(CATEGORIES)  # Usar categorías de config
        self.category_input.setEditable(True)  # Permitir escribir nuevas categorías

        self.save_button = QPushButton("Guardar Transacción")
        self.save_button.clicked.connect(self.save_transaction)

        self.form_layout.addRow(QLabel("Fecha:"), self.date_input)
        self.form_layout.addRow(QLabel("Descripción:"), self.description_input)
        self.form_layout.addRow(QLabel("Monto:"), self.amount_input)
        self.form_layout.addRow(QLabel("Tipo:"), self.type_input)
        self.form_layout.addRow(QLabel("Categoría:"), self.category_input)

        form_group.setLayout(self.form_layout)
        self.main_layout.addWidget(form_group)
        self.main_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Centrar botón
        self.main_layout.addStretch()  # Empuja el formulario hacia arriba

    def save_transaction(self):
        try:
            date_str = self.date_input.date().toString("yyyy-MM-dd")
            description = self.description_input.text().strip()
            amount = float(self.amount_input.text().replace(',', '.'))  # Asegurar formato de punto decimal
            transaction_type = self.type_input.currentText()
            category = self.category_input.currentText().strip()

            if not description or amount <= 0 or not category:
                QMessageBox.warning(self, "Error",
                                    "Por favor, complete todos los campos y asegúrese de que el monto sea positivo.")
                return

            transaction = Transaction(
                date=date_str,
                description=description,
                amount=amount,
                type=transaction_type,
                category=category
            )
            self.db_manager.add_transaction(transaction)

            QMessageBox.information(self, "Éxito", "Transacción guardada correctamente.")

            self.description_input.clear()
            self.amount_input.clear()
            self.category_input.setCurrentIndex(0)  # Volver a la primera categoría o limpiar

            self.transaction_saved.emit()  # Emitir la señal

        except ValueError:
            QMessageBox.warning(self, "Error", "El monto debe ser un número válido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar la transacción: {e}")