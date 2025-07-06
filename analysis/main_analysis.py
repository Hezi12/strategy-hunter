"""
Main Analysis Script
סקריפט ראשי למערכת הניתוח המלאה
"""

from nq_analyzer import NQAnalyzer
from strategy_engine import StrategyEngine
import pandas as pd
import numpy as np
from datetime import datetime
import json

def main():
    """
    הפעלת המערכת המלאה
    """
    print("🚀 מתחיל מערכת הניתוח המלאה של NQ!")
    print("=" * 60)
    
    # שלב 1: ניתוח בסיסי
    print("\n📊 שלב 1: ניתוח בסיסי")
    print("-" * 30)
    
    analyzer = NQAnalyzer()
    basic_report = analyzer.run_full_analysis()
    
    # שלב 2: ניתוח אסטרטגיות מתקדם
    print("\n🤖 שלב 2: ניתוח אסטרטגיות מתקדם")
    print("-" * 30)
    
    engine = StrategyEngine(analyzer)
    strategy_comparison = engine.run_full_strategy_analysis()
    
    # שלב 3: דוח מסכם
    print("\n📋 שלב 3: דוח מסכם")
    print("-" * 30)
    
    final_report = {
        'timestamp': datetime.now().isoformat(),
        'basic_analysis': basic_report,
        'strategy_analysis': strategy_comparison,
        'best_strategy': strategy_comparison[0] if strategy_comparison else None,
        'recommendations': generate_final_recommendations(basic_report, strategy_comparison)
    }
    
    # שמירת דוח
    with open('nq_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(final_report, f, ensure_ascii=False, indent=2, default=str)
    
    print("\n🎉 המערכת הושלמה!")
    print("📄 דוח מלא נשמר בקובץ: nq_analysis_report.json")
    
    # הצגת סיכום
    print("\n🏆 סיכום התוצאות:")
    if strategy_comparison:
        best = strategy_comparison[0]
        print(f"  🥇 האסטרטגיה הטובה ביותר: {best['strategy']}")
        print(f"  💰 תשואה: {best['total_return']:.2%}")
        print(f"  ✅ אחוז הצלחה: {best['win_rate']:.2%}")
        print(f"  📊 יחס רווח: {best['profit_factor']:.2f}")
    
    print("\n💡 המלצות עיקריות:")
    for rec in final_report['recommendations']:
        print(f"  • {rec}")
    
    return final_report

def generate_final_recommendations(basic_report, strategy_comparison):
    """
    יצירת המלצות סופיות
    """
    recommendations = []
    
    # המלצות מהניתוח הבסיסי
    if basic_report and 'המלצות' in basic_report:
        recommendations.extend(basic_report['המלצות'])
    
    # המלצות מהאסטרטגיות
    if strategy_comparison:
        best_strategy = strategy_comparison[0]
        
        if best_strategy['total_return'] > 0.1:
            recommendations.append(f"האסטרטגיה {best_strategy['strategy']} מציגה תשואה מצוינת של {best_strategy['total_return']:.2%}")
        
        if best_strategy['win_rate'] > 0.6:
            recommendations.append(f"אחוז הצלחה גבוה של {best_strategy['win_rate']:.2%} מעיד על יציבות האסטרטגיה")
        
        if best_strategy['profit_factor'] > 1.5:
            recommendations.append(f"יחס רווח של {best_strategy['profit_factor']:.2f} מעיד על פוטנציאל רווחיות גבוה")
        
        # המלצות כלליות
        if len(strategy_comparison) > 1:
            top_3 = strategy_comparison[:3]
            recommendations.append(f"מומלץ לשקול שילוב של {len(top_3)} האסטרטגיות המובילות")
    
    # המלצות נוספות
    recommendations.extend([
        "מומלץ לבדוק את האסטרטגיות במספר תקופות זמן שונות",
        "כדאי להגדיר stop-loss מתאים לניהול סיכונים",
        "מומלץ לעקוב אחר הנפחים הגבוהים בשעות 8-10 בבוקר",
        "כדאי לבדוק את האסטרטגיות עם נתונים נוספים מתקופות שונות"
    ])
    
    return recommendations

if __name__ == "__main__":
    # הפעלת המערכת
    try:
        report = main()
        print("\n✅ המערכת הושלמה בהצלחה!")
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        import traceback
        traceback.print_exc() 