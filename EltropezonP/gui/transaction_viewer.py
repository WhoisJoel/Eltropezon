# gui/transaction_viewer.py

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableView, QHeaderView, QComboBox, QLineEdit, QLabel, QDialog,
    QFormLayout, QMessageBox, QDateEdit, QStyle
)
from PyQt6.QtCore import Qt, QDate, QAbstractTableModel, QVariant, pyqtSignal
from PyQt6.QtGui import QDoubleValidator

from database.db_manager import DBManager
from models.transaction import Transaction
from config import EXPENSE_CATEGORIES, INCOME_CATEGORIES, TRANSACTION_TYPES


class TransactionTableModel(QAbstractTableModel):
    """Modelo de tabla para mostrar transacciones."""

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self.headers = ["ID", "Fecha", "Descripción", "Monto", "Tipo", "Categoría"]

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return QVariant()

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return QVariant()

    def refresh(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()


class TransactionViewerWindow(QMainWindow):
    transaction_updated = pyqtSignal()

    def __init__(self, db_manager: DBManager):
        super().__init__()
        self.db_manager = db_manager
        self.setWindowTitle("Gestionar Transacciones")
        self.setGeometry(200, 200, 1000, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.model = TransactionTableModel([])

        self.create_filter_area()
        self.create_table_view()
        self.create_button_area()
        self.load_transactions()

    def create_filter_area(self):
        """Crea el área con los filtros y la barra de búsqueda."""
        filter_layout = QHBoxLayout()

        # Filtro de Tipo (Ingreso/Gasto)
        filter_layout.addWidget(QLabel("Filtrar por Tipo:"))
        self.type_filter = QComboBox()
        self.type_filter.addItem("Todos")
        self.type_filter.addItems(TRANSACTION_TYPES)
        self.type_filter.currentIndexChanged.connect(self.filter_transactions)
        filter_layout.addWidget(self.type_filter)

        # Filtro de Categoría
        filter_layout.addWidget(QLabel("Filtrar por Categoría:"))
        self.category_filter = QComboBox()
        self.category_filter.addItem("Todas")
        self.category_filter.currentIndexChanged.connect(self.filter_transactions)
        filter_layout.addWidget(self.category_filter)

        # Barra de búsqueda
        filter_layout.addWidget(QLabel("Buscar:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Descripción o monto...")
        self.search_input.textChanged.connect(self.filter_transactions)
        filter_layout.addWidget(self.search_input)

        filter_layout.addStretch()
        self.main_layout.addLayout(filter_layout)

        # Llenar el filtro de categorías al inicio
        self.populate_category_filter()
        self.type_filter.currentIndexChanged.connect(self.populate_category_filter)

    def populate_category_filter(self):
        """Llena el ComboBox de categorías según el tipo seleccionado."""
        self.category_filter.clear()
        self.category_filter.addItem("Todas")
        selected_type = self.type_filter.currentText()

        if selected_type == "Ingreso":
            self.category_filter.addItems(INCOME_CATEGORIES)
        elif selected_type == "Gasto":
            self.category_filter.addItems(EXPENSE_CATEGORIES)
        else:
            # Si "Todos", añadir todas las categorías
            all_categories = sorted(list(set(INCOME_CATEGORIES + EXPENSE_CATEGORIES)))
            self.category_filter.addItems(all_categories)

    def create_table_view(self):
        """Crea la tabla para mostrar las transacciones."""
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.main_layout.addWidget(self.table_view)

    def create_button_area(self):
        """Crea los botones de acción (Editar y Borrar)."""
        button_layout = QHBoxLayout()

        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.edit_transaction)

        self.delete_button = QPushButton("Borrar")
        self.delete_button.clicked.connect(self.delete_transaction)

        button_layout.addStretch()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()

        self.main_layout.addLayout(button_layout)

    def load_transactions(self):
        """Carga y muestra todas las transacciones en la tabla."""
        transactions = self.db_manager.get_all_transactions()
        data = [[t.id, t.date, t.description, t.amount, t.type, t.category] for t in transactions]
        self.model = TransactionTableModel(data)
        self.table_view.setModel(self.model)

    def filter_transactions(self):
        """Filtra las transacciones basándose en la selección del usuario."""
        selected_type = self.type_filter.currentText()
        selected_category = self.category_filter.currentText()
        search_term = self.search_input.text().strip().lower()

        all_transactions = self.db_manager.get_all_transactions()
        filtered_transactions = []

        for t in all_transactions:
            matches_type = selected_type == "Todos" or t.type == selected_type
            matches_category = selected_category == "Todas" or t.category == selected_category
            matches_search = search_term in t.description.lower() or search_term in str(t.amount)

            if matches_type and matches_category and matches_search:
                filtered_transactions.append([t.id, t.date, t.description, t.amount, t.type, t.category])

        self.model.refresh(filtered_transactions)

    def edit_transaction(self):
        """Abre un diálogo para editar la transacción seleccionada."""
        selected_index = self.table_view.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, "Error", "Por favor, seleccione una transacción para editar.")
            return

        row = selected_index.row()
        transaction_data = self.model._data[row]
        transaction_id = transaction_data[0]

        # Cargar la transacción completa desde la base de datos
        transaction_to_edit = self.db_manager.get_transaction_by_id(transaction_id)

        # Diálogo para editar
        edit_dialog = TransactionEditDialog(transaction_to_edit, self.db_manager)
        # Aquí está la corrección: usa 'QDialog.Accepted' con 'A' minúscula
        if edit_dialog.exec() == QDialog.accepted:
            self.load_transactions()  # Recargar la tabla
            self.transaction_updated.emit()  # Notificar a la ventana principal

    def delete_transaction(self):
        """Borra la transacción seleccionada de la base de datos."""
        selected_index = self.table_view.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, "Error", "Por favor, seleccione una transacción para borrar.")
            return

        row = selected_index.row()
        transaction_id = self.model._data[row][0]

        reply = QMessageBox.question(self, "Confirmar Borrado",
                                     f"¿Está seguro de que desea borrar la transacción ID: {transaction_id}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.db_manager.delete_transaction(transaction_id)
            self.load_transactions()
            self.transaction_updated.emit()
            QMessageBox.information(self, "Éxito", "Transacción borrada correctamente.")


class TransactionEditDialog(QDialog):
    """Diálogo para editar una transacción existente."""

    def __init__(self, transaction, db_manager):
        super().__init__()
        self.transaction = transaction
        self.db_manager = db_manager

        self.setWindowTitle(f"Editar Transacción: ID {self.transaction.id}")
        self.setFixedSize(400, 300)

        layout = QFormLayout(self)

        self.date_input = QDateEdit(QDate.fromString(self.transaction.date, "yyyy-MM-dd"))
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")

        self.description_input = QLineEdit(self.transaction.description)
        self.amount_input = QLineEdit(str(self.transaction.amount))
        self.amount_input.setValidator(QDoubleValidator(0.0, 1000000.0, 2))

        self.type_input = QComboBox()
        self.type_input.addItems(TRANSACTION_TYPES)
        self.type_input.setCurrentText(self.transaction.type)
        self.type_input.currentIndexChanged.connect(self.update_category_combobox)

        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.update_category_combobox()  # Cargar las categorías iniciales
        self.category_input.setCurrentText(self.transaction.category)

        layout.addRow("Fecha:", self.date_input)
        layout.addRow("Descripción:", self.description_input)
        layout.addRow("Monto:", self.amount_input)
        layout.addRow("Tipo:", self.type_input)
        layout.addRow("Categoría:", self.category_input)

        self.save_button = QPushButton("Guardar Cambios")
        self.save_button.clicked.connect(self.save_changes)

        layout.addRow(self.save_button)

    def update_category_combobox(self):
        self.category_input.clear()
        selected_type = self.type_input.currentText()

        if selected_type == "Ingreso":
            self.category_input.addItems(EXPENSE_CATEGORIES)
        elif selected_type == "Gasto":
            self.category_input.addItems(INCOME_CATEGORIES)

    def save_changes(self):
        try:
            date_str = self.date_input.date().toString("yyyy-MM-dd")
            description = self.description_input.text().strip()
            amount = float(self.amount_input.text().replace(',', '.'))
            transaction_type = self.type_input.currentText()
            category = self.category_input.currentText().strip()

            if not description or amount <= 0 or not category:
                QMessageBox.warning(self, "Error",
                                    "Por favor, complete todos los campos y asegúrese de que el monto sea positivo.")
                return

            self.transaction.date = date_str
            self.transaction.description = description
            self.transaction.amount = amount
            self.transaction.type = transaction_type
            self.transaction.category = category

            self.db_manager.update_transaction(self.transaction)

            QMessageBox.information(self, "Éxito", "Transacción actualizada correctamente.")
            self.accept()  # Cerrar el diálogo

        except ValueError:
            QMessageBox.warning(self, "Error", "El monto debe ser un número válido.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al actualizar la transacción: {e}")