"""
Ration Model for Zootekni Pro - Ration Data and Versioning
SQLite-based ration archive management
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import sqlite3
import json
from pathlib import Path
from utils.logger import get_logger
from utils.constants import DB_PATH, ANIMAL_GROUPS, VERSION_PREFIX

logger = get_logger(__name__)


@dataclass
class RationItem:
    """Single feed item within a ration."""
    
    feed_id: int
    feed_name: str
    amount_kg: float  # kg DM
    percentage: float  # % of total ration DM
    
    # Values at inclusion level
    cp_contribution: float = 0.0  # kg
    nel_contribution: float = 0.0  # Mcal
    cost_contribution: float = 0.0  # TL
    
    def to_dict(self) -> Dict:
        return {
            "feed_id": self.feed_id,
            "feed_name": self.feed_name,
            "amount_kg": self.amount_kg,
            "percentage": self.percentage,
            "cp_contribution": self.cp_contribution,
            "nel_contribution": self.nel_contribution,
            "cost_contribution": self.cost_contribution
        }


@dataclass 
class Ration:
    """Complete ration with metadata."""
    
    id: Optional[int] = None
    name: str = ""
    version: int = 1
    animal_group: str = ""
    status: str = "Draft"  # Draft, Optimizing, Active, Archived, Infeasible
    
    # Animal parameters
    animal_type: str = "lactating_cow"
    live_weight: float = 600.0  # kg
    milk_yield: float = 30.0  # kg/day
    milk_fat: float = 3.5  # %
    milk_protein: float = 3.2  # %
    lactation_week: int = 1
    days_in_milk: int = 0
    
    # Ration summary (calculated)
    total_dmi: float = 0.0  # kg DM/day
    cp_percent: float = 0.0  # % in DM
    ndf_percent: float = 0.0  # % in DM
    nel_mcal_kg: float = 0.0
    total_cost: float = 0.0  # TL/day
    
    # Economic metrics
    milk_revenue: float = 0.0  # TL/day
    iofc: float = 0.0  # Income Over Feed Cost
    
    # Environmental
    methane_g_day: float = 0.0
    n_excreted_g_day: float = 0.0  # N excretion
    
    # Timestamps
    created_at: str = ""
    updated_at: str = ""
    
    # Feed items
    items: List[RationItem] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "animal_group": self.animal_group,
            "status": self.status,
            "animal_type": self.animal_type,
            "live_weight": self.live_weight,
            "milk_yield": self.milk_yield,
            "milk_fat": self.milk_fat,
            "milk_protein": self.milk_protein,
            "lactation_week": self.lactation_week,
            "days_in_milk": self.days_in_milk,
            "total_dmi": self.total_dmi,
            "cp_percent": self.cp_percent,
            "ndf_percent": self.ndf_percent,
            "nel_mcal_kg": self.nel_mcal_kg,
            "total_cost": self.total_cost,
            "milk_revenue": self.milk_revenue,
            "iofc": self.iofc,
            "methane_g_day": self.methane_g_day,
            "n_excreted_g_day": self.n_excreted_g_day,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "items": [item.to_dict() for item in self.items]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Ration":
        """Create ration from dictionary."""
        items_data = data.pop("items", [])
        ration = cls(**data)
        ration.items = [RationItem(**item) for item in items_data]
        return ration


class RationDatabase:
    """SQLite database for ration archive management."""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = Path(db_path)
        self.logger = get_logger(__name__)
        self.init_database()
    
    def init_database(self):
        """Initialize database and tables."""
        try:
            # Ensure parent directory exists
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Rations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    animal_group TEXT,
                    status TEXT DEFAULT 'Draft',
                    animal_type TEXT DEFAULT 'lactating_cow',
                    live_weight REAL DEFAULT 600.0,
                    milk_yield REAL DEFAULT 30.0,
                    milk_fat REAL DEFAULT 3.5,
                    milk_protein REAL DEFAULT 3.2,
                    lactation_week INTEGER DEFAULT 1,
                    days_in_milk INTEGER DEFAULT 0,
                    total_dmi REAL DEFAULT 0.0,
                    cp_percent REAL DEFAULT 0.0,
                    ndf_percent REAL DEFAULT 0.0,
                    nel_mcal_kg REAL DEFAULT 0.0,
                    total_cost REAL DEFAULT 0.0,
                    milk_revenue REAL DEFAULT 0.0,
                    iofc REAL DEFAULT 0.0,
                    methane_g_day REAL DEFAULT 0.0,
                    n_excreted_g_day REAL DEFAULT 0.0,
                    created_at TEXT,
                    updated_at TEXT,
                    data_json TEXT
                )
            """)
            
            conn.commit()
            self.logger.info(f"Database initialized: {self.db_path}")
            
        except Exception as e:
            self.logger.error(f"Database initialization error: {e}")
        finally:
            conn.close()
    
    def save_ration(self, ration: Ration) -> int:
        """Save a ration to database."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            
            if ration.id is None:
                # Insert new ration
                cursor.execute("""
                    INSERT INTO rations (
                        name, version, animal_group, status, animal_type,
                        live_weight, milk_yield, milk_fat, milk_protein,
                        lactation_week, days_in_milk, total_dmi, cp_percent,
                        ndf_percent, nel_mcal_kg, total_cost, milk_revenue,
                        iofc, methane_g_day, n_excreted_g_day, created_at,
                        updated_at, data_json
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ration.name, ration.version, ration.animal_group, ration.status,
                    ration.animal_type, ration.live_weight, ration.milk_yield,
                    ration.milk_fat, ration.milk_protein, ration.lactation_week,
                    ration.days_in_milk, ration.total_dmi, ration.cp_percent,
                    ration.ndf_percent, ration.nel_mcal_kg, ration.total_cost,
                    ration.milk_revenue, ration.iofc, ration.methane_g_day,
                    ration.n_excreted_g_day, now, now, json.dumps(ration.to_dict())
                ))
                
                ration_id = cursor.lastrowid
                
            else:
                # Update existing ration
                cursor.execute("""
                    UPDATE rations SET
                        name = ?, version = ?, animal_group = ?, status = ?,
                        animal_type = ?, live_weight = ?, milk_yield = ?,
                        milk_fat = ?, milk_protein = ?, lactation_week = ?,
                        days_in_milk = ?, total_dmi = ?, cp_percent = ?,
                        ndf_percent = ?, nel_mcal_kg = ?, total_cost = ?,
                        milk_revenue = ?, iofc = ?, methane_g_day = ?,
                        n_excreted_g_day = ?, updated_at = ?, data_json = ?
                    WHERE id = ?
                """, (
                    ration.name, ration.version, ration.animal_group, ration.status,
                    ration.animal_type, ration.live_weight, ration.milk_yield,
                    ration.milk_fat, ration.milk_protein, ration.lactation_week,
                    ration.days_in_milk, ration.total_dmi, ration.cp_percent,
                    ration.ndf_percent, ration.nel_mcal_kg, ration.total_cost,
                    ration.milk_revenue, ration.iofc, ration.methane_g_day,
                    ration.n_excreted_g_day, now, json.dumps(ration.to_dict()),
                    ration.id
                ))
                
                ration_id = ration.id
            
            conn.commit()
            self.logger.info(f"Saved ration: {ration.name} v{ration.version}")
            
            return ration_id
            
        except Exception as e:
            self.logger.error(f"Error saving ration: {e}")
            return -1
            
        finally:
            conn.close()
    
    def load_ration(self, ration_id: int) -> Optional[Ration]:
        """Load a ration from database."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT data_json FROM rations WHERE id = ?", (ration_id,))
            row = cursor.fetchone()
            
            if row:
                data = json.loads(row["data_json"])
                return Ration.from_dict(data)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error loading ration: {e}")
            return None
            
        finally:
            conn.close()
    
    def list_rations(self, animal_group: str = None, status: str = None) -> List[Ration]:
        """List rations with optional filtering."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT id, name, version, animal_group, status, created_at, updated_at FROM rations"
            conditions = []
            params = []
            
            if animal_group:
                conditions.append("animal_group = ?")
                params.append(animal_group)
            
            if status:
                conditions.append("status = ?")
                params.append(status)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY updated_at DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            rations = []
            for row in rows:
                ration = Ration(
                    id=row["id"],
                    name=row["name"],
                    version=row["version"],
                    animal_group=row["animal_group"],
                    status=row["status"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
                rations.append(ration)
            
            return rations
            
        except Exception as e:
            self.logger.error(f"Error listing rations: {e}")
            return []
            
        finally:
            conn.close()
    
    def delete_ration(self, ration_id: int) -> bool:
        """Delete a ration from database."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM rations WHERE id = ?", (ration_id,))
            
            conn.commit()
            self.logger.info(f"Deleted ration ID: {ration_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting ration: {e}")
            return False
            
        finally:
            conn.close()
    
    def get_next_version(self, name: str) -> int:
        """Get next version number for a ration name."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT MAX(version) FROM rations WHERE name = ?
            """, (name,))
            
            result = cursor.fetchone()[0]
            
            return (result or 0) + 1
            
        except Exception as e:
            self.logger.error(f"Error getting version: {e}")
            return 1
            
        finally:
            conn.close()
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Total rations
            cursor.execute("SELECT COUNT(*) FROM rations")
            total = cursor.fetchone()[0]
            
            # By status
            cursor.execute("""
                SELECT status, COUNT(*) FROM rations GROUP BY status
            """)
            status_counts = dict(cursor.fetchall())
            
            # By animal group
            cursor.execute("""
                SELECT animal_group, COUNT(*) FROM rations GROUP BY animal_group
            """)
            group_counts = dict(cursor.fetchall())
            
            return {
                "total": total,
                "by_status": status_counts,
                "by_group": group_counts
            }
            
        except Exception as e:
            self.logger.error(f"Error getting stats: {e}")
            return {}
            
        finally:
            conn.close()