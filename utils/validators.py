def validate_experience_level(level: str) -> None:
    """Validate experience level input"""
    valid_levels = ['beginner', 'intermediate', 'advanced']
    if level not in valid_levels:
        raise ValueError(f"Experience level must be one of: {valid_levels}")

def validate_goals(goals: str) -> None:
    """Validate training goals input"""
    valid_goals = ['strength', 'endurance', 'balanced']
    if goals not in valid_goals:
        raise ValueError(f"Goals must be one of: {valid_goals}")

def validate_week(current_week: int, total_weeks: int = 6) -> None:
    """Validate week number"""
    if not 1 <= current_week <= total_weeks:
        raise ValueError(f"Week must be between 1 and {total_weeks}")