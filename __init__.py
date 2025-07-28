"""
Adaptive Breath Hold Training System
A modular system for generating personalized breath hold training plans.
"""

from .core.athlete import Athlete
from .core.training_zones import TrainingZones
from .core.sessions import SessionGenerator
from .generators.schedule import ScheduleGenerator
from .generators.pdf_generator import PDFGenerator
from .data.storage import ProgressStorage

__version__ = "1.0.0"
__all__ = [
    'Athlete',
    'TrainingZones', 
    'SessionGenerator',
    'ScheduleGenerator',
    'PDFGenerator',
    'ProgressStorage'
]