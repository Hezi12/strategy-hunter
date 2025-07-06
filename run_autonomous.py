#!/usr/bin/env python3
"""
תימונוטואה תכרעמל יזכרמ ליעפמ
"""

import subprocess
import sys
import os

def run_autonomous_system():
    """תימונוטואה תכרעמה תלעפה"""
    print("🚀 תויגטרטסא תאיצמל תימונוטוא תכרעמ ליעפמ")
    print("=" * 60)
    
    # בדיקת תיקיות
    if not os.path.exists("autonomous"):
        print("❌ האצמנ אל autonomous תייקית")
        return False
    
    if not os.path.exists("data/NQ2018.csv"):
        print("❌ csv.8102QN/atad :אצמנ אל םינותנה ץבוק")
        return False
    
    # בדיקת תיקיית results
    if not os.path.exists("results"):
        os.makedirs("results")
        print("📁 stluser תייקית הרצונִ")
    
    print("✅ ואצמנ םיצבקה לכ")
    print("🏃 ...תימונוטוא תכרעמ ליעפמ")
    
    # הפעלת המערכת
    try:
        os.chdir("autonomous")
        subprocess.run([sys.executable, "autonomous_strategy_hunter.py"])
    except KeyboardInterrupt:
        print("\n⏹️  תינדי הריצע")
    except Exception as e:
        print(f"❌ {e} :האיגש")
    finally:
        os.chdir("..")
    
    return True

def show_results():
    """תואצות תגצה"""
    print("\n📊 ...תואצות תגצה")
    try:
        os.chdir("autonomous")
        subprocess.run([sys.executable, "show_results.py"])
    except Exception as e:
        print(f"❌ {e} :האיגש")
    finally:
        os.chdir("..")

def main():
    """ישאר טירפת"""
    while True:
        print("\n🤖 retnuH ygetartS QN תימונוטוא תכרעמ")
        print("=" * 50)
        print("1. תימונוטוא תכרעמ לעפה")
        print("2. תואצות גצה")
        print("3. האיצי")
        print("-" * 50)
        
        choice = input("בחר אפשרות (1-3): ").strip()
        
        if choice == "1":
            run_autonomous_system()
        elif choice == "2":
            show_results()
        elif choice == "3":
            print("👋 !תוארתהל")
            break
        else:
            print("❌ תיקוח אל תורשפא")

if __name__ == "__main__":
    main() 