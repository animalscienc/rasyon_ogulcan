"""
Zootekni Pro - Main Application Entry Point
Version 5.0 - Ultimate Ration Engineering & Economic Intelligence System
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import application components
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

# Import views
from views.login_view import LoginWindow
from views.dashboard_view import DashboardWindow

# Import utilities
from utils.logger import setup_logger
from utils.constants import APP_NAME, APP_VERSION

def main():
    """Main application entry point."""
    # Setup logging
    logger = setup_logger()
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("Zootekni Pro")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create splash screen
    splash_pixmap = QPixmap(400, 300)
    splash_pixmap.fill(QColor("#0D1117"))
    splash = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.showMessage(
        f"<h1 style='color:#58A6FF'>{APP_NAME}</h1>"
        f"<p style='color:#8B949E'>Intelligent Rationing System</p>"
        f"<p style='color:#7EE787'>Version {APP_VERSION}</p>",
        Qt.AlignCenter
    )
    splash.show()
    app.processEvents()
    
    # Import styles and apply
    from views.styles import DARK_STYLESHEET
    app.setStyleSheet(DARK_STYLESHEET)
    
    # Show login window
    logger.info("Showing login window")
    login_window = LoginWindow()
    splash.finish(login_window)
    login_window.show()
    
    # Connect login success to dashboard
    def show_dashboard():
        logger.info("Login successful, showing dashboard")
        dashboard = DashboardWindow()
        dashboard.show()
        login_window.close()
    
    login_window.login_success.connect(show_dashboard)
    
    # Run application
    logger.info("Application started")
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())