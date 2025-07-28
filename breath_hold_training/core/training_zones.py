from typing import Dict
from .athlete import Athlete

class TrainingZones:
    """Calculate personalized training zones based on athlete data"""
    
    BASE_ZONES = {
        'beginner': {
            'co2_base': 0.40,
            'co2_recovery': 0.30,
            'o2_start': 0.35,
            'o2_peak': 0.75,
            'test_target': 0.90
        },
        'intermediate': {
            'co2_base': 0.50,
            'co2_recovery': 0.40,
            'o2_start': 0.40,
            'o2_peak': 0.85,
            'test_target': 0.95
        },
        'advanced': {
            'co2_base': 0.60,
            'co2_recovery': 0.50,
            'o2_start': 0.45,
            'o2_peak': 0.90,
            'test_target': 1.00
        }
    }
    
    def __init__(self, athlete: Athlete):
        self.athlete = athlete
        self._zones = self._calculate_zones()
    
    def _calculate_zones(self) -> Dict[str, int]:
        """Calculate training zones with adaptive adjustments"""
        base_zones = self.BASE_ZONES[self.athlete.experience_level].copy()
        
        # Adjust based on progress rate
        progress_rate = self.athlete.progress_rate
        if progress_rate > 0.15:  # >15% improvement
            multiplier = 1.1  # Aggressive progression
        elif progress_rate < 0.05:  # <5% improvement
            multiplier = 0.9  # Conservative progression
        else:
            multiplier = 1.0
        
        # Apply multiplier (except test_target)
        for key in base_zones:
            if key != 'test_target':
                base_zones[key] *= multiplier
        
        # Convert to seconds
        return {k: int(self.athlete.current_max * v) for k, v in base_zones.items()}
    
    def get_zone(self, zone_name: str) -> int:
        """Get specific training zone value"""
        return self._zones.get(zone_name, 0)
    
    @property
    def zones(self) -> Dict[str, int]:
        """Get all training zones"""
        return self._zones.copy()