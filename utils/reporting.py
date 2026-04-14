# PDF Reporting Module for Zootekni Pro
# Generates professional reports in PDF format

from fpdf import FPDF
from datetime import datetime
from typing import Dict, List, Optional
import os

from utils.logger import setup_logger

logger = setup_logger(__name__)


class RationPDFReporter:
    """Generates PDF reports for ration analysis."""
    
    def __init__(self):
        """Initialize PDF reporter."""
        self.pdf = None
        
    def create_ration_report(
        self,
        ration_data: Dict,
        animal_group: str,
        farm_name: str = "İşletme Adı",
        output_path: str = None
    ) -> str:
        """
        Create a comprehensive ration report.
        
        Args:
            ration_data: Ration data with ingredients
            animal_group: Animal group name
            farm_name: Farm/business name
            output_path: Output file path (optional)
            
        Returns:
            Path to generated PDF
        """
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
        # Set font
        self.pdf.set_font("Arial", size=10)
        
        # Header
        self._create_header(farm_name)
        
        # Title
        self.pdf.ln(15)
        self.pdf.set_font("Arial", "B", 18)
        self.pdf.cell(0, 10, "Rasyon Analiz Raporu", ln=True, align="C")
        self.pdf.ln(5)
        
        # Date and group info
        self.pdf.set_font("Arial", size=10)
        self.pdf.cell(0, 6, f"Tarih: {datetime.now().strftime('%d.%m.%Y')}", ln=True)
        self.pdf.cell(0, 6, f"Hayvan Grubu: {animal_group}", ln=True)
        self.pdf.ln(5)
        
        # Nutritional summary
        self._create_nutrition_summary(ration_data)
        
        # Ingredients table
        self._create_ingredients_table(ration_data.get('ingredients', []))
        
        # Economic summary
        self._create_economic_summary(ration_data)
        
        # Feeding instructions
        self._create_feeding_instructions(ration_data)
        
        # Footer
        self._create_footer()
        
        # Save
        if output_path is None:
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f'ration_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
            
        self.pdf.output(output_path)
        logger.info(f"Report generated: {output_path}")
        
        return output_path
    
    def _create_header(self, farm_name: str):
        """Create report header with logo placeholder and farm name."""
        self.pdf.set_fill_color(74, 144, 217)  # #4a90d9
        self.pdf.rect(0, 0, 210, 25, "F")
        
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.cell(0, 25, "Zootekni Pro", ln=True, align="C")
        
        self.pdf.set_font("Arial", size=12)
        self.pdf.cell(0, 5, "Intelligent Rationing System v5.0", ln=True, align="C")
        
        self.pdf.set_text_color(0, 0, 0)
        
    def _create_nutrition_summary(self, ration_data: Dict):
        """Create nutrition summary section."""
        self.pdf.ln(10)
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 8, "Besin Özeti", ln=True, align="L")
        
        self.pdf.set_font("Arial", size=10)
        
        # Table header
        self.pdf.set_fill_color(240, 240, 240)
        self.pdf.cell(45, 8, "Parametre", 1, 0, "C", True)
        self.pdf.cell(35, 8, "Birim", 1, 0, "C", True)
        self.pdf.cell(35, 8, "Hedef", 1, 0, "C", True)
        self.pdf.cell(35, 8, "Gerçek", 1, 0, "C", True)
        self.pdf.cell(30, 8, "Durum", 1, 1, "C", True)
        
        # Values
        nutrients = [
            ("Kuru Madde (DMI)", "kg/gün", ration_data.get('target_dmi'), ration_data.get('total_dmi')),
            ("Ham Protein (HP)", "% KM", ration_data.get('target_cp'), ration_data.get('cp_total')),
            ("NDF", "% KM", "28", ration_data.get('ndf_total')),
            ("Net Enerji (NEL)", "Mcal/kg", "1.65", ration_data.get('nel_total')),
        ]
        
        for param, unit, target, actual in nutrients:
            self.pdf.cell(45, 8, param, 1)
            self.pdf.cell(35, 8, unit, 1, 0, "C")
            self.pdf.cell(35, 8, str(target) if target else "-", 1, 0, "C")
            self.pdf.cell(35, 8, f"{actual:.2f}" if actual else "-", 1, 0, "C")
            
            # Status
            if actual and target:
                try:
                    status = "OK" if float(actual) >= float(target) * 0.9 else "Düşük"
                except:
                    status = "-"
            else:
                status = "-"
                
            self.pdf.cell(30, 8, status, 1, 1, "C")
            
        self.pdf.ln(5)
        
    def _create_ingredients_table(self, ingredients: List[Dict]):
        """Create ingredients table section."""
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 8, "Rasyon Bileşenleri", ln=True, align="L")
        
        self.pdf.set_font("Arial", size=9)
        
        # Table header
        self.pdf.set_fill_color(240, 240, 240)
        headers = ["Yem", "Miktar (kg)", "KM (kg)", "Oran (%)", "Maliyet (₺)"]
        widths = [70, 30, 25, 25, 30]
        
        for h, w in zip(headers, widths):
            self.pdf.cell(w, 8, h, 1, 0, "C", True)
        self.pdf.ln()
        
        # Data rows
        for ing in ingredients:
            feed_name = ing.get('feed_name', 'Unknown')[:25]
            amount = ing.get('amount_kg', 0)
            dm = ing.get('amount_dm', 0)
            cost = ing.get('cost', 0)
            proportion = (amount / sum(i.get('amount_kg', 0) for i in ingredients)) * 100 if ingredients else 0
            
            self.pdf.cell(70, 7, feed_name, 1)
            self.pdf.cell(30, 7, f"{amount:.2f}", 1, 0, "R")
            self.pdf.cell(25, 7, f"{dm:.2f}", 1, 0, "R")
            self.pdf.cell(25, 7, f"{proportion:.1f}", 1, 0, "R")
            self.pdf.cell(30, 7, f"{cost:.2f}", 1, 1, "R")
            
        self.pdf.ln(5)
        
    def _create_economic_summary(self, ration_data: Dict):
        """Create economic summary section."""
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 8, "Ekonomik Özet", ln=True, align="L")
        
        self.pdf.set_font("Arial", size=10)
        
        cost_per_dm = ration_data.get('cost_per_kg_dm', 0)
        total_cost = ration_data.get('total_cost', 0)
        
        self.pdf.cell(80, 7, "Toplam Maliyet:", 1)
        self.pdf.cell(0, 7, f"₺{total_cost:.2f}/gün", 1, 1, "R")
        
        self.pdf.cell(80, 7, "Maliyet (kg KM başına):", 1)
        self.pdf.cell(0, 7, f"₺{cost_per_dm:.2f}", 1, 1, "R")
        
        self.pdf.ln(5)
        
    def _create_feeding_instructions(self, ration_data: Dict):
        """Create feeding instructions section."""
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 8, "Besleme Talimatı", ln=True, align="L")
        
        self.pdf.set_font("Arial", size=10)
        
        instructions = [
            "• Rasyon günde iki eşit öğünde verilmelidir.",
            "• Taze su her zaman erişilebilir olmalıdır.",
            "• Rasyon değişiklikleri kademeli yapılmalıdır (7-10 gün).",
            "• İlk 2 saat sonra artan yem uzaklaştırılmalıdır.",
        ]
        
        for instr in instructions:
            self.pdf.cell(0, 7, instr, ln=True)
            
        self.pdf.ln(5)
        
    def _create_footer(self):
        """Create report footer."""
        self.pdf.set_y(-20)
        self.pdf.set_font("Arial", "I", 8)
        self.pdf.set_text_color(128, 128, 128)
        self.pdf.cell(0, 5, "Zootekni Pro - Precision Livestock Farming & Computational Nutrition", ln=True, align="C")
        self.pdf.cell(0, 5, f"Rapor tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True, align="C")
        
        self.pdf.set_text_color(0, 0, 0)


class EconomicPDFReporter:
    """Generates PDF reports for economic analysis."""
    
    def create_economic_report(
        self,
        iofc_data: Dict,
        sensitivity_data: List[Dict],
        farm_name: str = "İşletme Adı",
        output_path: str = None
    ) -> str:
        """
        Create economic analysis report.
        
        Args:
            iofc_data: IOFC calculation data
            sensitivity_data: Sensitivity analysis data
            farm_name: Farm name
            output_path: Output path
            
        Returns:
            Path to generated PDF
        """
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
        self.pdf.set_font("Arial", size=10)
        
        # Header
        self.pdf.set_fill_color(74, 144, 217)
        self.pdf.rect(0, 0, 210, 20, "F")
        self.pdf.set_font("Arial", "B", 14)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.cell(0, 20, "Ekonomik Analiz Raporu", ln=True, align="C")
        
        self.pdf.ln(10)
        self.pdf.set_text_color(0, 0, 0)
        
        # IOFC Section
        self.pdf.set_font("Arial", "B", 12)
        self.pdf.cell(0, 8, "IOFC Analizi", ln=True)
        
        self.pdf.set_font("Arial", size=10)
        
        milk_revenue = iofc_data.get('milk_revenue', 0)
        feed_cost = iofc_data.get('feed_cost', 0)
        iofc = iofc_data.get('iofc', 0)
        
        self.pdf.cell(100, 7, "Süt Geliri:", 1)
        self.pdf.cell(0, 7, f"₺{milk_revenue:.2f}/gün", 1, 1, "R")
        
        self.pdf.cell(100, 7, "Yem Maliyeti:", 1)
        self.pdf.cell(0, 7, f"₺{feed_cost:.2f}/gün", 1, 1, "R")
        
        self.pdf.cell(100, 7, "IOFC (Gelir - Yem Maliyeti):", 1)
        self.pdf.set_font("Arial", "B", 10)
        self.pdf.cell(0, 7, f"₺{iofc:.2f}/gün", 1, 1, "R")
        
        self.pdf.set_font("Arial", size=10)
        self.pdf.ln(5)
        
        # Sensitivity Analysis
        if sensitivity_data:
            self.pdf.set_font("Arial", "B", 12)
            self.pdf.cell(0, 8, "Duyarlılık Analizi (%10 Fiyat Artışı)", ln=True)
            
            self.pdf.set_font("Arial", size=9)
            
            headers = ["Yem", "Orijinal Maliyet", "Yeni Maliyet", "Etki"]
            widths = [60, 40, 40, 40]
            
            for h, w in zip(headers, widths):
                self.pdf.cell(w, 7, h, 1, 0, "C", True)
            self.pdf.ln()
            
            for row in sensitivity_data:
                self.pdf.cell(60, 7, row.get('feed_name', '')[:25], 1)
                self.pdf.cell(40, 7, f"₺{row.get('original_cost', 0):.2f}", 1, 0, "R")
                self.pdf.cell(40, 7, f"₺{row.get('new_cost', 0):.2f}", 1, 0, "R")
                self.pdf.cell(40, 7, f"%{row.get('impact_percent', 0):.1f}", 1, 1, "R")
        
        # Footer
        self.pdf.set_y(-15)
        self.pdf.set_font("Arial", "I", 8)
        self.pdf.set_text_color(128, 128, 128)
        self.pdf.cell(0, 5, "Zootekni Pro - Ekonomik Analiz", ln=True, align="C")
        
        if output_path is None:
            output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f'economic_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf')
            
        self.pdf.output(output_path)
        
        return output_path
