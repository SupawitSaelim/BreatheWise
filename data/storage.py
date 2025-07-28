import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from ..core.athlete import Athlete

class ProgressStorage:
    """Handle data persistence for training progress"""
    
    def __init__(self, filename: str = 'breath_hold_progress.json'):
        self.filename = filename
    
    def load_progress(self) -> Dict[str, Any]:
        """Load training progress from file"""
        if not os.path.exists(self.filename):
            return {'training_history': []}
        
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {'training_history': []}
        except Exception as e:
            raise Exception(f"Error loading progress data: {e}")
    
    def save_progress(self, athlete: Athlete, training_zones: Dict[str, int], new_max_hold: Optional[int] = None) -> str:
        """Save training progress to file"""
        data = self.load_progress()
        
        current_session = {
            'date': datetime.now().isoformat(),
            'week': athlete.current_week,
            'max_hold': new_max_hold if new_max_hold else athlete.current_max,
            'experience_level': athlete.experience_level,
            'goals': athlete.goals,
            'training_zones': training_zones
        }
        
        data['training_history'].append(current_session)
        data['current'] = current_session
        
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return self.filename
    
    def get_current_data(self) -> Optional[Dict[str, Any]]:
        """Get current training data"""
        data = self.load_progress()
        return data.get('current')
    
    def update_max_hold(self, new_max: int) -> str:
        """Update maximum hold time"""
        data = self.load_progress()
        if 'current' in data:
            data['current']['max_hold'] = new_max
            
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
        
        return self.filename