# breath_hold_training/generators/pdf_generator.py
from fpdf import FPDF
from datetime import datetime
from typing import Dict, Any
from ..core.athlete import Athlete
from ..core.training_zones import TrainingZones
from ..utils.time_utils import format_time

class PDFGenerator(FPDF):
    """PDF generator for training plans"""
    
    def __init__(self, athlete: Athlete, training_zones: TrainingZones):
        super().__init__()
        self.athlete = athlete
        self.zones = training_zones
    
    def header(self):
        """PDF header"""
        self.set_font('Arial', 'B', 16)
        title = f"Adaptive Breath-Hold Training - Week {self.athlete.current_week}/{self.athlete.total_weeks}"
        self.cell(0, 10, title, 0, 1, 'C')

        self.set_font('Arial', '', 10)
        progress_info = f"Current Max: {format_time(self.athlete.current_max)} | "
        if self.athlete.previous_max and self.athlete.previous_max > 0:
            improvement = self.athlete.current_max - self.athlete.previous_max
            progress_info += f"Progress: +{format_time(improvement)} | "
        progress_info += f"Level: {self.athlete.experience_level.title()}"

        self.cell(0, 5, progress_info, 0, 1, 'C')
        self.ln(5)
    
    def generate_complete_plan(self, weekly_schedule: Dict[str, Any]):
        """Generate complete PDF plan"""
        # Add overview page
        self.add_page()
        self._draw_overview(weekly_schedule)
        
        # Add session pages
        for day, session in weekly_schedule.items():
            self._draw_session_detail(day, session)
    
    def _draw_overview(self, schedule: Dict[str, Any]):
        """Draw training overview"""
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, f'Personalized Training Plan - {self.athlete.goals.title()} Focus', 0, 1, 'L')
        self.ln(5)
        
        # Personal stats
        self.set_font('Arial', '', 11)
        stats_text = f"Experience: {self.athlete.experience_level.title()} | "
        stats_text += f"Current Max: {format_time(self.athlete.current_max)}"
        if self.athlete.previous_max and self.athlete.previous_max > 0:
            improvement = ((self.athlete.current_max - self.athlete.previous_max) / self.athlete.previous_max) * 100
            stats_text += f" | Recent Progress: {improvement:.1f}%"
        
        self.multi_cell(0, 6, stats_text)
        self.ln(10)
        
        # Weekly schedule table
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'This Week\'s Schedule:', 0, 1)
        self.ln(5)
        
        for day, session in schedule.items():
            self.set_font('Arial', 'B', 10)
            self.cell(0, 6, f"{day}: {session.get('type', 'Rest')}", 0, 1)
            if 'description' in session:
                self.set_font('Arial', '', 9)
                self.cell(0, 5, f"  {session['description']}", 0, 1)
        
        self.ln(10)
    
    def _draw_session_detail(self, day: str, session: Dict[str, Any]):
        """Draw detailed session page"""
        self.add_page()
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, f'{day} - {session["type"]}', 0, 1)
        self.ln(5)
        
        if 'description' in session:
            self.set_font('Arial', '', 11)
            self.multi_cell(0, 6, session['description'])
            self.ln(5)
        
        # If session has rounds, draw table
        if 'rounds' in session:
            self._draw_rounds_table(session['rounds'])
        
        # Add notes section
        self.set_font('Arial', 'B', 11)
        self.cell(0, 8, 'Notes & Performance:', 0, 1)
        for i in range(8):
            self.cell(0, 8, '', 'B', 1)
    
    def _draw_rounds_table(self, rounds):
        """Draw rounds table"""
        # Headers
        headers = ['Round', 'Hold Time', 'Rest', 'Target RPE']
        if 'focus' in rounds[0]:
            headers.append('Focus')
        
        col_widths = [20, 30, 30, 30] + ([70] if len(headers) > 4 else [])
        
        self.set_font('Arial', 'B', 10)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C')
        self.ln()
        
        # Data rows
        self.set_font('Arial', '', 9)
        for round_data in rounds:
            self.cell(col_widths[0], 8, str(round_data['round']), 1, 0, 'C')
            self.cell(col_widths[1], 8, round_data['hold_time'], 1, 0, 'C')
            self.cell(col_widths[2], 8, round_data['rest_time'], 1, 0, 'C')
            self.cell(col_widths[3], 8, round_data.get('target_rpe', ''), 1, 0, 'C')
            
            if 'focus' in round_data:
                focus_text = round_data['focus'][:25] + '...' if len(round_data['focus']) > 25 else round_data['focus']
                self.cell(col_widths[4], 8, focus_text, 1, 0, 'L')
            
            self.ln()
        
        self.ln(5)
    
    def save_pdf(self, filename: str):
        """Save PDF to file"""
        self.output(filename, 'F')
        return filename