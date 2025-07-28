def format_time(seconds: int) -> str:
    """Convert seconds to MM:SS format"""
    if seconds < 0:
        return "0:00"
    
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"

def parse_time_input(minutes: int, seconds: int) -> int:
    """Convert minutes and seconds input to total seconds"""
    return (minutes * 60) + seconds