"""
Reusable UI Components for Zootekni Pro
Modern styled widgets
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QCheckBox, QRadioButton, QSlider, QProgressBar, QScrollArea,
    QGroupBox, QFormLayout, QGridLayout, QSplitter, QSizePolicy,
    QScrollBar, QFileDialog, QMessageBox, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QLinearGradient, QIcon
from utils.logger import get_logger
from utils.constants import APP_NAME

logger = get_logger(__name__)


class ModernButton(QPushButton):
    """Modern styled button with hover effects."""
    
    def __init__(self, text: str = "", button_type: str = "primary"):
        super().__init__(text)
        self.button_type = button_type
        self.setCursor(Qt.PointingHandCursor)
        self.apply_style()
    
    def apply_style(self):
        """Apply button styles based on type."""
        if self.button_type == "primary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #238636;
                    border: none;
                    border-radius: 8px;
                    color: #FFFFFF;
                    padding: 12px 24px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #2EA043;
                }
                QPushButton:pressed {
                    background-color: #238636;
                    transform: translateY(1px);
                }
                QPushButton:disabled {
                    background-color: #21262D;
                    color: #484F58;
                }
            """)
        elif self.button_type == "secondary":
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 1px solid #30363D;
                    border-radius: 8px;
                    color: #C9D1D9;
                    padding: 12px 24px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #21262D;
                    border-color: #58A6FF;
                    color: #58A6FF;
                }
            """)
        elif self.button_type == "danger":
            self.setStyleSheet("""
                QPushButton {
                    background-color: #DA3633;
                    border: none;
                    border-radius: 8px;
                    color: #FFFFFF;
                    padding: 12px 24px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #F85149;
                }
            """)
        elif self.button_type == "icon":
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 8px;
                    padding: 8px;
                }
                QPushButton:hover {
                    background-color: #21262D;
                }
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.button_type};
                    border: none;
                    border-radius: 8px;
                    color: #FFFFFF;
                    padding: 12px 24px;
                    font-weight: 600;
                }}
            """)


class ModernCard(QFrame):
    """Modern styled card with hover effects."""
    
    def __init__(self, title: str = ""):
        super().__init__()
        self.title_text = title
        self.init_ui()
    
    def init_ui(self):
        """Initialize card UI."""
        self.setObjectName("card")
        self.setStyleSheet("""
            QFrame#card {
                background-color: #161B22;
                border-radius: 12px;
                border: 1px solid #30363D;
            }
            QFrame#card:hover {
                border-color: #58A6FF;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        if self.title_text:
            title_label = QLabel(self.title_text)
            title_label.setStyleSheet("""
                color: #F0F6FC;
                font-size: 16px;
                font-weight: 600;
            """)
            layout.addWidget(title_label)


class ModernInput(QLineEdit):
    """Modern styled input field."""
    
    def __init__(self, placeholder: str = "", label: str = ""):
        super().__init__()
        self.input_label = label
        self.setPlaceholderText(placeholder)
        self.apply_style()
    
    def apply_style(self):
        """Apply input styles."""
        self.setStyleSheet("""
            QLineEdit {
                background-color: #0D1117;
                border: 1px solid #30363D;
                border-radius: 8px;
                color: #F0F6FC;
                padding: 12px 16px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #58A6FF;
            }
            QLineEdit:focus {
                border-color: #58A6FF;
                border-width: 2px;
            }
            QLineEdit:disabled {
                background-color: #161B22;
                color: #484F58;
            }
            QLineEdit::placeholder {
                color: #484F58;
            }
        """)


class ModernTable(QTableWidget):
    """Modern styled data table."""
    
    def __init__(self, columns: list = None):
        super().__init__()
        self.columns = columns or []
        self.init_ui()
    
    def init_ui(self):
        """Initialize table UI."""
        self.setStyleSheet("""
            QTableWidget {
                background-color: #0D1117;
                alternate-background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 12px;
                gridline-color: #30363D;
                selection-background-color: #21262D;
                selection-color: #F0F6FC;
            }
            QHeaderView::section {
                background-color: #161B22;
                border: none;
                border-bottom: 2px solid #30363D;
                color: #8B949E;
                font-weight: 600;
                padding: 12px;
                text-align: left;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border: none;
                color: #F0F6FC;
            }
            QTableWidget::item:selected {
                background-color: #21262D;
            }
            QTableWidget::item:hover {
                background-color: #161B22;
            }
        """)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.setFont(QFont("Segoe UI", 12))
        
        if self.columns:
            self.setup_columns(self.columns)
    
    def setup_columns(self, columns: list):
        """Setup table columns."""
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Interactive)
    
    def add_row(self, data: list):
        """Add a data row."""
        row = self.rowCount()
        self.insertRow(row)
        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value) if value is not None else "")
            self.setItem(row, col, item)
    
    def clear_data(self):
        """Clear all data rows."""
        self.setRowCount(0)


class SidebarButton(QPushButton):
    """Sidebar navigation button."""
    
    def __init__(self, text: str, icon: str = ""):
        super().__init__(text)
        self.setIcon(icon)
        self.setCheckable(True)


class StatusIndicator(QFrame):
    """Status indicator dot."""
    
    STATUS_COLORS = {
        "success": "#7EE787",
        "warning": "#F0883E",
        "danger": "#F85149",
        "info": "#58A6FF",
        "neutral": "#8B949E"
    }
    
    def __init__(self, status: str = "neutral", size: int = 8):
        super().__init__()
        self.status = status
        self.size = size
        self.init_ui()
    
    def init_ui(self):
        """Initialize status indicator."""
        color = self.STATUS_COLORS.get(self.status, self.STATUS_COLORS["neutral"])
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: {self.size}px;
            }}
        """)
        self.setFixedSize(self.size * 2, self.size * 2)


class StatCard(QFrame):
    """Dashboard statistics card."""
    
    def __init__(self, title: str, value: str, icon: str = "", change: str = ""):
        super().__init__()
        self.title_text = title
        self.value_text = value
        self.init_ui()
    
    def init_ui(self):
        """Initialize stat card."""
        self.setObjectName("card")
        self.setStyleSheet("""
            QFrame#card {
                background-color: #161B22;
                border-radius: 12px;
                border: 1px solid #30363D;
            }
            QFrame#card:hover {
                border-color: #58A6FF;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(self.title_text)
        title_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        
        # Value
        value_label = QLabel(str(self.value_text))
        value_label.setStyleSheet("color: #F0F6FC; font-size: 28px; font-weight: 600;")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)


class LoadingOverlay(QFrame):
    """Loading overlay for async operations."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize loading overlay."""
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(13, 17, 23, 0.8);
            }
        """)
        self.setVisible(False)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Progress indicator
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #21262D;
                border: none;
                border-radius: 8px;
                height: 4px;
            }
            QProgressBar::chunk {
                background-color: #58A6FF;
                border-radius: 8px;
            }
        """)
        self.progress.setFixedWidth(200)
        self.progress.setRange(0, 0)  # Indeterminate
        
        # Label
        label = QLabel("İşleniyor...")
        label.setStyleSheet("color: #F0F6FC; font-size: 14px;")
        
        layout.addWidget(self.progress)
        layout.addWidget(label)


class TitleBar(QFrame):
    """Custom title bar for window."""
    
    def __init__(self, title: str = APP_NAME):
        super().__init__()
        self.title_text = title
        self.init_ui()
    
    def init_ui(self):
        """Initialize title bar."""
        self.setObjectName("headerFrame")
        self.setStyleSheet("""
            QFrame#headerFrame {
                background-color: #161B22;
                border-bottom: 1px solid #30363D;
            }
        """)
        self.setFixedHeight(60)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        
        # Logo and title
        title_label = QLabel(self.title_text)
        title_label.setStyleSheet("color: #58A6FF; font-size: 18px; font-weight: 600;")
        
        layout.addWidget(title_label)
        layout.addStretch()
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging."""
        if event.button() == Qt.LeftButton:
            self.window().windowHandle().startSystemMove()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if event.buttons() & Qt.LeftButton:
            self.window().windowHandle().startSystemMove()


class ScrollArea(QScrollArea):
    """Custom scroll area with modern styling."""
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class ConfirmDialog(QDialog):
    """Confirmation dialog."""
    
    def __init__(self, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setup_ui(message)
    
    def setup_ui(self, message: str):
        """Setup dialog UI."""
        self.setMinimumWidth(400)
        self.setStyleSheet("""
            QDialog {
                background-color: #0D1117;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # Message
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("color: #F0F6FC; font-size: 14px;")
        
        layout.addWidget(msg_label)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Yes | QDialogButtonBox.No,
            Qt.Horizontal
        )
        buttons.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                border: none;
                border-radius: 8px;
                color: #FFFFFF;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2EA043;
            }
            QDialogButtonBox button[role="DestructiveRole"] {
                background-color: #DA3633;
            }
        """)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)