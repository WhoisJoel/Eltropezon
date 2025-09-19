import sys
from PyQt6.QtWidgets import QApplication

from database.db_manager import DBManager
from business_logic.analytics import FinancialAnalytics
from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_manager = DBManager()
    financial_analytics = FinancialAnalytics(db_manager)
    main_window = MainWindow(db_manager, financial_analytics)
    main_window.show()
    sys.exit(app.exec())