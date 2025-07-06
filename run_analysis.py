#!/usr/bin/env python3
"""
מפעיל סקריפט להפעלת ניתוח נתונים
"""

import subprocess
import sys
import os

def run_analysis():
    """הפעלת ניתוח נתונים"""
    print("📊 מפעיל ניתוח נתוני NQ")
    print("=" * 50)
    
    # בדיקת תיקיות
    if not os.path.exists("analysis"):
        print("❌ תיקיית analysis לא נמצאה")
        return False
    
    if not os.path.exists("data/NQ2018.csv"):
        print("❌ קובץ הנתונים לא נמצא: data/NQ2018.csv")
        return False
    
    # בדיקת תיקיית results
    if not os.path.exists("results"):
        os.makedirs("results")
        print("📁 נוצרה תיקיית results")
    
    print("✅ כל הקבצים נמצאו")
    print("🔍 מתחיל ניתוח...")
    
    # הפעלת הניתוח
    try:
        os.chdir("analysis")
        subprocess.run([sys.executable, "main_analysis.py"])
    except Exception as e:
        print(f"❌ שגיאה: {e}")
    finally:
        os.chdir("..")
    
    return True

def run_demo():
    """הפעלת דמו מהיר"""
    print("🎪 מפעיל דמו מהיר")
    print("=" * 50)
    
    try:
        os.chdir("analysis")
        subprocess.run([sys.executable, "quick_demo.py"])
    except Exception as e:
        print(f"❌ שגיאה: {e}")
    finally:
        os.chdir("..")

def main():
    """תפריט ראשי"""
    while True:
        print("\n📊 מערכת ניתוח נתוני NQ")
        print("=" * 40)
        print("1. ניתוח מלא")
        print("2. דמו מהיר")
        print("3. יציאה")
        print("-" * 40)
        
        choice = input("בחר אפשרות (1-3): ").strip()
        
        if choice == "1":
            run_analysis()
        elif choice == "2":
            run_demo()
        elif choice == "3":
            print("👋 להתראות!")
            break
        else:
            print("❌ אפשרות לא חוקית")

if __name__ == "__main__":
    main() 