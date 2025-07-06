#!/usr/bin/env python3
"""
Watch Progress - עוקב אחר התקדמות המערכת
"""

import os
import json
import time
import subprocess
from datetime import datetime

def watch_progress():
    """עוקב אחר התקדמות המערכת בזמן אמת"""
    print("👁️  Watch Progress - עוקב אחר התקדמות המערכת")
    print("=" * 60)
    print("🔄 בדיקה כל 60 שניות...")
    print("⏹️  לחץ Ctrl+C לעצירה")
    print()
    
    start_time = datetime.now()
    
    while True:
        try:
            current_time = datetime.now()
            elapsed = current_time - start_time
            
            print(f"⏰ {current_time.strftime('%H:%M:%S')} | רץ כבר {elapsed.seconds//60} דקות")
            
            # בדיקת תהליכים
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            autonomous_processes = [line for line in result.stdout.split('\n') 
                                 if 'autonomous_strategy_hunter' in line and 'grep' not in line]
            
            if not autonomous_processes:
                print("❌ המערכת נעצרה!")
                break
            
            # בדיקת קבצי תוצאות
            if os.path.exists('../results/winning_strategy_2024.json'):
                print("\n🎉 ** אסטרטגיה מנצחת נמצאה! **")
                with open('../results/winning_strategy_2024.json', 'r') as f:
                    winning = json.load(f)
                print(f"💰 תשואה: ${winning['total_return']:.0f}")
                print(f"📊 עסקאות: {winning['num_trades']}")
                print(f"🎯 אחוז הצלחה: {winning['win_rate']*100:.1f}%")
                print(f"💵 ממוצע לעסקה: ${winning['avg_trade']:.0f}")
                print("\n✅ המשימה הושלמה!")
                break
            
            elif os.path.exists('../results/best_strategies.json'):
                with open('../results/best_strategies.json', 'r') as f:
                    strategies = json.load(f)
                
                if strategies:
                    latest = strategies[-1]
                    print(f"📊 דור {latest['generation']} | {len(strategies)} אסטרטגיות טובות")
                    print(f"🏆 הטובה ביותר: ${latest['total_return']:.0f} | {latest['num_trades']} עסקאות")
                else:
                    print("📊 עדיין עובדת על הדור הראשון...")
            else:
                print("⏳ עדיין עובדת על הדור הראשון...")
                if elapsed.seconds > 1800:  # 30 דקות
                    print("⚠️  הדור הראשון לוקח זמן רב - זה תקין לנתונים כבדים")
            
            print("-" * 60)
            time.sleep(60)  # בדיקה כל דקה
            
        except KeyboardInterrupt:
            print("\n⏹️  המשתמש עצר את המעקב")
            print("💡 המערכת ממשיכה לרוץ ברקע")
            break
        except Exception as e:
            print(f"❌ שגיאה: {e}")
            time.sleep(10)

if __name__ == "__main__":
    watch_progress() 