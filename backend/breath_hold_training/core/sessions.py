from typing import Dict, List, Any
from .athlete import Athlete
from .training_zones import TrainingZones
from ..utils.time_utils import format_time

class SessionGenerator:
    """Generate different types of training sessions"""
    
    def __init__(self, athlete: Athlete, training_zones: TrainingZones):
        self.athlete = athlete
        self.zones = training_zones
    
    def calculate_weekly_progression(self) -> float:
        """Calculate progression multiplier for current week"""
        progression_curves = {
            'strength': [1.0, 1.05, 1.12, 0.95, 1.18, 1.25],
            'endurance': [1.0, 1.08, 1.15, 0.90, 1.20, 1.28],
            'balanced': [1.0, 1.1, 1.2, 1.0, 1.25, 1.3]
        }
        
        curve = progression_curves[self.athlete.goals]
        week_index = min(self.athlete.current_week - 1, 5)
        return curve[week_index]
    
    def generate_co2_table(self, session_type: str = "standard") -> Dict[str, Any]:
        """Generate CO2 tolerance table"""
        multiplier = self.calculate_weekly_progression()
        
        if session_type == "recovery":
            base_hold = int(self.zones.get_zone('co2_recovery') * multiplier)
            rest_start, rest_end = 150, 60
            target_rpe = '5-6'
            rounds_count = 6
        else:
            base_hold = int(self.zones.get_zone('co2_base') * multiplier)
            rest_start, rest_end = 120, 30
            target_rpe = '7-8'
            rounds_count = 7
        
        rounds = []
        for i in range(rounds_count):
            if rounds_count > 1:
                rest_time = rest_start - (i * (rest_start - rest_end) // (rounds_count - 1))
            else:
                rest_time = rest_start
            
            rounds.append({
                'round': i + 1,
                'hold_time': format_time(base_hold),
                'rest_time': format_time(rest_time),
                'target_rpe': target_rpe
            })
        
        return {
            'type': f'Adaptive CO2 Table ({session_type.title()})',
            'description': f'Personalized CO2 tolerance - Base: {format_time(base_hold)}',
            'rounds': rounds,
            'notes': f'Adapted for {self.athlete.experience_level} level. Focus on consistent performance.'
        }
    
    def generate_o2_table(self) -> Dict[str, Any]:
        """Generate O2 efficiency table"""
        multiplier = self.calculate_weekly_progression()
        start_time = int(self.zones.get_zone('o2_start') * multiplier)
        peak_time = int(self.zones.get_zone('o2_peak') * multiplier)
        
        round_counts = {'beginner': 5, 'intermediate': 6, 'advanced': 7}
        rounds_count = round_counts[self.athlete.experience_level]
        
        rounds = []
        increment = (peak_time - start_time) // (rounds_count - 1) if rounds_count > 1 else 0
        
        for i in range(rounds_count):
            hold_time = start_time + (i * increment)
            rest_time = 150 + (30 if i >= rounds_count - 2 else 0)
            target_rpe = '8-9' if i >= rounds_count - 2 else '6-8'
            
            rounds.append({
                'round': i + 1,
                'hold_time': format_time(hold_time),
                'rest_time': format_time(rest_time),
                'target_rpe': target_rpe
            })
        
        return {
            'type': 'Adaptive O2 Table',
            'description': f'O2 efficiency training - Peak: {format_time(peak_time)}',
            'rounds': rounds,
            'notes': f'Progressive overload adapted to your {self.athlete.experience_level} level.'
        }
    
    def generate_performance_test(self) -> Dict[str, Any]:
        """Generate performance test session"""
        multiplier = self.calculate_weekly_progression()
        target = int(self.zones.get_zone('test_target') * multiplier)
        
        if self.athlete.experience_level == 'beginner':
            rounds = [
                {'round': 1, 'hold_time': format_time(int(target * 0.6)), 'rest_time': '2:30', 'target_rpe': '6-7'},
                {'round': 2, 'hold_time': format_time(int(target * 0.8)), 'rest_time': '3:30', 'target_rpe': '8'},
                {'round': 3, 'hold_time': f'{format_time(target)}+', 'rest_time': 'Complete', 'target_rpe': '9'}
            ]
        else:
            rounds = [
                {'round': 1, 'hold_time': format_time(int(target * 0.7)), 'rest_time': '3:00', 'target_rpe': '6-7'},
                {'round': 2, 'hold_time': format_time(int(target * 0.85)), 'rest_time': '4:00', 'target_rpe': '8'},
                {'round': 3, 'hold_time': f'{format_time(target)}+', 'rest_time': 'Complete', 'target_rpe': '9-10'}
            ]
        
        return {
            'type': 'Adaptive Performance Test',
            'description': f'Target: Beat {format_time(target)} (Current goal: +{target - self.athlete.current_max}s)',
            'rounds': rounds,
            'notes': 'Record your actual max time. This becomes your new baseline for next planning cycle.'
        }
    
    def generate_technique_session(self) -> Dict[str, Any]:
        """Generate technique-focused session"""
        base_time = self.zones.get_zone('co2_recovery')
        
        techniques = [
            'Box Breathing (4-4-4-4)',
            'Relaxation Scan',
            'Heart Rate Awareness',
            'Mental Focus Training'
        ]
        
        rounds = []
        for i, technique in enumerate(techniques):
            rounds.append({
                'round': i + 1,
                'hold_time': format_time(base_time),
                'rest_time': '2:00',
                'target_rpe': '4-6',
                'focus': technique
            })
        
        return {
            'type': 'Adaptive Technique Work',
            'description': 'Skill development and active recovery',
            'rounds': rounds,
            'notes': 'Focus on quality over performance. Should feel refreshing and educational.'
        }