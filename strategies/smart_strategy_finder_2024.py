"""
Smart Strategy Finder 2024
מערכת חכמה למציאת אסטרטגיות מנצחות
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class SmartStrategyFinder:
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
            print(f"📅 תקופה: {self.df_2024.index.min()} עד {self.df_2024.index.max()}")
            
            return True
            
        except Exception as e:
            print(f"❌ שגיאה: {e}")
            return False
    
    def calculate_indicators(self):
        """חישוב אינדיקטורים מתקדמים"""
        print("📊 מחשב אינדיקטורים מתקדמים...")
        
        df = self.df_2024
        
        # Basic
        df['returns'] = df['close'].pct_change()
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['is_market_open'] = df['hour'].between(9, 15)
        
        # Moving averages
        df['ema_9'] = df['close'].ewm(span=9).mean()
        df['ema_21'] = df['close'].ewm(span=21).mean()
        df['ema_50'] = df['close'].ewm(span=50).mean()
        df['sma_20'] = df['close'].rolling(window=20).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        df['macd'] = df['ema_9'] - df['ema_21']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        df['bb_middle'] = df['sma_20']
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # Volume
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        # Stochastic
        df['lowest_low'] = df['low'].rolling(window=14).min()
        df['highest_high'] = df['high'].rolling(window=14).max()
        df['stoch_k'] = 100 * (df['close'] - df['lowest_low']) / (df['highest_high'] - df['lowest_low'])
        df['stoch_d'] = df['stoch_k'].rolling(window=3).mean()
        
        # ATR
        df['high_low'] = df['high'] - df['low']
        df['high_close'] = np.abs(df['high'] - df['close'].shift())
        df['low_close'] = np.abs(df['low'] - df['close'].shift())
        df['true_range'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
        df['atr'] = df['true_range'].rolling(window=14).mean()
        
        # Price patterns
        df['body'] = abs(df['close'] - df['open'])
        df['upper_shadow'] = df['high'] - np.maximum(df['open'], df['close'])
        df['lower_shadow'] = np.minimum(df['open'], df['close']) - df['low']
        df['total_range'] = df['high'] - df['low']
        
        # Trend strength
        df['trend_strength'] = (df['close'] - df['close'].shift(20)) / df['close'].shift(20)
        
        # Support/Resistance
        df['resistance'] = df['high'].rolling(window=20).max()
        df['support'] = df['low'].rolling(window=20).min()
        
        print("✅ אינדיקטורים מחושבים")
        
    def strategy_ultimate_rsi_bb(self):
        """אסטרטגיית RSI + Bollinger Bands מותאמת למכסימום רווחיות"""
        print("🎯 בוחן אסטרטגיה: Ultimate RSI + BB")
        
        df = self.df_2024.copy()
        
        # תנאי כניסה מתקדמים
        entry_conditions = (
            # RSI בטווח אופטימלי
            (df['rsi'] > 30) & (df['rsi'] < 45) &
            
            # Bollinger Bands - בחלק התחתון
            (df['bb_position'] > 0.1) & (df['bb_position'] < 0.35) &
            
            # מגמה חיובית
            (df['ema_9'] > df['ema_21']) &
            (df['close'] > df['ema_50']) &
            
            # MACD חיובי
            (df['macd_hist'] > 0) &
            (df['macd_hist'] > df['macd_hist'].shift(1)) &
            
            # Volume confirmation
            (df['volume_ratio'] > 1.2) &
            
            # Stochastic
            (df['stoch_k'] > 25) & (df['stoch_k'] < 50) &
            
            # שעות מסחר אופטימליות
            (df['hour'].isin([9, 10, 11, 13, 14])) &
            (df['is_market_open']) &
            
            # לא בסופי שבוע
            (df['day_of_week'] < 5) &
            
            # טרנד לא שלילי
            (df['trend_strength'] > -0.01) &
            
            # מחיר לא קרוב מדי להתנגדות
            (df['close'] < df['resistance'] * 0.998)
        )
        
        # תנאי יציאה
        exit_conditions = (
            # RSI overbought
            (df['rsi'] > 68) |
            
            # Bollinger Bands - בחלק העליון
            (df['bb_position'] > 0.8) |
            
            # מגמה התהפכה
            (df['ema_9'] < df['ema_21']) |
            
            # MACD שלילי
            (df['macd_hist'] < 0) |
            
            # Stochastic overbought
            (df['stoch_k'] > 75) |
            
            # מחיר קרוב להתנגדות
            (df['close'] > df['resistance'] * 0.999)
        )
        
        return self.realistic_backtest(df, entry_conditions, exit_conditions, "Ultimate RSI + BB")
    
    def strategy_momentum_breakout(self):
        """אסטרטגיית Momentum Breakout מתקדמת"""
        print("🎯 בוחן אסטרטגיה: Momentum Breakout")
        
        df = self.df_2024.copy()
        
        # חישוב momentum
        df['momentum_5'] = df['close'] / df['close'].shift(5) - 1
        df['momentum_10'] = df['close'] / df['close'].shift(10) - 1
        
        # תנאי כניסה
        entry_conditions = (
            # Momentum חיובי
            (df['momentum_5'] > 0.001) &
            (df['momentum_10'] > 0.002) &
            
            # פריצת התנגדות
            (df['close'] > df['resistance'].shift(1)) &
            (df['close'] > df['high'].shift(1)) &
            
            # Volume confirmation
            (df['volume_ratio'] > 1.5) &
            
            # RSI לא extreme
            (df['rsi'] > 40) & (df['rsi'] < 70) &
            
            # MACD חיובי
            (df['macd_hist'] > 0) &
            
            # ATR מספיק גבוה
            (df['atr'] > df['atr'].rolling(50).mean()) &
            
            # שעות מסחר
            (df['hour'].isin([9, 10, 11, 13, 14])) &
            (df['is_market_open']) &
            
            # לא בסופי שבוע
            (df['day_of_week'] < 5) &
            
            # מגמה חיובית
            (df['ema_9'] > df['ema_21']) &
            (df['ema_21'] > df['ema_50'])
        )
        
        # תנאי יציאה
        exit_conditions = (
            # Momentum נחלש
            (df['momentum_5'] < 0) |
            
            # RSI overbought
            (df['rsi'] > 75) |
            
            # מגמה התהפכה
            (df['ema_9'] < df['ema_21']) |
            
            # MACD שלילי
            (df['macd_hist'] < 0) |
            
            # Volume נחלש
            (df['volume_ratio'] < 0.8)
        )
        
        return self.realistic_backtest(df, entry_conditions, exit_conditions, "Momentum Breakout")
    
    def strategy_time_volume_pattern(self):
        """אסטרטגיית Time + Volume Pattern"""
        print("🎯 בוחן אסטרטגיה: Time + Volume Pattern")
        
        df = self.df_2024.copy()
        
        # חישוב דפוסי נפח
        df['volume_spike'] = df['volume'] > df['volume_ma'] * 1.8
        df['volume_dry'] = df['volume'] < df['volume_ma'] * 0.6
        
        # תנאי כניסה
        entry_conditions = (
            # Volume spike
            (df['volume_spike']) &
            
            # נר חיובי
            (df['close'] > df['open']) &
            
            # Body גדול
            (df['body'] > df['total_range'] * 0.6) &
            
            # Shadow תחתון גדול (תמיכה)
            (df['lower_shadow'] > df['upper_shadow']) &
            
            # RSI באזור טוב
            (df['rsi'] > 35) & (df['rsi'] < 65) &
            
            # Above EMA
            (df['close'] > df['ema_21']) &
            
            # MACD חיובי
            (df['macd_hist'] > 0) &
            
            # שעות מסחר מצוינות
            (df['hour'].isin([9, 10, 11])) &
            (df['is_market_open']) &
            
            # לא בסופי שבוע
            (df['day_of_week'] < 5) &
            
            # מרחק מתמיכה
            (df['close'] > df['support'] * 1.002) &
            
            # מרחק מהתנגדות
            (df['close'] < df['resistance'] * 0.995)
        )
        
        # תנאי יציאה
        exit_conditions = (
            # Volume יבש
            (df['volume_dry']) |
            
            # נר שלילי
            (df['close'] < df['open']) &
            
            # RSI overbought
            (df['rsi'] > 70) |
            
            # Below EMA
            (df['close'] < df['ema_21']) |
            
            # MACD שלילי
            (df['macd_hist'] < 0) |
            
            # קרוב להתנגדות
            (df['close'] > df['resistance'] * 0.998)
        )
        
        return self.realistic_backtest(df, entry_conditions, exit_conditions, "Time + Volume Pattern")
    
    def strategy_adaptive_scalping(self):
        """אסטרטגיית Scalping אדפטיבית"""
        print("🎯 בוחן אסטרטגיה: Adaptive Scalping")
        
        df = self.df_2024.copy()
        
        # זיהוי תנאי שוק
        df['volatility'] = df['atr'] / df['close']
        df['high_vol'] = df['volatility'] > df['volatility'].rolling(50).quantile(0.7)
        
        # תנאי כניסה מותאמים לתנודתיות
        low_vol_entry = (
            (df['rsi'] < 40) &
            (df['bb_position'] < 0.3) &
            (df['stoch_k'] < 35)
        )
        
        high_vol_entry = (
            (df['rsi'] > 35) & (df['rsi'] < 65) &
            (df['bb_position'] > 0.2) & (df['bb_position'] < 0.8) &
            (df['stoch_k'] > 30) & (df['stoch_k'] < 70)
        )
        
        entry_conditions = (
            # תנאי לפי תנודתיות
            ((~df['high_vol'] & low_vol_entry) | (df['high_vol'] & high_vol_entry)) &
            
            # מגמה חיובית
            (df['ema_9'] > df['ema_21']) &
            
            # MACD חיובי
            (df['macd_hist'] > 0) &
            
            # Volume מספיק
            (df['volume_ratio'] > 1.1) &
            
            # שעות מסחר
            (df['hour'].isin([9, 10, 11, 13, 14])) &
            (df['is_market_open']) &
            
            # לא בסופי שבוע
            (df['day_of_week'] < 5)
        )
        
        # תנאי יציאה מותאמים
        low_vol_exit = (
            (df['rsi'] > 65) |
            (df['bb_position'] > 0.75)
        )
        
        high_vol_exit = (
            (df['rsi'] > 70) |
            (df['bb_position'] > 0.8)
        )
        
        exit_conditions = (
            # תנאי לפי תנודתיות
            ((~df['high_vol'] & low_vol_exit) | (df['high_vol'] & high_vol_exit)) |
            
            # מגמה התהפכה
            (df['ema_9'] < df['ema_21']) |
            
            # MACD שלילי
            (df['macd_hist'] < 0)
        )
        
        return self.realistic_backtest(df, entry_conditions, exit_conditions, "Adaptive Scalping")
    
    def realistic_backtest(self, df, entry_signals, exit_signals, strategy_name):
        """Backtesting מתקדם עם ביצוע realistic"""
        
        position = 0
        entry_price = 0
        trades = []
        equity_curve = []
        current_equity = 100000
        peak_equity = 100000
        
        for i in range(1, len(df)):
            if i >= len(df) - 1:
                break
                
            # Entry (signal on previous bar, execute on current open)
            if position == 0 and entry_signals.iloc[i-1]:
                position = 1
                entry_price = df.iloc[i]['open']
                
            # Exit (signal on previous bar, execute on current open)
            elif position == 1 and exit_signals.iloc[i-1]:
                exit_price = df.iloc[i]['open']
                
                # Calculate trade
                trade_return = (exit_price - entry_price) / entry_price
                trade_pnl = trade_return * 20000  # NQ point value
                
                # Record trade
                trades.append({
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'pnl': trade_pnl,
                    'return': trade_return,
                    'entry_time': df.index[i-1],
                    'exit_time': df.index[i]
                })
                
                # Update equity
                current_equity += trade_pnl
                peak_equity = max(peak_equity, current_equity)
                
                position = 0
                entry_price = 0
            
            # Update equity curve
            if position == 1:
                unrealized_pnl = (df.iloc[i]['close'] - entry_price) / entry_price * 20000
                current_unrealized_equity = 100000 + sum([t['pnl'] for t in trades]) + unrealized_pnl
            else:
                current_unrealized_equity = current_equity
            
            equity_curve.append(current_unrealized_equity)
        
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
        
        return self.evaluate_strategy(trades, equity_curve, strategy_name)
    
    def evaluate_strategy(self, trades, equity_curve, strategy_name):
        """הערכת אסטרטגיה מתקדמת"""
        
        if len(trades) < 200:
            return None
        
        # Basic metrics
        trade_returns = [t['pnl'] for t in trades]
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        
        if len(losing_trades) == 0:
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
        equity_curve = np.array(equity_curve)
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
            'all_criteria_met': all_criteria_met
        }
        
        return result
    
    def run_smart_search(self):
        """הרצת חיפוש חכם"""
        
        if not self.load_data():
            return None
        
        # חישוב אינדיקטורים
        self.calculate_indicators()
        
        print(f"\n🎯 מחפש אסטרטגיות מנצחות על 2024...")
        print(f"📈 מחיר התחלה: ${self.df_2024['close'].iloc[0]:.2f}")
        print(f"📈 מחיר סיום: ${self.df_2024['close'].iloc[-1]:.2f}")
        print(f"📊 Buy & Hold: {((self.df_2024['close'].iloc[-1] / self.df_2024['close'].iloc[0]) - 1) * 100:.1f}%")
        
        # רשימת אסטרטגיות
        strategies = [
            self.strategy_ultimate_rsi_bb,
            self.strategy_momentum_breakout,
            self.strategy_time_volume_pattern,
            self.strategy_adaptive_scalping
        ]
        
        winning_strategies = []
        
        for strategy_func in strategies:
            try:
                result = strategy_func()
                
                if result and result['all_criteria_met']:
                    winning_strategies.append(result)
                    print(f"✅ {result['strategy']} - עומד בכל הקריטריונים!")
                    self.print_strategy_summary(result)
                elif result:
                    print(f"❌ {result['strategy']} - לא עומד בכל הקריטריונים")
                    failed = [k for k, v in result['criteria_met'].items() if not v]
                    print(f"   נכשל ב: {failed}")
                    self.print_strategy_summary(result)
                else:
                    print(f"❌ אסטרטגיה לא עברה בדיקה בסיסית")
                    
            except Exception as e:
                print(f"❌ שגיאה באסטרטגיה: {e}")
        
        # תוצאות
        if winning_strategies:
            print(f"\n🏆 נמצאו {len(winning_strategies)} אסטרטגיות מנצחות!")
            
            # מיון לפי תשואה
            winning_strategies.sort(key=lambda x: x['total_return'], reverse=True)
            
            best_strategy = winning_strategies[0]
            print(f"\n🥇 האסטרטגיה הטובה ביותר: {best_strategy['strategy']}")
            self.print_detailed_report(best_strategy)
            
            return best_strategy
        else:
            print(f"\n❌ לא נמצאו אסטרטגיות שעומדות בכל הקריטריונים")
            return None
    
    def print_strategy_summary(self, result):
        """הדפסת סיכום אסטרטגיה"""
        print(f"  📊 עסקאות: {result['num_trades']}")
        print(f"  💰 רווח: ${result['total_return']:.0f}")
        print(f"  🎯 הצלחה: {result['win_rate']*100:.1f}%")
        print(f"  📈 Sharpe: {result['sharpe_ratio']:.2f}")
        print(f"  🔢 PF: {result['profit_factor']:.2f}")
        print(f"  📉 DD: ${result['max_drawdown']:.0f}")
    
    def print_detailed_report(self, result):
        """הדפסת דוח מפורט"""
        print(f"\n📋 דו\"ח מפורט - {result['strategy']}")
        print("=" * 60)
        
        # Entry/Exit logic description
        if result['strategy'] == "Ultimate RSI + BB":
            print("🎯 תנאי כניסה:")
            print("   • RSI בין 30-45 (oversold אך לא קיצוני)")
            print("   • Bollinger Bands position בין 0.1-0.35")
            print("   • EMA 9 > EMA 21 (מגמה חיובית)")
            print("   • מחיר מעל EMA 50")
            print("   • MACD histogram חיובי ומשתפר")
            print("   • Volume ratio > 1.2")
            print("   • Stochastic בין 25-50")
            print("   • שעות מסחר: 9,10,11,13,14")
            print("   • לא בסופי שבוע")
            print()
            print("🚪 תנאי יציאה:")
            print("   • RSI > 68 (overbought)")
            print("   • BB position > 0.8")
            print("   • EMA 9 < EMA 21 (מגמה התהפכה)")
            print("   • MACD histogram שלילי")
            print("   • Stochastic > 75")
            print("   • מחיר קרוב להתנגדות")
        
        print(f"\n📊 מספר עסקאות: {result['num_trades']}")
        print(f"🎯 אחוז הצלחה: {result['win_rate']*100:.1f}%")
        print(f"💰 רווח כולל: ${result['total_return']:.0f}")
        print(f"📉 Drawdown מקסימלי: ${result['max_drawdown']:.0f}")
        print(f"💵 רווח ממוצע לעסקה: ${result['avg_trade']:.0f}")
        print(f"🔢 Profit Factor: {result['profit_factor']:.2f}")
        print(f"⚖️ יחס רווח/הפסד: {result['win_loss_ratio']:.2f}")
        print(f"📈 Sharpe Ratio: {result['sharpe_ratio']:.2f}")
        print(f"🔄 רצף הפסדים מקסימלי: {result['max_consecutive_losses']}")
        
        print(f"\n📅 רווח חודשי:")
        for month, profit in result['monthly_profits'].items():
            print(f"   {month}: ${profit:.0f}")
        
        print(f"\n✅ עמידה בקריטריונים:")
        criteria_names = {
            'min_trades': '✅ מספר עסקאות ≥ 200',
            'max_drawdown': '✅ Drawdown ≤ $10,000',
            'min_avg_trade': '✅ רווח ממוצע ≥ $30',
            'min_profit_factor': '✅ Profit Factor ≥ 1.7',
            'min_sharpe': '✅ Sharpe Ratio ≥ 1.5',
            'min_win_loss_ratio': '✅ Win/Loss Ratio ≥ 1.5',
            'min_win_rate': '✅ Win Rate ≥ 50%',
            'max_consecutive_losses': '✅ רצף הפסדים ≤ 6',
            'positive_total_return': '✅ רווח כולל חיובי',
            'positive_monthly': '✅ רווח חודשי חיובי'
        }
        
        for criterion, met in result['criteria_met'].items():
            status = "✅" if met else "❌"
            print(f"   {status} {criteria_names.get(criterion, criterion)}")

def main():
    """פונקציה ראשית"""
    print("🎯 Smart Strategy Finder 2024")
    print("=" * 60)
    print("חיפוש חכם ומתקדם לאסטרטגיות מנצחות")
    print()
    
    finder = SmartStrategyFinder()
    result = finder.run_smart_search()
    
    if result:
        print(f"\n🎉 משימה הושלמה בהצלחה!")
        print(f"💎 נמצאה אסטרטגיה מנצחת!")
        print(f"🚀 מוכנה לשימוש מיידי!")
    else:
        print(f"\n🔍 לא נמצאה אסטרטגיה שעומדת בכל הקריטריונים")

if __name__ == "__main__":
    main() 