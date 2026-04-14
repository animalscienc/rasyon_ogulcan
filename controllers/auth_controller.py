# Authentication Controller for Zootekni Pro

from PyQt5.QtWidgets import QMessageBox
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from views.login_view import LoginView
from views.dashboard_view import DashboardView
from utils.database import DatabaseManager
from utils.auth import verify_password
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AuthController:
    """Controller for authentication operations."""
    
    def __init__(self):
        """Initialize authentication controller."""
        self.db = DatabaseManager()
        self.login_view = LoginView()
        self.login_view.set_controller(self)
        self.dashboard_view = None
        self.current_user = None
        self.db.create_default_admin()
        
    def show_login(self):
        """Show login view."""
        self.login_view.show()
        
    def login(self, username: str, password: str) -> bool:
        """Authenticate user."""
        logger.info(f"Login attempt: {username}")
        
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        result = self.db.execute_query(query, (username,))
        
        if not result:
            logger.warning(f"User not found: {username}")
            self.login_view.show_error("Kullanıcı adı veya şifre hatalı!")
            return False
            
        user = result[0]
        
        if not verify_password(password, user['password_hash']):
            logger.warning(f"Invalid password: {username}")
            self.login_view.show_error("Kullanıcı adı veya şifre hatalı!")
            return False
            
        # Update last login
        self.db.execute_update(
            "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
            (user['id'],)
        )
        
        self.current_user = user
        logger.info(f"Login successful: {username}")
        
        # Hide login (don't close!)
        self.login_view.hide()
        
        # Create and show dashboard
        self.dashboard_view = DashboardView()
        self.dashboard_view.set_controller(self)
        self.dashboard_view.show()
        
        logger.info("Dashboard shown")
        return True
        
    def logout(self):
        """Logout and show login again."""
        if self.dashboard_view:
            self.dashboard_view.close()
        self.current_user = None
        self.login_view.show()
