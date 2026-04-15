"""
Nutritional and Economic Calculations for Zootekni Pro
Based on NRC (2021), INRA, ARC standards
"""

import numpy as np
from typing import Dict, Optional, Tuple, List
from dataclasses import dataclass
from utils.logger import get_logger
from utils.constants import (
    DMI_PARAMETERS, NUTRIENT_REQUIREMENTS, MINERAL_RATIOS,
    DCAD_RANGES, NPN_LIMITS, ECONOMIC_PARAMS, ENVIRONMENTAL_FACTORS
)

logger = get_logger(__name__)

@dataclass
class AnimalParameters:
    """Animal input parameters for ration calculation."""
    animal_type: str  # "lactating_cow", "dry_cow", "growing_heifer"
    live_weight: float  # kg
    milk_yield: float = 0.0  # kg/day
    milk_fat: float = 3.5  # %
    milk_protein: float = 3.2  # %
    milk_lactose: float = 4.8  # %
    lactation_week: int = 1  # 1-52
    body_condition_score: float = 3.0  # 1-5
    days_milked: float = 0.0  # For dry period
    dry_period_days: float = 60.0
    pregnancy_months: float = 0.0
    average_daily_gain: float = 0.0  # kg/day for heifers
    age_months: float = 24.0  # For heifers
    activity_level: str = "moderate"  # "low", "moderate", "high"


class NutritionalCalculator:
    """Nutritional calculation engine based on NRC (2021), INRA, ARC."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def calculate_dmi(self, params: AnimalParameters) -> float:
        """
        Calculate Dry Matter Intake based on NRC (2021).
        
        Args:
            params: Animal parameters
        
        Returns:
            DMI in kg DM/day
        """
        try:
            if params.animal_type == "lactating_cow":
                # Base DMI calculation for lactating cows
                base_dmi = DMI_PARAMETERS["lactating_cow"]["base_dmi"] * (params.live_weight / 100)
                
                # Milk component
                milk_factor = DMI_PARAMETERS["lactating_cow"]["milk_factor"]
                milk_dmi = milk_factor * params.milk_yield
                
                # Fat correction
                fat_correction = DMI_PARAMETERS["lactating_cow"]["fat_correction"] * max(0, params.milk_fat - 3.5) * params.milk_yield
                
                # Lactation week adjustment
                if params.lactation_week <= 10:
                    week_factor = 1.0
                else:
                    week_factor = max(0.5, 1.0 - DMI_PARAMETERS["lactating_cow"]["week_factor"] * (params.lactation_week - 10))
                
                total_dmi = (base_dmi + milk_dmi + fat_correction) * week_factor
                
            elif params.animal_type == "dry_cow":
                # Dry cow DMI
                base_dmi = DMI_PARAMETERS["dry_cow"]["base_dmi"] * (params.live_weight / 100)
                bcs_factor = 1.0 + DMI_PARAMETERS["dry_cow"]["body_condition_factor"] * max(0, params.body_condition_score - 3.0)
                total_dmi = base_dmi * bcs_factor
                
            elif params.animal_type == "growing_heifer":
                # Growing heifer DMI
                base_dmi = DMI_PARAMETERS["growing_heifer"]["base_dmi"] * (params.live_weight / 100)
                adg_factor = DMI_PARAMETERS["growing_heifer"]["adg_factor"] * params.average_daily_gain
                total_dmi = base_dmi + adg_factor
                
            else:
                self.logger.warning(f"Unknown animal type: {params.animal_type}")
                total_dmi = params.live_weight * 0.03  # Default 3% of BW
            
            return round(total_dmi, 2)
            
        except Exception as e:
            self.logger.error(f"DMI calculation error: {e}")
            return 0.0
    
    def calculate_requirements(self, params: AnimalParameters) -> Dict[str, float]:
        """
        Calculate nutrient requirements based on animal parameters.
        
        Args:
            params: Animal parameters
        
        Returns:
            Dictionary of nutrient requirements
        """
        try:
            # Base requirements from NRC
            reqs = NUTRIENT_REQUIREMENTS.get(
                params.animal_type, 
                NUTRIENT_REQUIREMENTS["lactating_cow"]
            ).copy()
            
            dmi = self.calculate_dmi(params)
            
            # Calculate energy requirements
            if params.animal_type == "lactating_cow":
                # NEL for maintenance
                nEm = reqs["nEm"]
                maintenance_nel = nEm * (params.live_weight ** 0.75) * 0.08  # Mcal/day
                
                # NEL for milk
                nEl_milk = (0.0929 * (milk_fat_pct_to_decimal(params.milk_fat)) + 
                           0.0563 * (params.milk_protein / 100) + 
                           0.0395 * (params.milk_lactose / 100)) * params.milk_yield
                milk_nel = nEl_milk * params.milk_yield
                
                # Activity adjustment
                activity_factor = 1.0
                if params.activity_level == "high":
                    activity_factor = 1.10
                elif params.activity_level == "low":
                    activity_factor = 0.95
                
                total_nel = (maintenance_nel + milk_nel) * activity_factor
                
                # Convert to per kg DM basis
                reqs["NEl_Mcal_kg"] = round(total_nel / dmi, 3) if dmi > 0 else 1.6
                
                # Calculate protein requirements
                milk_cp = params.milk_yield * (params.milk_protein / 100) * 1000 / 6.38  # g CP in milk
                retained_cp = reqs["cp"] * dmi * 10  # g CP retained
                reqs["CP_g_day"] = round(milk_cp + retained_cp, 1)
                
            elif params.animal_type == "dry_cow":
                # Dry cow requirements
                pregnancy_factor = 1.0 + (params.pregnancy_months / 9.0) * 0.5
                maintenance_nel = reqs["nEm"] * (params.live_weight ** 0.75) * 0.08 * pregnancy_factor
                reqs["NEl_Mcal_kg"] = round(maintenance_nel / dmi, 3) if dmi > 0 else 1.6
            
            reqs["DMI_kg"] = dmi
            
            return reqs
            
        except Exception as e:
            self.logger.error(f"Requirements calculation error: {e}")
            return {}
    
    def calculate_energies(self, feed_data: Dict) -> Dict[str, float]:
        """
        Calculate energy values from feed composition.
        
        Args:
            feed_data: Feed composition dictionary
        
        Returns:
            Dictionary with NEL, ME, DE values
        """
        try:
            # Get raw values
            td_ndf = feed_data.get("tdNDF", 0)  # % TDN from NDF
            adf = feed_data.get("ADF", 0)
            cp = feed_data.get("CP", 0)
            fat = feed_data.get("EE", 0)
            ash = feed_data.get("Ash", 0)
            
            # Calculate DE (Digestible Energy) - estimated from TDN
            tdn = (td_ndf + cp * 0.95 + fat * 0.98 + (100 - td_ndf - cp - fat - ash) * 0.75) / 100
            de_mcal_kg = tdn * 4.4  # 4.4 Mcal DE per kg TDN
            
            # Calculate ME (Metabolizable Energy)
            me_factor = 0.82 if feed_data.get("is_forage", False) else 0.86
            me_mcal_kg = de_mcal_kg * me_factor
            
            # Calculate NEL (Net Energy for Lactation)
            # NEL = 0.0245 * TDN - 0.012 for lactating cows
            nel_mcal_kg = max(0, (0.0245 * tdn * 100 - 0.012) * 0.44) if tdn > 0 else 0
            
            return {
                "DE_Mcal_kg": round(de_mcal_kg, 3),
                "ME_Mcal_kg": round(me_mcal_kg, 3),
                "NEL_Mcal_kg": round(nel_mcal_kg, 3),
                "TDN_pct": round(tdn * 100, 1)
            }
            
        except Exception as e:
            self.logger.error(f"Energy calculation error: {e}")
            return {"DE_Mcal_kg": 0, "ME_Mcal_kg": 0, "NEL_Mcal_kg": 0, "TDN_pct": 0}
    
    def calculate_dcad(self, minerals: Dict[str, float]) -> float:
        """
        Calculate Dietary Cation-Anion Difference (DCAD).
        
        DCAD = (Na + K + Ca + Mg) - (Cl + S)
        Units: meq/kg DM
        
        Args:
            minerals: Dictionary with mineral concentrations (%, not %/100)
        
        Returns:
            DCAD in meq/kg DM
        """
        try:
            # Molecular weights for conversion
            n_wt = 23.0  # Na
            k_wt = 39.1   # K
            ca_wt = 40.1  # Ca
            mg_wt = 24.3  # Mg
            cl_wt = 35.5  # Cl
            s_wt = 32.1   # S
            
            # Convert % to meq/kg
            na_meq = (minerals.get("Na", 0) / n_wt) * 10000
            k_meq = (minerals.get("K", 0) / k_wt) * 10000
            ca_meq = (minerals.get("Ca", 0) / ca_wt) * 10000 * 2  # Ca2+
            mg_meq = (minerals.get("Mg", 0) / mg_wt) * 10000 * 2  # Mg2+
            cl_meq = (minerals.get("Cl", 0) / cl_wt) * 10000
            s_meq = (minerals.get("S", 0) / s_wt) * 10000
            
            dcad = (na_meq + k_meq + ca_meq + mg_meq) - (cl_meq + s_meq)
            
            return round(dcad, 1)
            
        except Exception as e:
            self.logger.error(f"DCAD calculation error: {e}")
            return 0.0
    
    def validate_mineral_ratios(self, ca: float, p: float, k: float, mg: float) -> Dict[str, bool]:
        """
        Validate mineral ratios against constraints.
        
        Args:
            ca: Calcium % DM
            p: Phosphorus % DM
            k: Potassium % DM
            mg: Magnesium % DM
        
        Returns:
            Validation results dictionary
        """
        results = {}
        
        # Ca:P ratio (1.6 - 2.1)
        if p > 0:
            ca_p_ratio = ca / p
            results["ca_p_ratio"] = MINERAL_RATIOS["ca_p_ratio"]["min"] <= ca_p_ratio <= MINERAL_RATIOS["ca_p_ratio"]["max"]
        
        # K:Mg ratio (max 2.2)
        if mg > 0:
            k_mg_ratio = k / mg
            results["k_mg_ratio"] = k_mg_ratio <= MINERAL_RATIOS["k_mg_ratio"]["max"]
        
        return results
    
    def validate_npn(self, total_n: float, npn_n: float) -> Dict[str, bool]:
        """
        Validate NPN (Non-Protein Nitrogen) usage.
        
        Args:
            total_n: Total nitrogen in ration % DM
            npn_n: NPN nitrogen % DM
        
        Returns:
            Validation results
        """
        results = {}
        
        if total_n > 0:
            npn_percent = (npn_n / total_n) * 100
            results["npn_safe"] = npn_percent <= NPN_LIMITS["max_npn_percent"]
            results["npn_percent"] = npn_percent
        
        return results
    
    def validate_fiber(self, ndf: float, adf: float, adl: float, dmi: float) -> Dict[str, bool]:
        """
        Validate fiber constraints.
        
        Args:
            NDF: % Neutral Detergent Fiber
            ADF: % Acid Detergent Fiber
            ADL: % Acid Detergent Lignin
            DMI: kg DM/day
        
        Returns:
            Validation results
        """
        results = {}
        
        # eNDF requires minimum physical fiber
        # Assuming effective NDF ~ 0.85 * NDF for forages
        endf = ndf * 0.85
        results["endf_min"] = endf >= 20.0  # Minimum 20% eNDF
        
        # ADF ratio to NDF
        if ndf > 0:
            adf_ndf_ratio = adf / ndf
            results["adf_ratio"] = adf_ndf_ratio >= 0.5
        
        return results
    
    def calculate_env_impact(self, params: AnimalParameters, ration_data: Dict) -> Dict[str, float]:
        """
        Calculate environmental impact (methane, nitrogen excretion).
        
        Args:
            params: Animal parameters
            ration_data: Ration composition dictionary
        
        Returns:
            Environmental impact metrics
        """
        try:
            # Get feed intake
            dmi = self.calculate_dmi(params)
            
            # Gross energy intake (estimated from DMI and average GE)
            ge_intake = dmi * 4.5  # Assume ~4.5 Mcal GE/kg DM average
            
            # Methane emissions (Mills et al. model)
            # CH4 (g/day) = 0.065 * (GE intake)^0.75
            methane_g = ENVIRONMENTAL_FACTORS["methane_factor"] * 1000 * (ge_intake ** 0.75)
            
            # Nitrogen excretion
            if params.animal_type == "cow":
                n_retention = ENVIRONMENTAL_FACTORS["n_retention_factors"]["cow"]
            else:
                n_retention = ENVIRONMENTAL_FACTORS["n_retention_factors"]["heifer"]
            
            # Calculate N intake (assuming 16% CP average)
            cp_intake = dmi * 0.16  # CP fraction
            n_intake = cp_intake * 0.16  # N = CP / 6.25
            
            n_excreted = n_intake * (1 - n_retention)
            
            return {
                "methane_g_day": round(methane_g, 2),
                "methane_kg_year": round(methane_g * 365 / 1000, 2),
                "n_excreted_kg_day": round(n_excreted, 3),
                "n_excreted_kg_year": round(n_excreted * 365, 1)
            }
            
        except Exception as e:
            self.logger.error(f"Environmental impact calculation error: {e}")
            return {}


def milk_fat_pct_to_decimal(pct: float) -> float:
    """Convert milk fat percentage to decimal."""
    return max(0.01, pct / 100)


def calculate_aa_ratio(essential_aa: Dict[str, float], lysine: float) -> Dict[str, float]:
    """
    Calculate amino acid ratios relative to lysine for poultry.
    
    Args:
        essential_aa: Dictionary with AA amounts (g/100g CP)
        lysine: Lysine content
    
    Returns:
        Dictionary with ratios
    """
    if lysine <= 0:
        return {}
    
    return {
        f"{aa}_ratio": round(value / lysine, 3)
        for aa, value in essential_aa.items()
    }