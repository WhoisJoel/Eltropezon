from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QButtonGroup
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from gui.transaction_viewer import TransactionViewerWindow

from database.db_manager import DBManager
from business_logic.analytics import FinancialAnalytics
from gui.dashboard_tab import DashboardTab
from gui.forms import TransactionFormWidget
from gui.reports_tab import ReportsTab
from gui.styles import APP_STYLES


class MainWindow(QMainWindow):
    def __init__(self, db_manager: DBManager, analytics: FinancialAnalytics):
        super().__init__()

        self.db_manager = db_manager
        self.analytics = analytics

        self.setWindowTitle("Control de Costos y Gastos - EL TROPEZON")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(APP_STYLES)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_sidebar()
        self.create_content_area()

    def create_sidebar(self):
        self.sidebar_frame = QWidget()
        self.sidebar_frame.setObjectName("sidebar")
        self.sidebar_frame.setFixedWidth(200)
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_dashboard = QPushButton("  Panel de control")
        self.btn_dashboard.setCheckable(True)
        self.btn_dashboard.setChecked(True)
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))

        self.btn_ingreso = QPushButton("  Ingreso")
        self.btn_ingreso.setCheckable(True)
        self.btn_ingreso.clicked.connect(lambda: self.show_transaction_form("Ingreso"))

        self.btn_egreso = QPushButton("  Gasto")
        self.btn_egreso.setCheckable(True)
        self.btn_egreso.clicked.connect(lambda: self.show_transaction_form("Gasto"))

        self.btn_reportes = QPushButton("  Informes")
        self.btn_reportes.setCheckable(True)
        self.btn_reportes.clicked.connect(lambda: self.switch_page(2))

        # Nuevo botón para la ventana de gestión
        self.btn_ver_transacciones = QPushButton("  Ver Transacciones")
        self.btn_ver_transacciones.clicked.connect(self.show_viewer_window)

        self.sidebar_layout.addWidget(self.btn_dashboard)
        self.sidebar_layout.addWidget(self.btn_ingreso)
        self.sidebar_layout.addWidget(self.btn_egreso)
        self.sidebar_layout.addWidget(self.btn_reportes)
        self.sidebar_layout.addWidget(self.btn_ver_transacciones)  # Añadir el nuevo botón
        self.sidebar_layout.addStretch()

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self.button_group.addButton(self.btn_dashboard)
        self.button_group.addButton(self.btn_ingreso)
        self.button_group.addButton(self.btn_egreso)
        self.button_group.addButton(self.btn_reportes)

        self.main_layout.addWidget(self.sidebar_frame)

    def create_content_area(self):
        self.content_frame = QWidget()
        self.content_frame.setObjectName("content_frame")
        self.content_layout = QVBoxLayout(self.content_frame)

        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)

        self.dashboard_page = DashboardTab(self.db_manager, self.analytics)
        self.transaction_page = TransactionFormWidget(self.db_manager)
        self.reports_page = ReportsTab(self.db_manager, self.analytics)

        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.transaction_page)
        self.stacked_widget.addWidget(self.reports_page)

        self.transaction_page.transaction_saved.connect(self.dashboard_page.update_dashboard)
        self.transaction_page.transaction_saved.connect(self.reports_page.update_reports)

        self.main_layout.addWidget(self.content_frame)

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        if index == 0:
            self.dashboard_page.update_dashboard()
        elif index == 2:
            self.reports_page.update_reports()

    def show_transaction_form(self, transaction_type):
        self.transaction_page.set_transaction_type(transaction_type)
        self.stacked_widget.setCurrentIndex(1)

    def show_viewer_window(self):
        self.viewer_window = TransactionViewerWindow(self.db_manager)
        self.viewer_window.transaction_updated.connect(self.dashboard_page.update_dashboard)
        self.viewer_window.transaction_updated.connect(self.reports_page.update_reports)
        self.viewer_window.show()