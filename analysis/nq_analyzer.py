"""
NQ Strategy Analyzer
מערכת מתקדמת לניתוח נתוני NQ וגילוי אסטרטגיות רווחיות
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# הגדרת עיצוב עברית
plt.rcParams['font.family'] = 'Arial Unicode MS'
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.unicode_minus'] = False

class NQAnalyzer:
    """
    מנתח נתוני NQ מתקדם
    """
    
    def __init__(self, data_file='../data/NQ2018.csv'):
        """
        אתחול המנתח
        """
        self.data_file = data_file
        self.df = None
        self.strategies = []
        self.results = {}
        
    def load_data(self):
        """
        טעינת נתונים מהקובץ
        """
        print("📊 טוען נתוני NQ...")
        try:
            self.df = pd.read_csv(self.data_file)
            self.df['datetime'] = pd.to_datetime(self.df['datetime'])
            self.df.set_index('datetime', inplace=True)
            print(f"✅ נטענו {len(self.df):,} שורות נתונים")
            print(f"📅 תקופה: {self.df.index.min()} עד {self.df.index.max()}")
            return True
        except Exception as e:
            print(f"❌ שגיאה בטעינת הנתונים: {e}")
            return False
    
    def basic_analysis(self):
        """
        ניתוח בסיסי של הנתונים
        """
        print("\n🔍 מבצע ניתוח בסיסי...")
        
        # סטטיסטיקות בסיסיות
        stats = {
            'מספר_נקודות': len(self.df),
            'מחיר_ממוצע': self.df['close'].mean(),
            'מחיר_מקסימלי': self.df['high'].max(),
            'מחיר_מינימלי': self.df['low'].min(),
            'נפח_ממוצע': self.df['volume'].mean(),
            'נפח_מקסימלי': self.df['volume'].max(),
            'תקופת_ניתוח': f"{self.df.index.min()} - {self.df.index.max()}"
        }
        
        print("\n📈 סטטיסטיקות בסיסיות:")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"  {key}: {value:,.2f}")
            else:
                print(f"  {key}: {value}")
        
        # חישוב תנודתיות
        self.df['returns'] = self.df['close'].pct_change()
        self.df['volatility'] = self.df['returns'].rolling(window=20).std()
        
        # זיהוי שעות מסחר פעילות
        self.df['hour'] = self.df.index.hour
        self.df['day_of_week'] = self.df.index.dayofweek
        
        self.results['basic_stats'] = stats
        
        return stats
    
    def identify_patterns(self):
        """
        זיהוי דפוסים בנתונים
        """
        print("\n🎯 מזהה דפוסים...")
        
        # חישוב אינדיקטורים טכניים
        self.calculate_technical_indicators()
        
        # זיהוי תנודות גדולות
        self.df['price_change'] = self.df['close'].diff()
        self.df['price_change_pct'] = self.df['close'].pct_change() * 100
        
        # זיהוי breakouts
        self.df['high_breakout'] = self.df['high'] > self.df['high'].rolling(20).max().shift(1)
        self.df['low_breakout'] = self.df['low'] < self.df['low'].rolling(20).min().shift(1)
        
        # זיהוי נפח חריג
        volume_mean = self.df['volume'].rolling(20).mean()
        volume_std = self.df['volume'].rolling(20).std()
        self.df['volume_spike'] = self.df['volume'] > (volume_mean + 2 * volume_std)
        
        patterns = {
            'high_breakouts': self.df['high_breakout'].sum(),
            'low_breakouts': self.df['low_breakout'].sum(),
            'volume_spikes': self.df['volume_spike'].sum(),
            'max_daily_change': self.df['price_change_pct'].max(),
            'min_daily_change': self.df['price_change_pct'].min()
        }
        
        print("\n🔍 דפוסים שנמצאו:")
        for key, value in patterns.items():
            print(f"  {key}: {value}")
        
        self.results['patterns'] = patterns
        return patterns
    
    def calculate_technical_indicators(self):
        """
        חישוב אינדיקטורים טכניים
        """
        print("📊 מחשב אינדיקטורים טכניים...")
        
        # Moving Averages
        self.df['sma_20'] = self.df['close'].rolling(window=20).mean()
        self.df['sma_50'] = self.df['close'].rolling(window=50).mean()
        self.df['ema_20'] = self.df['close'].ewm(span=20).mean()
        
        # RSI
        self.df['rsi'] = self.calculate_rsi(self.df['close'])
        
        # MACD
        self.calculate_macd()
        
        # Bollinger Bands
        self.calculate_bollinger_bands()
        
        # Volume indicators
        self.df['volume_sma'] = self.df['volume'].rolling(window=20).mean()
        self.df['volume_ratio'] = self.df['volume'] / self.df['volume_sma']
        
        print("✅ אינדיקטורים טכניים חושבו")
    
    def calculate_rsi(self, prices, period=14):
        """
        חישוב RSI
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self):
        """
        חישוב MACD
        """
        exp1 = self.df['close'].ewm(span=12).mean()
        exp2 = self.df['close'].ewm(span=26).mean()
        self.df['macd'] = exp1 - exp2
        self.df['macd_signal'] = self.df['macd'].ewm(span=9).mean()
        self.df['macd_histogram'] = self.df['macd'] - self.df['macd_signal']
    
    def calculate_bollinger_bands(self, period=20):
        """
        חישוב Bollinger Bands
        """
        sma = self.df['close'].rolling(window=period).mean()
        std = self.df['close'].rolling(window=period).std()
        self.df['bb_upper'] = sma + (std * 2)
        self.df['bb_lower'] = sma - (std * 2)
        self.df['bb_middle'] = sma
    
    def find_trading_opportunities(self):
        """
        חיפוש הזדמנויות מסחר
        """
        print("\n🎯 מחפש הזדמנויות מסחר...")
        
        # יצירת אותות קנייה ומכירה
        self.df['buy_signal'] = False
        self.df['sell_signal'] = False
        
        # אסטרטגיה 1: Golden Cross (SMA 20 > SMA 50)
        self.df['golden_cross'] = (self.df['sma_20'] > self.df['sma_50']) & \
                                 (self.df['sma_20'].shift(1) <= self.df['sma_50'].shift(1))
        
        # אסטרטגיה 2: RSI Oversold/Overbought
        self.df['rsi_oversold'] = self.df['rsi'] < 30
        self.df['rsi_overbought'] = self.df['rsi'] > 70
        
        # אסטרטגיה 3: MACD Crossover
        self.df['macd_bullish'] = (self.df['macd'] > self.df['macd_signal']) & \
                                 (self.df['macd'].shift(1) <= self.df['macd_signal'].shift(1))
        
        # אסטרטגיה 4: Bollinger Bands
        self.df['bb_oversold'] = self.df['close'] < self.df['bb_lower']
        self.df['bb_overbought'] = self.df['close'] > self.df['bb_upper']
        
        # חיפוש אותות חזקים (חלק מהתנאים יחד)
        self.df['strong_buy'] = (self.df['golden_cross'] | self.df['rsi_oversold'] | 
                                self.df['macd_bullish'] | self.df['bb_oversold'])
        
        self.df['strong_sell'] = (self.df['rsi_overbought'] | self.df['bb_overbought'])
        
        opportunities = {
            'golden_cross_signals': self.df['golden_cross'].sum(),
            'rsi_oversold_signals': self.df['rsi_oversold'].sum(),
            'rsi_overbought_signals': self.df['rsi_overbought'].sum(),
            'macd_bullish_signals': self.df['macd_bullish'].sum(),
            'bb_oversold_signals': self.df['bb_oversold'].sum(),
            'bb_overbought_signals': self.df['bb_overbought'].sum(),
            'strong_buy_signals': self.df['strong_buy'].sum(),
            'strong_sell_signals': self.df['strong_sell'].sum()
        }
        
        print("\n🎯 הזדמנויות מסחר שנמצאו:")
        for key, value in opportunities.items():
            print(f"  {key}: {value}")
        
        self.results['opportunities'] = opportunities
        return opportunities
    
    def analyze_market_hours(self):
        """
        ניתוח שעות מסחר
        """
        print("\n🕐 מנתח שעות מסחר...")
        
        # ניתוח לפי שעות
        hourly_stats = self.df.groupby('hour').agg({
            'volume': 'mean',
            'returns': 'mean',
            'volatility': 'mean'
        }).round(4)
        
        # ניתוח לפי ימים בשבוע
        daily_stats = self.df.groupby('day_of_week').agg({
            'volume': 'mean',
            'returns': 'mean',
            'volatility': 'mean'
        }).round(4)
        
        print("\n📊 סטטיסטיקות לפי שעות (top 5):")
        top_hours = hourly_stats.nlargest(5, 'volume')
        for hour, stats in top_hours.iterrows():
            print(f"  שעה {hour}: נפח={stats['volume']:.0f}, תשואה={stats['returns']:.4f}")
        
        self.results['hourly_stats'] = hourly_stats
        self.results['daily_stats'] = daily_stats
        
        return hourly_stats, daily_stats
    
    def generate_summary_report(self):
        """
        יצירת דוח סיכום
        """
        print("\n📋 יוצר דוח סיכום...")
        
        report = {
            'תאריך_ניתוח': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'נתונים_בסיסיים': self.results.get('basic_stats', {}),
            'דפוסים': self.results.get('patterns', {}),
            'הזדמנויות_מסחר': self.results.get('opportunities', {}),
            'המלצות': self.generate_recommendations()
        }
        
        return report
    
    def generate_recommendations(self):
        """
        יצירת המלצות
        """
        recommendations = []
        
        # המלצות בסיסיות
        if self.results.get('opportunities', {}).get('strong_buy_signals', 0) > 1000:
            recommendations.append("יש הרבה אותות קנייה - כדאי לבדוק תקופות פעילות")
        
        if self.results.get('opportunities', {}).get('golden_cross_signals', 0) > 100:
            recommendations.append("אסטרטגיית Golden Cross מראה פוטנציאל טוב")
        
        if self.results.get('patterns', {}).get('volume_spikes', 0) > 500:
            recommendations.append("יש הרבה עליות נפח - כדאי לנתח קשר למחירים")
        
        return recommendations
    
    def run_full_analysis(self):
        """
        הרצת ניתוח מלא
        """
        print("🚀 מתחיל ניתוח מלא של נתוני NQ...")
        
        # טעינת נתונים
        if not self.load_data():
            return None
        
        # ניתוח בסיסי
        self.basic_analysis()
        
        # זיהוי דפוסים
        self.identify_patterns()
        
        # חיפוש הזדמנויות
        self.find_trading_opportunities()
        
        # ניתוח שעות מסחר
        self.analyze_market_hours()
        
        # יצירת דוח סיכום
        report = self.generate_summary_report()
        
        print("\n✅ ניתוח הושלם בהצלחה!")
        print("\n📊 סיכום המלצות:")
        for rec in report['המלצות']:
            print(f"  • {rec}")
        
        return report

if __name__ == "__main__":
    # הרצת הניתוח
    analyzer = NQAnalyzer()
    report = analyzer.run_full_analysis() 