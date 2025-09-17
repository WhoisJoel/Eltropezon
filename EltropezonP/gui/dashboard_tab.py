from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QGridLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpacerItem, QSizePolicy, QComboBox
)
from PyQt6.QtCore import Qt
from business_logic.analytics import FinancialAnalytics
from database.db_manager import DBManager

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class DashboardTab(QWidget):
    def __init__(self, db_manager: DBManager, analytics: FinancialAnalytics):
        super().__init__()
        self.db_manager = db_manager
        self.analytics = analytics

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Ajustar márgenes

        self.create_header_section()
        self.create_summary_metrics()
        self.create_performance_section()
        self.create_tasks_section()  # Nueva sección para tareas pendientes

        self.update_dashboard()

    def create_header_section(self):
        """Crea el encabezado con el título y el selector de período."""
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_label = QLabel("PANEL DE CONTROL")
        title_label.setObjectName("DashboardTitle")  # Para QSS específico
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #FFFFFF; margin-bottom: 20px;")

        header_layout.addWidget(title_label)
        header_layout.addStretch()  # Empuja el título a la izquierda

        # Aquí iría el selector de período (ej. QComboBox o QDateEdit)
        # Por ahora, un simple placeholder
        period_selector = QComboBox()
        period_selector.addItems(["Este Mes", "Últimos 3 Meses", "Este Año"])
        period_selector.setFixedWidth(150)
        header_layout.addWidget(period_selector)

        self.main_layout.addLayout(header_layout)

    def create_summary_metrics(self):
        """Crea la sección de cálculo de ganancias con grandes métricas."""
        gain_calc_group = QGroupBox("CÁLCULO DE GANANCIAS")
        gain_calc_layout = QGridLayout()
        gain_calc_layout.setContentsMargins(20, 30, 20, 20)  # Margenes internos del groupbox
        gain_calc_layout.setSpacing(20)  # Espacio entre widgets

        # Ingresos Totales
        income_box = QWidget()
        income_box_layout = QVBoxLayout(income_box)
        income_box_layout.setContentsMargins(0, 0, 0, 0)
        income_box_layout.addWidget(QLabel("INGRESOS TOTALES", objectName="SmallMetricLabel"))
        self.total_income_label = QLabel("Bs0.00", objectName="MetricLabel")
        income_box_layout.addWidget(self.total_income_label)
        gain_calc_layout.addWidget(income_box, 0, 0)

        # Gastos Totales
        expenses_box = QWidget()
        expenses_box_layout = QVBoxLayout(expenses_box)
        expenses_box_layout.setContentsMargins(0, 0, 0, 0)
        expenses_box_layout.addWidget(QLabel("GASTOS TOTALES", objectName="SmallMetricLabel"))
        self.total_expenses_label = QLabel("Bs0.00", objectName="MetricLabel")
        expenses_box_layout.addWidget(self.total_expenses_label)
        gain_calc_layout.addWidget(expenses_box, 0, 1)

        # Ganancia Neta
        profit_box = QWidget()
        profit_box_layout = QVBoxLayout(profit_box)
        profit_box_layout.setContentsMargins(0, 0, 0, 0)
        profit_box_layout.addWidget(QLabel("GANANCIA NETA", objectName="SmallMetricLabel"))
        self.net_profit_label = QLabel("Bs0.00", objectName="MetricLabel")
        profit_box_layout.addWidget(self.net_profit_label)
        gain_calc_layout.addWidget(profit_box, 0, 2)

        gain_calc_group.setLayout(gain_calc_layout)
        self.main_layout.addWidget(gain_calc_group)

    def create_performance_section(self):
        """Crea la sección de rendimiento mensual y metas (gráficos de donas)."""
        performance_group = QGroupBox("RENDIMIENTO MENSUAL")
        performance_layout = QHBoxLayout()
        performance_layout.setContentsMargins(20, 30, 20, 20)
        performance_layout.setSpacing(20)

        # Gráfico de Línea (Rendimiento Mensual)
        self.monthly_performance_figure = Figure(figsize=(5, 3), facecolor='#4F4F4F')
        self.monthly_performance_canvas = FigureCanvas(self.monthly_performance_figure)
        self.monthly_performance_canvas.setMinimumHeight(200)
        performance_layout.addWidget(self.monthly_performance_canvas)

        # Sección de Metas (gráficos de dona)
        goals_layout = QVBoxLayout()

        # Meta de Ventas
        sales_goal_group = QGroupBox("METAS DE VENTAS")
        sales_goal_layout = QVBoxLayout(sales_goal_group)
        self.sales_goal_figure = Figure(figsize=(2, 2), facecolor='#4F4F4F')
        self.sales_goal_canvas = FigureCanvas(self.sales_goal_figure)
        self.sales_goal_canvas.setFixedSize(120, 120)  # Tamaño fijo para el gráfico
        sales_goal_layout.addWidget(self.sales_goal_canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        goals_layout.addWidget(sales_goal_group)

        # Control de Gastos
        expenses_control_group = QGroupBox("CONTROL DE GASTOS")
        expenses_control_layout = QVBoxLayout(expenses_control_group)
        self.expenses_control_figure = Figure(figsize=(2, 2), facecolor='#4F4F4F')
        self.expenses_control_canvas = FigureCanvas(self.expenses_control_figure)
        self.expenses_control_canvas.setFixedSize(120, 120)
        expenses_control_layout.addWidget(self.expenses_control_canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        goals_layout.addWidget(expenses_control_group)

        performance_layout.addLayout(goals_layout)
        performance_group.setLayout(performance_layout)
        self.main_layout.addWidget(performance_group)

    def create_tasks_section(self):
        """Crea la sección de Tareas Pendientes."""
        tasks_group = QGroupBox("TAREAS PENDIENTES")
        tasks_layout = QVBoxLayout(tasks_group)

        self.task1_label = QLabel("Revisar factura #2023-005")
        self.task2_label = QLabel("Contactar a Proveedor A")
        self.task3_label = QLabel("Actualizar inventario")

        tasks_layout.addWidget(self.task1_label)
        tasks_layout.addWidget(self.task2_label)
        tasks_layout.addWidget(self.task3_label)

        self.main_layout.addWidget(tasks_group)

    def update_dashboard(self):
        """Actualiza todos los datos y gráficos del dashboard."""
        summary = self.analytics.get_financial_summary()
        self.total_income_label.setText(f"Bs{summary['Ingresos Totales']:.2f}")
        self.total_expenses_label.setText(f"Bs{summary['Gastos Totales']:.2f}")
        self.net_profit_label.setText(f"Bs{summary['Utilidad Neta']:.2f}")

        # Actualizar gráficos
        self.plot_monthly_performance()
        self.plot_donut_chart(self.sales_goal_figure, self.sales_goal_canvas, 0.75, "75%")  # Ejemplo 75% completado
        self.plot_donut_chart(self.expenses_control_figure, self.expenses_control_canvas, 0.90, "90%")  # Ejemplo 90%

    def plot_monthly_performance(self):
        """Genera un gráfico de línea de rendimiento mensual (ejemplo)."""
        self.monthly_performance_figure.clear()
        ax = self.monthly_performance_figure.add_subplot(111)

        # Datos de ejemplo (sustituir con datos reales)
        months = ["Ene", "Feb", "Mar", "Abr", "May"]
        performance = [10, 15, 12, 18, 22]  # Ejemplo de métrica

        ax.plot(months, performance, marker='o', color='#FFD700')
        ax.set_title("Rendimiento Mensual", color='#E0E0E0')
        ax.set_xlabel("Mes", color='#E0E0E0')
        ax.set_ylabel("%", color='#E0E0E0')
        ax.set_facecolor('#4F4F4F')  # Fondo del gráfico
        ax.tick_params(axis='x', colors='#E0E0E0')
        ax.tick_params(axis='y', colors='#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        self.monthly_performance_figure.tight_layout()
        self.monthly_performance_canvas.draw()

    def plot_donut_chart(self, figure, canvas, percentage, text_label):
        """Genera un gráfico de dona."""
        figure.clear()
        ax = figure.add_subplot(111)

        size = [percentage, 1 - percentage]
        colors = ['#FFD700', '#555555']  # Color para la parte completada y el resto

        # Crear el gráfico de dona
        wedges, texts = ax.pie(size, colors=colors, startangle=90, wedgeprops=dict(width=0.4))

        # Agregar el texto central
        centre_circle = plt.Circle((0, 0), 0.60, fc='#4F4F4F')
        figure.gca().add_artist(centre_circle)

        ax.text(0, 0, text_label, ha='center', va='center', fontsize=14, color='#FFFFFF', fontweight='bold')

        ax.axis('equal')  # Asegura que el círculo sea un círculo.
        figure.set_facecolor('#4F4F4F')
        canvas.draw()