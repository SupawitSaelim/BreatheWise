from dataclasses import dataclass
from typing import Optional
from ..utils.validators import validate_experience_level, validate_goals

@dataclass
class Athlete:
    """Athlete data model with validation"""
    current_max: int  # seconds
    experience_level: str  # 'beginner', 'intermediate', 'advanced'
    goals: str  # 'strength', 'endurance', 'balanced'
    current_week: int
    total_weeks: int = 6
    previous_max: Optional[int] = None
    
    def __post_init__(self):
        """Validate data after initialization"""
        validate_experience_level(self.experience_level)
        validate_goals(self.goals)
        
        if not 1 <= self.current_week <= self.total_weeks:
            raise ValueError(f"Week must be between 1 and {self.total_weeks}")
            
        if self.current_max <= 0:
            raise ValueError("Current max must be positive")
    
    @property
    def progress_rate(self) -> float:
        """Calculate progress rate compared to previous max"""
        if not self.previous_max or self.previous_max == 0:
            return 0.0
        return (self.current_max - self.previous_max) / self.previous_max
    
    @property
    def improvement_seconds(self) -> int:
        """Get improvement in seconds"""
        if not self.previous_max:
            return 0
        return self.current_max - self.previous_max