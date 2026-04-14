# Ration Optimization Model for Zootekni Pro
# Uses SciPy Simplex algorithm for linear programming

import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
from typing import Dict, List, Tuple, Optional
import pandas as pd

from utils.logger import setup_logger

logger = setup_logger(__name__)


class RationOptimizer:
    """Linear programming optimizer for dairy rations."""
    
    def __init__(self, feeds: pd.DataFrame, requirements: Dict):
        """
        Initialize optimizer.
        
        Args:
            feeds: DataFrame of available feeds
            requirements: Nutritional requirements dictionary
        """
        self.feeds = feeds
        self.requirements = requirements
        self.solution = None
        self.status = None
        
    def optimize(self) -> Tuple[Optional[Dict], str]:
        """
        Find minimum cost ration meeting all constraints.
        
        Returns:
            Tuple of (solution dict, status message)
        """
        n_feeds = len(self.feeds)
        
        if n_feeds == 0:
            return None, "No feeds available"
        
        # Objective: minimize cost
        c = self.feeds['price'].values
        
        # Build constraint matrix
        # Constraints: nutrient requirements (>=), min/max usage (<=, >=)
        
        constraints = []
        
        # Nutrient constraints (A_ub * x >= b)
        nutrient_cols = ['cp', 'ndf', 'nel', 'me', 'ca', 'p']
        nutrient_names = ['cp', 'ndf', 'nel', 'me', 'ca', 'p']
        
        for col, name in zip(nutrient_cols, nutrient_names):
            if col in self.feeds.columns and name in self.requirements:
                # Minimum requirement: -A*x <= -b (converts to scipy format)
                pass
        
        # Instead, let's use the standard linprog format
        # A_ub * x <= b_ub (inequality constraints)
        
        # For minimum requirements: -A >= -b => A <= b (scipy uses A_ub * x <= b_ub)
        # We'll transform: to enforce x >= min, we use -x <= -min
        
        # Collect constraint coefficients
        A_ub_list = []
        b_ub_list = []
        
        # Add nutrient minimum constraints
        # For each nutrient: sum(feed_nutrient * x) >= requirement
        # Convert to: -sum(feed_nutrient * x) <= -requirement
        
        nutrient_map = {
            'cp': 'cp',
            'ndf': 'ndf', 
            'nel': 'ne_lact',
            'me': 'me',
            'ca': 'ca',
            'p': 'p',
            'mg': 'mg',
            'k': 'k'
        }
        
        for name, col in nutrient_map.items():
            if col in self.feeds.columns and name in self.requirements:
                req = self.requirements[name]
                if req is not None and req > 0:
                    coeff = -self.feeds[col].fillna(0).values
                    A_ub_list.append(coeff)
                    b_ub_list.append(-req)
        
        # Fiber maximum constraint (NDF <= max)
        if 'ndf_max' in self.requirements:
            ndf_max = self.requirements['ndf_max']
            coeff = self.feeds['ndf'].fillna(0).values
            A_ub_list.append(coeff)
            b_ub_list.append(ndf_max)
            
        # Starch maximum (if needed)
        if 'starch_max' in self.requirements:
            starch_max = self.requirements['starch_max']
            coeff = self.feeds['starch'].fillna(0).values
            A_ub_list.append(coeff)
            b_ub_list.append(starch_max)
        
        # Stack constraints
        if A_ub_list:
            A_ub = np.array(A_ub_list)
            b_ub = np.array(b_ub_list)
        else:
            A_ub = None
            b_ub = None
            
        # Bounds for each feed (min and max usage)
        lb = self.feeds['min_usage'].fillna(0).values
        ub = self.feeds['max_usage'].fillna(100).values
        
        # Adjust for None values
        ub = np.where(pd.isna(ub), 100, ub)
        
        bounds = list(zip(lb, ub))
        
        # Additional constraints: sum of DMI approximately equals target
        # This ensures we get a complete ration
        if 'dmi' in self.requirements:
            dmi_target = self.requirements['dmi']
            dmi_coeff = self.feeds['dry_matter'].fillna(0).values / 100
            
            # Add equality constraint: sum(dmi * amount) = target
            # This requires sum(dmi_coeff * x) == dmi_target
            
        # Run optimization
        try:
            result = linprog(
                c=c,
                A_ub=A_ub,
                b_ub=b_ub,
                bounds=bounds,
                method='highs'
            )
            
            if result.success:
                self.solution = result
                
                # Build solution dict
                amounts = result.x
                selected_feeds = []
                
                for i, row in self.feeds.iterrows():
                    if amounts[i] > 0.01:  # Non-negligible amount
                        feed_data = {
                            'feed_id': row['id'],
                            'feed_name': row['feed_name'],
                            'amount_kg': amounts[i],
                            'amount_dm': amounts[i] * row['dry_matter'] / 100,
                            'cost': amounts[i] * row['price']
                        }
                        
                        # Calculate nutrient contribution
                        for nut in ['cp', 'ndf', 'ne_lact', 'me', 'ca', 'p']:
                            if nut in row and pd.notna(row[nut]):
                                feed_data[nut] = amounts[i] * row[nut] / 100
                        feed_data['dmi'] = amounts[i] * row['dry_matter'] / 100
                        
                        selected_feeds.append(feed_data)
                
                solution_dict = {
                    'ingredients': selected_feeds,
                    'total_dmi': sum(f['dmi'] for f in selected_feeds),
                    'total_cost': result.fun,
                    'cost_per_kg_dm': result.fun / sum(f['dmi'] for f in selected_feeds) if selected_feeds else 0,
                    'status': 'optimal',
                    'message': 'Optimal solution found'
                }
                
                return solution_dict, "Success"
            else:
                return self._handle_infeasibility(result), "Infeasible"
                
        except Exception as e:
            logger.error(f"Optimization error: {e}")
            return None, str(e)
    
    def _handle_infeasibility(self, result) -> Dict:
        """Handle infeasible optimization problem."""
        message = result.message
        
        # Analyze which constraints might be causing infeasibility
        advice = []
        
        if 'cp' in self.requirements:
            advice.append("Protein gereksinimi çok yüksek olabilir")
        if 'ndf_min' in self.requirements:
            advice.append("Lif gereksinimi çok yüksek olabilir")
        if 'dmi' in self.requirements:
            advice.append("DMI hedefi kontrol edilmeli")
            
        return {
            'ingredients': [],
            'total_dmi': 0,
            'total_cost': 0,
            'status': 'infeasible',
            'message': message,
            'relaxation_advice': advice
        }
    
    def get_shadow_prices(self) -> Dict:
        """
        Get shadow prices (dual values) from the solution.
        
        Returns:
            Dict of shadow prices for each constraint
        """
        if self.solution is None or not self.solution.success:
            return {}
            
        # Shadow prices are in solution.dual
        # Note: Highs solver may not return duals in the same format
        shadow_prices = {}
        
        # Map constraints to names
        nutrient_names = ['cp', 'ndf', 'nel', 'me', 'ca', 'p', 'mg', 'k']
        
        for i, name in enumerate(nutrient_names):
            if name in self.requirements:
                if hasattr(self.solution, 'dual') and self.solution.dual is not None:
                    if i < len(self.solution.dual):
                        shadow_prices[name] = self.solution.dual[i]
                        
        return shadow_prices


class SensitivityAnalyzer:
    """Sensitivity analysis for ration costs."""
    
    def __init__(self, optimizer: RationOptimizer):
        """
        Initialize analyzer.
        
        Args:
            optimizer: Trained optimizer
        """
        self.optimizer = optimizer
        
    def analyze_price_volatility(self, feed_index: int, price_change: float = 0.10) -> Dict:
        """
        Analyze impact of price change on ration cost.
        
        Args:
            feed_index: Index of feed to analyze
            price_change: Percentage change (default 10%)
            
        Returns:
            Dict with analysis results
        """
        if self.optimizer.solution is None:
            return {'error': 'No solution available'}
            
        original_cost = self.optimizer.solution.fun
        
        # Calculate impact for 10% price increase
        feeds = self.optimizer.feeds.copy()
        feeds.loc[feeds.index[feed_index], 'price'] *= (1 + price_change)
        
        # Re-optimize
        new_optimizer = RationOptimizer(feeds, self.optimizer.requirements)
        result, _ = new_optimizer.optimize()
        
        if result:
            new_cost = result['total_cost']
            impact = new_cost - original_cost
            impact_pct = (impact / original_cost) * 100
            
            return {
                'original_cost': original_cost,
                'new_cost': new_cost,
                'impact': impact,
                'impact_percent': impact_pct,
                'feed_name': feeds.iloc[feed_index]['feed_name'],
                'price_change': f"+{price_change*100}%"
            }
        
        return {'error': 'Could not re-optimize'}
    
    def run_full_sensitivity(self) -> pd.DataFrame:
        """
        Run full sensitivity analysis for all feeds.
        
        Returns:
            DataFrame with sensitivity results
        """
        results = []
        
        for i in range(len(self.optimizer.feeds)):
            analysis = self.analyze_price_volatility(i)
            if 'error' not in analysis:
                results.append(analysis)
                
        return pd.DataFrame(results)


class EconomicAnalyzer:
    """Economic analysis module for rations."""
    
    @staticmethod
    def calculate_iofc(milk_yield: float, milk_price: float, feed_cost: float) -> float:
        """
        Calculate Income Over Feed Cost.
        
        Args:
            milk_yield: Daily milk yield (kg)
            milk_price: Price per kg milk (TL)
            feed_cost: Daily feed cost (TL)
            
        Returns:
            IOFC in TL/day
        """
        return (milk_yield * milk_price) - feed_cost
    
    @staticmethod
    def calculate_marginal_return(
        current_milk: float,
        current_cost: float,
        current_price: float,
        added_energy_cost: float,
        energy_efficiency: float
    ) -> Tuple[float, bool]:
        """
        Calculate if adding more energy is profitable.
        
        Args:
            current_milk: Current daily milk yield (kg)
            current_cost: Current daily feed cost (TL)
            current_price: Milk price per kg (TL)
            added_energy_cost: Cost of added energy (TL/day)
            energy_efficiency: Milk response to added energy (kg milk per 0.1 Mcal NEL)
            
        Returns:
            Tuple of (marginal return, is_profitable)
        """
        # Additional milk from added energy
        added_milk = energy_efficiency * 10  # Simplified
        
        # Additional revenue
        added_revenue = added_milk * current_price
        
        # Marginal return
        marginal_return = added_revenue - added_energy_cost
        
        is_profitable = marginal_return > 0
        
        return marginal_return, is_profitable
    
    @staticmethod
    def calculate_feed_cost_per_kg_milk(feed_cost: float, milk_yield: float) -> float:
        """
        Calculate feed cost per kg milk.
        
        Args:
            feed_cost: Daily feed cost
            milk_yield: Daily milk yield
            
        Returns:
            Cost per kg milk
        """
        if milk_yield <= 0:
            return float('inf')
        return feed_cost / milk_yield
