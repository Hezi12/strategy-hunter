#!/usr/bin/env python3
"""
NQ Strategy Hunter - Website Launcher
מפעיל אתר לניהול המערכת
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_requirements():
    """בדיקת התקנת חבילות"""
    print("🔍 בודק התקנת חבילות...")
    
    required_packages = [
        'flask',
        'pandas',
        'numpy',
        'plotly'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - חסר")
    
    if missing_packages:
        print(f"\n🚨 חסרות החבילות הבאות: {', '.join(missing_packages)}")
        print("📦 התקנת חבילות חסרות...")
        
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages, check=True)
            print("✅ כל החבילות הותקנו בהצלחה!")
        except subprocess.CalledProcessError:
            print("❌ שגיאה בהתקנת חבילות")
            return False
    
    return True

def start_website():
    """הפעלת האתר"""
    print("\n🚀 מפעיל אתר...")
    
    # מעבר לתיקיית web
    web_dir = os.path.join(os.path.dirname(__file__), 'web')
    if not os.path.exists(web_dir):
        print("❌ תיקיית web לא נמצאה")
        return False
    
    os.chdir(web_dir)
    
    # הפעלת השרת
    print("🌐 האתר זמין בכתובת: http://localhost:5001")
    print("🔄 לעצירה: Ctrl+C")
    print("-" * 50)
    
    # פתיחת הדפדפן
    time.sleep(2)
    webbrowser.open('http://localhost:5001')
    
    # הפעלת השרת
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 האתר נעצר")
    except subprocess.CalledProcessError as e:
        print(f"❌ שגיאה בהפעלת השרת: {e}")
        return False
    
    return True

def main():
    """פונקציה ראשית"""
    print("🌐 מפעיל אתר NQ Strategy Hunter")
    print("=" * 50)
    
    # בדיקת חבילות
    if not check_requirements():
        return
    
    # הפעלת האתר
    start_website()

if __name__ == "__main__":
    main() 