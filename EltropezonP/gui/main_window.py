import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon

from gui.dashboard_tab import DashboardTab
from gui.forms import TransactionFormWidget
from gui.reports_tab import ReportsTab

from database.db_manager import DBManager
from business_logic.analytics import FinancialAnalytics


class MainWindow(QMainWindow):
    def __init__(self, db_manager: DBManager, analytics: FinancialAnalytics):
        super().__init__()

        self.db_manager = db_manager
        self.analytics = analytics

        self.setWindowTitle("Control de Costos y Gastos - EL TROPEZON")
        self.setGeometry(100, 100, 1200, 800)  # Tamaño de la ventana
        self.setWindowIcon(QIcon('path/to/icon.png'))  # Puedes agregar un ícono para la aplicación

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.create_tabs()

    def create_tabs(self):
        """Crea las pestañas de la aplicación."""
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # Pestaña 1: Dashboard
        self.dashboard_tab = DashboardTab(self.db_manager, self.analytics)
        self.tabs.addTab(self.dashboard_tab, "Panel de control")

        # Pestaña 2: Formulario de Transacción
        self.transaction_form_tab = TransactionFormWidget(self.db_manager, self.dashboard_tab)
        self.tabs.addTab(self.transaction_form_tab, "Ingresar Transacción")

        # Pestaña 3: Reportes y Gráficos
        self.reports_tab = ReportsTab(self.db_manager, self.analytics)
        self.tabs.addTab(self.reports_tab, "Informes")

        # Conexión para actualizar el dashboard y reportes al guardar una transacción
        self.transaction_form_tab.transaction_saved.connect(self.dashboard_tab.update_dashboard)
        self.transaction_form_tab.transaction_saved.connect(self.reports_tab.update_reports)