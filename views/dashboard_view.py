# Dashboard View for Zootekni Pro - Simple Working Version

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DashboardView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Zootekni Pro - Intelligent Rationing")
        self.setGeometry(100, 100, 1400, 900)
        
        # Main widget
        main = QWidget()
        self.setCentralWidget(main)
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #1a1a2e;")
        
        sLayout = QVBoxLayout()
        sLayout.setSpacing(0)
        sLayout.setContentsMargins(0, 0, 0, 0)
        
        # Logo
        logo = QLabel("Zootekni Pro")
        logo.setStyleSheet("font-size: 24px; font-weight: bold; color: #4a90d9; padding: 20px; background-color: #0f0f1a;")
        
        # Menu buttons - each button created individually with its own click handler
        self.btn1 = QPushButton("🏠  Anasayfa")
        self.btn1.setFixedHeight(45)
        self.btn1.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn1.clicked.connect(self.btn1_clicked)
        
        self.btn2 = QPushButton("🌾  Yem Kütüphanesi")
        self.btn2.setFixedHeight(45)
        self.btn2.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn2.clicked.connect(self.btn2_clicked)
        
        self.btn3 = QPushButton("🐄  Hayvan Grupları")
        self.btn3.setFixedHeight(45)
        self.btn3.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn3.clicked.connect(self.btn3_clicked)
        
        self.btn4 = QPushButton("📋  Rasyon Oluştur")
        self.btn4.setFixedHeight(45)
        self.btn4.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn4.clicked.connect(self.btn4_clicked)
        
        self.btn5 = QPushButton("⚡  Optimizasyon")
        self.btn5.setFixedHeight(45)
        self.btn5.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn5.clicked.connect(self.btn5_clicked)
        
        self.btn6 = QPushButton("💰  Ekonomik Analiz")
        self.btn6.setFixedHeight(45)
        self.btn6.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn6.clicked.connect(self.btn6_clicked)
        
        self.btn7 = QPushButton("📄  Raporlar")
        self.btn7.setFixedHeight(45)
        self.btn7.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn7.clicked.connect(self.btn7_clicked)
        
        self.btn8 = QPushButton("⚙️  Ayarlar")
        self.btn8.setFixedHeight(45)
        self.btn8.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn8.clicked.connect(self.btn8_clicked)
        
        # User info
        self.user_label = QLabel("Kullanıcı: Admin")
        self.user_label.setStyleSheet("color: #808090; font-size: 12px; padding: 10px; background-color: #0f0f1a;")
        
        sLayout.addWidget(logo)
        sLayout.addWidget(self.btn1)
        sLayout.addWidget(self.btn2)
        sLayout.addWidget(self.btn3)
        sLayout.addWidget(self.btn4)
        sLayout.addWidget(self.btn5)
        sLayout.addWidget(self.btn6)
        sLayout.addWidget(self.btn7)
        sLayout.addWidget(self.btn8)
        sLayout.addStretch()
        sLayout.addWidget(self.user_label)
        sidebar.setLayout(sLayout)
        
        # Right content area
        content = QFrame()
        content.setStyleSheet("background-color: #0a0a14;")
        
        cLayout = QVBoxLayout()
        cLayout.setContentsMargins(20, 20, 20, 20)
        cLayout.setSpacing(15)
        
        # Header
        header = QLabel("Hoş Geldiniz - Zootekni Pro")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        # Info cards
        cards = QHBoxLayout()
        
        c1 = self.make_card("📊", "Toplam Yem", "310", "Kalem")
        c2 = self.make_card("🐄", "Hayvan Grubu", "12", "Grup")
        c3 = self.make_card("📋", "Kayıtlı Rasyon", "45", "Adet")
        c4 = self.make_card("💰", "Son Maliyet", "₺12.50", "/kg KM")
        
        cards.addWidget(c1)
        cards.addWidget(c2)
        cards.addWidget(c3)
        cards.addWidget(c4)
        
        cLayout.addWidget(header)
        cLayout.addLayout(cards)
        cLayout.addStretch()
        
        content.setLayout(cLayout)
        
        layout.addWidget(sidebar)
        layout.addWidget(content, 1)
        main.setLayout(layout)
        
    def make_card(self, icon, title, value, unit):
        card = QFrame()
        card.setStyleSheet("background-color: #12121e; border: 1px solid #2a2a4e; border-radius: 12px;")
        
        l = QVBoxLayout()
        l.setContentsMargins(15, 15, 15, 15)
        
        i = QLabel(icon)
        i.setStyleSheet("font-size: 24px;")
        
        t = QLabel(title)
        t.setStyleSheet("font-size: 13px; color: #808090;")
        
        v = QLabel(value)
        v.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        
        u = QLabel(unit)
        u.setStyleSheet("font-size: 12px; color: #606070;")
        
        l.addWidget(i)
        l.addWidget(t)
        l.addWidget(v)
        l.addWidget(u)
        
        card.setLayout(l)
        return card
        
    def set_controller(self, controller):
        self.controller = controller
        if hasattr(controller, 'current_user') and controller.current_user:
            u = controller.current_user.get('username', 'Admin')
        else:
            u = 'Admin'
        self.user_label.setText(f"Kullanıcı: {u}")
    
    # Button click handlers - each button has its own method
    def btn1_clicked(self):
        print("Anasayfa clicked")
        
    def btn2_clicked(self):
        print("Yem Kütüphanesi clicked")
        
    def btn3_clicked(self):
        print("Hayvan Grupları clicked")
        
    def btn4_clicked(self):
        print("Rasyon Oluştur clicked")
        
    def btn5_clicked(self):
        print("Optimizasyon clicked")
        
    def btn6_clicked(self):
        print("Ekonomik Analiz clicked")
        
    def btn7_clicked(self):
        print("Raporlar clicked")
        
    def btn8_clicked(self):
        print("Ayarlar clicked - logging out")
        if self.controller:
            self.controller.logout()