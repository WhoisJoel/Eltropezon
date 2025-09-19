import pandas as pd
from datetime import datetime
from database.db_manager import DBManager
from models.transaction import Transaction


class FinancialAnalytics:
    """Clase para el análisis financiero de los datos de transacciones."""

    def __init__(self, db_manager: DBManager):
        self.db = db_manager

    def get_financial_summary(self, start_date=None, end_date=None):

        transactions = self.db.get_all_transactions()
        if not transactions:
            return {"Ingresos Totales": 0.0, "Gastos Totales": 0.0, "Utilidad Neta": 0.0}

        df = pd.DataFrame([t.__dict__ for t in transactions])

        if start_date and end_date:
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        total_income = df[df['type'] == 'Ingreso']['amount'].sum()
        total_expenses = df[df['type'] == 'Gasto']['amount'].sum()
        net_profit = total_income - total_expenses

        return {
            "Ingresos Totales": total_income,
            "Gastos Totales": total_expenses,
            "Utilidad Neta": net_profit
        }

    def get_monthly_summary(self, start_date=None, end_date=None) -> dict:
        """
        Calcula los ingresos y gastos totales por mes en un rango de fechas.

        Args:
            start_date (str, opcional): Fecha de inicio en formato 'YYYY-MM-DD'.
            end_date (str, opcional): Fecha de fin en formato 'YYYY-MM-DD'.

        Returns:
            dict: Un diccionario con las etiquetas de los meses, y listas de ingresos y gastos.
        """
        transactions = self.db.get_all_transactions()
        if not transactions:
            return {"labels": [], "income": [], "expenses": []}

        df = pd.DataFrame([t.__dict__ for t in transactions])
        df['date'] = pd.to_datetime(df['date'])

        if start_date and end_date:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        # Pivotar la tabla para tener Ingreso y Gasto como columnas
        monthly_summary = df.pivot_table(
            index=df['date'].dt.to_period('M'),
            columns='type',
            values='amount',
            aggfunc='sum'
        ).fillna(0)

        # Preparar los datos para el gráfico
        labels = [m.strftime('%b %y') for m in monthly_summary.index]
        income = monthly_summary['Ingreso'].tolist()
        expenses = monthly_summary['Gasto'].tolist()

        return {
            "labels": labels,
            "income": income,
            "expenses": expenses
        }

    def get_expenses_by_category(self, start_date=None, end_date=None):
        """
        Calcula el total de gastos por categoría en un rango de fechas.

        Args:
            start_date (str, opcional): Fecha de inicio en formato 'YYYY-MM-DD'.
            end_date (str, opcional): Fecha de fin en formato 'YYYY-MM-DD'.

        Returns:
            DataFrame: Un DataFrame de pandas con los gastos por categoría.
        """
        transactions = self.db.get_all_transactions()
        if not transactions:
            return pd.DataFrame()

        df = pd.DataFrame([t.__dict__ for t in transactions])

        if start_date and end_date:
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        expenses_df = df[df['type'] == 'Gasto']
        return expenses_df.groupby('category')['amount'].sum().reset_index()

    def get_break_even_point(self, fixed_costs, price_per_unit, variable_cost_per_unit):
        """
        Calcula el punto de equilibrio en unidades.

        Args:
            fixed_costs (float): Costos fijos totales.
            price_per_unit (float): Precio de venta por unidad.
            variable_cost_per_unit (float): Costo variable por unidad.

        Returns:
            float: El punto de equilibrio en unidades.
        """
        if (price_per_unit - variable_cost_per_unit) <= 0:
            return float('inf')

        return fixed_costs / (price_per_unit - variable_cost_per_unit)