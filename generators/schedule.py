from typing import Dict, Any
from ..core.athlete import Athlete
from ..core.sessions import SessionGenerator

class ScheduleGenerator:
    """Generate weekly training schedules"""
    
    def __init__(self, athlete: Athlete, session_generator: SessionGenerator):
        self.athlete = athlete
        self.session_gen = session_generator
    
    def generate_weekly_schedule(self) -> Dict[str, Any]:
        """Generate adaptive weekly schedule based on goals and level"""
        base_schedule = {
            'Monday': self.session_gen.generate_co2_table("recovery"),
            'Tuesday': self.session_gen.generate_performance_test(),
            'Wednesday': {'type': 'Active Recovery', 'description': 'Light mobility, breathing technique practice'},
            'Thursday': self.session_gen.generate_o2_table(),
            'Friday': self.session_gen.generate_co2_table("standard"),
            'Saturday': self.session_gen.generate_technique_session(),
            'Sunday': {'type': 'Complete Rest', 'description': 'Full recovery day'}
        }
        
        # Adjust for goals
        if self.athlete.goals == 'strength':
            base_schedule['Saturday'] = self.session_gen.generate_co2_table("recovery")
        elif self.athlete.goals == 'endurance':
            base_schedule['Wednesday'] = self.session_gen.generate_technique_session()
        
        # Deload week adjustments
        if self.athlete.current_week == 4:
            base_schedule['Tuesday'] = self.session_gen.generate_technique_session()
            base_schedule['Thursday'] = self.session_gen.generate_co2_table("recovery")
            base_schedule['Friday'] = self.session_gen.generate_technique_session()
        
        return base_schedule