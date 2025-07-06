"""
Quick Demo - דמו מהיר למערכת NQ
בדיקה פשוטה שמראה איך המערכת עובדת
"""

from nq_analyzer import NQAnalyzer
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def quick_analysis():
    """
    ניתוח מהיר - מקבל תוצאות תוך דקות ספורות
    """
    print("🚀 דמו מהיר למערכת NQ")
    print("=" * 50)
    
    # טעינת נתונים
    print("\n📊 טוען מדגם נתונים...")
    analyzer = NQAnalyzer()
    
    if not analyzer.load_data():
        print("❌ לא ניתן לטעון נתונים")
        return
    
    # עבודה עם מדגם קטן יותר לבדיקה מהירה
    print("📊 עובד עם מדגם נתונים מהשבוע האחרון...")
    
    # לקיחת השבוע האחרון בלבד
    recent_data = analyzer.df.tail(7 * 24 * 60)  # 7 ימים x 24 שעות x 60 דקות
    analyzer.df = recent_data
    
    print(f"✅ עובד עם {len(recent_data):,} נקודות נתונים")
    print(f"📅 תקופה: {recent_data.index.min()} עד {recent_data.index.max()}")
    
    # ניתוח בסיסי מהיר
    print("\n🔍 מבצע ניתוח מהיר...")
    
    # סטטיסטיקות בסיסיות
    basic_stats = {
        'מחיר_ממוצע': recent_data['close'].mean(),
        'מחיר_מקסימלי': recent_data['high'].max(),
        'מחיר_מינימלי': recent_data['low'].min(),
        'נפח_ממוצע': recent_data['volume'].mean(),
        'תנודתיות': recent_data['close'].pct_change().std()
    }
    
    print("\n📈 סטטיסטיקות השבוע האחרון:")
    for key, value in basic_stats.items():
        print(f"  {key}: {value:.2f}")
    
    # חישוב אינדיקטורים מהיר
    print("\n📊 מחשב אינדיקטורים...")
    
    # RSI פשוט
    delta = recent_data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Moving averages
    sma_20 = recent_data['close'].rolling(window=20).mean()
    sma_50 = recent_data['close'].rolling(window=50).mean()
    
    # אותות פשוטים
    current_price = recent_data['close'].iloc[-1]
    current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
    current_sma20 = sma_20.iloc[-1] if not pd.isna(sma_20.iloc[-1]) else current_price
    current_sma50 = sma_50.iloc[-1] if not pd.isna(sma_50.iloc[-1]) else current_price
    
    print(f"  מחיר נוכחי: ${current_price:.2f}")
    print(f"  RSI נוכחי: {current_rsi:.1f}")
    print(f"  SMA 20: ${current_sma20:.2f}")
    print(f"  SMA 50: ${current_sma50:.2f}")
    
    # אותות מסחר פשוטים
    print("\n🎯 אותות מסחר:")
    
    signals = []
    
    if current_rsi < 30:
        signals.append("🟢 RSI מצביע על יתר-מכירה - רמז לקנייה")
    elif current_rsi > 70:
        signals.append("🔴 RSI מצביע על יתר-קנייה - רמז למכירה")
    else:
        signals.append("🟡 RSI באזור נייטרלי")
    
    if current_sma20 > current_sma50:
        signals.append("🟢 ממוצע קצר מעל ארוך - מגמה חיובית")
    else:
        signals.append("🔴 ממוצע קצר מתחת לארוך - מגמה שלילית")
    
    # בדיקת נפח
    recent_volume = recent_data['volume'].tail(60).mean()  # שעה אחרונה
    avg_volume = recent_data['volume'].mean()
    
    if recent_volume > avg_volume * 1.5:
        signals.append("🟢 נפח גבוה - פעילות מוגברת")
    else:
        signals.append("🟡 נפח רגיל")
    
    for signal in signals:
        print(f"  {signal}")
    
    # ניתוח שעות
    print("\n🕐 ניתוח שעות פעילות:")
    hourly_volume = recent_data.groupby(recent_data.index.hour)['volume'].mean().sort_values(ascending=False)
    
    print("  שעות עם הנפח הגבוה ביותר:")
    for hour in hourly_volume.head(3).index:
        volume = hourly_volume[hour]
        print(f"    שעה {hour}:00 - נפח ממוצע: {volume:.0f}")
    
    # המלצות פשוטות
    print("\n💡 המלצות מהירות:")
    
    recommendations = [
        "מסחר בשעות עם נפח גבוה (רשימה למעלה)",
        "שימוש ב-RSI לזיהוי נקודות כניסה",
        "מעקב אחר כיוון הממוצעים הנעים",
        "שימוש ב-stop loss של 1-2% מהפוזיציה"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    # סיכום
    print(f"\n✅ הדמו הושלם בהצלחה!")
    print(f"📊 המערכת מוכנה לניתוח מתקדם יותר")
    
    return {
        'basic_stats': basic_stats,
        'current_price': current_price,
        'current_rsi': current_rsi,
        'signals': signals,
        'top_hours': hourly_volume.head(3).to_dict(),
        'recommendations': recommendations
    }

def show_available_features():
    """
    הצגת כל הפיצ'רים הזמינים
    """
    print("\n🎛️ פיצ'רים זמינים במערכת:")
    print("=" * 50)
    
    features = [
        ("nq_analyzer.py", "ניתוח בסיסי מלא + אינדיקטורים טכניים"),
        ("strategy_engine.py", "מודלי Machine Learning + Backtesting"),
        ("report_generator.py", "דוחות מפורטים + גרפים"),
        ("dashboard.py", "ממשק ויזואלי (Streamlit)"),
        ("quick_demo.py", "דמו מהיר (הקובץ הזה)")
    ]
    
    for file, description in features:
        print(f"📄 {file}")
        print(f"   └─ {description}")
    
    print(f"\n🚀 איך להריץ:")
    print(f"   python3 quick_demo.py          - דמו מהיר")
    print(f"   python3 nq_analyzer.py         - ניתוח מלא")
    print(f"   python3 report_generator.py    - דוח + גרפים")
    print(f"   python3 -m streamlit run dashboard.py - ממשק גרפי")

if __name__ == "__main__":
    print("🎯 בחר אפשרות:")
    print("1. דמו מהיר (מומלץ להתחלה)")
    print("2. הצגת כל הפיצ'רים")
    
    try:
        choice = input("\nהזן 1 או 2: ").strip()
        
        if choice == "1":
            results = quick_analysis()
        elif choice == "2":
            show_available_features()
        else:
            print("🚀 מריץ דמו מהיר כברירת מחדל...")
            results = quick_analysis()
            
    except KeyboardInterrupt:
        print("\n\n👋 יציאה מהתוכנית")
    except Exception as e:
        print(f"\n❌ שגיאה: {e}")
        print("🔄 מנסה לרוץ דמו מהיר בכל זאת...")
        try:
            results = quick_analysis()
        except:
            print("❌ לא ניתן להריץ את הדמו. בדוק את קובץ הנתונים.") 