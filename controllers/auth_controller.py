# Authentication Controller for Zootekni Pro
# Handles user login and session management

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
        self.view = LoginView()
        self.view.set_controller(self)
        self.current_user = None
        self.dashboard_view = None
        
        # Create default admin on first run
        self.db.create_default_admin()
        
    def show(self):
        """Show login view."""
        self.view.show()
        
    def login(self, username: str, password: str) -> bool:
        """Authenticate user."""
        logger.info(f"Login attempt for user: {username}")
        
        # Query user
        query = "SELECT * FROM users WHERE username = ? AND is_active = 1"
        result = self.db.execute_query(query, (username,))
        
        if not result:
            logger.warning(f"Login failed: User not found - {username}")
            self.view.show_error("Kullanıcı adı veya şifre hatalı!")
            return False
            
        user = result[0]
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            logger.warning(f"Login failed: Invalid password for {username}")
            self.view.show_error("Kullanıcı adı veya şifre hatalı!")
            return False
            
        # Update last login
        self.db.execute_update(
            "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
            (user['id'],)
        )
        
        # Store current user
        self.current_user = user
        logger.info(f"Login successful: {username}")
        
        # Close login and open dashboard
        self.view.close()
        
        # Create new dashboard instance
        dashboard = DashboardView()
        dashboard.set_controller(self)
        dashboard.show()
        
        logger.info("Dashboard opened successfully")
        
        return True
        
    def logout(self):
        """Logout current user."""
        logger.info(f"User logged out: {self.current_user['username']}")
        self.current_user = None
        self.show()
