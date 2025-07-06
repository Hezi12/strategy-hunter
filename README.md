# 🤖 NQ Trading Strategy Hunter

פרויקט מתקדם למציאת אסטרטגיות מסחר מנצחות עבור NQ (Nasdaq Futures) באמצעות אלגוריתמים גנטיים ובינה מלאכותית.

## 📁 מבנה הפרויקט

```
📦 NQ Trading Project
├── 🤖 autonomous/           # מערכת אוטונומית - הרץ ללא תלות ב-AI
├── 🎯 strategies/           # מנועי חיפוש אסטרטגיות מתקדמים
├── 📊 analysis/             # כלי ניתוח נתונים ודוחות
├── 💾 data/                 # נתוני שוק וקבצי CSV
├── 📈 results/              # תוצאות, גרפים ואסטרטגיות שנמצאו
├── 🖥️  dashboard/            # ממשק משתמש ויזואלי
├── 📚 docs/                 # תיעוד והוראות הפעלה
└── 📋 README.md             # קובץ זה
```

## 🚀 התחלה מהירה

### 🎯 הפעלה מהירה עם סקריפטים מוכנים:
```bash
# המערכת האוטונומית (מומלץ!)
python3 run_autonomous.py

# ממשק ויזואלי
python3 run_dashboard.py

# ניתוח נתונים
python3 run_analysis.py
```

### 💻 הפעלה ידנית לפי תיקיות:

#### 1. המערכת האוטונומית:
```bash
cd autonomous
python3 autonomous_strategy_hunter.py  # רץ ברקע
python3 show_results.py                # הצגת תוצאות
python3 watch_progress.py              # מעקב בזמן אמת
```

#### 2. מנועי חיפוש אסטרטגיות:
```bash
cd strategies
python3 winning_strategy_finder_2024.py        # חיפוש מהיר
python3 ultimate_strategy_builder_2024.py      # חיפוש מתקדם
python3 genetic_strategy_optimizer_2024.py     # אלגוריתם גנטי
```

#### 3. ניתוח נתונים:
```bash
cd analysis
python3 main_analysis.py               # ניתוח בסיסי
python3 quick_demo.py                  # דמו מהיר
```

#### 4. דשבורד ויזואלי:
```bash
cd dashboard
streamlit run dashboard.py --server.port 8521
```

## 🎯 המערכת האוטונומית - הפיצ'ר הכי חשוב!

המערכת האוטונומית היא הפיצ'ר המתקדם ביותר בפרויקט:

### ✨ יתרונות:
- 🔄 **רצה לבד** - ללא תלות בשירותי AI
- 💻 **מקומי** - לא צריך אינטרנט
- 💰 **חינמי** - ללא עלויות
- 🎯 **מדויק** - בודק כל קריטריון בקפידה
- ⚡ **מהיר** - מנצל את כל כוח המחשב

### 🎪 איך להפעיל:
```bash
# דרך הקלה ביותר
python3 run_autonomous.py

# או באופן ידני
cd autonomous
python3 autonomous_strategy_hunter.py &    # רץ ברקע
python3 show_results.py                    # בדיקת תוצאות
```

## 📊 קריטריונים למציאת אסטרטגיה מנצחת

המערכת מחפשת אסטרטגיות שעומדות בכל הקריטריונים הבאים:

- ✅ **לפחות 200 עסקאות בשנה**
- ✅ **Drawdown מקסימלי: $10,000**
- ✅ **רווח ממוצע לעסקה: $30**
- ✅ **Profit Factor ≥ 1.7**
- ✅ **Sharpe Ratio ≥ 1.5**
- ✅ **יחס רווח/הפסד ≥ 1.5**
- ✅ **אחוז הצלחה ≥ 50%**
- ✅ **רצף הפסדים מקסימלי: 6**
- ✅ **רווח כולל חיובי**

## 🗂️ פירוט התיקיות

### 🤖 autonomous/
המערכת האוטונומית שרצה ללא תלות ב-AI:
- `autonomous_strategy_hunter.py` - המנוע הראשי
- `show_results.py` - הצגת תוצאות
- `watch_progress.py` - מעקב בזמן אמת
- `quick_check.py` - בדיקה מהירה
- `wait_for_gen10.py` - המתנה לתוצאות ראשונות
- `monitor_progress.py` - ניטור התקדמות

### 🎯 strategies/
מנועי חיפוש אסטרטגיות מתקדמים:
- `winning_strategy_finder_2024.py` - 6 אסטרטגיות פשוטות
- `ultimate_strategy_builder_2024.py` - אסטרטגיות עם 6+ שכבות
- `smart_strategy_finder_2024.py` - 4 אסטרטגיות חכמות
- `advanced_strategy_hunter_2024.py` - 5 אסטרטגיות מתקדמות
- `genetic_strategy_optimizer_2024.py` - אלגוריתם גנטי
- `strategy_engine.py` - מנוע האסטרטגיות

### 📊 analysis/
כלי ניתוח נתונים ודוחות:
- `main_analysis.py` - ניתוח בסיסי של נתוני NQ
- `nq_analyzer.py` - כלי ניתוח מתקדם
- `report_generator.py` - יצירת דוחות מפורטים
- `strategy_2023_tester.py` - בדיקת אסטרטגיות היסטוריות
- `quick_demo.py` - דמו מהיר של המערכת

### 💾 data/
נתוני שוק וקבצי CSV:
- `NQ2018.csv` - נתוני NQ מ-2018 עד 2024
- `strategy_2023_*.csv` - תוצאות אסטרטגיות מ-2023

### 📈 results/
תוצאות, גרפים ואסטרטגיות:
- `best_strategies.json` - האסטרטגיות הטובות ביותר
- `winning_strategy_2024.json` - אסטרטגיה מנצחת (אם נמצאה)
- `nq_full_report.json` - דוח מלא על הנתונים
- `*.png` - גרפים וויזואליזציות

### 🖥️ dashboard/
ממשק משתמש ויזואלי:
- `dashboard.py` - דשבורד Streamlit אינטראקטיבי

### 📚 docs/
תיעוד והוראות:
- `INSTRUCTIONS.md` - הוראות מפורטות למערכת האוטונומית

## 🎯 המלצות שימוש

### ⚡ הפעלה מהירה - סקריפטים מוכנים:
```bash
# חיפוש מהיר של אסטרטגיה
python3 run_autonomous.py

# ממשק ויזואלי מתקדם
python3 run_dashboard.py

# ניתוח נתונים מפורט
python3 run_analysis.py
```

### 🛠️ הפעלה ידנית מתקדמת:

#### לחיפוש מהיר של אסטרטגיה:
```bash
cd autonomous
python3 autonomous_strategy_hunter.py &
python3 wait_for_gen10.py
```

#### לניתוח מתקדם:
```bash
cd analysis
python3 main_analysis.py
python3 report_generator.py
```

#### לממשק ויזואלי:
```bash
cd dashboard
streamlit run dashboard.py --server.port 8521
```

#### לבדיקת תוצאות:
```bash
cd results
ls -la                                  # רשימת קבצים
cat best_strategies.json | head -20    # אסטרטגיות טובות
```

## 🔧 דרישות מערכת

- Python 3.8+
- pandas, numpy, matplotlib
- streamlit (לדשבורד)
- כ-2GB זיכרון פנוי
- כ-500MB שטח דיסק

## 📞 תמיכה

הפרויקט תוכנן להיות אוטונומי ומקומי לחלוטין:
- 🔄 רץ ללא תלות בשירותי ענן
- 💰 ללא עלויות נוספות
- 🛠️ כל הכלים כלולים

## 🎉 מה הלאה?

### 🚀 התחלה מהירה - 3 שלבים פשוטים:
```bash
# 1. הפעל את המערכת האוטונומית
python3 run_autonomous.py

# 2. בדוק תוצאות תוך כדי
python3 run_dashboard.py

# 3. ניתוח מפורט של הנתונים
python3 run_analysis.py
```

### 📊 תהליך מלא:
1. **הפעל את המערכת האוטונומית** - תמצא אסטרטגיות 24/7
2. **חכה לתוצאות** - שעות-ימים תלוי במזל
3. **בדוק את האסטרטגיות שנמצאו** - בתיקיית results
4. **השתמש בדשבורד לניתוח מתקדם** - ממשק ויזואלי יפה

### 🏆 מה תקבל:
- **אסטרטגיות מנצחות מוכחות** לטריידינג NQ
- **ניתוח מפורט** של כל אסטרטגיה
- **דוחות ויזואליים** עם גרפים
- **מערכת אוטונומית** שרצה לבד

**המערכת תמצא לך אסטרטגיות מנצחות לטריידינג NQ!** 🚀 