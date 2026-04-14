# Dashboard View for Zootekni Pro
# Main dashboard with sidebar navigation

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QStackedWidget, QScrollArea,
                             QTableWidget, QHeaderView, QComboBox, QDoubleSpinBox, 
                             QGroupBox, QFormLayout, QRadioButton, QButtonGroup,
                             QLineEdit, QTextEdit)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DashboardView(QMainWindow):
    """Main dashboard with sidebar navigation."""
    
    def __init__(self):
        """Initialize dashboard view."""
        super().__init__()
        self.controller = None
        self.menu_buttons = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize UI components."""
        self.setWindowTitle("Zootekni Pro - Intelligent Rationing System")
        self.setGeometry(100, 100, 1400, 900)
        
        # Main container
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Horizontal layout
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left sidebar (250px)
        sidebar = self.create_sidebar()
        sidebar.setFixedWidth(250)
        
        # Right content area (takes remaining space)
        content = self.create_content()
        
        layout.addWidget(sidebar)
        layout.addWidget(content, 1)
        
        main_widget.setLayout(layout)
        
        # Apply stylesheet
        self.apply_styles()
        
    def create_sidebar(self) -> QFrame:
        """Create sidebar."""
        sidebar = QFrame()
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border-right: 2px solid #2a2a4e;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo area
        logo = QFrame()
        logo.setFixedHeight(100)
        logo.setStyleSheet("background-color: #0f0f1a;")
        logo_layout = QVBoxLayout()
        
        title = QLabel("Zootekni Pro")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4a90d9; padding: 20px;")
        
        subtitle = QLabel("Intelligent Rationing")
        subtitle.setStyleSheet("font-size: 12px; color: #606070; padding-left: 20px;")
        
        logo_layout.addWidget(title)
        logo_layout.addWidget(subtitle)
        logo.setLayout(logo_layout)
        
        # Menu buttons
        menu_items = [
            ("🏠", "Anasayfa"),
            ("🌾", "Yem Kütüphanesi"),
            ("🐄", "Hayvan Grupları"),
            ("📋", "Rasyon Oluştur"),
            ("⚡", "Optimizasyon"),
            ("💰", "Ekonomik Analiz"),
            ("📄", "Raporlar"),
            ("⚙️", "Ayarlar"),
        ]
        
        menu_frame = QFrame()
        menu_frame.setStyleSheet("background-color: transparent;")
        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(2)
        
        for icon, text in menu_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setFixedHeight(45)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #a0a0b0;
                    font-size: 14px;
                    text-align: left;
                    padding-left: 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #2a2a4e;
                    color: #ffffff;
                }
                QPushButton:pressed {
                    background-color: #3a3a5e;
                }
            """)
            menu_layout.addWidget(btn)
            self.menu_buttons[text] = btn
            
        menu_layout.addStretch()
        menu_frame.setLayout(menu_layout)
        
        # User info
        user_section = QFrame()
        user_section.setFixedHeight(60)
        user_section.setStyleSheet("background-color: #0f0f1a; border-top: 1px solid #2a2a4e;")
        user_layout = QHBoxLayout()
        
        self.user_label = QLabel("Kullanıcı: Admin")
        self.user_label.setStyleSheet("color: #808090; font-size: 12px; padding: 10px;")
        
        logout_btn = QPushButton("🚪 Çıkış")
        logout_btn.setFixedWidth(60)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a4e;
                border: none;
                border-radius: 5px;
                color: #a0a0b0;
            }
            QPushButton:hover {
                background-color: #3a3a5e;
                color: #ffffff;
            }
        """)
        
        user_layout.addWidget(self.user_label)
        user_layout.addStretch()
        user_layout.addWidget(logout_btn)
        user_section.setLayout(user_layout)
        
        # Add all to sidebar
        layout.addWidget(logo)
        layout.addWidget(menu_frame, 1)
        layout.addWidget(user_section)
        
        sidebar.setLayout(layout)
        return sidebar
        
    def create_content(self) -> QFrame:
        """Create content area."""
        content = QFrame()
        content.setStyleSheet("background-color: #0a0a14;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("Hoş Geldiniz - Zootekni Pro")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            padding-bottom: 10px;
        """)
        
        # Info cards row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)
        
        cards_data = [
            ("📊", "Toplam Yem", "310", "Kalem"),
            ("🐄", "Hayvan Grubu", "12", "Grup"),
            ("📋", "Kayıtlı Rasyon", "45", "Adet"),
            ("💰", "Son Maliyet", "₺12.50", "/kg KM"),
        ]
        
        for icon, title, value, unit in cards_data:
            card = self.create_card(icon, title, value, unit)
            cards_layout.addWidget(card)
            
        # Quick actions
        actions_label = QLabel("Hızlı İşlemler")
        actions_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #c0c0d0;")
        
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        actions = [
            ("➕ Yeni Rasyon", "#4a90d9"),
            ("⚡ Optimize Et", "#2ecc71"),
            ("📄 Rapor Al", "#9b59b6"),
        ]
        
        for text, color in actions:
            btn = QPushButton(text)
            btn.setFixedHeight(40)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0 20px;
                }}
                QPushButton:hover {{
                    opacity: 0.8;
                }}
            """)
            actions_layout.addWidget(btn)
            
        # Recent rations
        recent_label = QLabel("Son Rasyonlar")
        recent_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #c0c0d0;")
        
        table = QTableWidget(5, 6)
        table.setStyleSheet("""
            QTableWidget {
                background-color: #12121e;
                border: 1px solid #2a2a4e;
                border-radius: 8px;
                color: #c0c0d0;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #2a2a4e;
            }
            QHeaderView::section {
                background-color: #1a1a2e;
                color: #a0a0b0;
                padding: 10px;
                font-weight: bold;
            }
        """)
        table.setHorizontalHeaderLabels(["Rasyon Adı", "Grup", "KM (kg)", "HP (%)", "Maliyet (₺)", "Tarih"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(header)
        layout.addLayout(cards_layout)
        layout.addWidget(actions_label)
        layout.addLayout(actions_layout)
        layout.addWidget(recent_label)
        layout.addWidget(table)
        layout.addStretch()
        
        content.setLayout(layout)
        return content
        
    def create_card(self, icon: str, title: str, value: str, unit: str) -> QFrame:
        """Create info card."""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #12121e;
                border: 1px solid #2a2a4e;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13px; color: #808090;")
        
        value_label = QLabel(f"{value}")
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        
        unit_label = QLabel(unit)
        unit_label.setStyleSheet("font-size: 12px; color: #606070;")
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(unit_label)
        
        card.setLayout(layout)
        return card
        
    def set_controller(self, controller):
        """Set controller."""
        self.controller = controller
        # Get username
        if hasattr(controller, 'current_user') and controller.current_user:
            user = controller.current_user
        else:
            user = {'username': 'Admin'}
        username = user.get('full_name') or user.get('username', 'Admin')
        self.user_label.setText(f"Kullanıcı: {username}")
        
    def apply_styles(self):
        """Apply overall styles."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a14;
            }
        """)

