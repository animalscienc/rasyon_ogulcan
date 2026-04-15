"""
Feed Data Model for Zootekni Pro
Feed library management with CRUD operations
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import pandas as pd
from pathlib import Path
from utils.logger import get_logger
from utils.constants import FEED_CSV_PATH

logger = get_logger(__name__)


@dataclass
class Feed:
    """Feed data class representing a feed ingredient."""
    
    id: int
    name: str
    category: str
    dm: float  # Dry Matter %
    cp: float  # Crude Protein %
    ee: float  # Ether Extract (Fat) %
    ndf: float # Neutral Detergent Fiber %
    adf: float # Acid Detergent Fiber %
    adl: float # Acid Detergent Lignin %
    
    # Energy values
    nel: float = 0.0  # Net Energy Lactation Mcal/kg
    me: float = 0.0  # Metabolizable Energy Mcal/kg
    tdn: float = 0.0  # Total Digestible Nutrients %
    
    # Minerals (%)
    ca: float = 0.0
    p: float = 0.0
    mg: float = 0.0
    k: float = 0.0
    na: float = 0.0
    cl: float = 0.0
    s: float = 0.0
    
    # Trace minerals (mg/kg)
    fe: float = 0.0
    cu: float = 0.0
    mn: float = 0.0
    zn: float = 0.0
    co: float = 0.0
    i: float = 0.0
    se: float = 0.0
    
    # Vitamins (IU/kg or mg/kg)
    vit_a: float = 0.0
    vit_d: float = 0.0
    vit_e: float = 0.0
    
    # Economic
    price: float = 0.0  # TL/kg DM
    source: str = ""  # NRC 2021, INRA, etc.
    
    # Additional calculated fields
    nfc: float = 0.0  # Non-Fiber Carbs %
    starch: float = 0.0
    sugar: float = 0.0
    
    # Rumen parameters
    is_forage: bool = False
    ndf_digestibility: float = 0.0  # %/30hr
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "DM": self.dm,
            "CP": self.cp,
            "EE": self.ee,
            "NDF": self.ndf,
            "ADF": self.adf,
            "ADL": self.adl,
            "NEL": self.nel,
            "ME": self.me,
            "TDN": self.tdn,
            "Ca": self.ca,
            "P": self.p,
            "Mg": self.mg,
            "K": self.k,
            "Na": self.na,
            "Cl": self.cl,
            "S": self.s,
            "Fe": self.fe,
            "Cu": self.cu,
            "Mn": self.mn,
            "Zn": self.zn,
            "Co": self.co,
            "I": self.i,
            "Se": self.se,
            "VitA": self.vit_a,
            "VitD": self.vit_d,
            "VitE": self.vit_e,
            "price": self.price,
            "source": self.source,
            "NFC": self.nfc,
            "Starch": self.starch,
            "Sugar": self.sugar,
            "is_forage": self.is_forage,
            "NDFD": self.ndf_digestibility
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Feed":
        """Create from dictionary."""
        return cls(
            id=data.get("id", 0),
            name=data.get("name", ""),
            category=data.get("category", ""),
            dm=data.get("DM", data.get("dm", 0)),
            cp=data.get("CP", data.get("cp", 0)),
            ee=data.get("EE", data.get("ee", 0)),
            ndf=data.get("NDF", data.get("ndf", 0)),
            adf=data.get("ADF", data.get("adf", 0)),
            adl=data.get("ADL", data.get("adl", 0)),
            nel=data.get("NEL", 0),
            me=data.get("ME", 0),
            tdn=data.get("TDN", data.get("tdn", 0)),
            ca=data.get("Ca", 0),
            p=data.get("P", 0),
            mg=data.get("Mg", 0),
            k=data.get("K", 0),
            na=data.get("Na", 0),
            cl=data.get("Cl", 0),
            s=data.get("S", 0),
            fe=data.get("Fe", 0),
            cu=data.get("Cu", 0),
            mn=data.get("Mn", 0),
            zn=data.get("Zn", 0),
            co=data.get("Co", 0),
            i=data.get("I", 0),
            se=data.get("Se", 0),
            vit_a=data.get("VitA", 0),
            vit_d=data.get("VitD", 0),
            vit_e=data.get("VitE", 0),
            price=data.get("price", 0),
            source=data.get("source", ""),
            nfc=data.get("NFC", 0),
            starch=data.get("Starch", 0),
            sugar=data.get("Sugar", 0),
            is_forage=data.get("is_forage", False),
            ndf_digestibility=data.get("NDFD", 0)
        )


class FeedLibrary:
    """Feed library manager for CRUD operations."""
    
    def __init__(self):
        self.feeds: Dict[int, Feed] = {}
        self.categories: List[str] = []
        self.logger = get_logger(__name__)
        self.load_feeds()
    
    def load_feeds(self):
        """Load feeds from CSV file."""
        try:
            csv_path = Path(FEED_CSV_PATH)
            
            if not csv_path.exists():
                self.logger.warning(f"Feed CSV not found: {csv_path}")
                self.create_sample_feeds()
                return
            
            df = pd.read_csv(csv_path)
            
            for _, row in df.iterrows():
                feed = Feed.from_dict(row.to_dict())
                self.feeds[feed.id] = feed
            
            # Extract unique categories
            self.categories = list(set(f.category for f in self.feeds.values()))
            self.categories.sort()
            
            self.logger.info(f"Loaded {len(self.feeds)} feeds")
            
        except Exception as e:
            self.logger.error(f"Error loading feeds: {e}")
            self.create_sample_feeds()
    
    def create_sample_feeds(self):
        """Create sample feeds for initial setup."""
        feeds_data = [
            {
                "id": 1, "name": "Mısır Silajı", "category": "Roughages/Forages",
                "DM": 35.0, "CP": 8.5, "EE": 3.2, "NDF": 45.0, "ADF": 28.0,
                "ADL": 3.0, "NEL": 1.65, "ME": 2.0, "TDN": 65.0,
                "Ca": 0.25, "P": 0.22, "Mg": 0.20, "K": 1.2, "Na": 0.05,
                "Cl": 0.3, "S": 0.15, "price": 0.85, "source": "NRC 2021",
                "is_forage": True, "NDFD": 45.0
            },
            {
                "id": 2, "name": "Yonca Kuru Otu", "category": "Roughages/Forages",
                "DM": 90.0, "CP": 18.5, "EE": 2.8, "NDF": 35.0, "ADF": 22.0,
                "ADL": 4.0, "NEL": 1.52, "ME": 1.9, "TDN": 60.0,
                "Ca": 1.45, "P": 0.25, "Mg": 0.30, "K": 2.5, "Na": 0.08,
                "Cl": 0.25, "S": 0.25, "price": 2.50, "source": "NRC 2021",
                "is_forage": True, "NDFD": 42.0
            },
            {
                "id": 3, "name": "Mısır Tanem", "category": "Concentrates",
                "DM": 89.0, "CP": 9.5, "EE": 4.2, "NDF": 12.0, "ADF": 3.5,
                "ADL": 0.5, "NEL": 2.10, "ME": 2.6, "TDN": 85.0,
                "Ca": 0.03, "P": 0.28, "Mg": 0.12, "K": 0.35, "Na": 0.02,
                "Cl": 0.08, "S": 0.12, "price": 3.20, "source": "NRC 2021",
                "is_forage": False, "NDFD": 75.0, "Starch": 70.0, "Sugar": 2.0
            },
            {
                "id": 4, "name": "Soya Fasulyesi", "category": "Protein Supplements",
                "DM": 89.0, "CP": 45.0, "EE": 1.5, "NDF": 15.0, "ADF": 6.0,
                "ADL": 1.0, "NEL": 2.05, "ME": 2.5, "TDN": 82.0,
                "Ca": 0.25, "P": 0.60, "Mg": 0.28, "K": 1.8, "Na": 0.02,
                "Cl": 0.08, "S": 0.25, "price": 8.50, "source": "NRC 2021",
                "is_forage": False
            },
            {
                "id": 5, "name": "Kepek", "category": "Concentrates",
                "DM": 88.0, "CP": 15.0, "EE": 4.0, "NDF": 30.0, "ADF": 12.0,
                "ADL": 3.0, "NEL": 1.55, "ME": 1.9, "TDN": 62.0,
                "Ca": 0.08, "P": 0.50, "Mg": 0.40, "K": 1.2, "Na": 0.02,
                "Cl": 0.05, "S": 0.20, "price": 1.80, "source": "Yerli",
                "is_forage": False, "Starch": 8.0, "Sugar": 4.0
            },
            {
                "id": 6, "name": "Arpa Tanem", "category": "Concentrates",
                "DM": 88.0, "CP": 12.0, "EE": 2.0, "NDF": 18.0, "ADF": 6.0,
                "ADL": 1.0, "NEL": 1.95, "ME": 2.4, "TDN": 78.0,
                "Ca": 0.05, "P": 0.35, "Mg": 0.12, "K": 0.45, "Na": 0.02,
                "Cl": 0.10, "S": 0.12, "price": 2.90, "source": "Yerli",
                "is_forage": False, "Starch": 55.0, "Sugar": 2.5
            },
            {
                "id": 7, "name": "Pamuk Tohumu", "category": "Protein Supplements",
                "DM": 92.0, "CP": 23.0, "EE": 18.0, "NDF": 25.0, "ADF": 18.0,
                "ADL": 5.0, "NEL": 2.05, "ME": 2.5, "TDN": 80.0,
                "Ca": 0.15, "P": 0.60, "Mg": 0.35, "K": 1.2, "Na": 0.05,
                "Cl": 0.12, "S": 0.25, "price": 6.50, "source": "Yerli",
                "is_forage": False
            },
            {
                "id": 8, "name": "Rastone NP-40", "category": "Additives",
                "DM": 95.0, "CP": 40.0, "EE": 0.5, "NDF": 5.0, "ADF": 2.0,
                "ADL": 0.0, "NEL": 1.80, "ME": 2.2, "TDN": 72.0,
                "Ca": 0.50, "P": 0.40, "Mg": 0.15, "K": 0.2, "Na": 0.01,
                "Cl": 0.05, "S": 0.10, "price": 12.00, "source": "Üretici",
                "is_forage": False
            },
            {
                "id": 9, "name": "Kireçtaşı", "category": "Mineral Supplements",
                "DM": 100.0, "CP": 0.0, "EE": 0.0, "NDF": 0.0, "ADF": 0.0,
                "ADL": 0.0, "NEL": 0.0, "ME": 0.0, "TDN": 0.0,
                "Ca": 38.0, "P": 0.01, "Mg": 0.5, "K": 0.01, "Na": 0.01,
                "Cl": 0.01, "S": 0.01, "price": 0.50, "source": "Yerli",
                "is_forage": False
            },
            {
                "id": 10, "name": "DCP (Dikalsiyum Fosfat)", "category": "Mineral Supplements",
                "DM": 100.0, "CP": 0.0, "EE": 0.0, "NDF": 0.0, "ADF": 0.0,
                "ADL": 0.0, "NEL": 0.0, "ME": 0.0, "TDN": 0.0,
                "Ca": 24.0, "P": 19.0, "Mg": 0.5, "K": 0.01, "Na": 0.01,
                "Cl": 0.01, "S": 0.01, "price": 15.00, "source": "Üretici",
                "is_forage": False
            }
        ]
        
        for feed_data in feeds_data:
            feed = Feed.from_dict(feed_data)
            self.feeds[feed.id] = feed
        
        self.categories = ["Roughages/Forages", "Concentrates", "Protein Supplements",
                        "Mineral Supplements", "Additives"]
        
        self.logger.info(f"Created {len(self.feeds)} sample feeds")
    
    def get_feed(self, feed_id: int) -> Optional[Feed]:
        """Get feed by ID."""
        return self.feeds.get(feed_id)
    
    def get_feeds_by_category(self, category: str) -> List[Feed]:
        """Get all feeds in a category."""
        return [f for f in self.feeds.values() if f.category == category]
    
    def search_feeds(self, query: str) -> List[Feed]:
        """Search feeds by name."""
        query_lower = query.lower()
        return [f for f in self.feeds.values() if query_lower in f.name.lower()]
    
    def add_feed(self, feed: Feed) -> bool:
        """Add a new feed."""
        try:
            if feed.id in self.feeds:
                self.logger.warning(f"Feed ID {feed.id} already exists")
                return False
            
            self.feeds[feed.id] = feed
            
            if feed.category not in self.categories:
                self.categories.append(feed.category)
                self.categories.sort()
            
            self.logger.info(f"Added feed: {feed.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding feed: {e}")
            return False
    
    def update_feed(self, feed: Feed) -> bool:
        """Update an existing feed."""
        try:
            if feed.id not in self.feeds:
                self.logger.warning(f"Feed ID {feed.id} not found")
                return False
            
            self.feeds[feed.id] = feed
            self.logger.info(f"Updated feed: {feed.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating feed: {e}")
            return False
    
    def delete_feed(self, feed_id: int) -> bool:
        """Delete a feed by ID."""
        try:
            if feed_id not in self.feeds:
                self.logger.warning(f"Feed ID {feed_id} not found")
                return False
            
            feed_name = self.feeds[feed_id].name
            del self.feeds[feed_id]
            self.logger.info(f"Deleted feed: {feed_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting feed: {e}")
            return False
    
    def to_dataframe(self) -> pd.DataFrame:
        """Convert all feeds to DataFrame."""
        if not self.feeds:
            return pd.DataFrame()
        
        data = [feed.to_dict() for feed in self.feeds.values()]
        return pd.DataFrame(data)
    
    def save_to_csv(self, path: str = None) -> bool:
        """Save feeds to CSV file."""
        try:
            csv_path = Path(path) if path else Path(FEED_CSV_PATH)
            df = self.to_dataframe()
            df.to_csv(csv_path, index=False)
            self.logger.info(f"Saved feeds to {csv_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving feeds: {e}")
            return False
    
    def __len__(self) -> int:
        return len(self.feeds)
    
    def __iter__(self):
        return iter(self.feeds.values())
    
    def __getitem__(self, feed_id: int) -> Feed:
        return self.feeds[feed_id]