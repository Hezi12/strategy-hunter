"""
Winning Strategy Finder 2024
מערכת למציאת אסטרטגיות מנצחות עם גישה פשוטה ויעילה
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class WinningStrategyFinder:
    def __init__(self):
        self.df = None
        self.df_2024 = None
        
    def load_data(self):
        """טעינת נתונים"""
        print("📊 טוען נתוני NQ לשנת 2024...")
        
        try:
            self.df = pd.read_csv('../data/NQ2018.csv')
            self.df['datetime'] = pd.to_datetime(self.df['datetime'])
            self.df.set_index('datetime', inplace=True)
            
            # הפרדת 2024
            self.df_2024 = self.df[self.df.index.year == 2024].copy()
            
            print(f"✅ נטענו {len(self.df_2024):,} נקודות נתונים מ-2024")
            
            return True
            
        except Exception as e:
            print(f"❌ שגיאה: {e}")
            return False
    
    def calculate_simple_indicators(self):
        """חישוב אינדיקטורים פשוטים"""
        print("📊 מחשב אינדיקטורים פשוטים...")
        
        df = self.df_2024
        
        # Basic
        df['returns'] = df['close'].pct_change()
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['minute'] = df.index.minute
        df['is_market_open'] = df['hour'].between(9, 15)
        df['is_weekday'] = df['day_of_week'] < 5
        
        # Simple moving averages
        df['ma_20'] = df['close'].rolling(window=20).mean()
        df['ma_50'] = df['close'].rolling(window=50).mean()
        df['ema_20'] = df['close'].ewm(span=20).mean()
        
        # Simple RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Simple volume
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_high'] = df['volume'] > df['volume_ma'] * 1.5
        
        # Price patterns
        df['is_green'] = df['close'] > df['open']
        df['is_red'] = df['close'] < df['open']
        df['body'] = abs(df['close'] - df['open'])
        df['range'] = df['high'] - df['low']
        df['strong_green'] = df['is_green'] & (df['body'] > df['range'] * 0.6)
        df['strong_red'] = df['is_red'] & (df['body'] > df['range'] * 0.6)
        
        # Trend
        df['uptrend'] = df['close'] > df['ma_20']
        df['strong_uptrend'] = (df['close'] > df['ma_20']) & (df['ma_20'] > df['ma_50'])
        
        # Support/Resistance
        df['recent_high'] = df['high'].rolling(window=10).max()
        df['recent_low'] = df['low'].rolling(window=10).min()
        df['near_high'] = df['close'] > df['recent_high'] * 0.998
        df['near_low'] = df['close'] < df['recent_low'] * 1.002
        
        print("✅ אינדיקטורים פשוטים מחושבים")
    
    def simple_trend_following_strategy(self):
        """אסטרטגיית מעקב מגמה פשוטה"""
        print("\n🎯 בוחן: Simple Trend Following")
        
        df = self.df_2024.copy()
        
        # תנאי כניסה פשוטים
        entry_conditions = (
            # מגמה עולה
            (df['uptrend']) &
            (df['close'] > df['ma_50']) &
            
            # נר ירוק חזק
            (df['strong_green']) &
            
            # נפח גבוה
            (df['volume_high']) &
            
            # לא בשיא
            (~df['near_high']) &
            
            # שעות מסחר
            (df['is_market_open']) &
            (df['is_weekday']) &
            
            # שעות טובות
            (df['hour'].isin([9, 10, 11, 13, 14, 15]))
        )
        
        # תנאי יציאה פשוטים
        exit_conditions = (
            # נר אדום
            (df['is_red']) |
            
            # מתחת לממוצע
            (df['close'] < df['ma_20']) |
            
            # בשיא
            (df['near_high']) |
            
            # נפח נמוך
            (~df['volume_high'])
        )
        
        return self.simple_backtest(df, entry_conditions, exit_conditions, "Simple Trend Following")
    
    def rsi_mean_reversion_strategy(self):
        """אסטרטגיית RSI mean reversion"""
        print("\n🎯 בוחן: RSI Mean Reversion")
        
        df = self.df_2024.copy()
        
        # תנאי כניסה
        entry_conditions = (
            # RSI נמוך
            (df['rsi'] < 40) &
            (df['rsi'] > 25) &
            
            # מעל מגמה ארוכת טווח
            (df['close'] > df['ma_50']) &
            
            # נפח גבוה
            (df['volume_high']) &
            
            # לא בשפל
            (~df['near_low']) &
            
            # שעות מסחר
            (df['is_market_open']) &
            (df['is_weekday']) &
            
            # שעות טובות
            (df['hour'].isin([9, 10, 11, 13, 14]))
        )
        
        # תנאי יציאה
        exit_conditions = (
            # RSI גבוה
            (df['rsi'] > 65) |
            
            # מתחת לממוצע
            (df['close'] < df['ma_20']) |
            
            # בשיא
            (df['near_high'])
        )
        
        return self.simple_backtest(df, entry_conditions, exit_conditions, "RSI Mean Reversion")
    
    def volume_breakout_strategy(self):
        """אסטרטגיית פריצת נפח"""
        print("\n🎯 בוחן: Volume Breakout")
        
        df = self.df_2024.copy()
        
        # תנאי כניסה
        entry_conditions = (
            # נפח גבוה מאוד
            (df['volume'] > df['volume_ma'] * 2) &
            
            # נר ירוק חזק
            (df['strong_green']) &
            
            # מעל ממוצע
            (df['close'] > df['ma_20']) &
            
            # פריצה מעל שיא
            (df['close'] > df['recent_high'].shift(1)) &
            
            # שעות מסחר
            (df['is_market_open']) &
            (df['is_weekday']) &
            
            # שעות טובות
            (df['hour'].isin([9, 10, 11, 13, 14]))
        )
        
        # תנאי יציאה
        exit_conditions = (
            # נפח נמוך
            (df['volume'] < df['volume_ma'] * 0.8) |
            
            # נר אדום
            (df['is_red']) |
            
            # מתחת לממוצע
            (df['close'] < df['ma_20'])
        )
        
        return self.simple_backtest(df, entry_conditions, exit_conditions, "Volume Breakout")
    
    def time_based_strategy(self):
        """אסטרטגיה מבוססת זמן"""
        print("\n🎯 בוחן: Time Based Strategy")
        
        df = self.df_2024.copy()
        
        # תנאי כניסה
        entry_conditions = (
            # שעות מסחר מצוינות
            (df['hour'].isin([9, 10, 11])) &
            
            # נר ירוק
            (df['is_green']) &
            
            # מעל ממוצע
            (df['close'] > df['ma_20']) &
            
            # RSI לא extreme
            (df['rsi'] > 30) & (df['rsi'] < 70) &
            
            # נפח נורמלי
            (df['volume'] > df['volume_ma'] * 0.8) &
            
            # ימי חול
            (df['is_weekday'])
        )
        
        # תנאי יציאה
        exit_conditions = (
            # סוף יום
            (df['hour'] >= 15) |
            
            # נר אדום
            (df['is_red']) |
            
            # מתחת לממוצע
            (df['close'] < df['ma_20']) |
            
            # RSI extreme
            (df['rsi'] > 75)
        )
        
        return self.simple_backtest(df, entry_conditions, exit_conditions, "Time Based Strategy")
    
    def aggressive_scalping_strategy(self):
        """אסטרטגיית scalping אגרסיבית"""
        print("\n🎯 בוחן: Aggressive Scalping")
        
        df = self.df_2024.copy()
        
        # תנאי כניסה רחבים
        entry_conditions = (
            # נר ירוק
            (df['is_green']) &
            
            # מעל ממוצע קצר
            (df['close'] > df['ema_20']) &
            
            # נפח בסיסי
            (df['volume'] > df['volume_ma'] * 0.7) &
            
            # RSI לא extreme
            (df['rsi'] > 20) & (df['rsi'] < 80) &
            
            # שעות מסחר
            (df['is_market_open']) &
            (df['is_weekday']) &
            
            # שעות טובות
            (df['hour'].isin([9, 10, 11, 13, 14, 15]))
        )
        
        # תנאי יציאה מהירה
        exit_conditions = (
            # נר אדום
            (df['is_red']) |
            
            # RSI גבוה
            (df['rsi'] > 70) |
            
            # מתחת לממוצע
            (df['close'] < df['ema_20'])
        )
        
        return self.simple_backtest(df, entry_conditions, exit_conditions, "Aggressive Scalping")
    
    def conservative_long_strategy(self):
        """אסטרטגיה שמרנית לונג"""
        print("\n🎯 בוחן: Conservative Long")
        
        df = self.df_2024.copy()
        
        # תנאי כניסה שמרניים
        entry_conditions = (
            # מגמה עולה חזקה
            (df['strong_uptrend']) &
            
            # RSI מאוזן
            (df['rsi'] > 40) & (df['rsi'] < 60) &
            
            # נר ירוק
            (df['is_green']) &
            
            # נפח טוב
            (df['volume'] > df['volume_ma']) &
            
            # לא בשיא
            (~df['near_high']) &
            
            # שעות מסחר
            (df['is_market_open']) &
            (df['is_weekday']) &
            
            # שעות בטוחות
            (df['hour'].isin([10, 11, 13, 14]))
        )
        
        # תנאי יציאה שמרניים
        exit_conditions = (
            # RSI גבוה
            (df['rsi'] > 65) |
            
            # מתחת לממוצע
            (df['close'] < df['ma_20']) |
            
            # בשיא
            (df['near_high']) |
            
            # נר אדום חזק
            (df['strong_red'])
        )
        
        return self.simple_backtest(df, entry_conditions, exit_conditions, "Conservative Long")
    
    def simple_backtest(self, df, entry_signals, exit_signals, strategy_name):
        """Backtesting פשוט ומהיר"""
        
        position = 0
        entry_price = 0
        trades = []
        
        for i in range(1, len(df)):
            if i >= len(df) - 1:
                break
            
            current_price = df.iloc[i]['open']  # Realistic execution
            
            # Entry
            if position == 0 and entry_signals.iloc[i-1]:
                position = 1
                entry_price = current_price
                
            # Exit
            elif position == 1 and exit_signals.iloc[i-1]:
                exit_price = current_price
                trade_return = (exit_price - entry_price) / entry_price
                trade_pnl = trade_return * 20000  # NQ point value
                
                trades.append({
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'pnl': trade_pnl,
                    'return': trade_return,
                    'entry_time': df.index[i-1],
                    'exit_time': df.index[i]
                })
                
                position = 0
                entry_price = 0
        
        # Close final position
        if position == 1:
            exit_price = df.iloc[-1]['close']
            trade_return = (exit_price - entry_price) / entry_price
            trade_pnl = trade_return * 20000
            
            trades.append({
                'entry_price': entry_price,
                'exit_price': exit_price,
                'pnl': trade_pnl,
                'return': trade_return,
                'entry_time': df.index[-2],
                'exit_time': df.index[-1]
            })
        
        return self.evaluate_strategy(trades, strategy_name)
    
    def evaluate_strategy(self, trades, strategy_name):
        """הערכת אסטרטגיה"""
        
        print(f"   📊 מספר עסקאות: {len(trades)}")
        
        if len(trades) < 200:
            print(f"   ❌ {strategy_name}: פחות מ-200 עסקאות")
            return None
        
        # Basic metrics
        trade_returns = [t['pnl'] for t in trades]
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        
        if len(losing_trades) == 0:
            print(f"   ❌ {strategy_name}: אין עסקאות מפסידות")
            return None
        
        total_return = sum(trade_returns)
        num_trades = len(trades)
        win_rate = len(winning_trades) / num_trades
        avg_trade = total_return / num_trades
        
        # Profit Factor
        gross_profit = sum([t['pnl'] for t in winning_trades])
        gross_loss = abs(sum([t['pnl'] for t in losing_trades]))
        profit_factor = gross_profit / gross_loss
        
        # Win/Loss ratio
        avg_win = gross_profit / len(winning_trades)
        avg_loss = gross_loss / len(losing_trades)
        win_loss_ratio = avg_win / avg_loss
        
        # Sharpe Ratio
        returns_std = np.std(trade_returns)
        sharpe = (avg_trade / returns_std) * np.sqrt(252*24) if returns_std > 0 else 0
        
        # Drawdown
        equity_curve = np.cumsum(trade_returns) + 100000
        peak = np.maximum.accumulate(equity_curve)
        drawdown = equity_curve - peak
        max_drawdown = np.min(drawdown)
        
        # Max consecutive losses
        consecutive_losses = 0
        max_consecutive_losses = 0
        for trade in trades:
            if trade['pnl'] < 0:
                consecutive_losses += 1
                max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
            else:
                consecutive_losses = 0
        
        # Monthly profits
        monthly_profits = {}
        for trade in trades:
            month = trade['exit_time'].strftime('%Y-%m')
            if month not in monthly_profits:
                monthly_profits[month] = 0
            monthly_profits[month] += trade['pnl']
        
        # Check criteria
        criteria_met = {
            'min_trades': num_trades >= 200,
            'max_drawdown': max_drawdown >= -10000,
            'min_avg_trade': avg_trade >= 30,
            'min_profit_factor': profit_factor >= 1.7,
            'min_sharpe': sharpe >= 1.5,
            'min_win_loss_ratio': win_loss_ratio >= 1.5,
            'min_win_rate': win_rate >= 0.5,
            'max_consecutive_losses': max_consecutive_losses <= 6,
            'positive_total_return': total_return > 0,
            'positive_monthly': all(p > 0 for p in monthly_profits.values())
        }
        
        all_criteria_met = all(criteria_met.values())
        criteria_count = sum(criteria_met.values())
        
        print(f"   📈 קריטריונים: {criteria_count}/10")
        print(f"   💰 רווח: ${total_return:.0f}")
        print(f"   📊 PF: {profit_factor:.2f}")
        print(f"   📈 Sharpe: {sharpe:.2f}")
        print(f"   🎯 Win Rate: {win_rate*100:.1f}%")
        print(f"   📉 DD: ${max_drawdown:.0f}")
        
        if all_criteria_met:
            print(f"   ✅ {strategy_name}: עומד בכל הקריטריונים!")
        else:
            failed_criteria = [k for k, v in criteria_met.items() if not v]
            print(f"   ❌ נכשל ב: {failed_criteria}")
        
        result = {
            'strategy': strategy_name,
            'num_trades': num_trades,
            'win_rate': win_rate,
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'avg_trade': avg_trade,
            'profit_factor': profit_factor,
            'win_loss_ratio': win_loss_ratio,
            'sharpe_ratio': sharpe,
            'max_consecutive_losses': max_consecutive_losses,
            'monthly_profits': monthly_profits,
            'criteria_met': criteria_met,
            'all_criteria_met': all_criteria_met,
            'criteria_count': criteria_count
        }
        
        return result
    
    def run_winning_search(self):
        """הרצת חיפוש מנצח"""
        
        if not self.load_data():
            return None
        
        # חישוב אינדיקטורים
        self.calculate_simple_indicators()
        
        print(f"\n🎯 מחפש אסטרטגיות מנצחות פשוטות על 2024...")
        print(f"📈 מחיר התחלה: ${self.df_2024['close'].iloc[0]:.2f}")
        print(f"📈 מחיר סיום: ${self.df_2024['close'].iloc[-1]:.2f}")
        buy_hold = ((self.df_2024['close'].iloc[-1] / self.df_2024['close'].iloc[0]) - 1) * 100
        print(f"📊 Buy & Hold: {buy_hold:.1f}%")
        
        # רשימת אסטרטגיות פשוטות
        strategies = [
            self.simple_trend_following_strategy,
            self.rsi_mean_reversion_strategy,
            self.volume_breakout_strategy,
            self.time_based_strategy,
            self.aggressive_scalping_strategy,
            self.conservative_long_strategy
        ]
        
        winning_strategies = []
        best_partial = None
        best_score = 0
        
        for strategy_func in strategies:
            try:
                result = strategy_func()
                
                if result:
                    if result['all_criteria_met']:
                        winning_strategies.append(result)
                        print(f"   ✅ נמצאה אסטרטגיה מנצחת!")
                    elif result['criteria_count'] > best_score:
                        best_score = result['criteria_count']
                        best_partial = result
                        
            except Exception as e:
                print(f"   ❌ שגיאה: {e}")
        
        # תוצאות
        if winning_strategies:
            print(f"\n🏆 נמצאו {len(winning_strategies)} אסטרטגיות מנצחות!")
            
            winning_strategies.sort(key=lambda x: x['total_return'], reverse=True)
            best_strategy = winning_strategies[0]
            
            print(f"\n🥇 האסטרטגיה הטובה ביותר: {best_strategy['strategy']}")
            self.print_winning_report(best_strategy)
            
            return best_strategy
        
        elif best_partial:
            print(f"\n⚠️ לא נמצאה אסטרטגיה מושלמת")
            print(f"🔍 הטובה ביותר: {best_partial['strategy']} ({best_partial['criteria_count']}/10)")
            self.print_winning_report(best_partial)
            
            return best_partial
        
        else:
            print(f"\n❌ לא נמצאו אסטרטגיות מתאימות")
            return None
    
    def print_winning_report(self, result):
        """דוח מנצח"""
        print(f"\n📋 דו\"ח סופי - {result['strategy']}")
        print("=" * 60)
        
        # Strategy description
        if "Aggressive Scalping" in result['strategy']:
            print("🎯 תיאור האסטרטגיה:")
            print("   אסטרטגיית Scalping אגרסיבית:")
            print("   • כניסה: נר ירוק + מעל EMA20 + נפח בסיסי + RSI 20-80")
            print("   • יציאה: נר אדום או RSI>70 או מתחת EMA20")
            print("   • שעות: 9-11, 13-15 (שעות מסחר עיקריות)")
            print("   • ימים: ימי חול בלבד")
            print("   • גישה: כניסות מהירות ויציאות מהירות")
        
        print(f"\n📊 סטטיסטיקות:")
        print(f"📊 מספר עסקאות: {result['num_trades']}")
        print(f"🎯 אחוז הצלחה: {result['win_rate']*100:.1f}%")
        print(f"💰 רווח כולל: ${result['total_return']:.0f}")
        print(f"📉 Drawdown מקסימלי: ${result['max_drawdown']:.0f}")
        print(f"💵 רווח ממוצע לעסקה: ${result['avg_trade']:.0f}")
        print(f"🔢 Profit Factor: {result['profit_factor']:.2f}")
        print(f"⚖️ יחס רווח/הפסד: {result['win_loss_ratio']:.2f}")
        print(f"📈 Sharpe Ratio: {result['sharpe_ratio']:.2f}")
        print(f"🔄 רצף הפסדים מקסימלי: {result['max_consecutive_losses']}")
        
        print(f"\n📅 רווח חודשי:")
        positive_months = sum(1 for p in result['monthly_profits'].values() if p > 0)
        total_months = len(result['monthly_profits'])
        print(f"   חודשים רווחיים: {positive_months}/{total_months}")
        
        for month, profit in result['monthly_profits'].items():
            status = "✅" if profit > 0 else "❌"
            print(f"   {status} {month}: ${profit:.0f}")
        
        print(f"\n✅ קריטריונים ({sum(result['criteria_met'].values())}/10):")
        criteria_names = {
            'min_trades': f"מספר עסקאות ≥ 200",
            'max_drawdown': f"Drawdown ≤ $10,000",
            'min_avg_trade': f"רווח ממוצע ≥ $30",
            'min_profit_factor': f"Profit Factor ≥ 1.7",
            'min_sharpe': f"Sharpe Ratio ≥ 1.5",
            'min_win_loss_ratio': f"Win/Loss Ratio ≥ 1.5",
            'min_win_rate': f"Win Rate ≥ 50%",
            'max_consecutive_losses': f"רצף הפסדים ≤ 6",
            'positive_total_return': f"רווח כולל חיובי",
            'positive_monthly': f"כל החודשים חיוביים"
        }
        
        for criterion, met in result['criteria_met'].items():
            status = "✅" if met else "❌"
            name = criteria_names.get(criterion, criterion)
            print(f"   {status} {name}")

def main():
    """פונקציה ראשית"""
    print("🎯 Winning Strategy Finder 2024")
    print("=" * 60)
    print("מערכת לאיתור אסטרטגיות מנצחות פשוטות ויעילות")
    print()
    
    finder = WinningStrategyFinder()
    result = finder.run_winning_search()
    
    if result and result['all_criteria_met']:
        print(f"\n🎉 משימה הושלמה בהצלחה!")
        print(f"💎 נמצאה אסטרטגיה מנצחת שעומדת בכל הקריטריונים!")
        print(f"🚀 מוכנה לשימוש מיידי!")
    elif result:
        print(f"\n⚠️ נמצאה אסטרטגיה חלקית")
        print(f"📊 עומדת ב-{result['criteria_count']}/10 קריטריונים")
    else:
        print(f"\n❌ לא נמצאו אסטרטגיות מתאימות")

if __name__ == "__main__":
    main() 