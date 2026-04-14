# Nutrition Models for Zootekni Pro
# Implements NRC (2021), INRA, and ARC standards for ruminant nutrition

import numpy as np
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AnimalParameters:
    """Animal nutritional parameters."""
    animal_type: str  # 'dairy_cow', 'beef_cow', 'sheep', 'goat', 'poultry'
    body_weight: float  # kg
    milk_yield: float = 0  # kg/day
    milk_fat: float = 3.5  # %
    milk_protein: float = 3.2  # %
    lactation_week: int = 1
    pregnancy_months: int = 0
    is_pregnant: bool = False
    is_lactating: bool = False
    is_growing: bool = False
    age_months: float = 24
    breed: str = 'holstein'


class NRC2021Model:
    """NRC 2021 Dairy Cattle Nutrition Model."""
    
    # Maintenance requirements coefficients
    MAINTENANCE_NEL_MCAL = 0.08  # per kg body weight^0.75
    
    @staticmethod
    def calculate_dmi(animal: AnimalParameters) -> float:
        """
        Calculate Dry Matter Intake using NRC 2021 equations.
        
        Args:
            animal: Animal parameters
            
        Returns:
            DMI in kg/day
        """
        bw = animal.body_weight
        
        # Base maintenance DMI
        dmi_maintenance = 1.2 * (bw ** 0.75) / 100 * 3.63  # Simplified
        
        if animal.is_lactating:
            # Lactating cow DMI equation
            milk_factor = 0.372 * animal.milk_yield + 0.0968 * animal.body_weight
            fat_factor = 0.19 * animal.milk_fat
            week_factor = -0.0001 * (animal.lactation_week ** 2) + 0.015
            
            dmi = max(dmi_maintenance, milk_factor * (1 + fat_factor) + week_factor * bw / 100)
        elif animal.is_pregnant:
            # Dry/pregnant cow
            trimester = min(animal.pregnancy_months // 3 + 1, 3)
            preg_factor = 0.013 * bw if trimester == 3 else 0.008 * bw
            dmi = dmi_maintenance + preg_factor
        else:
            # Dry cow
            dmi = dmi_maintenance * 1.1
            
        return max(dmi, 10)  # Minimum 10 kg for cows
    
    @staticmethod
    def calculate_nel_requirement(animal: AnimalParameters) -> float:
        """
        Calculate Net Energy for Lactation requirement.
        
        Args:
            animal: Animal parameters
            
        Returns:
            NEL requirement in Mcal/day
        """
        bw = animal.body_weight
        
        # Maintenance
        nel_maintenance = NRC2021Model.MAINTENANCE_NEL_MCAL * (bw ** 0.75)
        
        # Activity factor (grazing vs confined)
        activity_factor = 1.0
        
        # Lactation
        nel_lactation = 0.0
        if animal.is_lactating:
            # NEL for milk (Mcal/kg milk)
            fat_correction = (animal.milk_fat - 3.5) * 0.036
            nel_per_kg_milk = 0.0925 * animal.milk_fat + 0.0548 * animal.milk_protein + 0.192
            nel_lactation = animal.milk_yield * nel_per_kg_milk
            
            # Efficiency of ME to NEL conversion
            nel_lactation *= 0.64
            
        # Pregnancy
        nel_pregnancy = 0.0
        if animal.is_pregnant and animal.pregnancy_months >= 7:
            # Last 2 months of pregnancy
            fetal_growth = 0.05 * (animal.pregnancy_months - 5) ** 2
            nel_pregnancy = fetal_growth * bw / 100
            
        # Growth
        nel_growth = 0.0
        if animal.is_growing:
            # Growing animal
            avg_daily_gain = 0.5  # kg/day assumed
            nel_growth = avg_daily_gain * (0.84 * avg_daily_gain + 0.26 * bw / 100)
            
        return (nel_maintenance + nel_lactation + nel_pregnancy + nel_growth) * activity_factor
    
    @staticmethod
    def calculate_protein_requirement(animal: AnimalParameters) -> Dict[str, float]:
        """
        Calculate protein requirements.
        
        Args:
            animal: Animal parameters
            
        Returns:
            Dict with MP, RDP, RUP requirements in g/day
        """
        bw = animal.body_weight
        
        # Maintenance N (g/day)
        n_maintenance = 2.3 * (bw ** 0.75)
        
        # Milk protein N
        n_milk = 0
        if animal.is_lactating:
            n_milk = animal.milk_yield * animal.milk_protein * 10  # Convert % to g/kg
            
        # Milk protein = milk_protein% * milk_yield * 10
        milk_protein_g = animal.milk_yield * animal.milk_protein * 10
        
        # Efficiency of N use
        efficiency = 0.67
        
        # Metabolizable protein requirement
        mp_required = (n_maintenance + milk_protein_g / efficiency) * 6.25  # Convert N to protein
        
        # RDP and RUP split (typical: 65% RDP, 35% RUP)
        rdp = mp_required * 0.65
        rup = mp_required * 0.35
        
        return {
            'mp': mp_required,
            'rdp': rdp,
            'rup': rup,
            'cp': mp_required * 1.1  # Crude protein
        }
    
    @staticmethod
    def calculate_mineral_requirements(animal: AnimalParameters) -> Dict[str, float]:
        """
        Calculate mineral requirements based on animal type and production.
        
        Args:
            animal: Animal parameters
            
        Returns:
            Dict with mineral requirements in g/day (except where noted)
        """
        bw = animal.body_weight
        
        # Base maintenance requirements
        ca_maintenance = 0.015 * bw  # g/kg BW
        p_maintenance = 0.01 * bw
        
        # Milk secretion
        ca_milk = 0
        p_milk = 0
        if animal.is_lactating:
            ca_milk = animal.milk_yield * 1.2  # g/kg milk
            p_milk = animal.milk_yield * 0.9
            
        # Total requirements
        ca_total = (ca_maintenance + ca_milk) * 1.1  # 10% safety margin
        p_total = (p_maintenance + p_milk) * 1.1
        
        # Other minerals
        mg = max(0.003 * bw, 2.0)  # Minimum 2g
        k = max(0.006 * bw, 10.0)  # Minimum 10g (avoid tetany)
        na = 0.003 * bw
        cl = 0.004 * bw
        s = 0.003 * bw
        
        return {
            'ca': ca_total,
            'p': p_total,
            'mg': mg,
            'k': k,
            'na': na,
            'cl': cl,
            's': s
        }
    
    @staticmethod
    def calculate_dcad(animal: AnimalParameters, diet: Dict[str, float]) -> float:
        """
        Calculate Dietary Cation-Anion Difference.
        
        Args:
            animal: Animal parameters
            diet: Diet mineral composition (g/kg DM)
            
        Returns:
            DCAD in mEq/kg DM
        """
        # DCAD = (Na + K + Ca + Mg) - (Cl + S)
        # Convert to mEq
        
        na_meq = (diet.get('na', 0) / 23) * 1000  # Na atomic weight
        k_meq = (diet.get('k', 0) / 39) * 1000   # K atomic weight
        ca_meq = (diet.get('ca', 0) / 20) * 1000 / 2  # Ca / valence
        mg_meq = (diet.get('mg', 0) / 24) * 1000 / 2
        
        cl_meq = (diet.get('cl', 0) / 35.5) * 1000
        s_meq = (diet.get('s', 0) / 32) * 1000
        
        dcad = (na_meq + k_meq + ca_meq + mg_meq) - (cl_meq + s_meq)
        
        return dcad


class PoultryModel:
    """Poultry nutrition model for ideal protein calculations."""
    
    # Ideal amino acid ratios (relative to Lysine)
    IDEAL_AA_RATIOS = {
        'lys': 1.0,
        'met': 0.35,  # Met + Cys
        'met_cys': 0.85,
        'thr': 0.65,
        'trp': 0.18,
        'arg': 1.0,
        'his': 0.35,
        'ile': 0.70,
        'leu': 1.10,
        'phe': 0.60,  # Phe + Tyr
        'phe_tyr': 1.00,
        'val': 0.80,
    }
    
    @staticmethod
    def validate_amino_acid_balance(diet: Dict[str, float]) -> Dict[str, float]:
        """
        Validate amino acid balance in poultry diet.
        
        Args:
            diet: Dict of amino acids in g/kg DM
            
        Returns:
            Dict with deviations from ideal ratios
        """
        if 'lys' not in diet or diet['lys'] == 0:
            return {'status': 'error', 'message': 'Lysine not provided'}
        
        lysine = diet['lys']
        deviations = {}
        
        for aa, ratio in PoultryModel.IDEAL_AA_RATIOS.items():
            if aa in diet and diet[aa] > 0:
                actual_ratio = diet[aa] / lysine
                deviation = (actual_ratio - ratio) / ratio * 100
                deviations[aa] = deviation
        
        return deviations


class EnvironmentalModel:
    """Environmental impact calculation model."""
    
    @staticmethod
    def calculate_methane_emission(animal: AnimalParameters, diet: Dict) -> float:
        """
        Calculate daily methane emission.
        
        Based on Mills et al. (2003) and IPCC Tier 2 method.
        
        Args:
            animal: Animal parameters
            diet: Diet composition
            
        Returns:
            CH4 emission in g/day
        """
        dmi = diet.get('dmi', 0)
        
        if dmi <= 0:
            return 0
        
        # Methane yield (L CH4 / kg DMI)
        # Varies by feed type
        forage_fraction = diet.get('ndf', 25) / 100
        
        if forage_fraction > 0.6:
            # High forage diet
            methane_yield = 21.3
        elif forage_fraction > 0.3:
            # Mixed diet
            methane_yield = 18.5
        else:
            # High concentrate
            methane_yield = 15.2
        
        # Gross energy intake (MJ/day)
        ge_intake = dmi * diet.get('me', 10)  # Assuming ME 10 MJ/kg DM
        
        # Methane energy loss (MJ/day)
        methane_energy = methane_yield * dmi / 55.5  # Convert to energy
        
        # CH4 in grams (1 MJ = 5.88 g CH4)
        ch4_grams = methane_energy * 5.88 * 0.67  # 67% of GE as CH4
        
        return max(ch4_grams, 0)
    
    @staticmethod
    def calculate_nitrogen_excretion(animal: AnimalParameters, diet: Dict) -> float:
        """
        Calculate nitrogen excretion.
        
        Args:
            animal: Animal parameters
            diet: Diet composition
            
        Returns:
            N excretion in g/day
        """
        if animal.is_lactating:
            # N in milk
            n_milk = animal.milk_yield * animal.milk_protein * 10 / 6.25  # Protein to N
        else:
            n_milk = 0
        
        # N intake
        n_intake = diet.get('dmi', 0) * diet.get('cp', 0) / 100 * 6.25  # CP to N
        
        # N retained (for pregnancy/growth)
        n_retained = 0
        if animal.is_growing:
            n_retained = 20  # g N/day for growing
        if animal.is_pregnant:
            n_retained += 10
            
        # N excretion
        n_excreted = max(0, n_intake - n_milk - n_retained)
        
        return n_excreted
