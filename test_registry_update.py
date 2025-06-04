#!/usr/bin/env python3
"""
Test script để update registry với startup fixes mới
"""
import sys
import winreg
from pathlib import Path

def test_registry_update():
    """Test việc update registry với fixes mới"""
    print("🔧 Testing registry update với startup fixes...")
    
    try:
        # Simulate the new _enable_startup logic
        if getattr(sys, 'frozen', False):
            # EXE mode
            app_path = f'"{sys.executable}"'
            print(f"📦 EXE mode detected: {app_path}")
        else:
            # Script mode - use pythonw.exe + silent script
            python_exe = sys.executable
            print(f"🐍 Current python: {python_exe}")
            
            # Use pythonw.exe instead of python.exe
            if python_exe.endswith('python.exe'):
                pythonw_exe = python_exe.replace('python.exe', 'pythonw.exe')
                print(f"🔇 Will use pythonw: {pythonw_exe}")
            else:
                pythonw_exe = python_exe
                print(f"🔇 Using current exe: {pythonw_exe}")
            
            # Use silent startup script
            script_path = Path(__file__).parent / "main_qt_silent.py"
            app_path = f'"{pythonw_exe}" "{script_path}"'
            print(f"📄 Silent script: {script_path}")
            print(f"📂 Script exists: {script_path.exists()}")
        
        print(f"\n🔧 New startup command: {app_path}")
        
        # Check current registry value
        print("\n📝 Current registry status:")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Run", 
                               0, winreg.KEY_READ)
            try:
                current_value, _ = winreg.QueryValueEx(key, "TextNow")
                print(f"   Current: {current_value}")
                
                if current_value == app_path:
                    print("   ✅ Registry already updated with new command")
                else:
                    print("   ⚠️ Registry needs update")
                    
            except FileNotFoundError:
                print("   ℹ️ No TextNow entry found")
            winreg.CloseKey(key)
        except Exception as e:
            print(f"   ❌ Registry read error: {e}")
        
        # Ask if user wants to update
        print(f"\n❓ Update registry với command mới?")
        print(f"   Command: {app_path}")
        response = input("   (y/n): ").lower().strip()
        
        if response == 'y':
            print("\n🔧 Updating registry...")
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                   r"Software\Microsoft\Windows\CurrentVersion\Run", 
                                   0, winreg.KEY_WRITE)
                
                winreg.SetValueEx(key, "TextNow", 0, winreg.REG_SZ, app_path)
                winreg.CloseKey(key)
                
                print("✅ Registry updated successfully!")
                print("🔄 Restart Windows để test silent startup")
                
            except Exception as e:
                print(f"❌ Registry update failed: {e}")
        else:
            print("⏭️ Skipped registry update")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function"""
    print("🧪 Registry Update Test")
    print("=" * 50)
    
    test_registry_update()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")

if __name__ == "__main__":
    main() 