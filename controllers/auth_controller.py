# Authentication Controller for Zootekni Pro
# Handles user login and session management

from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from views.login_view import LoginView
from utils.database import DatabaseManager
from utils.auth import verify_password
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AuthController:
    """Controller for authentication operations."""
    
    # Signal emitted when login is successful
    login_successful = pyqtSignal(dict)
    
    def __init__(self):
        """Initialize authentication controller."""
        self.db = DatabaseManager()
        self.view = LoginView()
        self.view.set_controller(self)
        self.current_user = None
        
        # Create default admin on first run
        self.db.create_default_admin()
        
    def show(self):
        """Show login view."""
        self.view.show()
        
    def login(self, username: str, password: str) -> bool:
        """
        Authenticate user.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            True if login successful
        """
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
        self.open_dashboard()
        
        return True
        
    def open_dashboard(self):
        """Open main dashboard after successful login."""
        from controllers.dashboard_controller import DashboardController
        
        dashboard = DashboardController(self.current_user)
        dashboard.show()
        self.login_successful.emit(self.current_user)
        
    def logout(self):
        """Logout current user."""
        logger.info(f"User logged out: {self.current_user['username']}")
        self.current_user = None
        self.show()
