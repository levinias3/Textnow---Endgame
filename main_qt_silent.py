#!/usr/bin/env python3
"""
TextNow - Silent Startup Entry Point v2.0.1
Dành cho khởi động cùng Windows mà không hiển thị terminal
EXE optimized version
"""
import sys
import os
from pathlib import Path

# ✅ EXE-optimized path handling
def get_data_path(relative_path):
    """Get absolute path for user data files (always in app directory)"""
    # For user data, always use the directory where exe/script is located
    if getattr(sys, 'frozen', False):
        # Running as exe
        app_dir = Path(sys.executable).parent
    else:
        # Running as script
        app_dir = Path(__file__).parent
    
    return app_dir / relative_path

# Setup paths
project_root = get_data_path("")
sys.path.insert(0, str(project_root))

# Add resource path for bundled resources in exe mode
if hasattr(sys, '_MEIPASS'):
    sys.path.insert(0, sys._MEIPASS)

def main():
    """Main entry point for silent startup - EXE optimized"""
    is_exe_mode = getattr(sys, 'frozen', False)
    
    try:
        # Import and run main app
        from main_qt import TextNowQtApp
        
        # Create and run app
        app = TextNowQtApp()
        
        # For startup mode, start minimized to tray
        app.startup_mode = True
        
        return app.run()
        
    except Exception as e:
        # Log error appropriately based on mode
        if is_exe_mode:
            # In exe mode, log to file since no console
            try:
                error_log = get_data_path("startup_error.log")
                with open(error_log, 'w', encoding='utf-8') as f:
                    f.write(f"TextNow startup error: {e}\n")
                    import traceback
                    traceback.print_exc(file=f)
            except:
                pass  # If can't write log, silently fail
        else:
            # In script mode, print to console
            print(f"❌ TextNow startup error: {e}")
            import traceback
            traceback.print_exc()
        
        return 1

if __name__ == "__main__":
    sys.exit(main()) 