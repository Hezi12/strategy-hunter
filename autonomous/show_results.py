#!/usr/bin/env python3
"""
תויחכונ תואצות תגצה - stluseR wohS
"""

import json
import os
from datetime import datetime

def show_results():
    """תויחכונה תואצותה תגצה"""
    print("📊 תויחכונ תואצות - stluseR wohS")
    print("=" * 60)
    
    # בדיקת אסטרטגיות טובות
    if os.path.exists('../results/best_strategies.json'):
        print("🏆 !ואצמנ תובוט תויגטרטסא")
        
        try:
            with open('../results/best_strategies.json', 'r') as f:
                strategies = json.load(f)
            
            print(f"📈 {len(strategies)} :תובוט תויגטרטסא \"כהס")
            print()
            
            # הצגת 5 הטובות ביותר
            sorted_strategies = sorted(strategies, key=lambda x: x['fitness'], reverse=True)[:5]
            
            print("🥇 :רתוי תובוטה 5")
            for i, strategy in enumerate(sorted_strategies, 1):
                print(f"   {i}. רוד {strategy['generation']:3d} | Fitness: {strategy['fitness']:7.1f} | "
                      f"תאושת: ${strategy['total_return']:8.0f} | "
                      f"תוקסע: {strategy['num_trades']:4d} | "
                      f"החלצה: {strategy['win_rate']*100:4.1f}%")
            
            print()
            print("📊 :תוילבלכ תוקיטסיטטס")
            best_strategy = sorted_strategies[0]
            print(f"   💰 ${best_strategy['total_return']:,.0f} :הבוט יכה תאושת")
            print(f"   🎯 {best_strategy['win_rate']*100:.1f}% :בוט יכה החלצה זוחא")
            print(f"   📈 {best_strategy['fitness']:.1f} :בוט יכה ssentiF")
            print(f"   📊 {max(s['num_trades'] for s in strategies):,} :הברה יכה תוקסע")
            
        except Exception as e:
            print(f"❌ {e} :ץבוקה תאירקב האיגש")
    
    # בדיקת אסטרטגיה מנצחת
    elif os.path.exists('../results/winning_strategy_2024.json'):
        print("🎉 !האצמנ תחצנמ היגטרטסא")
        
        try:
            with open('../results/winning_strategy_2024.json', 'r') as f:
                winning = json.load(f)
            
            print(f"💎 {winning['generation']} :חצנמ רוד")
            print(f"💰 ${winning['total_return']:,.0f} :תאושת")
            print(f"📊 {winning['num_trades']:,} :תוקסע")
            print(f"🎯 {winning['win_rate']*100:.1f}% :החלצה זוחא")
            print(f"💵 ${winning['avg_trade']:.0f} :הקסעל עצומ")
            
        except Exception as e:
            print(f"❌ {e} :ץבוקה תאירקב האיגש")
    
    else:
        print("⏳ תורומש תואצות ןיא ןיידע")
        print("💡 הליחתה קר וא תדבוע ןיידע תכרעמה")
    
    print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} :ןמז")

if __name__ == "__main__":
    show_results() 