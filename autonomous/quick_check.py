#!/usr/bin/env python3
"""
Quick Check - בדיקה מהירה למצב המערכת
"""

import os
import json
import subprocess
from datetime import datetime

def quick_check():
    """בדיקה מהירה של המערכת"""
    print("🔍 בדיקה מהירה של המערכת האוטונומית")
    print("=" * 50)
    
    # בדיקת תהליכים
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        autonomous_processes = [line for line in lines if 'autonomous_strategy_hunter' in line and 'grep' not in line]
        
        if autonomous_processes:
            print("✅ המערכת רצה!")
            for proc in autonomous_processes:
                parts = proc.split()
                if len(parts) >= 3:
                    cpu_usage = parts[2]
                    print(f"   🖥️  שימוש CPU: {cpu_usage}%")
            
            # בדיקת קבצים
            if os.path.exists('../results/best_strategies.json'):
                with open('../results/best_strategies.json', 'r') as f:
                    strategies = json.load(f)
                print(f"   📊 נמצאו {len(strategies)} אסטרטגיות טובות")
                
                if strategies:
                    latest = strategies[-1]
                    print(f"   🏆 דור אחרון: {latest['generation']}")
                    print(f"   💰 תשואה: ${latest['total_return']:.0f}")
            else:
                print("   ⏳ עדיין מעבדת את הדור הראשון...")
            
            if os.path.exists('../results/winning_strategy_2024.json'):
                print("   🎉 נמצאה אסטרטגיה מנצחת!")
            else:
                print("   🔄 עדיין מחפשת אסטרטגיה מנצחת...")
        else:
            print("❌ המערכת לא רצה")
            print("   💡 הפעל: python3 autonomous_strategy_hunter.py &")
    
    except Exception as e:
        print(f"❌ שגיאה: {e}")
    
    print(f"\n⏰ זמן: {datetime.now().strftime('%H:%M:%S')}")
    print("🔄 הפעל שוב כדי לבדוק עדכונים")

if __name__ == "__main__":
    quick_check() 