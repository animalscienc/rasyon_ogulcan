# Visualization Module for Zootekni Pro
# Creates charts and graphs for ration analysis

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

from typing import Dict, List, Optional
import io
import base64

from utils.logger import setup_logger

logger = setup_logger(__name__)


class RationVisualizer:
    """Creates visualizations for ration analysis."""
    
    @staticmethod
    def create_radar_chart(
        actual_values: Dict[str, float],
        target_values: Dict[str, float],
        title: str = "Besin Örümcek Ağı"
    ) -> str:
        """
        Create radar chart comparing actual vs target nutrition.
        
        Args:
            actual_values: Actual nutrient values
            target_values: Target nutrient values
            title: Chart title
            
        Returns:
            Base64 encoded PNG image
        """
        # Common nutrients to display
        nutrients = ['CP', 'NDF', 'NEL', 'Ca', 'P', 'Mg']
        labels_tr = {
            'CP': 'Ham Protein',
            'NDF': 'NDF',
            'NEL': 'Net Enerji',
            'Ca': 'Kalsiyum',
            'P': 'Fosfor',
            'Mg': 'Magnezyum'
        }
        
        # Get values, normalized to 100% of target
        values = []
        labels = []
        
        for nut in nutrients:
            actual = actual_values.get(nut.lower(), 0)
            target = target_values.get(nut.lower(), 1)
            if target > 0:
                values.append(min(actual / target, 1.5))  # Cap at 150%
                labels.append(labels_tr[nut])
        
        # Number of variables
        num_vars = len(values)
        
        # Compute angle for each axis
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values = values + [values[0]]
        angles = angles + [angles[0]]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        # Plot actual values
        ax.fill(angles, values, color='#4a90d9', alpha=0.25)
        ax.plot(angles, values, color='#4a90d9', linewidth=2, label='Gerçek')
        
        # Plot target (100% reference)
        target_line = [1.0] * (num_vars + 1)
        ax.plot(angles, target_line, color='#ff6b6b', linewidth=2, linestyle='--', label='Hedef')
        
        # Set labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, size=10)
        
        # Set radial limits
        ax.set_ylim(0, 1.5)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0, 1.25, 1.5])
        ax.set_yticklabels(['%25', '%50', '%75', '%100', '%125', '%150'], size=8)
        
        # Add legend
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        
        # Title
        plt.title(title, size=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, facecolor='#12121e')
        buffer.seek(0)
        
        # Convert to base64
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return img_base64
    
    @staticmethod
    def create_donut_chart(
        ingredients: List[Dict],
        title: str = "Yem Maliyet Dağılımı"
    ) -> str:
        """
        Create donut chart showing cost distribution by feed.
        
        Args:
            ingredients: List of ration ingredients with costs
            title: Chart title
            
        Returns:
            Base64 encoded PNG image
        """
        if not ingredients:
            return ""
        
        # Get data
        labels = [ing.get('feed_name', 'Unknown')[:15] for ing in ingredients]
        costs = [ing.get('cost', 0) for ing in ingredients]
        
        # Filter out zero costs
        non_zero = [(l, c) for l, c in zip(labels, costs) if c > 0]
        if not non_zero:
            return ""
            
        labels, costs = zip(*non_zero)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Color palette
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        
        # Create donut chart
        wedges, texts, autotexts = ax.pie(
            costs,
            labels=labels,
            autopct='%1.1f%%',
            colors=colors,
            wedgeprops=dict(width=0.5, edgecolor='white'),
            startangle=90
        )
        
        # Style text
        for text in texts:
            text.set_fontsize(9)
            text.set_color('#c0c0d0')
            
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_color('#ffffff')
            autotext.set_weight('bold')
            
        # Title
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20, color='#ffffff')
        
        # Equal aspect ratio
        ax.axis('equal')
        
        # Background
        fig.patch.set_facecolor('#12121e')
        ax.set_facecolor('#12121e')
        
        plt.tight_layout()
        
        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, facecolor='#12121e')
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return img_base64
    
    @staticmethod
    def create_cost_comparison_chart(
        current_cost: float,
        historical_costs: List[float],
        labels: List[str],
        title: str = "Maliyet Karşılaştırması"
    ) -> str:
        """
        Create bar chart for cost comparison.
        
        Args:
            current_cost: Current ration cost
            historical_costs: Historical costs
            labels: Labels for each cost
            title: Chart title
            
        Returns:
            Base64 encoded PNG image
        """
        all_costs = [current_cost] + historical_costs
        all_labels = ['Mevcut'] + labels[:len(historical_costs)]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bars
        colors = ['#4a90d9'] + ['#3a3a5e'] * len(historical_costs)
        bars = ax.bar(all_labels, all_costs, color=colors, edgecolor='white')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'₺{height:.2f}',
                   ha='center', va='bottom', fontsize=10, color='#ffffff')
        
        # Style
        ax.set_ylabel('Maliyet (₺/kg KM)', fontsize=10, color='#a0a0b0')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15, color='#ffffff')
        ax.set_facecolor('#12121e')
        fig.patch.set_facecolor('#12121e')
        
        # Grid
        ax.yaxis.grid(True, color='#2a2a4e', linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)
        
        # Tick colors
        for tick in ax.get_xticklabels():
            tick.set_color('#c0c0d0')
        for tick in ax.get_yticklabels():
            tick.set_color('#a0a0b0')
            
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, facecolor='#12121e')
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return img_base64
    
    @staticmethod
    def create_nutrient_bar_chart(
        actual: Dict[str, float],
        target: Dict[str, float],
        title: str = "Besin Karşılaştırması"
    ) -> str:
        """
        Create grouped bar chart for nutrient comparison.
        
        Args:
            actual: Actual nutrient values
            target: Target values
            title: Chart title
            
        Returns:
            Base64 encoded PNG image
        """
        nutrients = ['cp', 'ndf', 'nel', 'ca', 'p', 'mg']
        labels_tr = {'cp': 'HP', 'ndf': 'NDF', 'nel': 'NEL', 'ca': 'Ca', 'p': 'P', 'mg': 'Mg'}
        
        actual_vals = [actual.get(n, 0) for n in nutrients]
        target_vals = [target.get(n, 0) for n in nutrients]
        
        x = np.arange(len(nutrients))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        rects1 = ax.bar(x - width/2, actual_vals, width, label='Gerçek', color='#4a90d9')
        rects2 = ax.bar(x + width/2, target_vals, width, label='Hedef', color='#ff6b6b')
        
        ax.set_ylabel('Değer', fontsize=10, color='#a0a0b0')
        ax.set_title(title, fontsize=14, fontweight='bold', pad=15, color='#ffffff')
        ax.set_xticks(x)
        ax.set_xticklabels([labels_tr[n] for n in nutrients], fontsize=10)
        ax.legend()
        
        ax.set_facecolor('#12121e')
        fig.patch.set_facecolor('#12121e')
        
        for tick in ax.get_xticklabels():
            tick.set_color('#c0c0d0')
        for tick in ax.get_yticklabels():
            tick.set_color('#a0a0b0')
            
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, facecolor='#12121e')
        buffer.seek(0)
        
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        
        return img_base64
