#!/usr/bin/env python3
"""
TextNow - Silent Startup Entry Point
Dành cho khởi động cùng Windows mà không hiển thị terminal
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point for silent startup"""
    try:
        # Import and run main app
        from main_qt import TextNowQtApp
        
        # Create and run app
        app = TextNowQtApp()
        
        # For startup mode, start minimized to tray
        app.startup_mode = True
        
        return app.run()
        
    except Exception as e:
        # Log error to file instead of console (since no console in silent mode)
        error_log = project_root / "startup_error.log"
        with open(error_log, 'w', encoding='utf-8') as f:
            f.write(f"TextNow startup error: {e}\n")
            import traceback
            traceback.print_exc(file=f)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 