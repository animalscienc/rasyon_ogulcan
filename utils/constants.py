"""
Constants and Configuration for Zootekni Pro
NRC (2021), INRA, ARC Feeding Standards
"""

# Application constants
APP_NAME = "Zootekni Pro"
APP_VERSION = "5.0.0"
APP_SUBTITLE = "Intelligent Rationing"

# Database paths
DB_PATH = "database/rations.db"
FEED_CSV_PATH = "data/yemler.csv"

# UI Dimensions
SIDEBAR_WIDTH = 220
HEADER_HEIGHT = 60
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800

# NRC (2021) Feeding Standards for Dairy Cattle
# ===========================================

# Dry Matter Intake (DMI) Equations
# Based on NRC (2021) - Lactating Dairy Cows
DMI_PARAMETERS = {
    "lactating_cow": {
        "base_dmi": 3.7,  # % Body Weight for early lactation
        "milk_factor": 0.092,  # kg DMI per kg milk
        "fat_correction": 0.0025,  # Additional for fat %
        "week_factor": -0.05,  # Decline per lactation week after week 10
    },
    "dry_cow": {
        "base_dmi": 2.0,  # % Body Weight
        "body_condition_factor": 0.03,  # Per BCS point above 3.0
    },
    "growing_heifer": {
        "base_dmi": 2.5,  # % Body Weight
        "adg_factor": 0.033,  # kg DMI per kg ADG
    }
}

# Nutrient Requirements (NRC 2021)
NUTRIENT_REQUIREMENTS = {
    "lactating_cow": {
        "nEm": 1.6,  # Mcal NEL/kg DM for maintenance
        "nEl_milk": 0.74,  # Mcal NEL/kg milk (4.0% fat)
        "cp": 16.0,  # % CP in DM
        "rup": 35.0,  # % of CP as RUP
        "rdp": 65.0,  # % of CP as RDP
        "ndp": 12.0,  # % RDP of DM
        "adf": 21.0,  # % ADF in DM
        "adl": 3.0,  # % ADL in DM
        "ndf": 25.0,  # % NDF in DM
        "endf": 20.0,  # % eNDF (effective NDF)
        "ca": 0.60,  # % Ca
        "p": 0.30,  # % P
        "mg": 0.20,  # % Mg
        "k": 1.0,  # % K
        "na": 0.20,  # % Na
        "cl": 0.25,  # % Cl
        "s": 0.20,  # % S
        "fe": 50.0,  # mg/kg
        "cu": 10.0,  # mg/kg
        "mn": 40.0,  # mg/kg
        "zn": 50.0,  # mg/kg
        "co": 0.10,  # mg/kg
        "i": 0.50,  # mg/kg
        "se": 0.30,  # mg/kg
        "vit_a": 100.0,  # kIU/kg
        "vit_d": 30.0,  # kIU/kg
        "vit_e": 300.0,  # IU/kg
    },
    "dry_cow": {
        "nEm": 1.6,
        "cp": 12.0,
        "ca": 0.40,
        "p": 0.25,
        "mg": 0.16,
        "k": 0.80,
        "na": 0.15,
        "cl": 0.20,
        "s": 0.15,
        "dcad": -100.0,  # meq/kg (negative for dry period) - for DCAD
    },
    "growing_heifer": {
        "nEm": 2.0,
        "cp": 14.0,
        "ca": 0.40,
        "p": 0.25,
    }
}

# Mineral Ratio Constraints
MINERAL_RATIOS = {
    "ca_p_ratio": {"min": 1.6, "max": 2.1},
    "k_mg_ratio": {"max": 2.2},
    "na_k_ratio": {"min": 0.5},
    "cl_s_ratio": {"min": 1.0},
}

# DCAD (Dietary Cation-Anion Difference) Calculation
# DCAD = (Na + K + Ca + Mg) - (Cl + S)
# Positive DCAD for lactating cows: 150-300 meq/kg
# Negative DCAD for dry cows: -50 to -150 meq/kg
DCAD_RANGES = {
    "lactating": {"min": 150, "max": 300},
    "dry": {"min": -150, "max": -50},
    "closeup": {"min": -100, "max": -50},
}

# Poultry Ideal Protein Ratios (Ideal AA Pattern)
# ======================================
POULTRY_IDEAL_PROTEIN = {
    "broiler": {
        "met_lys": 0.45,  # Met : Lys ratio
        "thr_lys": 0.73,
        "trp_lys": 0.17,
        "arg_lys": 1.20,
        "val_lys": 0.82,
        "ile_lys": 0.75,
    },
    "layer": {
        "met_lys": 0.50,
        "thr_lys": 0.70,
        "trp_lys": 0.18,
        "arg_lys": 1.10,
        "val_lys": 0.80,
        "ile_lys": 0.70,
    }
}

# NPN (Non-Protein Nitrogen) Safety Limits
# ================================
NPN_LIMITS = {
    "max_npn_percent": 30.0,  # Max % of total N from NPN
    "urea_max": 1.5,  # % Urea in DM
    "max_npn_cpk": 200.0,  # % CP equivalent from NPN (max)
}

# Economic Parameters
# ===============
ECONOMIC_PARAMS = {
    "milk_price": 14.0,  # TL/kg (default)
    "milk_fat_price": 0.15,  # TL/%/kg
    "protein_price": 0.80,  # TL/g/kg (for MCS)
    " lactose_price": 0.50,  # TL/g/kg
    "margin_threshold": 0.0,  # Minimum IOFC to be viable
    "sensitivity_range": 0.10,  # 10% for volatility check
}

# Environmental Impact Factors
# ==========================
ENVIRONMENTAL_FACTORS = {
    # Methane prediction (Mills et al.)
    "methane_factor": 0.065,  # g CH4 / MJ gross energy
    "methane_efficiency": 0.85,  # Conversion efficiency
    
    # Nitrogen excretion
    "n_retention_factors": {
        "cow": 0.25,  # N retention (25% of intake)
        "heifer": 0.35,  # N retention for growing
    }
}

# Mathematical Solver Parameters
# ======================
SOLVER_PARAMS = {
    "max_iterations": 1000,
    "tolerance": 1e-6,
    "method": "highs",  # scipy.optimize method
    "time_limit": 30.0,  # seconds
}

# Animal Groups
# ============
ANIMAL_GROUPS = [
    "High Yielding Group A (HYA)",
    "High Yielding Group B (HYB)",
    "Medium Yielding Group (MY)",
    "Low Yielding Group (LY)",
    "Dry Cows (DC)",
    "Close-up Cows (CU)",
    "Growing Heifers (GH)",
    "Transition Cows (TC)",
]

# Feed Categories
# ============
FEED_CATEGORIES = [
    "Roughages/Forages",
    "Concentrates",
    "Protein Supplements",
    "Energy Feeds",
    "Mineral Supplements",
    "Vitamin Supplements",
    "Additives",
    "Total Mixed Ration (TMR)",
]

# Ration Status
# ============
RATION_STATUS = [
    "Draft",
    "Optimizing",
    "Active",
    "Archived",
    "Infeasible",
]

# Version Control
# =============
VERSION_PREFIX = "v"
INITIAL_VERSION = 1

# Logging
# ======
LOG_FILE = "zootekni_pro.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"