# breath_hold_training/cli/interface.py
import sys
from datetime import datetime
from ..core.athlete import Athlete
from ..core.training_zones import TrainingZones
from ..core.sessions import SessionGenerator
from ..generators.schedule import ScheduleGenerator
from ..generators.pdf_generator import PDFGenerator
from ..data.storage import ProgressStorage
from ..utils.time_utils import parse_time_input, format_time

def get_athlete_input():
    """Interactive input system for athlete data"""
    print("=== Adaptive Breath Hold Training Plan Generator ===\n")

    # Get current max hold
    while True:
        try:
            max_minutes = int(input("Current maximum breath hold (minutes): "))
            max_seconds = int(input("Additional seconds (0-59): "))
            current_max = parse_time_input(max_minutes, max_seconds)
            print(f"Current max: {format_time(current_max)}")
            break
        except ValueError:
            print("Please enter valid numbers.")

    # Get previous max for progress tracking
    has_previous = input("Do you have a previous max to compare? (y/n): ").lower().startswith('y')
    previous_max = None
    if has_previous:
        try:
            prev_min = int(input("Previous max (minutes): "))
            prev_sec = int(input("Previous max (seconds): "))
            previous_max = parse_time_input(prev_min, prev_sec)
            improvement = current_max - previous_max
            print(f"Progress: {'+' if improvement >= 0 else ''}{improvement} seconds")
        except ValueError:
            print("Invalid input, skipping previous max.")
            previous_max = None

    # Get experience level
    print("\nExperience Levels:")
    print("1. Beginner (< 6 months training)")
    print("2. Intermediate (6 months - 2 years)")
    print("3. Advanced (2+ years)")

    while True:
        try:
            level_choice = int(input("Select experience level (1-3): "))
            levels = {1: 'beginner', 2: 'intermediate', 3: 'advanced'}
            experience_level = levels[level_choice]
            break
        except (ValueError, KeyError):
            print("Please enter 1, 2, or 3.")

    # Get training goals
    print("\nTraining Goals:")
    print("1. Strength (longer single holds)")
    print("2. Endurance (multiple holds, volume)")
    print("3. Balanced (mix of both)")

    while True:
        try:
            goal_choice = int(input("Select primary goal (1-3): "))
            goals = {1: 'strength', 2: 'endurance', 3: 'balanced'}
            training_goals = goals[goal_choice]
            break
        except (ValueError, KeyError):
            print("Please enter 1, 2, or 3.")

    # Get week information
    while True:
        try:
            current_week = int(input("Which week of training? (1-6): "))
            if 1 <= current_week <= 6:
                break
            else:
                print("Please enter a week between 1 and 6.")
        except ValueError:
            print("Please enter a valid number.")

    # Confirm data
    print(f"\n=== Training Plan Summary ===")
    print(f"Current Max: {format_time(current_max)}")
    if previous_max:
        print(f"Previous Max: {format_time(previous_max)}")
    print(f"Experience: {experience_level.title()}")
    print(f"Goal: {training_goals.title()}")
    print(f"Week: {current_week}/6")

    confirm = input("\nGenerate training plan with this data? (y/n): ")
    if not confirm.lower().startswith('y'):
        print("Plan generation cancelled.")
        return None

    return Athlete(
        current_max=current_max,
        previous_max=previous_max,
        experience_level=experience_level,
        goals=training_goals,
        current_week=current_week,
        total_weeks=6
    )

def create_training_plan():
    """Main function to create adaptive training plan"""
    print("=== Adaptive Breath Hold Training System ===\n")
    
    # Check for previous data
    storage = ProgressStorage()
    previous_data = storage.get_current_data()
    
    if previous_data:
        print("Previous training data found:")
        prev_max = previous_data.get('max_hold', 0)
        if prev_max > 0:
            print(f"Last recorded max: {format_time(prev_max)}")
            print(f"Experience level: {previous_data.get('experience_level', 'unknown').title()}")
            print(f"Goals: {previous_data.get('goals', 'unknown').title()}")

            use_previous = input("Use this as baseline for comparison? (y/n): ").lower().startswith('y')
            athlete = get_athlete_input()
            if athlete and use_previous:
                # Create new athlete with previous max for comparison
                athlete = Athlete(
                    current_max=athlete.current_max,
                    previous_max=prev_max,
                    experience_level=athlete.experience_level,
                    goals=athlete.goals,
                    current_week=athlete.current_week,
                    total_weeks=athlete.total_weeks
                )
        else:
            athlete = get_athlete_input()
    else:
        athlete = get_athlete_input()
    
    if not athlete:
        print("No athlete data provided. Cannot generate plan.")
        return

    try:
        # Create the adaptive training plan
        print(f"\nGenerating adaptive training plan...")
        
        # Initialize components
        zones = TrainingZones(athlete)
        session_gen = SessionGenerator(athlete, zones)
        schedule_gen = ScheduleGenerator(athlete, session_gen)
        
        # Generate schedule
        weekly_schedule = schedule_gen.generate_weekly_schedule()
        
        # Generate PDF
        pdf_gen = PDFGenerator(athlete, zones)
        pdf_gen.generate_complete_plan(weekly_schedule)
        
        # Generate filename
        filename = f"adaptive_breath_hold_week{athlete.current_week}_max{athlete.current_max//60}m{athlete.current_max%60}s_{datetime.now().strftime('%Y%m%d')}.pdf"
        pdf_gen.save_pdf(filename)

        # Save progress data
        progress_file = storage.save_progress(athlete, zones.zones)

        print(f"\n✅ Adaptive training plan created: {filename}")
        print(f"📊 Progress data saved: {progress_file}")
        print(f"\n🔄 To generate next week's plan:")
        print(f"1. Complete this week's training")
        print(f"2. Record your new max hold time")
        print(f"3. Run this program again with updated data")
        print(f"4. The system will auto-adapt your training zones!")

        return filename

    except Exception as e:
        print(f"Error creating training plan: {e}")
        import traceback
        traceback.print_exc()
        return None

def update_max_after_testing():
    """Quick function to update max hold after performance testing"""
    print("=== Update Maximum Hold Time ===\n")

    storage = ProgressStorage()
    previous_data = storage.get_current_data()
    
    if not previous_data:
        print("No previous training data found. Please run the full setup first.")
        return

    old_max = previous_data.get('max_hold', 0)
    print(f"Current recorded max: {format_time(old_max)}")

    # Get new max
    try:
        new_minutes = int(input("New maximum hold (minutes): "))
        new_seconds = int(input("Additional seconds (0-59): "))
        new_max = parse_time_input(new_minutes, new_seconds)

        improvement = new_max - old_max
        improvement_pct = (improvement / old_max) * 100 if old_max > 0 else 0

        print(f"\nNew max: {format_time(new_max)}")
        print(f"Improvement: {'+' if improvement >= 0 else ''}{improvement} seconds ({improvement_pct:+.1f}%)")

        if improvement_pct > 15:
            print("🚀 Excellent progress! Next plan will use aggressive progression.")
        elif improvement_pct > 5:
            print("✅ Good progress! Continuing current progression rate.")
        elif improvement_pct > 0:
            print("📈 Steady progress! May adjust for better gains.")
        else:
            print("🔄 Consider technique focus or recovery week.")

        # Update the data
        storage.update_max_hold(new_max)
        print(f"\n✅ Max updated! Run create_training_plan() for next week.")

    except ValueError:
        print("Invalid input. Please enter numbers only.")
    except Exception as e:
        print(f"Error updating max hold: {e}")

# Main execution functions
def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1 and sys.argv[1].lower() == "update":
        update_max_after_testing()
    else:
        create_training_plan()

if __name__ == "__main__":
    main()