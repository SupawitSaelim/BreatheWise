# test_module.py
import sys
import os

# Add the breath_hold_training to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test imports
try:
    from breath_hold_training.cli.interface import create_training_plan, update_max_after_testing
    print("✅ All imports successful!")
    
    # Run the main function
    if len(sys.argv) > 1 and sys.argv[1].lower() == "update":
        update_max_after_testing()
    else:
        create_training_plan()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all required packages are installed:")
    print("pip install fpdf2")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()