"""
QSS Styles for Zootekni Pro - Modern Adobe/Linear Style Interface
Version 5.0 - Dark Mode Support
"""

# Dark Mode Stylesheet
DARK_STYLESHEET = """
/ ============================================================
   ZOOTEKNI PRO - DARK MODE STYLESHEET
   Modern Adobe/Linear Inspired Design
   ============================================================ /

QWidget {
    background-color: #0D1117;
    color: #F0F6FC;
    font-family: "Segoe UI", "SF Pro Display", system-ui, sans-serif;
    font-size: 14px;
}

/ ============================================================
   MAIN WINDOW
   ============================================================ /

QMainWindow {
    background-color: #0D1117;
}

QFrame#mainFrame {
    background-color: #0D1117;
}

/ ============================================================
   SIDEBAR NAVIGATION
   ============================================================ /

QFrame#sidebar {
    background-color: #161B22;
    border-right: 1px solid #30363D;
}

QPushButton:sidebar {
    background-color: transparent;
    border: none;
    border-radius: 0px;
    color: #8B949E;
    padding: 12px 16px;
    text-align: left;
    font-size: 14px;
}

QPushButton:sidebar:hover {
    background-color: #21262D;
    color: #F0F6FC;
}

QPushButton:sidebar:pressed {
    background-color: #30363D;
}

QPushButton:sidebar:checked {
    background-color: #21262D;
    color: #58A6FF;
    border-left: 3px solid #58A6FF;
}

/ ============================================================
   HEADER BAR
   ============================================================ /

QFrame#headerFrame {
    background-color: #161B22;
    border-bottom: 1px solid #30363D;
}

QLabel#companyLabel {
    color: #58A6FF;
    font-size: 18px;
    font-weight: 600;
}

QLabel#userLabel {
    color: #8B949E;
    font-size: 12px;
}

/ ============================================================
   BUTTONS
   ============================================================ /

QPushButton {
    background-color: #238636;
    border: none;
    border-radius: 8px;
    color: #FFFFFF;
    padding: 10px 20px;
    font-weight: 500;
    min-height: 36px;
}

QPushButton:hover {
    background-color: #2EA043;
}

QPushButton:pressed {
    background-color: #238636;
}

QPushButton:disabled {
    background-color: #21262D;
    color: #484F58;
}

QPushButton#secondaryButton {
    background-color: transparent;
    border: 1px solid #30363D;
    color: #C9D1D9;
}

QPushButton#secondaryButton:hover {
    background-color: #21262D;
    border-color: #58A6FF;
}

QPushButton#dangerButton {
    background-color: #DA3633;
}

QPushButton#dangerButton:hover {
    background-color: #F85149;
}

QPushButton#iconButton {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    padding: 8px;
}

QPushButton#iconButton:hover {
    background-color: #21262D;
}

/ ============================================================
   INPUT FIELDS
   ============================================================ /

QLineEdit {
    background-color: #0D1117;
    border: 1px solid #30363D;
    border-radius: 8px;
    color: #F0F6FC;
    padding: 10px 12px;
    selection-background-color: #58A6FF;
    min-height: 36px;
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

/ ============================================================
   TEXT EDIT
   ============================================================ /

QTextEdit {
    background-color: #0D1117;
    border: 1px solid #30363D;
    border-radius: 8px;
    color: #F0F6FC;
    padding: 8px;
}

QTextEdit:focus {
    border-color: #58A6FF;
}

/ ============================================================
   COMBO BOX
   ============================================================ /

QComboBox {
    background-color: #0D1117;
    border: 1px solid #30363D;
    border-radius: 8px;
    color: #F0F6FC;
    padding: 10px 12px;
    min-height: 36px;
}

QComboBox:hover {
    border-color: #58A6FF;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #8B949E;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 8px;
    selection-background-color: #21262D;
    selection-color: #F0F6FC;
    padding: 4px;
}

/ ============================================================
   SPIN BOX
   ============================================================ /

QSpinBox, QDoubleSpinBox {
    background-color: #0D1117;
    border: 1px solid #30363D;
    border-radius: 8px;
    color: #F0F6FC;
    padding: 8px 12px;
    min-height: 32px;
}

QSpinBox:hover, QDoubleSpinBox:hover {
    border-color: #58A6FF;
}

QSpinBox::up-button, QDoubleSpinBox::up-button {
    background-color: transparent;
    border: none;
    width: 20px;
}

QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: transparent;
    border: none;
    width: 20px;
}

/ ============================================================
   TABLES
   ============================================================ /

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

QHeaderView::section:hover {
    background-color: #21262D;
}

QTableWidget::item {
    padding: 12px 8px;
    border: none;
}

QTableWidget::item:selected {
    background-color: #21262D;
}

QTableWidget::item:hover {
    background-color: #161B22;
}

/ ============================================================
   TABS
   ============================================================ /

QTabWidget::pane {
    background-color: #0D1117;
    border: 1px solid #30363D;
    border-radius: 12px;
}

QTabBar::tab {
    background-color: #161B22;
    border: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    color: #8B949E;
    padding: 12px 24px;
    margin-right: 2px;
}

QTabBar::tab:hover {
    background-color: #21262D;
    color: #F0F6FC;
}

QTabBar::tab:selected {
    background-color: #0D1117;
    color: #58A6FF;
    border-bottom: 2px solid #58A6FF;
}

/ ============================================================
   SCROLL BAR
   ============================================================ /

QScrollBar:vertical {
    background-color: transparent;
    border: none;
    width: 10px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background-color: #30363D;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #484F58;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    height: 0px;
}

QScrollBar:horizontal {
    background-color: transparent;
    border: none;
    height: 10px;
    margin: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #30363D;
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #484F58;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    width: 0px;
}

/ ============================================================
   PROGRESS BAR
   ============================================================ /

QProgressBar {
    background-color: #21262D;
    border: none;
    border-radius: 8px;
    color: #F0F6FC;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #58A6FF;
    border-radius: 8px;
}

/ ============================================================
   SLIDER
   ============================================================ /

QSlider::groove:horizontal {
    background-color: #30363D;
    border-radius: 4px;
    height: 8px;
}

QSlider::handle:horizontal {
    background-color: #58A6FF;
    border-radius: 8px;
    width: 18px;
    margin: -5px 0;
}

QSlider::sub-page:horizontal {
    background-color: #58A6FF;
    border-radius: 4px;
}

/ ============================================================
   CHECK BOX
   ============================================================ /

QCheckBox {
    color: #F0F6FC;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
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

/ ============================================================
   RADIO BUTTON
   ============================================================ /

QRadioButton {
    color: #F0F6FC;
    spacing: 8px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #30363D;
    border-radius: 9px;
    background-color: transparent;
}

QRadioButton::indicator:hover {
    border-color: #58A6FF;
}

QRadioButton::indicator:checked {
    background-color: #58A6FF;
    border-color: #58A6FF;
}

/ ============================================================
   MENU
   ============================================================ /

QMenuBar {
    background-color: #161B22;
    border-bottom: 1px solid #30363D;
    color: #F0F6FC;
}

QMenuBar::item:selected {
    background-color: #21262D;
}

QMenu {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 8px;
    color: #F0F6FC;
    padding: 4px;
}

QMenu::item:selected {
    background-color: #21262D;
}

QMenu::separator {
    background-color: #30363D;
    height: 1px;
    margin: 4px 0px;
}

/ ============================================================
   TOOLTIP
   ============================================================ /

QToolTip {
    background-color: #161B22;
    border: 1px solid #30363D;
    border-radius: 8px;
    color: #F0F6FC;
    padding: 8px;
}

/ ============================================================
   STATUS BAR
   ============================================================ /

QStatusBar {
    background-color: #161B22;
    border-top: 1px solid #30363D;
    color: #8B949E;
}

QStatusBar::item {
    border: none;
}

/ ============================================================
   DIALOG
   ============================================================ /

QDialog {
    background-color: #0D1117;
}

QFrame#dialogFrame {
    background-color: #161B22;
    border-radius: 12px;
}

/ ============================================================
   CARDS
   ============================================================ /

QFrame#card {
    background-color: #161B22;
    border-radius: 12px;
    border: 1px solid #30363D;
}

QFrame#card:hover {
    border-color: #58A6FF;
}

/ ============================================================
   LABELS
   ============================================================ /

QLabel {
    color: #F0F6FC;
}

QLabel#titleLabel {
    font-size: 24px;
    font-weight: 600;
    color: #F0F6FC;
}

QLabel#subtitleLabel {
    font-size: 16px;
    color: #8B949E;
}

QLabel#headingLabel {
    font-size: 18px;
    font-weight: 600;
    color: #F0F6FC;
}

QLabel#infoLabel {
    font-size: 12px;
    color: #8B949E;
}

QLabel#successLabel {
    color: #7EE787;
}

QLabel#warningLabel {
    color: #F0883E;
}

QLabel#errorLabel {
    color: #F85149;
}

/ ============================================================
   LOGIN SCREEN SPECIFIC
   ============================================================ /

QFrame#loginFrame {
    background-color: #0D1117;
}

QFrame#loginCard {
    background-color: #161B22;
    border-radius: 15px;
    border: 1px solid #30363D;
}

QLabel#appNameLabel {
    color: #58A6FF;
    font-size: 28px;
    font-weight: 700;
}

QLabel#appSubtitleLabel {
    color: #8B949E;
    font-size: 14px;
}

/ ============================================================
   ANIMATIONS & TRANSITIONS
   ============================================================ /

QPushButton {
    transition: all 0.2s ease-in-out;
}

QPushButton:hover {
    transform: translateY(-1px);
}

QFrame#card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    transition: all 0.2s ease-in-out;
}

/ ============================================================
   UTILITY CLASSES
   ============================================================ /

.text-primary {
    color: #F0F6FC;
}

.text-secondary {
    color: #8B949E;
}

.text-accent {
    color: #58A6FF;
}

.text-success {
    color: #7EE787;
}

.text-warning {
    color: #F0883E;
}

.text-danger {
    color: #F85149;
}

.bg-primary {
    background-color: #0D1117;
}

.bg-secondary {
    background-color: #161B22;
}

.bg-tertiary {
    background-color: #21262D;
}

.border-default {
    border: 1px solid #30363D;
}

.border-accent {
    border: 1px solid #58A6FF;
}

.rounded-sm {
    border-radius: 8px;
}

.rounded-md {
    border-radius: 12px;
}

.rounded-lg {
    border-radius: 15px;
}

.shadow-card {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
"""


# Light Mode Stylesheet
LIGHT_STYLESHEET = """
/ ============================================================
   ZOOTEKNI PRO - LIGHT MODE STYLESHEET
   ============================================================ /

QWidget {
    background-color: #FFFFFF;
    color: #1F2328;
    font-family: "Segoe UI", "SF Pro Display", system-ui, sans-serif;
    font-size: 14px;
}

QMainWindow {
    background-color: #FFFFFF;
}

QFrame#sidebar {
    background-color: #F6F8FA;
    border-right: 1px solid #EAEEF2;
}

QFrame#headerFrame {
    background-color: #F6F8FA;
    border-bottom: 1px solid #EAEEF2;
}

QPushButton {
    background-color: #0969DA;
    border: none;
    border-radius: 8px;
    color: #FFFFFF;
    padding: 10px 20px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #0550AE;
}

QLineEdit, QTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #EAEEF2;
    border-radius: 8px;
    color: #1F2328;
}

QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #EAEEF2;
}
"""


# Print Stylesheet (for reports)
PRINT_STYLESHEET = """
QWidget {
    background-color: #FFFFFF;
    color: #000000;
    font-family: "Times New Roman", serif;
    font-size: 12pt;
}

QTableWidget {
    border: 1px solid #000000;
    gridline-color: #000000;
}
"""