"""
Monitor Progress
כלי ניטור התקדמות המערכת האוטונומית
"""

import json
import os
import time
from datetime import datetime

def monitor_progress():
    """ניטור התקדמות המערכת"""
    print("📊 Monitor Progress - ניטור התקדמות המערכת האוטונומית")
    print("=" * 60)
    
    while True:
        try:
            # בדיקת קובץ אסטרטגיות טובות
            if os.path.exists('../results/best_strategies.json'):
                with open('../results/best_strategies.json', 'r') as f:
                    best_strategies = json.load(f)
                
                if best_strategies:
                    latest = best_strategies[-1]
                    print(f"\n🏆 אסטרטגיה טובה אחרונה:")
                    print(f"   📅 זמן: {latest['timestamp']}")
                    print(f"   🔄 דור: {latest['generation']}")
                    print(f"   💰 תשואה: ${latest['total_return']:.0f}")
                    print(f"   📊 עסקאות: {latest['num_trades']}")
                    print(f"   🎯 אחוז הצלחה: {latest['win_rate']*100:.1f}%")
                    print(f"   📈 Fitness: {latest['fitness']:.1f}")
                    print(f"   🗃️  סה\"כ אסטרטגיות טובות: {len(best_strategies)}")
                else:
                    print("\n⏳ עדיין לא נמצאו אסטרטגיות טובות...")
            else:
                print("\n⏳ המערכת עדיין מתחילה...")
            
            # בדיקת אסטרטגיה מנצחת
            if os.path.exists('../results/winning_strategy_2024.json'):
                print(f"\n🎉 נמצאה אסטרטגיה מנצחת!")
                with open('../results/winning_strategy_2024.json', 'r') as f:
                    winning = json.load(f)
                
                print(f"   💎 זמן מציאה: {winning['timestamp']}")
                print(f"   🔄 דור: {winning['generation']}")
                print(f"   📊 עסקאות: {winning['num_trades']}")
                print(f"   💰 תשואה: ${winning['total_return']:.0f}")
                print(f"   🎯 אחוז הצלחה: {winning['win_rate']*100:.1f}%")
                print(f"   💵 ממוצע לעסקה: ${winning['avg_trade']:.0f}")
                
                print(f"\n✅ המשימה הושלמה! האסטרטגיה המנצחת נשמרה.")
                break
            
            print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - המערכת ממשיכה לחפש...")
            print("🔄 לחץ Ctrl+C לעצירה")
            print("-" * 40)
            
            time.sleep(30)  # בדיקה כל 30 שניות
            
        except KeyboardInterrupt:
            print(f"\n⏹️  ניטור הופסק על ידי המשתמש")
            break
        except Exception as e:
            print(f"❌ שגיאה: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_progress() 