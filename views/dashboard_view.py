# Dashboard View for Zootekni Pro - Full Working Version

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QStackedWidget, QTableWidget, QHeaderView,
                             QComboBox, QDoubleSpinBox, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DashboardView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.current_page = 0
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Zootekni Pro - Intelligent Rationing")
        self.setGeometry(100, 100, 1400, 900)
        
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
        
        logo = QLabel("Zootekni Pro")
        logo.setStyleSheet("font-size: 24px; font-weight: bold; color: #4a90d9; padding: 20px; background-color: #0f0f1a;")
        
        # Menu buttons - each calls switch_page with page number
        self.btn_home = QPushButton("🏠  Anasayfa")
        self.btn_home.setFixedHeight(45)
        self.btn_home.setStyleSheet("QPushButton {background-color: #2a2a4e; border: none; color: white; font-size: 14px; text-align: left; padding-left: 20px;}")
        self.btn_home.clicked.connect(lambda: self.switch_page(0))
        
        self.btn_feeds = QPushButton("🌾  Yem Kütüphanesi")
        self.btn_feeds.setFixedHeight(45)
        self.btn_feeds.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn_feeds.clicked.connect(lambda: self.switch_page(1))
        
        self.btn_animals = QPushButton("🐄  Hayvan Grupları")
        self.btn_animals.setFixedHeight(45)
        self.btn_animals.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn_animals.clicked.connect(lambda: self.switch_page(2))
        
        self.btn_ration = QPushButton("📋  Rasyon Oluştur")
        self.btn_ration.setFixedHeight(45)
        self.btn_ration.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn_ration.clicked.connect(lambda: self.switch_page(3))
        
        self.btn_optimize = QPushButton("⚡  Optimizasyon")
        self.btn_optimize.setFixedHeight(45)
        self.btn_optimize.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn_optimize.clicked.connect(lambda: self.switch_page(4))
        
        self.btn_economic = QPushButton("💰  Ekonomik Analiz")
        self.btn_economic.setFixedHeight(45)
        self.btn_economic.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn_economic.clicked.connect(lambda: self.switch_page(5))
        
        self.btn_reports = QPushButton("📄  Raporlar")
        self.btn_reports.setFixedHeight(45)
        self.btn_reports.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn_reports.clicked.connect(lambda: self.switch_page(6))
        
        self.btn_settings = QPushButton("⚙️  Ayarlar")
        self.btn_settings.setFixedHeight(45)
        self.btn_settings.setStyleSheet("QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}")
        self.btn_settings.clicked.connect(self.logout)
        
        self.user_label = QLabel("Kullanıcı: Admin")
        self.user_label.setStyleSheet("color: #808090; font-size: 12px; padding: 10px; background-color: #0f0f1a;")
        
        sLayout.addWidget(logo)
        sLayout.addWidget(self.btn_home)
        sLayout.addWidget(self.btn_feeds)
        sLayout.addWidget(self.btn_animals)
        sLayout.addWidget(self.btn_ration)
        sLayout.addWidget(self.btn_optimize)
        sLayout.addWidget(self.btn_economic)
        sLayout.addWidget(self.btn_reports)
        sLayout.addWidget(self.btn_settings)
        sLayout.addStretch()
        sLayout.addWidget(self.user_label)
        sidebar.setLayout(sLayout)
        
        # Right content area with stacked widget for multiple pages
        self.pages = QStackedWidget()
        
        # Page 0: Home
        self.page_home = self.create_home_page()
        self.pages.addWidget(self.page_home)
        
        # Page 1: Feeds
        self.page_feeds = self.create_feeds_page()
        self.pages.addWidget(self.page_feeds)
        
        # Page 2: Animals
        self.page_animals = self.create_animals_page()
        self.pages.addWidget(self.page_animals)
        
        # Page 3: Create Ration
        self.page_ration = self.create_ration_page()
        self.pages.addWidget(self.page_ration)
        
        # Page 4: Optimization
        self.page_optimize = self.create_optimize_page()
        self.pages.addWidget(self.page_optimize)
        
        # Page 5: Economic
        self.page_economic = self.create_economic_page()
        self.pages.addWidget(self.page_economic)
        
        # Page 6: Reports
        self.page_reports = self.create_reports_page()
        self.pages.addWidget(self.page_reports)
        
        layout.addWidget(sidebar)
        layout.addWidget(self.pages, 1)
        main.setLayout(layout)
        
    def switch_page(self, page_num):
        """Switch to different page."""
        self.current_page = page_num
        self.pages.setCurrentIndex(page_num)
        self.update_button_styles()
        
    def update_button_styles(self):
        """Update which button is highlighted."""
        all_buttons = [
            (self.btn_home, 0),
            (self.btn_feeds, 1),
            (self.btn_animals, 2),
            (self.btn_ration, 3),
            (self.btn_optimize, 4),
            (self.btn_economic, 5),
            (self.btn_reports, 6),
        ]
        
        active_style = "QPushButton {background-color: #2a2a4e; border: none; color: white; font-size: 14px; text-align: left; padding-left: 20px;}"
        inactive_style = "QPushButton {background-color: transparent; border: none; color: #a0a0b0; font-size: 14px; text-align: left; padding-left: 20px;} QPushButton:hover {background-color: #2a2a4e; color: white;}"
        
        for btn, idx in all_buttons:
            if idx == self.current_page:
                btn.setStyleSheet(active_style)
            else:
                btn.setStyleSheet(inactive_style)
        
    def create_home_page(self):
        """Home/Dashboard page."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("Hoş Geldiniz - Zootekni Pro")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        cards = QHBoxLayout()
        
        c1 = self.make_card("📊", "Toplam Yem", "310", "Kalem")
        c2 = self.make_card("🐄", "Hayvan Grubu", "12", "Grup")
        c3 = self.make_card("📋", "Kayıtlı Rasyon", "45", "Adet")
        c4 = self.make_card("💰", "Son Maliyet", "₺12.50", "/kg KM")
        
        cards.addWidget(c1)
        cards.addWidget(c2)
        cards.addWidget(c3)
        cards.addWidget(c4)
        
        layout.addWidget(header)
        layout.addLayout(cards)
        
        quick_label = QLabel("Hızlı İşlemler")
        quick_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #c0c0d0; padding-top: 20px;")
        layout.addWidget(quick_label)
        
        buttons = QHBoxLayout()
        
        b1 = QPushButton("➕ Yeni Rasyon")
        b1.setFixedHeight(40)
        b1.setStyleSheet("QPushButton {background-color: #4a90d9; border: none; border-radius: 8px; color: white; font-size: 14px; font-weight: bold; padding: 0 20px;}")
        b1.clicked.connect(lambda: self.switch_page(3))
        
        b2 = QPushButton("⚡ Optimize Et")
        b2.setFixedHeight(40)
        b2.setStyleSheet("QPushButton {background-color: #2ecc71; border: none; border-radius: 8px; color: white; font-size: 14px; font-weight: bold; padding: 0 20px;}")
        b2.clicked.connect(lambda: self.switch_page(4))
        
        b3 = QPushButton("📄 Rapor Al")
        b3.setFixedHeight(40)
        b3.setStyleSheet("QPushButton {background-color: #9b59b6; border: none; border-radius: 8px; color: white; font-size: 14px; font-weight: bold; padding: 0 20px;}")
        b3.clicked.connect(lambda: self.switch_page(6))
        
        buttons.addWidget(b1)
        buttons.addWidget(b2)
        buttons.addWidget(b3)
        
        layout.addLayout(buttons)
        layout.addStretch()
        
        page.setLayout(layout)
        return page
        
    def create_feeds_page(self):
        """Feeds library page."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("Yem Kütüphanesi")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        toolbar = QHBoxLayout()
        
        add_btn = QPushButton("➕ Yeni Yem Ekle")
        add_btn.setStyleSheet("QPushButton {background-color: #2a2a4e; border: none; border-radius: 5px; color: #c0c0d0; padding: 8px 15px;}")
        
        import_btn = QPushButton("📥 İçe Aktar")
        import_btn.setStyleSheet("QPushButton {background-color: #2a2a4e; border: none; border-radius: 5px; color: #c0c0d0; padding: 8px 15px;}")
        
        toolbar.addWidget(add_btn)
        toolbar.addWidget(import_btn)
        toolbar.addStretch()
        
        table = QTableWidget(10, 8)
        table.setStyleSheet("QTableWidget {background-color: #12121e; border: 1px solid #2a2a4e; border-radius: 8px; color: #c0c0d0;} QHeaderView::section {background-color: #1a1a2e; color: #a0a0b0; padding: 10px;}")
        table.setHorizontalHeaderLabels(["Kod", "Yem Adı", "KM (%)", "HP (%)", "NDF (%)", "NEL", "Fiyat", "Min %"])
        
        layout.addWidget(header)
        layout.addLayout(toolbar)
        layout.addWidget(table)
        layout.addStretch()
        
        page.setLayout(layout)
        return page
        
    def create_animals_page(self):
        """Animal groups page."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("Hayvan Grupları")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        add_btn = QPushButton("➕ Yeni Grup Ekle")
        add_btn.setStyleSheet("QPushButton {background-color: #2a2a4e; border: none; border-radius: 5px; color: #c0c0d0; padding: 8px 15px;}")
        
        table = QTableWidget(5, 7)
        table.setStyleSheet("QTableWidget {background-color: #12121e; border: 1px solid #2a2a4e; border-radius: 8px; color: #c0c0d0;}")
        table.setHorizontalHeaderLabels(["Grup Adı", "Tür", "Canlı Ağırlık", "Süt Verimi", "Yağ %", "Protein %", "Laktasyon Haftası"])
        
        layout.addWidget(header)
        layout.addWidget(add_btn)
        layout.addWidget(table)
        layout.addStretch()
        
        page.setLayout(layout)
        return page
        
    def create_ration_page(self):
        """Create ration page."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("Rasyon Oluştur")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        group_box = QGroupBox("Hayvan Grubu Seçimi")
        group_box.setStyleSheet("QGroupBox {color: #c0c0d0; font-weight: bold;}")
        group_layout = QFormLayout()
        
        combo = QComboBox()
        combo.addItems(["Yüksek Verimli Sürü (Laktasyon 1-12)", "Orta Verimli Sürü (Laktasyon 13-24)", "Kuru Dönem"])
        group_layout.addRow("Grup:", combo)
        
        group_box.setLayout(group_layout)
        
        targets_box = QGroupBox("Besin Hedefleri")
        targets_box.setStyleSheet("QGroupBox {color: #c0c0d0; font-weight: bold;}")
        targets_layout = QFormLayout()
        
        dmi = QDoubleSpinBox()
        dmi.setRange(10, 30)
        dmi.setValue(22)
        dmi.setSuffix(" kg/gün")
        
        cp = QDoubleSpinBox()
        cp.setRange(10, 25)
        cp.setValue(16)
        cp.setSuffix(" % KM")
        
        targets_layout.addRow("Kuru Madde Alımı (DMI):", dmi)
        targets_layout.addRow("Ham Protein (HP):", cp)
        
        targets_box.setLayout(targets_layout)
        
        save_btn = QPushButton("💾 Rasyonu Kaydet")
        save_btn.setFixedHeight(45)
        save_btn.setStyleSheet("QPushButton {background-color: #4a90d9; border: none; border-radius: 8px; color: white; font-size: 14px; font-weight: bold;}")
        
        layout.addWidget(header)
        layout.addWidget(group_box)
        layout.addWidget(targets_box)
        layout.addWidget(save_btn)
        layout.addStretch()
        
        page.setLayout(layout)
        return page
        
    def create_optimize_page(self):
        """Optimization page."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("Rasyon Optimizasyonu")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        info = QLabel("Bu modül, verilen besin hedeflerini en düşük maliyetle karşılayan rasyonu hesaplar.")
        info.setStyleSheet("color: #808090; font-size: 13px;")
        
        optimize_btn = QPushButton("⚡ Optimize Et")
        optimize_btn.setFixedHeight(45)
        optimize_btn.setStyleSheet("QPushButton {background-color: #2ecc71; border: none; border-radius: 8px; color: white; font-size: 14px; font-weight: bold;}")
        
        results = QLabel("Sonuçlar burada gösterilecek...")
        results.setStyleSheet("color: #808090; padding: 20px;")
        
        layout.addWidget(header)
        layout.addWidget(info)
        layout.addWidget(optimize_btn)
        layout.addWidget(results)
        layout.addStretch()
        
        page.setLayout(layout)
        return page
        
    def create_economic_page(self):
        """Economic analysis page."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("Ekonomik Analiz")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        iofc_box = QGroupBox("IOFC (Income Over Feed Cost)")
        iofc_box.setStyleSheet("QGroupBox {color: #c0c0d0; font-weight: bold;}")
        iofc_layout = QFormLayout()
        
        price = QDoubleSpinBox()
        price.setRange(0, 50)
        price.setValue(12.50)
        price.setPrefix("₺ ")
        price.setSuffix("/kg")
        
        yield_ = QDoubleSpinBox()
        yield_.setRange(0, 100)
        yield_.setValue(35)
        yield_.setSuffix(" kg/gün")
        
        iofc_layout.addRow("Süt Fiyatı:", price)
        iofc_layout.addRow("Günlük Süt Verimi:", yield_)
        
        iofc_box.setLayout(iofc_layout)
        
        calc_btn = QPushButton("📊 IOFC Hesapla")
        calc_btn.setStyleSheet("QPushButton {background-color: #2a2a4e; border: none; border-radius: 5px; color: #c0c0d0; padding: 10px 20px;}")
        
        layout.addWidget(header)
        layout.addWidget(iofc_box)
        layout.addWidget(calc_btn)
        layout.addStretch()
        
        page.setLayout(layout)
        return page
        
    def create_reports_page(self):
        """Reports page."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        header = QLabel("Raporlar")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        
        type_box = QGroupBox("Rapor Türü")
        type_box.setStyleSheet("QGroupBox {color: #c0c0d0; font-weight: bold;}")
        type_layout = QVBoxLayout()
        
        r1 = QPushButton("📋 Rasyon Raporu")
        r2 = QPushButton("💰 Ekonomik Rapor")
        r3 = QPushButton("🌿 Çevresel Etki Raporu")
        
        for r in [r1, r2, r3]:
            r.setStyleSheet("QPushButton {background-color: #1a1a2e; border: 1px solid #2a2a4e; border-radius: 5px; color: #c0c0d0; padding: 10px; text-align: left;}")
            type_layout.addWidget(r)
        
        type_box.setLayout(type_layout)
        
        gen_btn = QPushButton("📄 Rapor Oluştur")
        gen_btn.setFixedHeight(45)
        gen_btn.setStyleSheet("QPushButton {background-color: #9b59b6; border: none; border-radius: 8px; color: white; font-size: 14px; font-weight: bold;}")
        
        layout.addWidget(header)
        layout.addWidget(type_box)
        layout.addWidget(gen_btn)
        layout.addStretch()
        
        page.setLayout(layout)
        return page
        
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
    
    def logout(self):
        if self.controller:
            self.controller.logout()