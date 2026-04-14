# Zootekni Pro - Main Application Entry Point
# Version: 5.0
# Author: Precision Livestock Farming & Computational Nutrition Expert

import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.auth_controller import AuthController
from utils.database import DatabaseManager
from utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Main application entry point."""
    logger.info("Starting Zootekni Pro v5.0...")
    
    # Initialize database
    db = DatabaseManager()
    db.initialize()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Zootekni Pro")
    app.setOrganizationName("Zootekni")
    app.setOrganizationDomain("zootekni.com")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Show splash screen
    splash = create_splash_screen(app)
    splash.show()
    app.processEvents()
    
    # Create and show login
    login_controller = AuthController()
    login_controller.show_login()
    
    splash.finish(login_controller.login_view)
    
    result = app.exec_()
    logger.info("Application closed.")
    return result


def create_splash_screen(app):
    """Create splash screen with logo."""
    # Create a simple gradient pixmap for splash
    pixmap = QPixmap(600, 400)
    
    from PyQt5.QtWidgets import QLabel
    from PyQt5.QtGui import QPainter, QLinearGradient, QColor
    
    # Use label for splash
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    
    # Draw splash with painter
    painter = QPainter(pixmap)
    gradient = QLinearGradient(0, 0, 600, 400)
    gradient.setColorAt(0, QColor(30, 30, 45))
    gradient.setColorAt(1, QColor(50, 50, 70))
    painter.fillRect(pixmap.rect(), gradient)
    
    # Add text
    painter.setPen(QColor(255, 255, 255))
    painter.setFont(QFont("Segoe UI", 36, QFont.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "Zootekni Pro")
    painter.setFont(QFont("Segoe UI", 14))
    painter.drawText(pixmap.rect().adjusted(0, 50, 0, 0), Qt.AlignCenter, "Intelligent Rationing System v5.0")
    painter.end()
    
    splash.setPixmap(pixmap)
    return splash


if __name__ == "__main__":
    sys.exit(main())
