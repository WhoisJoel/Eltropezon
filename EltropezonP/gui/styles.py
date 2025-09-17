# gui/styles.py

APP_STYLES = """
QWidget {
    font-family: "Segoe UI", "Helvetica Neue", "Arial", sans-serif;
    font-size: 14px;
    color: #E0E0E0; /* Texto claro */
}

QMainWindow {
    background-color: #2E2E2E; /* Fondo oscuro de la ventana principal */
}

/* --- Sidebar --- */
#sidebar {
    background-color: #3C3C3C; /* Fondo del menú lateral */
    border-right: 1px solid #4F4F4F;
    padding: 10px 0px;
}

#sidebar QPushButton {
    background-color: transparent;
    border: none;
    color: #E0E0E0;
    text-align: left;
    padding: 10px 15px;
    margin: 5px 10px;
    border-radius: 5px;
    font-size: 15px;
}

#sidebar QPushButton:hover {
    background-color: #555555; /* Hover oscuro */
}

#sidebar QPushButton:checked { /* Estilo para el botón activo */
    background-color: #6A1B9A; /* Un color de acento púrpura */
    color: #FFFFFF;
    font-weight: bold;
    border-left: 3px solid #FFD700; /* Borde de acento */
}

/* --- Contenido Principal --- */
#content_frame {
    background-color: #3A3A3A; /* Fondo del área de contenido */
    padding: 20px;
    border-radius: 8px;
}

QTabWidget::pane { /* El marco de las pestañas */
    border: 1px solid #4F4F4F;
    background-color: #3A3A3A;
    border-radius: 8px;
}

QTabWidget::tab-bar {
    left: 5px; /* Mueve la barra de pestañas a la derecha */
}

QTabBar::tab {
    background: #4F4F4F; /* Fondo de la pestaña inactiva */
    color: #E0E0E0;
    padding: 8px 15px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border: 1px solid #5F5F5F;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: #6A1B9A; /* Fondo de la pestaña activa */
    color: #FFFFFF;
    font-weight: bold;
    border-color: #6A1B9A;
}

QTabBar::tab:hover {
    background: #555555;
}

/* --- QGroupBox --- */
QGroupBox {
    background-color: #4F4F4F;
    border: 1px solid #5F5F5F;
    border-radius: 8px;
    margin-top: 10px; /* Espacio para el título */
    padding: 10px;
    color: #FFFFFF;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left; /* Arriba a la izquierda */
    padding: 0 3px;
    background-color: #6A1B9A; /* Fondo del título del grupo */
    color: #FFFFFF;
    border-radius: 3px;
}

/* --- QLabels --- */
QLabel {
    color: #E0E0E0;
}

/* Estilo para las etiquetas de métricas grandes */
QLabel#MetricLabel {
    font-size: 24px;
    font-weight: bold;
    color: #FFD700; /* Color de acento para números importantes */
    background-color: #555555;
    padding: 15px;
    border-radius: 8px;
    text-align: center; /* Centrar el texto */
}

QLabel#SmallMetricLabel {
    font-size: 16px;
    font-weight: bold;
    color: #E0E0E0;
    margin-bottom: 5px;
}


/* --- QLineEdit (Campos de texto) --- */
QLineEdit {
    background-color: #555555;
    border: 1px solid #6A1B9A; /* Borde de acento */
    border-radius: 5px;
    padding: 8px;
    color: #FFFFFF;
}

QLineEdit:focus {
    border: 2px solid #FFD700; /* Borde de enfoque */
}

/* --- QComboBox (Desplegables) --- */
QComboBox {
    background-color: #555555;
    border: 1px solid #6A1B9A;
    border-radius: 5px;
    padding: 8px;
    color: #FFFFFF;
}

QComboBox::drop-down {
    border: 0px; /* Eliminar el borde de la flecha */
}

QComboBox::down-arrow {
    image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABf+N/AAAAAXNSR0IArs4c6QAAADFJREFUKBWVkEEKwCAMBAv6/3+zE0sQn4WjFhZtqTj0rS7gBq1/wYk+g3gBq1/wYk+g3gAAAAASUVORK5CYII=); /* Flecha personalizada, puedes usar un SVG */
    width: 12px;
    height: 12px;
}

QComboBox QAbstractItemView {
    border: 1px solid #6A1B9A;
    background-color: #555555;
    selection-background-color: #6A1B9A;
    color: #FFFFFF;
}


/* --- QPushButton (Botones) --- */
QPushButton {
    background-color: #6A1B9A; /* Fondo del botón */
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #7B24B3; /* Oscurecer al pasar el ratón */
}

QPushButton:pressed {
    background-color: #5A1780; /* Más oscuro al presionar */
}

/* --- QTableWidget --- */
QTableWidget {
    background-color: #4F4F4F;
    border: 1px solid #5F5F5F;
    border-radius: 8px;
    gridline-color: #6A1B9A; /* Color de las líneas de la cuadrícula */
    selection-background-color: #7B24B3; /* Color de selección */
    color: #E0E0E0;
}

QTableWidget::item {
    padding: 5px;
}

QHeaderView::section {
    background-color: #6A1B9A;
    color: #FFFFFF;
    padding: 5px;
    border: 1px solid #5F5F5F;
    font-weight: bold;
}
QHeaderView::section:horizontal {
    border-bottom: 2px solid #FFD700; /* Borde inferior de acento */
}

QTableWidget QScrollBar:vertical {
    border: none;
    background: #3A3A3A;
    width: 10px;
    margin: 0px 0px 0px 0px;
}
QTableWidget QScrollBar::handle:vertical {
    background: #6A1B9A;
    min-height: 20px;
    border-radius: 5px;
}
QTableWidget QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QTableWidget QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QDateEdit {
    background-color: #555555;
    border: 1px solid #6A1B9A;
    border-radius: 5px;
    padding: 8px;
    color: #FFFFFF;
}
QDateEdit::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left-width: 1px;
    border-left-color: #6A1B9A;
    border-left-style: solid;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
QDateEdit::down-arrow {
    image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABf+N/AAAAAXNSR0IArs4c6QAAADFJREFUKBWVkEEKwCAMBAv6/3+zE0sQn4WjFhZtqTj0rS7gBq1/wYk+g3gBq1/wYk+g3gAAAAASUVORK5CYII=);
}


"""