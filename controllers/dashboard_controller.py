# Dashboard Controller for Zootekni Pro
# Main application controller with sidebar navigation

from PyQt5.QtWidgets import QMessageBox
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from views.dashboard_view import DashboardView
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DashboardController:
    """Controller for main dashboard operations."""
    
    def __init__(self, user: dict):
        """
        Initialize dashboard controller.
        
        Args:
            user: Logged in user data
        """
        self.user = user
        self.view = DashboardView()
        self.view.set_controller(self)
        self.current_view = None
        
    def show(self):
        """Show dashboard view."""
        self.view.show()
        logger.info(f"Dashboard opened for user: {self.user['username']}")
        
    def navigate_to(self, view_name: str):
        """
        Navigate to specific view.
        
        Args:
            view_name: Name of the view to navigate to
        """
        logger.info(f"Navigating to: {view_name}")
        self.view.switch_view(view_name)
        
    def logout(self):
        """Handle logout."""
        reply = QMessageBox.question(
            self.view,
            "Çıkış",
            "Çıkış yapmak istediğinizden emin misiniz?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            logger.info(f"User logged out: {self.user['username']}")
            self.view.close()
            from controllers.auth_controller import AuthController
            auth = AuthController()
            auth.show()
            
    def get_user_info(self) -> dict:
        """Get current user info."""
        return self.user
