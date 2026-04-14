# Database Manager for Zootekni Pro
# SQLite-based data management for feeds, rations, and users

import sqlite3
import os
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime
from contextlib import contextmanager

from utils.logger import setup_logger

logger = setup_logger(__name__)


class DatabaseManager:
    """Manages SQLite database operations for the application."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'data', 
                'zootekni.db'
            )
        self.db_path = db_path
        self._ensure_data_dir()
        
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)
        
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
            
    def initialize(self):
        """Initialize database schema."""
        logger.info(f"Initializing database at {self.db_path}")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT,
                    full_name TEXT,
                    role TEXT DEFAULT 'user',
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            # Feed library table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feeds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feed_code TEXT UNIQUE NOT NULL,
                    feed_name TEXT NOT NULL,
                    feed_name_tr TEXT,
                    category TEXT,
                    dry_matter REAL,
                    cp REAL,
                    ndf REAL,
                    adf REAL,
                    starch REAL,
                    sugar REAL,
                    fat REAL,
                    ash REAL,
                    ca REAL,
                    p REAL,
                    mg REAL,
                    k REAL,
                    na REAL,
                    cl REAL,
                    s REAL,
                    n_el REAL,
                    ne_lact REAL,
                    me REAL,
                    rumen_degradable_protein REAL,
                    rumen_undegradable_protein REAL,
                    digestibility REAL,
                    ndf_digestibility REAL,
                    nPN REAL,
                    is_premium INTEGER DEFAULT 0,
                    min_usage REAL,
                    max_usage REAL,
                    price REAL DEFAULT 0,
                    vegetation_period TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Animal groups table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS animal_groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT NOT NULL,
                    animal_type TEXT NOT NULL,
                    average_weight REAL,
                    milk_yield REAL,
                    milk_fat REAL,
                    milk_protein REAL,
                    lactation_week INTEGER,
                    pregnancy_months INTEGER,
                    dry_period INTEGER,
                    target_dmi REAL,
                    target_nel REAL,
                    target_cp REAL,
                    target_rdp REAL,
                    target_rup REAL,
                    target_ndf REAL,
                    target_ca REAL,
                    target_p REAL,
                    is_active INTEGER DEFAULT 1,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Rations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ration_name TEXT NOT NULL,
                    group_id INTEGER,
                    version INTEGER DEFAULT 1,
                    version_notes TEXT,
                    dm_total REAL,
                    cp_total REAL,
                    ndf_total REAL,
                    nel_total REAL,
                    me_total REAL,
                    cost_per_kg_dm REAL,
                    cost_per_head_day REAL,
                    is_optimized INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by INTEGER,
                    FOREIGN KEY (group_id) REFERENCES animal_groups(id),
                    FOREIGN KEY (created_by) REFERENCES users(id)
                )
            ''')
            
            # Ration ingredients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ration_ingredients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ration_id INTEGER NOT NULL,
                    feed_id INTEGER NOT NULL,
                    amount_kg REAL NOT NULL,
                    amount_dm REAL,
                    proportion REAL,
                    cost REAL,
                    FOREIGN KEY (ration_id) REFERENCES rations(id),
                    FOREIGN KEY (feed_id) REFERENCES feeds(id)
                )
            ''')
            
            # Economic analysis table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS economic_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ration_id INTEGER NOT NULL,
                    iofc REAL,
                    marginal_return REAL,
                    shadow_prices TEXT,
                    volatility_impact REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ration_id) REFERENCES rations(id)
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_feeds_category ON feeds(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_feeds_code ON feeds(feed_code)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_rations_group ON rations(group_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_rations_active ON rations(is_active)')
            
            logger.info("Database schema initialized successfully")
            
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Execute SELECT query and return results as list of dicts."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
            
    def execute_update(self, query: str, params: tuple = None) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected rows."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
            
    def get_all_feeds(self) -> pd.DataFrame:
        """Get all feeds from library."""
        query = "SELECT * FROM feeds ORDER BY feed_name"
        with self._get_connection() as conn:
            return pd.read_sql_query(query, conn)
            
    def get_feed_by_code(self, feed_code: str) -> Optional[Dict]:
        """Get feed by code."""
        query = "SELECT * FROM feeds WHERE feed_code = ?"
        result = self.execute_query(query, (feed_code,))
        return result[0] if result else None
        
    def add_feed(self, feed_data: Dict) -> int:
        """Add new feed to library."""
        columns = ', '.join(feed_data.keys())
        placeholders = ', '.join(['?'] * len(feed_data))
        query = f"INSERT INTO feeds ({columns}) VALUES ({placeholders})"
        return self.execute_update(query, tuple(feed_data.values()))
        
    def update_feed(self, feed_id: int, feed_data: Dict) -> bool:
        """Update existing feed."""
        set_clause = ', '.join([f"{k} = ?" for k in feed_data.keys()])
        query = f"UPDATE feeds SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        params = tuple(feed_data.values()) + (feed_id,)
        return self.execute_update(query, params) > 0
        
    def delete_feed(self, feed_id: int) -> bool:
        """Delete feed from library."""
        query = "DELETE FROM feeds WHERE id = ?"
        return self.execute_update(query, (feed_id,)) > 0
        
    def get_all_rations(self, group_id: int = None) -> pd.DataFrame:
        """Get all rations, optionally filtered by group."""
        if group_id:
            query = "SELECT * FROM rations WHERE group_id = ? ORDER BY created_at DESC"
            with self._get_connection() as conn:
                return pd.read_sql_query(query, conn, params=(group_id,))
        else:
            query = "SELECT * FROM rations ORDER BY created_at DESC"
            with self._get_connection() as conn:
                return pd.read_sql_query(query, conn)
                
    def get_ration_with_ingredients(self, ration_id: int) -> Dict:
        """Get ration with all ingredients."""
        # Get ration details
        ration_query = "SELECT * FROM rations WHERE id = ?"
        ration = self.execute_query(ration_query, (ration_id,))
        
        if not ration:
            return None
            
        # Get ingredients
        ingredients_query = '''
            SELECT ri.*, f.feed_name, f.feed_name_tr, f.category, f.price
            FROM ration_ingredients ri
            JOIN feeds f ON ri.feed_id = f.id
            WHERE ri.ration_id = ?
        '''
        ingredients = self.execute_query(ingredients_query, (ration_id,))
        
        return {
            'ration': ration[0],
            'ingredients': ingredients
        }
        
    def save_ration(self, ration_data: Dict, ingredients: List[Dict]) -> int:
        """Save new ration with ingredients."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Insert ration
                ration_cols = ', '.join(ration_data.keys())
                ration_placeholders = ', '.join(['?'] * len(ration_data))
                ration_query = f"INSERT INTO rations ({ration_cols}) VALUES ({ration_placeholders})"
                cursor.execute(ration_query, tuple(ration_data.values()))
                ration_id = cursor.lastrowid
                
                # Insert ingredients
                for ing in ingredients:
                    ing['ration_id'] = ration_id
                    ing_cols = ', '.join(ing.keys())
                    ing_placeholders = ', '.join(['?'] * len(ing))
                    ing_query = f"INSERT INTO ration_ingredients ({ing_cols}) VALUES ({ing_placeholders})"
                    cursor.execute(ing_query, tuple(ing.values()))
                    
                conn.commit()
                logger.info(f"Ration {ration_id} saved successfully")
                return ration_id
                
            except Exception as e:
                conn.rollback()
                logger.error(f"Error saving ration: {e}")
                raise
                
    def create_default_admin(self):
        """Create default admin user if not exists."""
        from utils.auth import hash_password
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = 'admin'")
                if not cursor.fetchone():
                    password_hash = hash_password('admin123')
                    cursor.execute('''
                        INSERT INTO users (username, password_hash, email, full_name, role)
                        VALUES (?, ?, ?, ?, ?)
                    ''', ('admin', password_hash, 'admin@zootekni.com', 'Administrator', 'admin'))
                    logger.info("Default admin user created")
        except Exception as e:
            logger.warning(f"Could not create admin user: {e}")
