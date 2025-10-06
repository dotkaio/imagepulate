#!/usr/bin/env python3
"""Test script to verify the import structure is correct."""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import_structure():
    """Test that the import structure is correct."""
    print("Testing import structure...")
    
    # Test 1: Check that modules.utils points to the directory, not the file
    try:
        import modules.utils as utils_module
        utils_path = utils_module.__file__
        print(f"✓ modules.utils imports from: {utils_path}")
        
        if "modules/utils/__init__.py" in utils_path:
            print("✓ Correctly imports from modules/utils/ directory")
        else:
            print("✗ ERROR: Imports from wrong location")
            return False
    except ImportError as e:
        # Expected if dependencies aren't installed
        print(f"⚠ Import failed (expected if dependencies not installed): {e}")
        
        # Get the traceback to see the actual import path
        import traceback
        tb_str = traceback.format_exc()
        print("\nTraceback analysis:")
        print(tb_str)
        
        # Check if it's trying to import from the right place
        if "modules/utils/__init__.py" in tb_str or "modules/utils/file_utils.py" in tb_str:
            print("\n✓ Import path is correct (modules/utils/ directory)")
        else:
            print("\n✗ Import path seems incorrect")
            return False
    
    # Test 2: Verify old modules/utils.py is gone
    old_utils_path = os.path.join(os.path.dirname(__file__), "modules", "utils.py")
    if os.path.exists(old_utils_path):
        print(f"✗ ERROR: Old modules/utils.py still exists at {old_utils_path}")
        return False
    else:
        print("✓ Old modules/utils.py has been removed")
    
    # Test 3: Verify new modules/utils/ directory exists
    new_utils_dir = os.path.join(os.path.dirname(__file__), "modules", "utils")
    if os.path.isdir(new_utils_dir):
        print(f"✓ New modules/utils/ directory exists at {new_utils_dir}")
    else:
        print(f"✗ ERROR: New modules/utils/ directory not found")
        return False
    
    # Test 4: Check that required files exist
    required_files = [
        "modules/utils/__init__.py",
        "modules/utils/file_utils.py",
        "modules/utils/config_manager.py"
    ]
    
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ ERROR: {file_path} not found")
            return False
    
    print("\n" + "="*60)
    print("✓ ALL IMPORT STRUCTURE TESTS PASSED!")
    print("="*60)
    print("\nThe import error you experienced should be fixed.")
    print("Note: You may still see errors about missing dependencies")
    print("      (PIL, yaml, etc.) until you install requirements.")
    return True

if __name__ == "__main__":
    success = test_import_structure()
    sys.exit(0 if success else 1)
