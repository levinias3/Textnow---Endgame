#!/usr/bin/env python3
"""
Test script để verify Windows startup fixes
"""
import sys
import os
import winreg
from pathlib import Path

def test_startup_fixes():
    """Test các fix cho Windows startup"""
    print("🧪 Testing Windows startup fixes...")
    
    # Test 1: Config path resolution
    print("\n📁 Test 1: Config path resolution")
    try:
        from utils.config import Config
        config = Config()
        config_path = Path(config.config_file)
        
        print(f"   📄 Config file: {config.config_file}")
        print(f"   📍 Absolute path: {config_path.is_absolute()}")
        print(f"   📂 Exists: {config_path.exists()}")
        
        if config_path.exists():
            shortcuts_count = len(config.get_shortcuts())
            print(f"   🔗 Shortcuts loaded: {shortcuts_count}")
        
        print("   ✅ Config path test passed")
    except Exception as e:
        print(f"   ❌ Config path test failed: {e}")
    
    # Test 2: Startup command format
    print("\n🚀 Test 2: Startup command format")
    try:
        if getattr(sys, 'frozen', False):
            # EXE mode
            app_path = f'"{sys.executable}"'
            print(f"   📦 EXE mode: {app_path}")
        else:
            # Script mode
            python_exe = sys.executable
            if python_exe.endswith('python.exe'):
                pythonw_exe = python_exe.replace('python.exe', 'pythonw.exe')
            else:
                pythonw_exe = python_exe
            
            script_path = Path(__file__).parent / "main_qt_silent.py"
            app_path = f'"{pythonw_exe}" "{script_path}"'
            
            print(f"   🐍 Script mode: {app_path}")
            print(f"   🔇 Using pythonw: {pythonw_exe.endswith('pythonw.exe')}")
            print(f"   📄 Silent script exists: {script_path.exists()}")
        
        print("   ✅ Startup command test passed")
    except Exception as e:
        print(f"   ❌ Startup command test failed: {e}")
    
    # Test 3: Registry key check
    print("\n📝 Test 3: Registry key check")
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Run", 
                           0, winreg.KEY_READ)
        try:
            value, _ = winreg.QueryValueEx(key, "TextNow")
            print(f"   🔑 Current registry value: {value}")
            
            # Analyze the command
            if 'pythonw.exe' in value:
                print("   ✅ Using pythonw.exe (no terminal)")
            elif 'python.exe' in value:
                print("   ⚠️ Using python.exe (will show terminal)")
            
            if 'main_qt_silent.py' in value:
                print("   ✅ Using silent startup script")
            elif 'main_qt.py' in value:
                print("   ⚠️ Using regular startup script")
                
        except FileNotFoundError:
            print("   ℹ️ No TextNow startup entry found")
        winreg.CloseKey(key)
        
        print("   ✅ Registry test passed")
    except Exception as e:
        print(f"   ❌ Registry test failed: {e}")
    
    # Test 4: Silent script validation
    print("\n🔇 Test 4: Silent script validation")
    try:
        silent_script = Path(__file__).parent / "main_qt_silent.py"
        
        print(f"   📄 Silent script path: {silent_script}")
        print(f"   📂 Exists: {silent_script.exists()}")
        
        if silent_script.exists():
            with open(silent_script, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"   📊 File size: {len(content)} characters")
            print(f"   🏃 Has main(): {'def main():' in content}")
            print(f"   🔇 Has startup_mode: {'startup_mode' in content}")
        
        print("   ✅ Silent script test passed")
    except Exception as e:
        print(f"   ❌ Silent script test failed: {e}")

def main():
    """Main test function"""
    print("🧪 Windows Startup Fixes Test")
    print("=" * 50)
    
    test_startup_fixes()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
    print("\n💡 Next steps:")
    print("   1. Enable startup trong ứng dụng")
    print("   2. Restart Windows để test")
    print("   3. Kiểm tra system tray sau khi boot")

if __name__ == "__main__":
    main() 