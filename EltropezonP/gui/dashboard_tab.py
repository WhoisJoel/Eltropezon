from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QGridLayout,
    QSpacerItem, QSizePolicy, QComboBox
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
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.create_header_section()
        self.create_summary_metrics()
        self.create_performance_section()
        self.create_tasks_section()

        self.update_dashboard()

    def create_header_section(self):
        """Crea el encabezado con el título y el selector de período."""
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title_label = QLabel("PANEL DE CONTROL")
        title_label.setObjectName("DashboardTitle")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #FFFFFF; margin-bottom: 20px;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        period_selector = QComboBox()
        period_selector.addItems(["Este Mes", "Últimos 3 Meses", "Este Año"])
        period_selector.setFixedWidth(150)
        header_layout.addWidget(period_selector)

        self.main_layout.addLayout(header_layout)

    def create_summary_metrics(self):
        """Crea la sección de cálculo de ganancias con grandes métricas."""
        gain_calc_group = QGroupBox("CÁLCULO DE GANANCIAS")
        gain_calc_layout = QGridLayout()
        gain_calc_layout.setContentsMargins(20, 30, 20, 20)
        gain_calc_layout.setSpacing(20)

        income_box = QWidget()
        income_box_layout = QVBoxLayout(income_box)
        income_box_layout.setContentsMargins(0, 0, 0, 0)
        income_box_layout.addWidget(QLabel("INGRESOS TOTALES", objectName="SmallMetricLabel"))
        self.total_income_label = QLabel("Bs0.00", objectName="MetricLabel")
        income_box_layout.addWidget(self.total_income_label)
        gain_calc_layout.addWidget(income_box, 0, 0)

        expenses_box = QWidget()
        expenses_box_layout = QVBoxLayout(expenses_box)
        expenses_box_layout.setContentsMargins(0, 0, 0, 0)
        expenses_box_layout.addWidget(QLabel("GASTOS TOTALES", objectName="SmallMetricLabel"))
        self.total_expenses_label = QLabel("Bs0.00", objectName="MetricLabel")
        expenses_box_layout.addWidget(self.total_expenses_label)
        gain_calc_layout.addWidget(expenses_box, 0, 1)

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
        performance_group = QGroupBox("RENDIMIENTO FINANCIERO")
        performance_layout = QHBoxLayout()
        performance_layout.setContentsMargins(20, 30, 20, 20)
        performance_layout.setSpacing(20)

        self.monthly_performance_figure = Figure(figsize=(5, 3), facecolor='#4F4F4F')
        self.monthly_performance_canvas = FigureCanvas(self.monthly_performance_figure)
        self.monthly_performance_canvas.setMinimumHeight(200)
        performance_layout.addWidget(self.monthly_performance_canvas)

        goals_layout = QVBoxLayout()
        sales_goal_group = QGroupBox("METAS DE VENTAS")
        sales_goal_layout = QVBoxLayout(sales_goal_group)
        self.sales_goal_figure = Figure(figsize=(2, 2), facecolor='#4F4F4F')
        self.sales_goal_canvas = FigureCanvas(self.sales_goal_figure)
        self.sales_goal_canvas.setFixedSize(120, 120)
        sales_goal_layout.addWidget(self.sales_goal_canvas, alignment=Qt.AlignmentFlag.AlignCenter)
        goals_layout.addWidget(sales_goal_group)

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

        # Aquí podríamos cargar tareas dinámicas en el futuro
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

        # Actualizar gráficos con datos reales
        self.plot_monthly_performance()
        self.plot_sales_goal_donut()
        self.plot_expenses_control_donut()

    def plot_monthly_performance(self):
        """Genera un gráfico de línea de rendimiento mensual con ingresos y gastos."""
        self.monthly_performance_figure.clear()
        ax = self.monthly_performance_figure.add_subplot(111)

        monthly_data = self.analytics.get_monthly_summary()
        months = monthly_data['labels']
        income = monthly_data['income']
        expenses = monthly_data['expenses']

        ax.plot(months, income, marker='o', color='#4CAF50', label='Ingresos')
        ax.plot(months, expenses, marker='o', color='#F44336', label='Gastos')

        ax.set_title("Rendimiento Mensual", color='#E0E0E0', fontsize=12)
        ax.set_xlabel("Mes", color='#E0E0E0', fontsize=8)
        ax.set_ylabel("Monto (Bs)", color='#E0E0E0', fontsize=8)
        ax.set_facecolor('#4F4F4F')
        ax.tick_params(axis='x', colors='#E0E0E0', labelsize=8)
        ax.tick_params(axis='y', colors='#E0E0E0', labelsize=8)
        ax.legend(loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.6, color='#666666')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        self.monthly_performance_figure.tight_layout()
        self.monthly_performance_canvas.draw()

    def plot_sales_goal_donut(self):
        """Calcula y muestra el progreso de la meta de ventas."""
        sales_goal = 50000.00  # Objetivo de ventas (puedes cambiarlo)
        total_income = self.analytics.get_financial_summary()['Ingresos Totales']
        percentage = total_income / sales_goal if sales_goal > 0 else 0

        text_label = f"{percentage * 100:.0f}%"
        self._plot_donut_chart_helper(self.sales_goal_figure, self.sales_goal_canvas, percentage, text_label)

    def plot_expenses_control_donut(self):
        """Calcula y muestra el progreso de la meta de control de gastos."""
        expenses_limit = 40000.00  # Límite de gastos (puedes cambiarlo)
        total_expenses = self.analytics.get_financial_summary()['Gastos Totales']

        # Invertimos el cálculo para que el verde indique que está por debajo del límite
        percentage = 1 - (total_expenses / expenses_limit) if expenses_limit > 0 else 0
        if percentage < 0: percentage = 0

        text_label = f"{total_expenses:.0f}"
        self._plot_donut_chart_helper(self.expenses_control_figure, self.expenses_control_canvas, percentage,
                                      text_label)

    def _plot_donut_chart_helper(self, figure, canvas, percentage, text_label):
        """Función auxiliar para generar gráficos de dona."""
        figure.clear()
        ax = figure.add_subplot(111)

        size = [percentage, 1 - percentage]
        colors = ['#FFD700', '#555555']
        if percentage < 0.25:
            colors = ['#F44336', '#555555']  # Rojo si es muy bajo
        elif percentage > 0.90:
            colors = ['#4CAF50', '#555555']  # Verde si se acerca a la meta

        wedges, texts = ax.pie(size, colors=colors, startangle=90, wedgeprops=dict(width=0.4))

        centre_circle = plt.Circle((0, 0), 0.60, fc='#4F4F4F')
        figure.gca().add_artist(centre_circle)

        ax.text(0, 0, text_label, ha='center', va='center', fontsize=14, color='#FFFFFF', fontweight='bold')
        ax.axis('equal')
        figure.set_facecolor('#4F4F4F')
        canvas.draw()