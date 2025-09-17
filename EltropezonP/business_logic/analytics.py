import pandas as pd
from datetime import datetime
from database.db_manager import DBManager
from models.transaction import Transaction


class FinancialAnalytics:
    """Clase para el análisis financiero de los datos de transacciones."""

    def __init__(self, db_manager: DBManager):
        self.db = db_manager

    def get_financial_summary(self, start_date=None, end_date=None):
        """
        Calcula el resumen financiero (ingresos, gastos, utilidad) en un rango de fechas.

        Args:
            start_date (str, opcional): Fecha de inicio en formato 'YYYY-MM-DD'.
            end_date (str, opcional): Fecha de fin en formato 'YYYY-MM-DD'.

        Returns:
            dict: Un diccionario con los totales de ingresos, gastos y utilidad.
        """
        transactions = self.db.get_all_transactions()
        if not transactions:
            return {"Ingresos Totales": 0.0, "Gastos Totales": 0.0, "Utilidad Neta": 0.0}

        # Convertir la lista de objetos Transaction a un DataFrame de pandas
        df = pd.DataFrame([t.__dict__ for t in transactions])

        # Filtrar por rango de fechas si se proporcionan
        if start_date and end_date:
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        # Calcular los totales
        total_income = df[df['type'] == 'Ingreso']['amount'].sum()
        total_expenses = df[df['type'] == 'Gasto']['amount'].sum()
        net_profit = total_income - total_expenses

        return {
            "Ingresos Totales": total_income,
            "Gastos Totales": total_expenses,
            "Utilidad Neta": net_profit
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
            return float('inf')  # Retorna infinito si no hay margen de contribución

        return fixed_costs / (price_per_unit - variable_cost_per_unit)


# Ejemplo de uso:
if __name__ == "__main__":
    from database.db_manager import DBManager

    # Inicializar el gestor de la base de datos
    db_manager = DBManager()

    # Crear una instancia del objeto de análisis financiero
    analytics = FinancialAnalytics(db_manager)

    # Añadir algunas transacciones de prueba
    db_manager.add_transaction(
        Transaction(description="Venta de chicha", amount=150.0, type="Ingreso", category="Ventas"))
    db_manager.add_transaction(
        Transaction(description="Salario del personal", amount=600.0, type="Gasto", category="Salarios Fijos"))
    db_manager.add_transaction(
        Transaction(description="Compra de maiz", amount=75.0, type="Gasto", category="Materia Prima"))

    # Obtener el resumen financiero
    summary = analytics.get_financial_summary()
    print("--- Resumen Financiero ---")
    for key, value in summary.items():
        print(f"{key}: {value}")

    # Obtener gastos por categoría
    expenses_by_cat = analytics.get_expenses_by_category()
    print("\n--- Gastos por Categoría ---")
    print(expenses_by_cat)

    fixed_costs = 600.0  # Asumimos que el salario es un costo fijo
    price_per_unit = 5.0  # Precio de venta de la chicha
    variable_cost_per_unit = 2.5  # Costo de ingredientes por unidad

    break_even_point = analytics.get_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)
    print(f"\nEl punto de equilibrio es: {break_even_point:.2f} unidades.")

    db_manager.close()