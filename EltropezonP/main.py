import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QButtonGroup, \
    QMainWindow
from PyQt6.QtCore import Qt

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
        # Puedes añadir un icono si tienes uno: self.setWindowIcon(QIcon('path/to/icon.png'))

        # Aplicar estilos QSS
        self.setStyleSheet(APP_STYLES)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        self.create_sidebar()
        self.create_content_area()

    def create_sidebar(self):
        """Crea el menú de navegación lateral."""
        self.sidebar_frame = QWidget()
        self.sidebar_frame.setObjectName("sidebar")  # Para aplicar estilos QSS
        self.sidebar_frame.setFixedWidth(200)
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Botones de navegación (simulando iconos con texto)
        self.btn_dashboard = QPushButton("  Panel de control")
        self.btn_dashboard.setCheckable(True)
        self.btn_dashboard.setChecked(True)  # Activo por defecto
        self.btn_dashboard.clicked.connect(lambda: self.switch_page(0))
        # Puedes añadir íconos: self.btn_dashboard.setIcon(QIcon('path/to/dashboard_icon.png'))

        self.btn_ventas = QPushButton("  Ventas")  # Será el formulario de transacciones
        self.btn_ventas.setCheckable(True)
        self.btn_ventas.clicked.connect(lambda: self.switch_page(1))

        self.btn_gastos = QPushButton("  Gastos")  # Podría ser un formulario específico o filtro
        self.btn_gastos.setCheckable(True)
        self.btn_gastos.clicked.connect(lambda: self.switch_page(1))  # Por ahora apunta al mismo formulario

        self.btn_reportes = QPushButton("  Informes")
        self.btn_reportes.setCheckable(True)
        self.btn_reportes.clicked.connect(lambda: self.switch_page(2))

        self.sidebar_layout.addWidget(self.btn_dashboard)
        self.sidebar_layout.addWidget(self.btn_ventas)
        self.sidebar_layout.addWidget(self.btn_gastos)
        self.sidebar_layout.addWidget(self.btn_reportes)
        self.sidebar_layout.addStretch()  # Empuja los botones hacia arriba

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)  # Solo un botón puede estar seleccionado a la vez
        self.button_group.addButton(self.btn_dashboard)
        self.button_group.addButton(self.btn_ventas)
        self.button_group.addButton(self.btn_gastos)
        self.button_group.addButton(self.btn_reportes)

        self.main_layout.addWidget(self.sidebar_frame)

    def create_content_area(self):
        """Crea el área de contenido principal con un QStackedWidget."""
        self.content_frame = QWidget()
        self.content_frame.setObjectName("content_frame")  # Para aplicar estilos QSS
        self.content_layout = QVBoxLayout(self.content_frame)

        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget)

        # Páginas del StackedWidget
        self.dashboard_page = DashboardTab(self.db_manager, self.analytics)
        self.transaction_page = TransactionFormWidget(self.db_manager,
                                                      self.dashboard_page)  # Pasa dashboard_page para actualizar
        self.reports_page = ReportsTab(self.db_manager, self.analytics)

        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.transaction_page)
        self.stacked_widget.addWidget(self.reports_page)

        # Conexión para actualizar el dashboard y reportes al guardar una transacción
        self.transaction_page.transaction_saved.connect(self.dashboard_page.update_dashboard)
        self.transaction_page.transaction_saved.connect(self.reports_page.update_reports)

        self.main_layout.addWidget(self.content_frame)

    def switch_page(self, index):
        """Cambia la página visible en el QStackedWidget."""
        self.stacked_widget.setCurrentIndex(index)
        # Si la página es el dashboard o reportes, actualízala
        if index == 0:
            self.dashboard_page.update_dashboard()
        elif index == 2:
            self.reports_page.update_reports()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    db_manager = DBManager()
    financial_analytics = FinancialAnalytics(db_manager)

    main_window = MainWindow(db_manager, financial_analytics)
    main_window.show()

    sys.exit(app.exec())