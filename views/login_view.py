"""
Login Window for Zootekni Pro
Modern dark interface with credential validation
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QCheckBox, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPalette, QColor
from utils.constants import APP_NAME, APP_VERSION
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginWindow(QFrame):
    """Login screen for Zootekni Pro - Modern design."""
    
    login_success = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger(__name__)
        self.username = "admin"
        self.password = "admin123"
        self.init_ui()
    
    def handle_login(self):
        """Validate credentials and emit success signal."""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == self.username and password == self.password:
            self.logger.info(f"Login successful for user: {username}")
            self.login_success.emit()
        else:
            self.error_label.setText("Kullanıcı adı veya şifre hatalı.")
            self.error_label.setVisible(True)
            self.logger.warning(f"Failed login attempt: {username}")
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setObjectName("loginFrame")
        self.setStyleSheet("""
            QFrame#loginFrame {
                background-color: #0D1117;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Center container
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        # Spacer for vertical centering
        main_layout.addStretch()
        main_layout.addWidget(center_widget)
        main_layout.addStretch()
        
        # Login card
        login_card = QFrame()
        login_card.setObjectName("loginCard")
        login_card.setFixedWidth(400)
        login_card.setStyleSheet("""
            QFrame#loginCard {
                background-color: #161B22;
                border-radius: 15px;
                border: 1px solid #30363D;
            }
        """)
        
        # Add shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 128))
        shadow.setOffset(0, 8)
        login_card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(login_card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)
        
        # Logo and app name
        logo_layout = QVBoxLayout()
        logo_layout.setSpacing(8)
        
        # App name label
        app_name = QLabel(APP_NAME)
        app_name.setObjectName("appNameLabel")
        app_name.setStyleSheet("""
            QLabel#appNameLabel {
                color: #58A6FF;
                font-size: 28px;
                font-weight: 700;
            }
        """)
        app_name.setAlignment(Qt.AlignCenter)
        
        # Subtitle
        subtitle = QLabel("Intelligent Rationing System")
        subtitle.setObjectName("appSubtitleLabel")
        subtitle.setStyleSheet("""
            QLabel#appSubtitleLabel {
                color: #8B949E;
                font-size: 14px;
            }
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        
        logo_layout.addWidget(app_name)
        logo_layout.addWidget(subtitle)
        
        card_layout.addLayout(logo_layout)
        
        # Separator
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #30363D;")
        card_layout.addWidget(separator)
        
        # Username field
        username_label = QLabel("Kullanıcı Adı")
        username_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        card_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("kullanici@zootekni.com")
        self.username_input.setFixedHeight(44)
        self.username_input.setText("admin")
        self.username_input.setStyleSheet("""
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
        """)
        self.username_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Şifre")
        password_label.setStyleSheet("color: #8B949E; font-size: 12px;")
        card_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("••••••••")
        self.password_input.setFixedHeight(44)
        self.password_input.setText("admin123")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
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
        """)
        self.password_input.returnPressed.connect(self.handle_login)
        card_layout.addWidget(self.password_input)
        
        # Remember me and forgot password
        options_layout = QHBoxLayout()
        
        self.remember_checkbox = QCheckBox("Beni hatırla")
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #8B949E;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #30363D;
                border-radius: 4px;
                background-color: transparent;
            }
            QCheckBox::indicator:hover {
                border-color: #58A6FF;
            }
            QCheckBox::indicator:checked {
                background-color: #58A6FF;
                border-color: #58A6FF;
            }
        """)
        self.remember_checkbox.setChecked(True)
        
        forgot_button = QPushButton("Şifremi unuttum")
        forgot_button.setObjectName("secondaryButton")
        forgot_button.setStyleSheet("""
            QPushButton#secondaryButton {
                background-color: transparent;
                border: none;
                color: #58A6FF;
                font-size: 12px;
                padding: 0;
            }
            QPushButton#secondaryButton:hover {
                color: #79C0FF;
                text-decoration: underline;
            }
        """)
        forgot_button.setCursor(Qt.PointingHandCursor)
        
        options_layout.addWidget(self.remember_checkbox)
        options_layout.addStretch()
        options_layout.addWidget(forgot_button)
        
        card_layout.addLayout(options_layout)
        
        # Login button
        login_button = QPushButton("Giriş Yap")
        login_button.setFixedHeight(44)
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                border: none;
                border-radius: 8px;
                color: #FFFFFF;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2EA043;
            }
            QPushButton:pressed {
                background-color: #238636;
            }
        """)
        login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(login_button)
        
        # Error message label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("""
            color: #F85149;
            font-size: 12px;
            padding: 8px;
            background-color: rgba(248, 81, 73, 0.1);
            border-radius: 6px;
        """)
        self.error_label.setWordWrap(True)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setVisible(False)
        card_layout.addWidget(self.error_label)
        
        # Version info
        version_layout = QHBoxLayout()
        version_layout.addStretch()
        
        version_label = QLabel(f"Versiyon {APP_VERSION}")
        version_label.setStyleSheet("""
            color: #484F58;
            font-size: 11px;
        """)
        
        version_layout.addWidget(version_label)
        version_layout.addStretch()
        
        card_layout.addLayout(version_layout)
        
        # Add card to center layout
        center_layout.addWidget(login_card, 0, Qt.AlignCenter)
        
        # Set window properties
        self.setFixedSize(800, 600)
        self.setWindowTitle(f"{APP_NAME} - Giriş")
        
        # Make window frameless and centered
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)


class LoginDialog(QWidget):
    """Standalone login dialog."""
    
    login_success = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger(__name__)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI."""
        self.setWindowTitle(f"{APP_NAME} - Giriş")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Login window embedded
        self.login_window = LoginWindow()
        layout.addWidget(self.login_window)
        
        # Connect signals
        self.login_window.login_success.connect(self.login_success.emit)
    
    def handle_login(self):
        """Handle login with credentials."""
        username = self.login_window.username_input.text()
        password = self.login_window.password_input.text()
        
        # Validate credentials (demo: admin/admin123)
        if username == "admin" and password == "admin123":
            self.logger.info(f"Login successful for user: {username}")
            self.login_window.login_success.emit()
        else:
            self.login_window.error_label.setText(
                "Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin."
            )
            self.login_window.error_label.setVisible(True)
            self.logger.warning(f"Failed login attempt for user: {username}")