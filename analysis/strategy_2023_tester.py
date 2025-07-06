"""
Strategy 2023 Tester - בודק אסטרטגיות על נתוני 2023
מוצא אסטרטגיות רווחיות ומבדק אותן
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class Strategy2023Tester:
    def __init__(self):
        self.df = None
        self.df_2023 = None
        
    def load_data(self):
        """טעינת נתונים והפרדת 2023"""
        print("📊 טוען נתוני NQ...")
        
        try:
            # טעינת הנתונים
            self.df = pd.read_csv('../data/NQ2018.csv')
            self.df['datetime'] = pd.to_datetime(self.df['datetime'])
            self.df.set_index('datetime', inplace=True)
            
            # הפרדת שנת 2023
            self.df_2023 = self.df[self.df.index.year == 2023].copy()
            
            print(f"✅ נטענו {len(self.df):,} שורות נתונים כולל")
            print(f"📅 מתוכם {len(self.df_2023):,} שורות מ-2023")
            print(f"📅 תקופת 2023: {self.df_2023.index.min()} עד {self.df_2023.index.max()}")
            
            return True
            
        except Exception as e:
            print(f"❌ שגיאה בטעינת נתונים: {e}")
            return False
    
    def calculate_indicators(self, df):
        """חישוב אינדיקטורים טכניים"""
        print("📊 מחשב אינדיקטורים טכניים...")
        
        # חישוב תשואות
        df['returns'] = df['close'].pct_change()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Moving Averages
        df['sma_5'] = df['close'].rolling(window=5).mean()
        df['sma_10'] = df['close'].rolling(window=10).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        df['sma_200'] = df['close'].rolling(window=200).mean()
        
        # EMA
        df['ema_9'] = df['close'].ewm(span=9).mean()
        df['ema_21'] = df['close'].ewm(span=21).mean()
        
        # MACD
        df['macd'] = df['ema_9'] - df['ema_21']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # Volume indicators
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_spike'] = df['volume'] > df['volume_ma'] * 1.5
        
        # Price position
        df['price_position'] = (df['close'] - df['low']) / (df['high'] - df['low'])
        
        # Volatility
        df['volatility'] = df['returns'].rolling(window=20).std()
        
        # Time features
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month
        
        return df
    
    def strategy_golden_cross(self, df):
        """אסטרטגיית Golden Cross - פשוטה ויעילה"""
        print("🎯 בודק אסטרטגיית Golden Cross...")
        
        # אותות
        df['golden_cross'] = (df['sma_5'] > df['sma_20']) & (df['sma_5'].shift(1) <= df['sma_20'].shift(1))
        df['death_cross'] = (df['sma_5'] < df['sma_20']) & (df['sma_5'].shift(1) >= df['sma_20'].shift(1))
        
        # Backtesting
        df['position'] = 0
        df['signal'] = 0
        
        for i in range(1, len(df)):
            if df['golden_cross'].iloc[i]:
                df.iloc[i, df.columns.get_loc('signal')] = 1  # קנה
                df.iloc[i, df.columns.get_loc('position')] = 1
            elif df['death_cross'].iloc[i]:
                df.iloc[i, df.columns.get_loc('signal')] = -1  # מכור
                df.iloc[i, df.columns.get_loc('position')] = 0
            else:
                df.iloc[i, df.columns.get_loc('position')] = df.iloc[i-1, df.columns.get_loc('position')]
        
        # חישוב רווחים
        df['strategy_returns'] = df['position'].shift(1) * df['returns']
        df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()
        
        return df
    
    def strategy_rsi_mean_reversion(self, df):
        """אסטרטגיית RSI Mean Reversion"""
        print("🎯 בודק אסטרטגיית RSI Mean Reversion...")
        
        # אותות
        df['rsi_oversold'] = df['rsi'] < 30
        df['rsi_overbought'] = df['rsi'] > 70
        
        # Backtesting
        df['position'] = 0
        df['signal'] = 0
        
        for i in range(1, len(df)):
            if df['rsi_oversold'].iloc[i]:
                df.iloc[i, df.columns.get_loc('signal')] = 1  # קנה
                df.iloc[i, df.columns.get_loc('position')] = 1
            elif df['rsi_overbought'].iloc[i]:
                df.iloc[i, df.columns.get_loc('signal')] = -1  # מכור
                df.iloc[i, df.columns.get_loc('position')] = 0
            else:
                df.iloc[i, df.columns.get_loc('position')] = df.iloc[i-1, df.columns.get_loc('position')]
        
        # חישוב רווחים
        df['strategy_returns'] = df['position'].shift(1) * df['returns']
        df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()
        
        return df
    
    def strategy_breakout_volume(self, df):
        """אסטרטגיית Breakout עם אימות נפח"""
        print("🎯 בודק אסטרטגיית Breakout + Volume...")
        
        # חישוב רמות תמיכה והתנגדות
        df['resistance'] = df['high'].rolling(window=20).max()
        df['support'] = df['low'].rolling(window=20).min()
        
        # אותות
        df['breakout_up'] = (df['close'] > df['resistance'].shift(1)) & df['volume_spike']
        df['breakout_down'] = (df['close'] < df['support'].shift(1)) & df['volume_spike']
        
        # Backtesting
        df['position'] = 0
        df['signal'] = 0
        
        for i in range(1, len(df)):
            if df['breakout_up'].iloc[i]:
                df.iloc[i, df.columns.get_loc('signal')] = 1  # קנה
                df.iloc[i, df.columns.get_loc('position')] = 1
            elif df['breakout_down'].iloc[i]:
                df.iloc[i, df.columns.get_loc('signal')] = -1  # מכור
                df.iloc[i, df.columns.get_loc('position')] = 0
            else:
                df.iloc[i, df.columns.get_loc('position')] = df.iloc[i-1, df.columns.get_loc('position')]
        
        # חישוב רווחים
        df['strategy_returns'] = df['position'].shift(1) * df['returns']
        df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()
        
        return df
    
    def strategy_time_based(self, df):
        """אסטרטגיה מבוססת זמן - מסחר בשעות הטובות"""
        print("🎯 בודק אסטרטגיית Time-Based...")
        
        # שעות טובות למסחר (בדרך כלל 9-11 בבוקר)
        df['good_hours'] = df['hour'].isin([9, 10, 11])
        
        # אותות - רק בשעות הטובות
        df['time_buy'] = df['good_hours'] & (df['close'] > df['sma_5'])
        df['time_sell'] = ~df['good_hours'] | (df['close'] < df['sma_5'])
        
        # Backtesting
        df['position'] = 0
        df['signal'] = 0
        
        for i in range(1, len(df)):
            if df['time_buy'].iloc[i]:
                df.iloc[i, df.columns.get_loc('signal')] = 1  # קנה
                df.iloc[i, df.columns.get_loc('position')] = 1
            elif df['time_sell'].iloc[i]:
                df.iloc[i, df.columns.get_loc('signal')] = -1  # מכור
                df.iloc[i, df.columns.get_loc('position')] = 0
            else:
                df.iloc[i, df.columns.get_loc('position')] = df.iloc[i-1, df.columns.get_loc('position')]
        
        # חישוב רווחים
        df['strategy_returns'] = df['position'].shift(1) * df['returns']
        df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()
        
        return df
    
    def evaluate_strategy(self, df, strategy_name):
        """הערכת ביצועי אסטרטגיה"""
        
        # בדיקת תוצאות
        if 'strategy_returns' not in df.columns:
            return None
        
        strategy_returns = df['strategy_returns'].dropna()
        
        if len(strategy_returns) == 0:
            return None
        
        # חישוב מדדים
        total_return = df['cumulative_returns'].iloc[-1] - 1
        annual_return = total_return  # כי זה שנה אחת
        
        # Sharpe Ratio
        sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252*24*60) if strategy_returns.std() > 0 else 0
        
        # Max Drawdown
        cumulative = df['cumulative_returns'].dropna()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Win Rate
        winning_trades = (strategy_returns > 0).sum()
        total_trades = len(strategy_returns[strategy_returns != 0])
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        # מספר עסקאות
        signals = df['signal'].abs().sum()
        
        return {
            'strategy': strategy_name,
            'total_return': total_return,
            'annual_return': annual_return,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'total_trades': total_trades,
            'total_signals': signals
        }
    
    def run_all_strategies(self):
        """הרצת כל האסטרטגיות על 2023"""
        
        if not self.load_data():
            return
        
        # חישוב אינדיקטורים
        self.df_2023 = self.calculate_indicators(self.df_2023)
        
        print(f"\n🎯 בודק אסטרטגיות על שנת 2023...")
        print(f"📊 תקופה: {self.df_2023.index.min()} עד {self.df_2023.index.max()}")
        print(f"📈 מחיר התחלה: ${self.df_2023['close'].iloc[0]:.2f}")
        print(f"📈 מחיר סיום: ${self.df_2023['close'].iloc[-1]:.2f}")
        print(f"📊 Buy & Hold תשואה: {((self.df_2023['close'].iloc[-1] / self.df_2023['close'].iloc[0]) - 1) * 100:.1f}%")
        
        strategies = [
            ('Golden Cross (SMA 5/20)', self.strategy_golden_cross),
            ('RSI Mean Reversion', self.strategy_rsi_mean_reversion), 
            ('Breakout + Volume', self.strategy_breakout_volume),
            ('Time-Based Trading', self.strategy_time_based)
        ]
        
        results = []
        
        for name, strategy_func in strategies:
            print(f"\n" + "="*50)
            
            # הרצת האסטרטגיה
            df_strategy = self.df_2023.copy()
            df_strategy = strategy_func(df_strategy)
            
            # הערכת תוצאות
            result = self.evaluate_strategy(df_strategy, name)
            
            if result:
                results.append(result)
                
                print(f"📊 {name}:")
                print(f"  💰 תשואה שנתית: {result['annual_return']*100:.1f}%")
                print(f"  📈 Sharpe Ratio: {result['sharpe_ratio']:.2f}")
                print(f"  📉 Max Drawdown: {result['max_drawdown']*100:.1f}%")
                print(f"  🎯 Win Rate: {result['win_rate']*100:.1f}%")
                print(f"  🔢 מספר עסקאות: {result['total_trades']}")
                
                # שמירת תוצאות מפורטות
                df_strategy.to_csv(f'strategy_2023_{name.replace(" ", "_").replace("/", "_")}.csv')
            else:
                print(f"❌ {name}: לא ניתן לחשב תוצאות")
        
        # סיכום וממליצים
        print(f"\n🏆 סיכום אסטרטגיות 2023:")
        print("="*50)
        
        if results:
            # מיון לפי תשואה
            results.sort(key=lambda x: x['annual_return'], reverse=True)
            
            print(f"🥇 האסטרטגיה הטובה ביותר: {results[0]['strategy']}")
            print(f"   💰 תשואה: {results[0]['annual_return']*100:.1f}%")
            print(f"   📈 Sharpe: {results[0]['sharpe_ratio']:.2f}")
            
            # השוואה ל-Buy & Hold
            buy_hold_return = ((self.df_2023['close'].iloc[-1] / self.df_2023['close'].iloc[0]) - 1)
            best_strategy_return = results[0]['annual_return']
            
            if best_strategy_return > buy_hold_return:
                print(f"✅ עלתה על Buy & Hold ב-{(best_strategy_return - buy_hold_return)*100:.1f}%")
            else:
                print(f"❌ נמוכה מ-Buy & Hold ב-{(buy_hold_return - best_strategy_return)*100:.1f}%")
        
        # המלצות
        print(f"\n💡 המלצות לפיתוח אסטרטגיות:")
        print("="*50)
        
        recommendations = [
            "1. שילוב מספר אינדיקטורים לאמינות גבוהה יותר",
            "2. שימוש ב-Stop Loss ו-Take Profit",
            "3. מסחר רק בשעות עם נפח גבוה",
            "4. בדיקת האסטרטגיה על תקופות נוספות",
            "5. התאמת פרמטרים לתנאי שוק שונים"
        ]
        
        for rec in recommendations:
            print(f"   {rec}")
        
        return results

def main():
    """פונקציה ראשית"""
    print("🎯 Strategy 2023 Tester")
    print("=" * 50)
    print("מוצא את האסטרטגיות הטובות ביותר לשנת 2023")
    print()
    
    tester = Strategy2023Tester()
    results = tester.run_all_strategies()
    
    print(f"\n✅ הבדיקה הושלמה!")
    print(f"📁 קבצי תוצאות נשמרו בתיקיה")

if __name__ == "__main__":
    main() 