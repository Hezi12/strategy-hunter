#!/usr/bin/env python3
"""
Wait for Generation 10 - מחכה לדור 10
"""

import json
import os
import time
import subprocess
from datetime import datetime

def wait_for_gen10():
    """מחכה לדור 10 ומראה מתי המערכת מתחילה לשמור תוצאות"""
    print("⏳ Wait for Generation 10 - מחכה לדור 10")
    print("=" * 60)
    print("🎯 המערכת תתחיל לשמור תוצאות בדור 10")
    print("⏰ בדיקה כל 30 שניות...")
    print()
    
    start_time = datetime.now()
    
    while True:
        try:
            current_time = datetime.now()
            elapsed = current_time - start_time
            
            print(f"⏰ {current_time.strftime('%H:%M:%S')} | מחכה כבר {elapsed.seconds//60} דקות")
            
            # בדיקת אסטרטגיות שמורות
            if os.path.exists('../results/best_strategies.json'):
                with open('../results/best_strategies.json', 'r') as f:
                    strategies = json.load(f)
                
                if strategies:
                    latest = strategies[-1]
                    print(f"🎉 יש תוצאות! דור {latest['generation']}")
                    print(f"💰 תשואה: ${latest['total_return']:.0f}")
                    print(f"📊 עסקאות: {latest['num_trades']}")
                    print(f"🎯 אחוז הצלחה: {latest['win_rate']*100:.1f}%")
                    print(f"📈 Fitness: {latest['fitness']:.1f}")
                    print(f"📁 נשמרו {len(strategies)} אסטרטגיות")
                    print("\n✅ המערכת עובדת! עכשיו אתה יכול לעקוב אחר התקדמות")
                    print("💡 הפעל: python3 show_results.py")
                    break
            
            # בדיקת אסטרטגיה מנצחת
            if os.path.exists('../results/winning_strategy_2024.json'):
                print("\n🎉 אסטרטגיה מנצחת נמצאה!")
                break
            
            # בדיקת תהליך
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            autonomous_processes = [line for line in result.stdout.split('\n') 
                                 if 'autonomous_strategy_hunter' in line and 'grep' not in line]
            
            if not autonomous_processes:
                print("❌ המערכת נעצרה!")
                break
            
            # הצגת מידע על התהליך
            for proc in autonomous_processes:
                parts = proc.split()
                if len(parts) >= 10:
                    cpu_usage = parts[2]
                    time_running = parts[9]
                    print(f"🖥️  CPU: {cpu_usage}% | זמן: {time_running}")
            
            print("⏳ עדיין מחכה לדור 10...")
            print("-" * 40)
            
            time.sleep(30)  # בדיקה כל 30 שניות
            
        except KeyboardInterrupt:
            print("\n⏹️  המשתמש עצר את המעקב")
            print("💡 המערכת ממשיכה לרוץ ברקע")
            break
        except Exception as e:
            print(f"❌ שגיאה: {e}")
            time.sleep(10)

if __name__ == "__main__":
    wait_for_gen10() 