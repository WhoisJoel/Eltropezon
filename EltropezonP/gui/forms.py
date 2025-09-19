# gui/forms.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton,
    QMessageBox, QDateEdit, QLabel, QGroupBox
)
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import pyqtSignal, QDate, Qt

from models.transaction import Transaction
from database.db_manager import DBManager
from config import INCOME_CATEGORIES, EXPENSE_CATEGORIES, TRANSACTION_TYPES


class TransactionFormWidget(QWidget):
    transaction_saved = pyqtSignal()

    def __init__(self, db_manager: DBManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        form_group = QGroupBox("INGRESAR NUEVA TRANSACCIÓN")
        form_group.setStyleSheet(
            "QGroupBox { background-color: #3A3A3A; border: none; } QGroupBox::title { background-color: transparent; }")
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")

        self.description_input = QComboBox()
        self.description_input.setEditable(True)
        self.description_input.setPlaceholderText("Descripción de la transacción")
        self.description_input.currentIndexChanged.connect(self.fill_form_with_description)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")


        self.type_input = QComboBox()
        self.type_input.addItems(TRANSACTION_TYPES)
        self.type_input.currentIndexChanged.connect(self.update_category_combobox)

        self.category_input = QComboBox()

        self.save_button = QPushButton("Guardar Transacción")
        self.save_button.clicked.connect(self.save_transaction)

        self.form_layout.addRow(QLabel("Fecha:"), self.date_input)
        self.form_layout.addRow(QLabel("Descripción:"), self.description_input)
        self.form_layout.addRow(QLabel("Monto:"), self.amount_input)
        self.form_layout.addRow(QLabel("Tipo:"), self.type_input)
        self.form_layout.addRow(QLabel("Categoría:"), self.category_input)

        form_group.setLayout(self.form_layout)
        self.main_layout.addWidget(form_group)
        self.main_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch()

        self.update_category_combobox()
        self.load_descriptions()

    def load_descriptions(self):
        """Carga las descripciones únicas desde la base de datos al ComboBox."""
        self.description_input.clear()
        descriptions = self.db_manager.get_all_unique_descriptions()
        self.description_input.addItems(descriptions)

    def fill_form_with_description(self):
        """
        Busca la transacción más reciente por la descripción seleccionada
        y llena los campos de monto, tipo y categoría.
        """
        description = self.description_input.currentText().strip()
        if not description:
            return

        transaction = self.db_manager.get_transaction_by_description(description)
        if transaction:
            # Formateamos el monto directamente aquí para asegurar los decimales
            self.amount_input.setText(f"{transaction.amount:.2f}")
            self.type_input.setCurrentText(transaction.type)
            self.category_input.setCurrentText(transaction.category)

    def update_category_combobox(self):
        """Actualiza el QComboBox de categorías según el tipo de transacción seleccionado."""
        self.category_input.clear()
        selected_type = self.type_input.currentText()

        if selected_type == "Ingreso":
            self.category_input.addItems(INCOME_CATEGORIES)
        elif selected_type == "Gasto":
            self.category_input.addItems(EXPENSE_CATEGORIES)

    def set_transaction_type(self, type_str: str):
        """Establece el tipo de transacción en el QComboBox y actualiza las categorías."""
        index = self.type_input.findText(type_str)
        if index != -1:
            self.type_input.setCurrentIndex(index)

    def save_transaction(self):
        try:
            date_str = self.date_input.date().toString("yyyy-MM-dd")
            description = self.description_input.currentText().strip()
            # Validamos el monto manualmente
            amount = float(self.amount_input.text().replace(',', '.'))
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

            self.transaction_saved.emit()
            self.load_descriptions()

        except ValueError:
            QMessageBox.warning(self, "Error", "El monto debe ser un número válido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al guardar la transacción: {e}")