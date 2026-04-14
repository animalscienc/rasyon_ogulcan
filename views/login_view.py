# Login View for Zootekni Pro
# Modern dark-themed login interface with PyQt5

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QColor, QFontDatabase
from PyQt5.QtCore import Qt, QSize
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LoginView(QWidget):
    """Modern dark-themed login interface."""
    
    def __init__(self):
        """Initialize login view."""
        super().__init__()
        self.controller = None
        self.setup_ui()
        self.apply_stylesheet()
        
    def set_controller(self, controller):
        """Set the controller for this view."""
        self.controller = controller
        
    def setup_ui(self):
        """Setup UI components."""
        self.setWindowTitle("Zootekni Pro - Giriş")
        self.setFixedSize(900, 600)
        self.move_to_center()
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left panel - Branding
        left_panel = self.create_left_panel()
        left_panel.setMinimumWidth(450)
        left_panel.setMaximumWidth(500)
        
        # Right panel - Login form
        right_panel = self.create_right_panel()
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        self.setLayout(main_layout)
        
    def move_to_center(self):
        """Move window to center of screen."""
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            rect = screen.geometry()
            self.move((rect.width() - self.width()) // 2, 
                     (rect.height() - self.height()) // 2)
            
    def create_left_panel(self) -> QFrame:
        """Create left branding panel."""
        panel = QFrame()
        panel.setObjectName("leftPanel")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo/Title area
        title = QLabel("Zootekni Pro")
        title.setObjectName("brandTitle")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Intelligent Rationing System")
        subtitle.setObjectName("brandSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        
        version = QLabel("v5.0")
        version.setObjectName("brandVersion")
        version.setAlignment(Qt.AlignCenter)
        
        # Features list
        features = QLabel(
            "• Precision Livestock Farming\n"
            "• NRC & INRA Standartları\n"
            "• Ekonomik Analiz Modülü\n"
            "• Rasyon Optimizasyonu"
        )
        features.setObjectName("brandFeatures")
        features.setAlignment(Qt.AlignLeft)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(version)
        layout.addSpacing(40)
        layout.addWidget(features)
        
        panel.setLayout(layout)
        return panel
        
    def create_right_panel(self) -> QFrame:
        """Create right login form panel."""
        panel = QFrame()
        panel.setObjectName("rightPanel")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 80, 60, 80)
        layout.setSpacing(20)
        
        # Login header
        header = QLabel("Hoş Geldiniz")
        header.setObjectName("loginHeader")
        
        subheader = QLabel("Devam etmek için giriş yapın")
        subheader.setObjectName("loginSubheader")
        
        # Username field
        username_label = QLabel("Kullanıcı Adı")
        username_label.setObjectName("fieldLabel")
        
        self.username_input = QLineEdit()
        self.username_input.setObjectName("inputField")
        self.username_input.setPlaceholderText("Kullanıcı adınızı girin")
        self.username_input.setFixedHeight(50)
        
        # Password field
        password_label = QLabel("Şifre")
        password_label.setObjectName("fieldLabel")
        
        self.password_input = QLineEdit()
        self.password_input.setObjectName("inputField")
        self.password_input.setPlaceholderText("Şifrenizi girin")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(50)
        
        # Login button
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.setObjectName("loginButton")
        self.login_button.setFixedHeight(50)
        self.login_button.clicked.connect(self.handle_login)
        
        # Enter key handling
        self.password_input.returnPressed.connect(self.handle_login)
        self.username_input.returnPressed.connect(self.handle_login)
        
        # Demo credentials hint
        hint = QLabel("Demo: admin / admin123")
        hint.setObjectName("hintLabel")
        
        layout.addWidget(header)
        layout.addWidget(subheader)
        layout.addSpacing(30)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addSpacing(20)
        layout.addWidget(self.login_button)
        layout.addStretch()
        layout.addWidget(hint)
        
        panel.setLayout(layout)
        return panel
        
    def apply_stylesheet(self):
        """Apply modern dark theme stylesheet."""
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* Left Panel */
            #leftPanel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e,
                    stop:1 #16213e);
            }
            
            #brandTitle {
                font-size: 42px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #brandSubtitle {
                font-size: 16px;
                color: #a0a0b0;
                margin-top: 5px;
            }
            
            #brandVersion {
                font-size: 14px;
                color: #606080;
                margin-top: 5px;
            }
            
            #brandFeatures {
                font-size: 14px;
                color: #8080a0;
                line-height: 180%;
                margin-top: 40px;
            }
            
            /* Right Panel */
            #rightPanel {
                background: #0f0f1a;
            }
            
            #loginHeader {
                font-size: 28px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #loginSubheader {
                font-size: 14px;
                color: #606070;
                margin-top: 5px;
            }
            
            #fieldLabel {
                font-size: 13px;
                color: #a0a0b0;
                font-weight: 500;
            }
            
            /* Input Fields */
            #inputField {
                background: #1a1a2e;
                border: 2px solid #2a2a4e;
                border-radius: 10px;
                padding: 0 15px;
                font-size: 14px;
                color: #ffffff;
            }
            
            #inputField:focus {
                border: 2px solid #4a90d9;
                background: #1e1e3a;
            }
            
            #inputField::placeholder {
                color: #505060;
            }
            
            /* Login Button */
            #loginButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90d9,
                    stop:1 #357abd);
                border: none;
                border-radius: 10px;
                font-size: 15px;
                font-weight: 600;
                color: #ffffff;
            }
            
            #loginButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a9fe9,
                    stop:1 #458acd);
            }
            
            #loginButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3a80c9,
                    stop:1 #256aad);
            }
            
            #hintLabel {
                font-size: 12px;
                color: #404050;
                alignment: Qt.AlignCenter;
            }
        """)
        
    def handle_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("Lütfen kullanıcı adı ve şifre girin!")
            return
            
        if self.controller:
            self.controller.login(username, password)
            
    def show_error(self, message: str):
        """Show error message."""
        QMessageBox.warning(self, "Hata", message)
        
    def show_success(self, message: str):
        """Show success message."""
        QMessageBox.information(self, "Başarılı", message)
