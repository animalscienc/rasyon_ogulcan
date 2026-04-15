"""
Dashboard Window - Main Application Interface for Zootekni Pro
Modern dashboard structure with sidebar navigation
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QStackedWidget, QScrollArea, QSplitter, QGridLayout,
    QTableWidget, QTableWidgetItem, QComboBox, QLineEdit, QSpinBox,
    QDoubleSpinBox, QGroupBox, QFormLayout, QTabWidget, QTextEdit,
    QCheckBox, QRadioButton, QSlider, QProgressBar, QMenuBar, QMenu,
    QStatusBar, QAction, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer, QThread
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QLinearGradient
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from utils.logger import get_logger
from utils.constants import (
    APP_NAME, APP_VERSION, APP_SUBTITLE, SIDEBAR_WIDTH, 
    HEADER_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    ANIMAL_GROUPS, FEED_CATEGORIES
)
from views.widgets import ModernButton, ModernCard, ModernInput, ModernTable, StatCard

logger = get_logger(__name__)


class DashboardWindow(QWidget):
    """Main dashboard application window."""
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger(__name__)
        self.current_page = "dashboard"
        self.init_ui()
        self.logger.info("Dashboard initialized")
    
    def init_ui(self):
        """Initialize main dashboard UI."""
        self.setWindowTitle(f"{APP_NAME} - {APP_SUBTITLE}")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.menu_clicked.connect(self.on_menu_clicked)
        main_layout.addWidget(self.sidebar)
        
        # Create content area
        content_container = QFrame()
        content_container.setObjectName("contentContainer")
        content_container.setStyleSheet("""
            QFrame#contentContainer {
                background-color: #0D1117;
            }
        """)
        
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Header bar
        self.header = HeaderBar()
        content_layout.addWidget(self.header)
        
        # Content pages (stacked widget)
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack)
        
        # Create different pages
        self.dashboard_page = DashboardPage()
        self.feeds_page = FeedsPage()
        self.optimizer_page = OptimizerPage()
        self.reports_page = ReportsPage()
        self.settings_page = SettingsPage()
        
        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.feeds_page)
        self.content_stack.addWidget(self.optimizer_page)
        self.content_stack.addWidget(self.reports_page)
        self.content_stack.addWidget(self.settings_page)
        
        main_layout.addWidget(content_container, 1)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #161B22;
                border-top: 1px solid #30363D;
                color: #8B949E;
            }
            QStatusBar::item {
                border: none;
            }
        """)
        self.status_bar.showMessage(f"{APP_NAME} v{APP_VERSION} - Hazır")
        content_layout.addWidget(self.status_bar)
    
    def on_menu_clicked(self, menu_id: str):
        """Handle sidebar menu clicks."""
        self.logger.info(f"Menu clicked: {menu_id}")
        
        # Map menu IDs to page indices
        page_map = {
            "dashboard": 0,
            "feeds": 1,
            "optimizer": 2,
            "reports": 3,
            "settings": 4
        }
        
        if menu_id in page_map:
            self.content_stack.setCurrentIndex(page_map[menu_id])
            self.current_page = menu_id
            self.status_bar.showMessage(f"Sayfa: {menu_id.capitalize()}")


class Sidebar(QFrame):
    """Sidebar navigation menu."""
    
    menu_clicked = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_menu = "dashboard"
        self.init_ui()
    
    def init_ui(self):
        """Initialize sidebar UI."""
        self.setObjectName("sidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)
        self.setStyleSheet("""
            QFrame#sidebar {
                background-color: #161B22;
                border-right: 1px solid #30363D;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 16, 8, 16)
        layout.setSpacing(4)
        
        # Logo section
        logo_layout = QVBoxLayout()
        logo_layout.setSpacing(4)
        logo_layout.setContentsMargins(8, 0, 8, 16)
        
        # App name
        app_name = QLabel(APP_NAME)
        app_name.setStyleSheet("""
            color: #58A6FF;
            font-size: 20px;
            font-weight: 700;
        """)
        
        # Subtitle
        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setStyleSheet("""
            color: #8B949E;
            font-size: 11px;
        """)
        
        logo_layout.addWidget(app_name)
        logo_layout.addWidget(subtitle)
        
        layout.addLayout(logo_layout)
        
        # Separator
        separator = QFrame()
        separator.setFixedHeight(1)
        separator.setStyleSheet("""
            background-color: #30363D;
            margin: 8px;
        """)
        layout.addWidget(separator)
        
        # Menu buttons
        menu_items = [
            ("dashboard", "📊", "Dashboard"),
            ("feeds", "🌾", "Feed Master"),
            ("optimizer", "⚖️", "Optimizer"),
            ("reports", "📈", "Reports"),
            ("settings", "⚙️", "Settings")
        ]
        
        self.menu_buttons = []
        
        for menu_id, icon, text in menu_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName("menuButton")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 8px;
                    color: #8B949E;
                    padding: 12px 16px;
                    text-align: left;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #21262D;
                    color: #F0F6FC;
                }
                QPushButton:pressed {
                    background-color: #30363D;
                }
                QPushButton:checked {
                    background-color: #21262D;
                    color: #58A6FF;
                    border-left: 3px solid #58A6FF;
                }
            """)
            btn.clicked.connect(lambda checked, m=menu_id: self.on_menu_clicked(m))
            
            self.menu_buttons.append(btn)
            layout.addWidget(btn)
        
        # Default selection
        self.menu_buttons[0].setChecked(True)
        
        # Spacer
        layout.addStretch()
        
        # User info section
        user_layout = QVBoxLayout()
        user_layout.setContentsMargins(8, 8, 8, 0)
        user_layout.setSpacing(4)
        
        separator2 = QFrame()
        separator2.setFixedHeight(1)
        separator2.setStyleSheet("background-color: #30363D; margin: 8px;")
        user_layout.addWidget(separator2)
        
        username = QLabel("Admin")
        username.setStyleSheet("color: #F0F6FC; font-size: 12px; font-weight: 600;")
        
        user_status = QLabel("🟢 Çevrimiçi")
        user_status.setStyleSheet("color: #7EE787; font-size: 11px;")
        
        user_layout.addWidget(username)
        user_layout.addWidget(user_status)
        
        layout.addLayout(user_layout)
    
    def on_menu_clicked(self, menu_id: str):
        """Handle menu button click."""
        self.selected_menu = menu_id
        self.menu_clicked.emit(menu_id)


class HeaderBar(QFrame):
    """Header bar with user info and actions."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize header bar."""
        self.setObjectName("headerFrame")
        self.setFixedHeight(HEADER_HEIGHT)
        self.setStyleSheet("""
            QFrame#headerFrame {
                background-color: #161B22;
                border-bottom: 1px solid #30363D;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)
        
        # Page title
        self.title_label = QLabel("Dashboard")
        self.title_label.setStyleSheet("""
            color: #F0F6FC;
            font-size: 20px;
            font-weight: 600;
        """)
        
        layout.addWidget(self.title_label)
        
        # Spacer
        layout.addStretch()
        
        # Action buttons
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        # Notifications button
        notif_btn = QPushButton("🔔")
        notif_btn.setObjectName("iconButton")
        notif_btn.setStyleSheet("""
            QPushButton#iconButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                padding: 8px 12px;
            }
            QPushButton#iconButton:hover {
                background-color: #21262D;
            }
        """)
        
        # Help button
        help_btn = QPushButton("❓ Yardım")
        help_btn.setObjectName("iconButton")
        help_btn.setStyleSheet("""
            QPushButton#iconButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: #8B949E;
                font-size: 12px;
                padding: 8px 12px;
            }
            QPushButton#iconButton:hover {
                background-color: #21262D;
                color: #F0F6FC;
            }
        """)
        
        actions_layout.addWidget(notif_btn)
        actions_layout.addWidget(help_btn)
        
        layout.addLayout(actions_layout)


class DashboardPage(QWidget):
    """Dashboard home page with statistics."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize dashboard page."""
        self.setStyleSheet("background-color: #0D1117;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Welcome section
        welcome_card = ModernCard("Hoş Geldiniz")
        layout.addWidget(welcome_card)
        
        welcome_layout = QVBoxLayout()
        welcome_layout.setSpacing(8)
        
        welcome_text = QLabel("Zootekni Pro: Akıllı Rasyonlama Sistemi")
        welcome_text.setStyleSheet("""
            color: #F0F6FC;
            font-size: 24px;
            font-weight: 600;
        """)
        
        desc_text = QLabel("Hayvancılık sektörü için kapsamlı rasyon optimizasyonu ve ekonomik analiz platformu.")
        desc_text.setStyleSheet("color: #8B949E; font-size: 14px;")
        
        welcome_layout.addWidget(welcome_text)
        welcome_layout.addWidget(desc_text)
        
        welcome_card.layout().addLayout(welcome_layout)
        
        # Statistics row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        # Total feeds stat
        self.feeds_card = StatCard("Toplam Yem", "310", "🌾", "+12")
        stats_layout.addWidget(self.feeds_card)
        
        # Active rations stat
        self.rations_card = StatCard("Aktif Rasyon", "45", "📋", "+5")
        stats_layout.addWidget(self.rations_card)
        
        # Optimization runs stat
        self.opt_runs_card = StatCard("Optimizasyon", "128", "⚡", "+23")
        stats_layout.addWidget(self.opt_runs_card)
        
        # IOFC average stat
        self.iofc_card = StatCard("Ortalama IOFC", "₺45.20", "💰", "-2.1%")
        stats_layout.addWidget(self.iofc_card)
        
        layout.addLayout(stats_layout)
        
        # Recent rations section
        recent_card = ModernCard("Son Rasyonlar")
        
        recent_layout = QVBoxLayout()
        
        self.recent_table = ModernTable(["Tarih", "Hayvan Grubu", "Rasyon Adı", "DMI", "CP%", "NEL", "Maliyet", "Durum"])
        
        # Sample data
        sample_data = [
            ["2024-01-15", "HYA", "Lactation Peak A", "22.5", "16.8", "1.72", "₺125.50", "Aktif"],
            ["2024-01-14", "HYB", "Transition B", "18.2", "15.5", "1.65", "₺98.30", "Aktif"],
            ["2024-01-13", "MY", "Mid Lactation", "20.1", "15.8", "1.68", "₺108.00", "Arşiv"],
            ["2024-01-12", "DC", "Dry Cow Closeup", "12.5", "12.2", "1.45", "₺45.20", "Aktif"]
        ]
        
        for row in sample_data:
            self.recent_table.add_row(row)
        
        recent_layout.addWidget(self.recent_table)
        
        recent_card.layout().addLayout(recent_layout)
        
        layout.addWidget(recent_card)
        
        # Spacer to push content up
        layout.addStretch()


class FeedsPage(QWidget):
    """Feed Master table page."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize feeds page."""
        self.setStyleSheet("background-color: #0D1117;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Feed Master - Yem Kütüphanesi")
        title.setStyleSheet("""
            color: #F0F6FC;
            font-size: 24px;
            font-weight: 600;
        """)
        
        layout.addWidget(title)
        
        # Controls row
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(12)
        
        # Search
        search_input = ModernInput("Yem ara...", "Ara:")
        search_input.setFixedWidth(300)
        
        # Category filter
        category_combo = QComboBox()
        category_combo.addItems(["Tüm Kategoriler"] + FEED_CATEGORIES)
        category_combo.setFixedWidth(200)
        
        # Add button
        add_btn = ModernButton("➕ Yem Ekle", "primary")
        
        # Import/Export buttons
        import_btn = ModernButton("📥 İçe Aktar", "secondary")
        export_btn = ModernButton("📤 Dışa Aktar", "secondary")
        
        controls_layout.addWidget(search_input)
        controls_layout.addWidget(category_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(add_btn)
        controls_layout.addWidget(import_btn)
        controls_layout.addWidget(export_btn)
        
        layout.addLayout(controls_layout)
        
        # Feeds table
        table_card = ModernCard("")
        
        self.feeds_table = ModernTable([
            "ID", "Yem Adı", "Kategori", "KM%", "CP%", "EE%", "NDF%", "ADF%", 
            "NEL", "Ca", "P", "Fiyat (TL/kg)", "Kaynak"
        ])
        self.feeds_table.setColumnCount(13)
        self.feeds_table.setMinimumHeight(400)
        
        # Sample feed data
        sample_feeds = [
            ["1", "Mısır Silajı", "Roughages/Forages", 35.0, 8.5, 3.2, 45.0, 28.0, 1.65, 0.25, 0.22, 0.85, "NRC 2021"],
            ["2", "Yonca Kuru Otu", "Roughages/Forages", 90.0, 18.5, 2.8, 35.0, 22.0, 1.52, 1.45, 0.25, 2.50, "NRC 2021"],
            ["3", "Mısır Tanem", "Concentrates", 89.0, 9.5, 4.2, 12.0, 3.5, 2.10, 0.03, 0.28, 3.20, "NRC 2021"],
            ["4", "Soya Fasulyesi", "Protein Supplements", 89.0, 45.0, 1.5, 15.0, 6.0, 2.05, 0.25, 0.60, 8.50, "NRC 2021"],
            ["5", "Kepek", "Concentrates", 88.0, 15.0, 4.0, 30.0, 12.0, 1.55, 0.08, 0.50, 1.80, "Yerli"],
            ["6", "Arpa Tanem", "Concentrates", 88.0, 12.0, 2.0, 18.0, 6.0, 1.95, 0.05, 0.35, 2.90, "Yerli"]
        ]
        
        for feed in sample_feeds:
            self.feeds_table.add_row(feed)
        
        table_card.layout().addWidget(self.feeds_table)
        
        layout.addWidget(table_card, 1)


class OptimizerPage(QWidget):
    """Ration optimizer page."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize optimizer page."""
        self.setStyleSheet("background-color: #0D1117;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Rasyon Optimizasyonu")
        title.setStyleSheet("""
            color: #F0F6FC;
            font-size: 24px;
            font-weight: 600;
        """)
        
        layout.addWidget(title)
        
        # Input and output split
        splitter_h = QSplitter(Qt.Horizontal)
        
        # Input panel
        input_card = ModernCard("Hayvan Parametreleri")
        
        input_form = QFormLayout()
        input_form.setSpacing(12)
        
        # Animal type
        self.animal_type = QComboBox()
        self.animal_type.addItems(["Süt İnekleri (Laktasyon)", "Kuru İnekler", "Büyüyen Düve"])
        
        # Live weight
        self.live_weight = QSpinBox()
        self.live_weight.setRange(50, 800)
        self.live_weight.setValue(600)
        self.live_weight.setSuffix(" kg")
        
        # Milk yield
        self.milk_yield = QDoubleSpinBox()
        self.milk_yield.setRange(0, 60)
        self.milk_yield.setValue(30)
        self.milk_yield.setSuffix(" kg/gün")
        
        # Milk fat
        self.milk_fat = QDoubleSpinBox()
        self.milk_fat.setRange(2.0, 6.0)
        self.milk_fat.setValue(3.5)
        self.milk_fat.setSuffix(" %")
        
        # Add form fields
        input_form.addRow("Hayvan Tipi:", self.animal_type)
        input_form.addRow("Canlı Ağırlık:", self.live_weight)
        input_form.addRow("Süt Verimi:", self.milk_yield)
        input_form.addRow("Süt Yağı:", self.milk_fat)
        
        input_card.layout().addLayout(input_form)
        
        splitter_h.addWidget(input_card)
        
        # Constraints panel
        constraints_card = ModernCard("Kısıtlamalar")
        
        constraints_form = QFormLayout()
        constraints_form.setSpacing(12)
        
        self.min_ndf = QDoubleSpinBox()
        self.min_ndf.setRange(10, 50)
        self.min_ndf.setValue(20)
        self.min_ndf.setSuffix(" %")
        
        self.max_ndf = QDoubleSpinBox()
        self.max_ndf.setRange(20, 80)
        self.max_ndf.setValue(35)
        self.max_ndf.setSuffix(" %")
        
        self.min_cp = QDoubleSpinBox()
        self.min_cp.setRange(10, 30)
        self.min_cp.setValue(16)
        self.min_cp.setSuffix(" %")
        
        self.min_nel = QDoubleSpinBox()
        self.min_nel.setRange(1.0, 2.5)
        self.min_nel.setValue(1.6)
        self.min_nel.setSuffix(" Mcal/kg")
        
        constraints_form.addRow("Min eNDF:", self.min_ndf)
        constraints_form.addRow("Max eNDF:", self.max_ndf)
        constraints_form.addRow("Min CP:", self.min_cp)
        constraints_form.addRow("Min NEL:", self.min_nel)
        
        constraints_card.layout().addLayout(constraints_form)
        
        splitter_h.addWidget(constraints_card)
        
        layout.addWidget(splitter_h)
        
        # Optimize button
        optimize_btn = ModernButton("⚡ Optimizasyonu Başlat", "primary")
        
        layout.addWidget(optimize_btn)
        
        # Results card
        results_card = ModernCard("Optimizasyon Sonuçları")
        
        results_layout = QVBoxLayout()
        
        self.results_table = ModernTable([
            "Yem Adı", "Miktar (kg KM)", "%", "Maliyet (TL)", "CP%", "NEL"
        ])
        
        results_layout.addWidget(self.results_table)
        
        results_card.layout().addLayout(results_layout)
        
        layout.addWidget(results_card, 1)


class ReportsPage(QWidget):
    """Reports and charts page."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize reports page."""
        self.setStyleSheet("background-color: #0D1117;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Raporlar ve Analizler")
        title.setStyleSheet("""
            color: #F0F6FC;
            font-size: 24px;
            font-weight: 600;
        """)
        
        layout.addWidget(title)
        
        # Actions row
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)
        
        report_combo = QComboBox()
        report_combo.addItems([
            "Ekonomi Raporu", "Besin Değerleri", "Çevresel Etki", "Kıyaslama"
        ])
        report_combo.setFixedWidth(200)
        
        export_pdf_btn = ModernButton("📄 PDF İndir", "primary")
        export_excel_btn = ModernButton("📊 Excel İndir", "secondary")
        
        actions_layout.addWidget(report_combo)
        actions_layout.addStretch()
        actions_layout.addWidget(export_pdf_btn)
        actions_layout.addWidget(export_excel_btn)
        
        layout.addLayout(actions_layout)
        
        # Charts placeholder card
        charts_card = ModernCard("Görselleştirmeler")
        
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Radar chart placeholder
        radar_frame = QFrame()
        radar_frame.setMinimumSize(350, 300)
        radar_frame.setStyleSheet("""
            background-color: #21262D;
            border-radius: 12px;
            border: 1px solid #30363D;
        """)
        radar_label = QLabel("🕸️ Nutrient Radar Chart")
        radar_label.setAlignment(Qt.AlignCenter)
        radar_label.setStyleSheet("color: #8B949E; font-size: 16px;")
        
        radar_layout = QVBoxLayout(radar_frame)
        radar_layout.addWidget(radar_label)
        
        # Donut chart placeholder
        donut_frame = QFrame()
        donut_frame.setMinimumSize(350, 300)
        donut_frame.setStyleSheet("""
            background-color: #21262D;
            border-radius: 12px;
            border: 1px solid #30363D;
        """)
        donut_label = QLabel("🍩 Maliyet Dağılımı")
        donut_label.setAlignment(Qt.AlignCenter)
        donut_label.setStyleSheet("color: #8B949E; font-size: 16px;")
        
        donut_layout = QVBoxLayout(donut_frame)
        donut_layout.addWidget(donut_label)
        
        charts_layout.addWidget(radar_frame)
        charts_layout.addWidget(donut_frame)
        
        charts_card.layout().addLayout(charts_layout)
        
        layout.addWidget(charts_card)
        
        # Environmental impact
        env_card = ModernCard("Çevresel Etki")
        
        env_layout = QHBoxLayout()
        env_layout.setSpacing(20)
        
        methane_label = QLabel("🐄 Metan: 145 g/gün")
        methane_label.setStyleSheet("color: #F0F6FC; font-size: 14px;")
        
        n_excreted_label = QLabel("🧪 N Rejenerasyonu: 180 g/gün")
        n_excreted_label.setStyleSheet("color: #F0F6FC; font-size: 14px;")
        
        env_layout.addWidget(methane_label)
        env_layout.addWidget(n_excreted_label)
        env_layout.addStretch()
        
        env_card.layout().addLayout(env_layout)
        
        layout.addWidget(env_card)


class SettingsPage(QWidget):
    """Settings page."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize settings page."""
        self.setStyleSheet("background-color: #0D1117;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Ayarlar")
        title.setStyleSheet("""
            color: #F0F6FC;
            font-size: 24px;
            font-weight: 600;
        """)
        
        layout.addWidget(title)
        
        # Settings card
        settings_card = ModernCard("Genel Ayarlar")
        
        settings_form = QFormLayout()
        settings_form.setSpacing(16)
        
        # Language
        lang_combo = QComboBox()
        lang_combo.addItems(["Türkçe", "İngilizce"])
        
        # Theme
        theme_combo = QComboBox()
        theme_combo.addItems(["Dark Mode", "Light Mode"])
        
        # Default milk price
        milk_price = QDoubleSpinBox()
        milk_price.setRange(0, 100)
        milk_price.setValue(14.0)
        milk_price.setPrefix("₺ ")
        milk_price.setSuffix("/kg")
        
        settings_form.addRow("Dil:", lang_combo)
        settings_form.addRow("Tema:", theme_combo)
        settings_form.addRow("Süt Fiyatı:", milk_price)
        
        settings_card.layout().addLayout(settings_form)
        
        layout.addWidget(settings_card)
        
        # Update button
        save_btn = ModernButton("💾 Kaydet", "primary")
        
        layout.addWidget(save_btn)
        
        # About section
        about_card = ModernCard("Hakkında")
        
        about_text = QLabel(f"""
            <b>{APP_NAME}</b> v{APP_VERSION}<br><br>
            Türkiye'nin en kapsamlı rasyon mühendisliği platformu.<br>
            NRC (2021), INRA, ARC standartlarına dayalı.<br><br>
            © 2024 Zootekni Pro
        """)
        about_text.setWordWrap(True)
        about_text.setStyleSheet("color: #8B949E; font-size: 14px; line-height: 1.6;")
        
        about_card.layout().addWidget(about_text)
        
        layout.addWidget(about_card)