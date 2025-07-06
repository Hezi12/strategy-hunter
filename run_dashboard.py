#!/usr/bin/env python3
"""
מפעיל הדשבורד הויזואלי
"""

import subprocess
import sys
import os

def run_dashboard():
    """הפעלת הדשבורד"""
    print("🖥️  מפעיל דשבורד NQ Strategy Hunter")
    print("=" * 50)
    
    # בדיקת תיקיות
    if not os.path.exists("dashboard"):
        print("❌ תיקיית dashboard לא נמצאה")
        return False
    
    if not os.path.exists("data/NQ2018.csv"):
        print("❌ קובץ הנתונים לא נמצא: data/NQ2018.csv")
        return False
    
    print("✅ כל הקבצים נמצאו")
    print("🚀 מפעיל דשבורד...")
    print("📱 הדשבורד ייפתח בדפדפן שלך")
    print("⏹️  לחץ Ctrl+C לעצירה")
    
    # הפעלת הדשבורד
    try:
        os.chdir("dashboard")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py", "--server.port", "8521"])
    except KeyboardInterrupt:
        print("\n⏹️  דשבורד נעצר")
    except Exception as e:
        print(f"❌ שגיאה: {e}")
        print("💡 אולי צריך להתקין streamlit: pip install streamlit")
    finally:
        os.chdir("..")
    
    return True

if __name__ == "__main__":
    run_dashboard() 