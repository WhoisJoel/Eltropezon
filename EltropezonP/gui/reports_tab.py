from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox, QGroupBox,
    QHBoxLayout, QDateEdit, QLabel
)
from PyQt6.QtCore import QDateTime, QDate, Qt
from business_logic.analytics import FinancialAnalytics
from database.db_manager import DBManager

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ReportsTab(QWidget):
    def __init__(self, db_manager: DBManager, analytics: FinancialAnalytics):
        super().__init__()
        self.db_manager = db_manager
        self.analytics = analytics

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Ajustar márgenes

        self.create_controls_section()

        # Contenedor para el gráfico
        self.report_group = QGroupBox("Visualización de Reportes")
        self.report_group.setStyleSheet(
            "QGroupBox { background-color: #3A3A3A; border: none; } QGroupBox::title { background-color: transparent; }")  # Override style
        self.report_layout = QVBoxLayout(self.report_group)

        self.figure = Figure(figsize=(10, 6), facecolor='#4F4F4F')  # Fondo del gráfico
        self.canvas = FigureCanvas(self.figure)
        self.report_layout.addWidget(self.canvas)
        self.layout.addWidget(self.report_group)

        self.update_reports()

    def create_controls_section(self):
        """Crea los controles para filtrar y seleccionar reportes."""
        controls_layout = QHBoxLayout()

        # Selector de tipo de reporte
        self.report_selector = QComboBox()
        self.report_selector.addItems(["Gastos por Categoría (Circular)", "Ingresos vs. Gastos (Barras)"])
        self.report_selector.currentIndexChanged.connect(self.update_reports)
        controls_layout.addWidget(QLabel("Tipo de Reporte:"))
        controls_layout.addWidget(self.report_selector)

        # Selectores de fecha (QDateEdit)
        self.start_date_input = QDateEdit(QDate.currentDate().addMonths(-1))  # Último mes por defecto
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        self.start_date_input.dateChanged.connect(self.update_reports)

        self.end_date_input = QDateEdit(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDisplayFormat("yyyy-MM-dd")
        self.end_date_input.dateChanged.connect(self.update_reports)

        controls_layout.addSpacing(20)
        controls_layout.addWidget(QLabel("Desde:"))
        controls_layout.addWidget(self.start_date_input)
        controls_layout.addWidget(QLabel("Hasta:"))
        controls_layout.addWidget(self.end_date_input)

        controls_layout.addStretch()  # Empuja los controles a la izquierda
        self.layout.addLayout(controls_layout)

    def update_reports(self):
        """Actualiza el gráfico según la selección y el rango de fechas."""
        self.figure.clear()

        start_date_str = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date_str = self.end_date_input.date().toString("yyyy-MM-dd")

        if self.report_selector.currentText() == "Gastos por Categoría (Circular)":
            self.plot_expenses_by_category(start_date_str, end_date_str)
        elif self.report_selector.currentText() == "Ingresos vs. Gastos (Barras)":
            self.plot_income_vs_expenses(start_date_str, end_date_str)

        self.canvas.draw()

    def plot_expenses_by_category(self, start_date, end_date):
        """Crea un gráfico circular de gastos por categoría."""
        expenses_df = self.analytics.get_expenses_by_category(start_date, end_date)

        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#4F4F4F')  # Fondo del área del gráfico
        self.figure.patch.set_facecolor('#4F4F4F')  # Fondo de la figura

        if expenses_df.empty or expenses_df['amount'].sum() == 0:
            ax.text(0.5, 0.5, "No hay datos de gastos para mostrar en este período.", ha='center', va='center',
                    color='#E0E0E0', fontsize=16)
            ax.axis('off')  # Ocultar ejes
            return

        # Ajustar colores para el tema oscuro
        colors = plt.cm.Dark2.colors  # Puedes elegir otro colormap

        ax.pie(expenses_df['amount'], labels=expenses_df['category'], autopct='%1.1f%%', startangle=90,
               wedgeprops=dict(width=0.4, edgecolor='#3A3A3A'), colors=colors, textprops={'color': '#E0E0E0'})
        ax.axis('equal')  # Asegura que el círculo sea un círculo.
        ax.set_title("Distribución de Gastos por Categoría", color='#FFFFFF', fontsize=18)

    def plot_income_vs_expenses(self, start_date, end_date):
        """Crea un gráfico de barras comparando ingresos y gastos."""
        summary = self.analytics.get_financial_summary(start_date, end_date)

        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#4F4F4F')
        self.figure.patch.set_facecolor('#4F4F4F')

        labels = ['Ingresos Totales', 'Gastos Totales']
        values = [summary['Ingresos Totales'], summary['Gastos Totales']]

        if sum(values) == 0:
            ax.text(0.5, 0.5, "No hay datos de ingresos o gastos para mostrar en este período.", ha='center',
                    va='center', color='#E0E0E0', fontsize=16)
            ax.axis('off')
            return

        bars = ax.bar(labels, values, color=['#6A1B9A', '#FFD700'])  # Colores personalizados
        ax.set_title("Ingresos vs. Gastos", color='#FFFFFF', fontsize=18)
        ax.set_ylabel("Monto (Bs)", color='#E0E0E0')
        ax.tick_params(axis='x', colors='#E0E0E0')
        ax.tick_params(axis='y', colors='#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Mostrar valores en las barras
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 10, f'Bs{yval:.2f}', ha='center', va='bottom',
                    color='#E0E0E0')