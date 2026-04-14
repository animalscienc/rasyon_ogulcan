# Dashboard View for Zootekni Pro
# Main dashboard with sidebar navigation and content area

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QStackedWidget, QScrollArea,
                             QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
                             QComboBox, QSpinBox, QDoubleSpinBox, QGroupBox,
                             QFormLayout, QRadioButton, QButtonGroup)
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QTimer
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DashboardView(QMainWindow):
    """Main dashboard with sidebar navigation."""
    
    def __init__(self):
        """Initialize dashboard view."""
        super().__init__()
        self.controller = None
        self.current_page = "dashboard"
        self.setup_ui()
        self.apply_stylesheet()
        
    def set_controller(self, controller):
        """Set the controller for this view."""
        self.controller = controller
        # Handle both AuthController and DashboardController
        if hasattr(controller, 'current_user'):
            user = controller.current_user
        else:
            user = controller.user
        username = user.get('full_name') or user.get('username', 'Admin') if user else 'Admin'
        self.user_info_label.setText(f"Kullanıcı: {username}")
        
    def setup_ui(self):
        """Setup UI components."""
        self.setWindowTitle("Zootekni Pro - Intelligent Rationing System")
        self.setMinimumSize(1280, 800)
        self.move_to_center()
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left sidebar
        sidebar = self.create_sidebar()
        sidebar.setMinimumWidth(250)
        sidebar.setMaximumWidth(280)
        
        # Main content area
        content_area = self.create_content_area()
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area, 1)
        
        central.setLayout(main_layout)
        
    def move_to_center(self):
        """Move window to center of screen."""
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            rect = screen.geometry()
            self.move((rect.width() - self.width()) // 2, 
                     (rect.height() - self.height()) // 2)
            
    def create_sidebar(self) -> QFrame:
        """Create sidebar navigation."""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Logo area
        logo_area = self.create_logo_area()
        
        # Menu items
        menu = self.create_menu()
        
        # User info area
        user_area = self.create_user_area()
        
        layout.addWidget(logo_area)
        layout.addWidget(menu, 1)
        layout.addWidget(user_area)
        
        sidebar.setLayout(layout)
        return sidebar
        
    def create_logo_area(self) -> QFrame:
        """Create logo and title area."""
        area = QFrame()
        area.setObjectName("logoArea")
        area.setFixedHeight(80)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Logo placeholder (circle with Z)
        logo = QLabel("Z")
        logo.setObjectName("logoIcon")
        
        # Title
        title_layout = QVBoxLayout()
        title = QLabel("Zootekni Pro")
        title.setObjectName("logoTitle")
        
        subtitle = QLabel("Intelligent Rationing")
        subtitle.setObjectName("logoSubtitle")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        layout.addWidget(logo)
        layout.addLayout(title_layout)
        layout.addStretch()
        
        area.setLayout(layout)
        return area
        
    def create_menu(self) -> QFrame:
        """Create navigation menu."""
        frame = QFrame()
        frame.setObjectName("menuFrame")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)
        
        menu_items = [
            ("dashboard", "📊", "Anasayfa"),
            ("feeds", "🌾", "Yem Kütüphanesi"),
            ("animals", "🐄", "Hayvan Grupları"),
            ("ration", "📋", "Rasyon Oluştur"),
            ("optimize", "⚡", "Optimizasyon"),
            ("economic", "💰", "Ekonomik Analiz"),
            ("reports", "📄", "Raporlar"),
            ("settings", "⚙️", "Ayarlar"),
        ]
        
        self.menu_buttons = {}
        
        for item_id, icon, text in menu_items:
            btn = QPushButton(f"  {icon}  {text}")
            btn.setObjectName("menuButton")
            btn.setCheckable(True)
            # Use default argument in lambda to capture current value
            btn.clicked.connect(lambda checked, id=item_id: self.menu_clicked(id))
            self.menu_buttons[item_id] = btn
            layout.addWidget(btn)
            
        # Set first item as selected
        self.menu_buttons["dashboard"].setChecked(True)
        
        return frame
        
    def create_user_area(self) -> QFrame:
        """Create user info and logout area."""
        area = QFrame()
        area.setObjectName("userArea")
        area.setFixedHeight(60)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 0, 20, 0)
        
        # User info
        self.user_info_label = QLabel("Kullanıcı: Admin")
        self.user_info_label.setObjectName("userInfo")
        
        # Logout button
        logout_btn = QPushButton("🚪 Çıkış")
        logout_btn.setObjectName("logoutButton")
        logout_btn.clicked.connect(self.logout_clicked)
        
        layout.addWidget(self.user_info_label)
        layout.addStretch()
        layout.addWidget(logout_btn)
        
        area.setLayout(layout)
        return area
        
    def create_content_area(self) -> QFrame:
        """Create main content area with stacked pages."""
        content = QFrame()
        content.setObjectName("contentArea")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Content stack
        self.content_stack = QStackedWidget()
        
        # Add pages
        self.content_stack.addWidget(self.create_dashboard_page())
        self.content_stack.addWidget(self.create_feeds_page())
        self.content_stack.addWidget(self.create_animals_page())
        self.content_stack.addWidget(self.create_ration_page())
        self.content_stack.addWidget(self.create_optimize_page())
        self.content_stack.addWidget(self.create_economic_page())
        self.content_stack.addWidget(self.create_reports_page())
        self.content_stack.addWidget(self.create_settings_page())
        
        layout.addWidget(self.content_stack)
        
        content.setLayout(layout)
        return content
        
    def create_dashboard_page(self) -> QWidget:
        """Create dashboard home page."""
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Hoş Geldiniz - Zootekni Pro")
        header.setObjectName("pageHeader")
        
        # Info cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)
        
        cards = [
            ("📊", "Toplam Yem", "310", "Kalem"),
            ("🐄", "Hayvan Grubu", "12", "Grup"),
            ("📋", "Kayıtlı Rasyon", "45", "Adet"),
            ("💰", "Son Maliyet", "₺12.50", "/kg KM"),
        ]
        
        for icon, title, value, unit in cards:
            card = self.create_info_card(icon, title, value, unit)
            cards_layout.addWidget(card)
            
        layout.addWidget(header)
        layout.addLayout(cards_layout)
        
        # Recent rations table
        recent_label = QLabel("Son Rasyonlar")
        recent_label.setObjectName("sectionHeader")
        
        self.recent_table = QTableWidget(5, 6)
        self.recent_table.setObjectName("dataTable")
        self.recent_table.setHorizontalHeaderLabels([
            "Rasyon Adı", "Grup", "KM (kg)", "HP (%)", "Maliyet (₺)", "Tarih"
        ])
        self.recent_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Quick actions
        actions_label = QLabel("Hızlı İşlemler")
        actions_label.setObjectName("sectionHeader")
        
        actions_layout = QHBoxLayout()
        
        new_ration_btn = QPushButton("➕ Yeni Rasyon")
        new_ration_btn.setObjectName("actionButton")
        new_ration_btn.clicked.connect(lambda: self.menu_clicked("ration"))
        
        optimize_btn = QPushButton("⚡ Optimize Et")
        optimize_btn.setObjectName("actionButton")
        optimize_btn.clicked.connect(lambda: self.menu_clicked("optimize"))
        
        report_btn = QPushButton("📄 Rapor Al")
        report_btn.setObjectName("actionButton")
        report_btn.clicked.connect(lambda: self.menu_clicked("reports"))
        
        actions_layout.addWidget(new_ration_btn)
        actions_layout.addWidget(optimize_btn)
        actions_layout.addWidget(report_btn)
        
        layout.addStretch()
        
        page.setLayout(layout)
        return page
        
    def create_info_card(self, icon: str, title: str, value: str, unit: str) -> QFrame:
        """Create info card widget."""
        card = QFrame()
        card.setObjectName("infoCard")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        icon_label = QLabel(icon)
        icon_label.setObjectName("cardIcon")
        
        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        
        value_layout = QHBoxLayout()
        value_layout.setSpacing(5)
        
        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        
        unit_label = QLabel(unit)
        unit_label.setObjectName("cardUnit")
        
        value_layout.addWidget(value_label)
        value_layout.addWidget(unit_label)
        value_layout.addStretch()
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addLayout(value_layout)
        
        card.setLayout(layout)
        return card
        
    def create_feeds_page(self) -> QWidget:
        """Create feeds library page."""
        page = QScrollArea()
        page.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Yem Kütüphanesi")
        header.setObjectName("pageHeader")
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        search_box = QComboBox()
        search_box.setObjectName("searchBox")
        search_box.addItems(["Tüm Kategoriler", "Kaba Yem", "Konsantre", "Yem Katkıları"])
        
        search_btn = QPushButton("🔍 Ara")
        search_btn.setObjectName("toolButton")
        
        add_btn = QPushButton("➕ Yeni Yem Ekle")
        add_btn.setObjectName("toolButton")
        
        import_btn = QPushButton("📥 İçe Aktar")
        import_btn.setObjectName("toolButton")
        
        toolbar.addWidget(search_box)
        toolbar.addWidget(search_btn)
        toolbar.addStretch()
        toolbar.addWidget(add_btn)
        toolbar.addWidget(import_btn)
        
        # Feeds table
        self.feeds_table = QTableWidget(0, 10)
        self.feeds_table.setObjectName("dataTable")
        self.feeds_table.setHorizontalHeaderLabels([
            "Kod", "Yem Adı", "Kategori", "KM (%)", "HP (%)", "NDF (%)", 
            "NEL (Mcal/kg)", "Fiyat (₺)", "Min (%)", "Max (%)"
        ])
        self.feeds_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(header)
        layout.addLayout(toolbar)
        layout.addWidget(self.feeds_table)
        
        content.setLayout(layout)
        page.setWidget(content)
        return page
        
    def create_animals_page(self) -> QWidget:
        """Create animal groups page."""
        page = QScrollArea()
        page.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        header = QLabel("Hayvan Grupları")
        header.setObjectName("pageHeader")
        
        toolbar = QHBoxLayout()
        
        add_btn = QPushButton("➕ Yeni Grup Ekle")
        add_btn.setObjectName("toolButton")
        
        toolbar.addStretch()
        toolbar.addWidget(add_btn)
        
        # Animal groups table
        self.animals_table = QTableWidget(0, 8)
        self.animals_table.setObjectName("dataTable")
        self.animals_table.setHorizontalHeaderLabels([
            "Grup Adı", "Hayvan Türü", "Canlı Ağırlık (kg)", "Süt Verimi (kg)", 
            "Yağ (%)", "Protein (%)", "Laktasyon Haftası", "Durum"
        ])
        self.animals_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(header)
        layout.addLayout(toolbar)
        layout.addWidget(self.animals_table)
        
        content.setLayout(layout)
        page.setWidget(content)
        return page
        
    def create_ration_page(self) -> QWidget:
        """Create ration creation page."""
        page = QScrollArea()
        page.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        header = QLabel("Rasyon Oluştur")
        header.setObjectName("pageHeader")
        
        # Animal group selection
        group_box = QGroupBox("Hayvan Grubu Seçimi")
        group_layout = QFormLayout()
        
        self.group_combo = QComboBox()
        self.group_combo.addItems(["Yüksek Verimli Sürü (Laktasyon 1-12)", 
                                   "Orta Verimli Sürü (Laktasyon 13-24)",
                                   "Kuru Dönem"])
        group_layout.addRow("Grup:", self.group_combo)
        
        group_box.setLayout(group_layout)
        
        # Nutrition targets
        targets_box = QGroupBox("Besin Hedefleri")
        targets_layout = QFormLayout()
        
        self.dmi_target = QDoubleSpinBox()
        self.dmi_target.setRange(10, 30)
        self.dmi_target.setValue(22)
        self.dmi_target.setSuffix(" kg/gün")
        
        self.cp_target = QDoubleSpinBox()
        self.cp_target.setRange(10, 25)
        self.cp_target.setValue(16)
        self.cp_target.setSuffix(" % KM")
        
        self.ndf_target = QDoubleSpinBox()
        self.ndf_target.setRange(15, 40)
        self.ndf_target.setValue(28)
        self.ndf_target.setSuffix(" % KM")
        
        self.nel_target = QDoubleSpinBox()
        self.nel_target.setRange(1.0, 2.5)
        self.nel_target.setValue(1.65)
        self.nel_target.setSuffix(" Mcal/kg KM")
        
        targets_layout.addRow("Kuru Madde Alımı (DMI):", self.dmi_target)
        targets_layout.addRow("Ham Protein (HP):", self.cp_target)
        targets_layout.addRow("NDF:", self.ndf_target)
        targets_layout.addRow("Net Enerji (NEL):", self.nel_target)
        
        targets_box.setLayout(targets_layout)
        
        # Feed selection
        feeds_box = QGroupBox("Yem Seçimi")
        feeds_layout = QVBoxLayout()
        
        add_feed_btn = QPushButton("➕ Yem Ekle")
        add_feed_btn.setObjectName("toolButton")
        
        self.selected_feeds_table = QTableWidget(0, 6)
        self.selected_feeds_table.setObjectName("dataTable")
        self.selected_feeds_table.setHorizontalHeaderLabels([
            "Yem", "Miktar (kg)", "KM (kg)", "Oran (%)", "Maliyet (₺)", "İşlem"
        ])
        
        feeds_layout.addWidget(add_feed_btn)
        feeds_layout.addWidget(self.selected_feeds_table)
        
        feeds_box.setLayout(feeds_layout)
        
        # Save button
        save_btn = QPushButton("💾 Rasyonu Kaydet")
        save_btn.setObjectName("primaryButton")
        save_btn.setFixedHeight(50)
        
        layout.addWidget(header)
        layout.addWidget(group_box)
        layout.addWidget(targets_box)
        layout.addWidget(feeds_box)
        layout.addWidget(save_btn)
        
        content.setLayout(layout)
        page.setWidget(content)
        return page
        
    def create_optimize_page(self) -> QWidget:
        """Create optimization page."""
        page = QScrollArea()
        page.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        header = QLabel("Rasyon Optimizasyonu")
        header.setObjectName("pageHeader")
        
        info = QLabel(
            "Bu modül, verilen besin hedeflerini en düşük maliyetle karşılayan "
            "rasyonu Simplex algoritması kullanarak hesaplar."
        )
        info.setObjectName("infoText")
        
        optimize_btn = QPushButton("⚡ Optimize Et")
        optimize_btn.setObjectName("primaryButton")
        optimize_btn.setFixedHeight(50)
        
        results_box = QGroupBox("Optimizasyon Sonuçları")
        results_layout = QVBoxLayout()
        
        results_text = QLabel("Henüz optimizasyon yapılmadı.")
        results_layout.addWidget(results_text)
        
        results_box.setLayout(results_layout)
        
        layout.addWidget(header)
        layout.addWidget(info)
        layout.addWidget(optimize_btn)
        layout.addWidget(results_box)
        layout.addStretch()
        
        content.setLayout(layout)
        page.setWidget(content)
        return page
        
    def create_economic_page(self) -> QWidget:
        """Create economic analysis page."""
        page = QScrollArea()
        page.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        header = QLabel("Ekonomik Analiz")
        header.setObjectName("pageHeader")
        
        # IOFC section
        iofc_box = QGroupBox("IOFC (Income Over Feed Cost)")
        iofc_layout = QFormLayout()
        
        self.milk_price = QDoubleSpinBox()
        self.milk_price.setRange(0, 50)
        self.milk_price.setValue(12.50)
        self.milk_price.setPrefix("₺ ")
        self.milk_price.setSuffix("/kg")
        
        self.milk_yield_daily = QDoubleSpinBox()
        self.milk_yield_daily.setRange(0, 100)
        self.milk_yield_daily.setValue(35)
        self.milk_yield_daily.setSuffix(" kg/gün")
        
        iofc_layout.addRow("Süt Fiyatı:", self.milk_price)
        iofc_layout.addRow("Günlük Süt Verimi:", self.milk_yield_daily)
        
        iofc_box.setLayout(iofc_layout)
        
        # Analysis buttons
        buttons_layout = QHBoxLayout()
        
        iofc_calc_btn = QPushButton("📊 IOFC Hesapla")
        iofc_calc_btn.setObjectName("toolButton")
        
        sensitivity_btn = QPushButton("📈 Duyarlılık Analizi")
        sensitivity_btn.setObjectName("toolButton")
        
        shadow_btn = QPushButton("💡 Gölge Fiyatlar")
        shadow_btn.setObjectName("toolButton")
        
        buttons_layout.addWidget(iofc_calc_btn)
        buttons_layout.addWidget(sensitivity_btn)
        buttons_layout.addWidget(shadow_btn)
        
        # Results
        results_box = QGroupBox("Sonuçlar")
        results_layout = QVBoxLayout()
        
        results_layout.addWidget(QLabel("Henüz analiz yapılmadı."))
        
        results_box.setLayout(results_layout)
        
        layout.addWidget(header)
        layout.addWidget(iofc_box)
        layout.addLayout(buttons_layout)
        layout.addWidget(results_box)
        layout.addStretch()
        
        content.setLayout(layout)
        page.setWidget(content)
        return page
        
    def create_reports_page(self) -> QWidget:
        """Create reports page."""
        page = QScrollArea()
        page.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        header = QLabel("Raporlar")
        header.setObjectName("pageHeader")
        
        # Report type selection
        type_box = QGroupBox("Rapor Türü")
        type_layout = QVBoxLayout()
        
        self.report_type_group = QButtonGroup(self)
        
        ration_radio = QRadioButton("📋 Rasyon Raporu")
        ration_radio.setChecked(True)
        self.report_type_group.addButton(ration_radio, 1)
        
        economic_radio = QRadioButton("💰 Ekonomik Rapor")
        self.report_type_group.addButton(economic_radio, 2)
        
        environmental_radio = QRadioButton("🌿 Çevresel Etki Raporu")
        self.report_type_group.addButton(environmental_radio, 3)
        
        type_layout.addWidget(ration_radio)
        type_layout.addWidget(economic_radio)
        type_layout.addWidget(environmental_radio)
        
        type_box.setLayout(type_layout)
        
        # Generate button
        generate_btn = QPushButton("📄 Rapor Oluştur")
        generate_btn.setObjectName("primaryButton")
        generate_btn.setFixedHeight(50)
        
        layout.addWidget(header)
        layout.addWidget(type_box)
        layout.addWidget(generate_btn)
        layout.addStretch()
        
        content.setLayout(layout)
        page.setWidget(content)
        return page
        
    def create_settings_page(self) -> QWidget:
        """Create settings page."""
        page = QScrollArea()
        page.setWidgetResizable(True)
        
        content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        header = QLabel("Ayarlar")
        header.setObjectName("pageHeader")
        
        # Database settings
        db_box = QGroupBox("Veritabanı Ayarları")
        db_layout = QFormLayout()
        
        db_path = QLabel("/workspace/project/data/zootekni.db")
        db_layout.addRow("Veritabanı:", db_path)
        
        backup_btn = QPushButton("💾 Yedek Al")
        backup_btn.setObjectName("toolButton")
        db_layout.addRow("", backup_btn)
        
        db_box.setLayout(db_layout)
        
        # Standards settings
        standards_box = QGroupBox("Besleme Standartları")
        standards_layout = QFormLayout()
        
        self.standard_combo = QComboBox()
        self.standard_combo.addItems(["NRC 2021", "INRA", "ARC", "Türk Standartları"])
        
        standards_layout.addRow("Standart:", self.standard_combo)
        
        standards_box.setLayout(standards_layout)
        
        # About
        about_box = QGroupBox("Hakkında")
        about_layout = QVBoxLayout()
        
        about_text = QLabel(
            "Zootekni Pro v5.0\n"
            "Precision Livestock Farming & Computational Nutrition\n\n"
            "© 2024 Zootekni"
        )
        about_layout.addWidget(about_text)
        
        about_box.setLayout(about_layout)
        
        layout.addWidget(header)
        layout.addWidget(db_box)
        layout.addWidget(standards_box)
        layout.addWidget(about_box)
        layout.addStretch()
        
        content.setLayout(layout)
        page.setWidget(content)
        return page
        
    def menu_clicked(self, view_id: str):
        """Handle menu button click."""
        # Update button states
        for btn_id, btn in self.menu_buttons.items():
            btn.setChecked(btn_id == view_id)
        
        # Switch content
        page_map = {
            "dashboard": 0,
            "feeds": 1,
            "animals": 2,
            "ration": 3,
            "optimize": 4,
            "economic": 5,
            "reports": 6,
            "settings": 7,
        }
        
        if view_id in page_map:
            self.content_stack.setCurrentIndex(page_map[view_id])
            self.current_page = view_id
            
    def logout_clicked(self):
        """Handle logout button click."""
        if self.controller:
            self.controller.logout()
            
    def apply_stylesheet(self):
        """Apply dark theme stylesheet."""
        self.setStyleSheet("""
            QMainWindow {
                background: #0a0a14;
            }
            
            /* Sidebar */
            #sidebar {
                background: #12121e;
                border-right: 1px solid #1e1e2e;
            }
            
            #logoArea {
                background: #0f0f1a;
                border-bottom: 1px solid #1e1e2e;
            }
            
            #logoIcon {
                font-size: 36px;
                font-weight: bold;
                color: #4a90d9;
                background: #1a1a2e;
                border-radius: 20px;
                min-width: 40px;
                max-width: 40px;
                min-height: 40px;
                max-height: 40px;
                qproperty-alignment: AlignCenter;
            }
            
            #logoTitle {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #logoSubtitle {
                font-size: 11px;
                color: #606070;
            }
            
            #menuFrame {
                background: transparent;
            }
            
            #menuButton {
                background: transparent;
                border: none;
                border-radius: 10px;
                padding: 12px 15px;
                font-size: 14px;
                color: #a0a0b0;
                text-align: left;
                qproperty-alignment: AlignLeft;
            }
            
            #menuButton:hover {
                background: #1a1a2e;
                color: #ffffff;
            }
            
            #menuButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2a2a4e,
                    stop:1 #1e1e3e);
                color: #4a90d9;
                border-left: 3px solid #4a90d9;
            }
            
            #userArea {
                background: #0f0f1a;
                border-top: 1px solid #1e1e2e;
            }
            
            #userInfo {
                font-size: 12px;
                color: #808090;
            }
            
            #logoutButton {
                background: transparent;
                border: 1px solid #3a3a5e;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 12px;
                color: #a0a0b0;
            }
            
            #logoutButton:hover {
                background: #3a3a5e;
                color: #ffffff;
            }
            
            /* Content Area */
            #contentArea {
                background: #0a0a14;
            }
            
            /* Headers */
            #pageHeader {
                font-size: 24px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #sectionHeader {
                font-size: 16px;
                font-weight: 600;
                color: #c0c0d0;
            }
            
            /* Info Cards */
            #infoCard {
                background: #12121e;
                border-radius: 15px;
                border: 1px solid #1e1e2e;
            }
            
            #cardIcon {
                font-size: 28px;
            }
            
            #cardTitle {
                font-size: 13px;
                color: #808090;
            }
            
            #cardValue {
                font-size: 28px;
                font-weight: bold;
                color: #ffffff;
            }
            
            #cardUnit {
                font-size: 12px;
                color: #606070;
            }
            
            /* Buttons */
            #actionButton, #toolButton {
                background: #1a1a2e;
                border: 1px solid #2a2a4e;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                color: #c0c0d0;
            }
            
            #actionButton:hover, #toolButton:hover {
                background: #2a2a4e;
                color: #ffffff;
            }
            
            #primaryButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90d9,
                    stop:1 #357abd);
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
                color: #ffffff;
            }
            
            #primaryButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5a9fe9,
                    stop:1 #458acd);
            }
            
            /* Tables */
            #dataTable {
                background: #12121e;
                border: 1px solid #1e1e2e;
                border-radius: 10px;
                gridline-color: #1e1e2e;
            }
            
            QHeaderView::section {
                background: #1a1a2e;
                color: #a0a0b0;
                border: none;
                padding: 10px;
                font-weight: 600;
            }
            
            QTableWidget::item {
                color: #c0c0d0;
                border-bottom: 1px solid #1e1e2e;
                padding: 8px;
            }
            
            QTableWidget::item:selected {
                background: #2a2a4e;
                color: #ffffff;
            }
            
            /* Group Boxes */
            QGroupBox {
                background: #12121e;
                border: 1px solid #1e1e2e;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 20px;
                color: #c0c0d0;
                font-weight: 600;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                color: #4a90d9;
            }
            
            /* Form Fields */
            QFormLayout label {
                color: #a0a0b0;
            }
            
            QSpinBox, QDoubleSpinBox, QComboBox {
                background: #1a1a2e;
                border: 2px solid #2a2a4e;
                border-radius: 8px;
                padding: 8px 12px;
                color: #ffffff;
            }
            
            QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border: 2px solid #4a90d9;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #606070;
            }
            
            /* Radio Buttons */
            QRadioButton {
                color: #c0c0d0;
                spacing: 10px;
            }
            
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #3a3a5e;
                background: #1a1a2e;
            }
            
            QRadioButton::indicator:checked {
                border: 2px solid #4a90d9;
                background: #4a90d9;
            }
            
            /* Info Text */
            #infoText {
                font-size: 13px;
                color: #808090;
                line-height: 150%;
            }
            
            /* Scroll Area */
            QScrollArea {
                border: none;
            }
            
            QScrollBar:vertical {
                background: #12121e;
                width: 10px;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical {
                background: #2a2a4e;
                border-radius: 5px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: #3a3a5e;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)