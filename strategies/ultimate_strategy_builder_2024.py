"""
Ultimate Strategy Builder 2024
מערכת מתקדמת ביותר למציאת אסטרטגיות מנצחות
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class UltimateStrategyBuilder:
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
    
    def calculate_comprehensive_indicators(self):
        """חישוב אינדיקטורים מקיפים"""
        print("📊 מחשב אינדיקטורים מקיפים...")
        
        df = self.df_2024
        
        # Basic
        df['returns'] = df['close'].pct_change()
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['is_market_open'] = df['hour'].between(9, 15)
        
        # Moving averages - wide range
        for period in [3, 5, 8, 13, 21, 34, 55, 89]:
            df[f'ema_{period}'] = df['close'].ewm(span=period).mean()
            df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
        
        # RSI multiple periods
        for rsi_period in [9, 14, 21]:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
            rs = gain / loss
            df[f'rsi_{rsi_period}'] = 100 - (100 / (1 + rs))
        
        # MACD variants
        df['macd_fast'] = df['ema_8'] - df['ema_21']
        df['macd_slow'] = df['ema_13'] - df['ema_34']
        df['macd_signal_fast'] = df['macd_fast'].ewm(span=9).mean()
        df['macd_signal_slow'] = df['macd_slow'].ewm(span=9).mean()
        df['macd_hist_fast'] = df['macd_fast'] - df['macd_signal_fast']
        df['macd_hist_slow'] = df['macd_slow'] - df['macd_signal_slow']
        
        # Bollinger Bands multiple periods
        for bb_period in [15, 20, 30]:
            df[f'bb_middle_{bb_period}'] = df['close'].rolling(window=bb_period).mean()
            bb_std = df['close'].rolling(window=bb_period).std()
            df[f'bb_upper_{bb_period}'] = df[f'bb_middle_{bb_period}'] + (bb_std * 2)
            df[f'bb_lower_{bb_period}'] = df[f'bb_middle_{bb_period}'] - (bb_std * 2)
            df[f'bb_width_{bb_period}'] = df[f'bb_upper_{bb_period}'] - df[f'bb_lower_{bb_period}']
            df[f'bb_position_{bb_period}'] = (df['close'] - df[f'bb_lower_{bb_period}']) / df[f'bb_width_{bb_period}']
        
        # Stochastic
        for stoch_period in [14, 21]:
            df[f'lowest_low_{stoch_period}'] = df['low'].rolling(window=stoch_period).min()
            df[f'highest_high_{stoch_period}'] = df['high'].rolling(window=stoch_period).max()
            df[f'stoch_k_{stoch_period}'] = 100 * (df['close'] - df[f'lowest_low_{stoch_period}']) / (df[f'highest_high_{stoch_period}'] - df[f'lowest_low_{stoch_period}'])
            df[f'stoch_d_{stoch_period}'] = df[f'stoch_k_{stoch_period}'].rolling(window=3).mean()
        
        # Volume indicators
        for vol_period in [10, 20, 30]:
            df[f'volume_ma_{vol_period}'] = df['volume'].rolling(window=vol_period).mean()
            df[f'volume_ratio_{vol_period}'] = df['volume'] / df[f'volume_ma_{vol_period}']
        
        # ATR and volatility
        df['high_low'] = df['high'] - df['low']
        df['high_close'] = np.abs(df['high'] - df['close'].shift())
        df['low_close'] = np.abs(df['low'] - df['close'].shift())
        df['true_range'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
        df['atr'] = df['true_range'].rolling(window=14).mean()
        df['volatility'] = df['returns'].rolling(window=20).std()
        
        # Price action
        df['body'] = abs(df['close'] - df['open'])
        df['upper_shadow'] = df['high'] - np.maximum(df['open'], df['close'])
        df['lower_shadow'] = np.minimum(df['open'], df['close']) - df['low']
        df['total_range'] = df['high'] - df['low']
        df['is_bullish'] = df['close'] > df['open']
        df['is_doji'] = df['body'] < df['total_range'] * 0.1
        
        # Trend indicators
        df['trend_strength_short'] = (df['close'] - df['close'].shift(5)) / df['close'].shift(5)
        df['trend_strength_medium'] = (df['close'] - df['close'].shift(20)) / df['close'].shift(20)
        df['trend_strength_long'] = (df['close'] - df['close'].shift(50)) / df['close'].shift(50)
        
        # Support/Resistance
        for sr_period in [20, 50]:
            df[f'resistance_{sr_period}'] = df['high'].rolling(window=sr_period).max()
            df[f'support_{sr_period}'] = df['low'].rolling(window=sr_period).min()
            df[f'dist_to_resistance_{sr_period}'] = (df[f'resistance_{sr_period}'] - df['close']) / df['close']
            df[f'dist_to_support_{sr_period}'] = (df['close'] - df[f'support_{sr_period}']) / df['close']
        
        # Time-based features
        df['is_morning'] = df['hour'].isin([9, 10, 11])
        df['is_afternoon'] = df['hour'].isin([13, 14, 15])
        df['is_prime_time'] = df['hour'].isin([9, 10, 11, 13, 14])
        df['is_weekday'] = df['day_of_week'] < 5
        
        # Market regime indicators
        df['high_vol_regime'] = df['volatility'] > df['volatility'].rolling(100).quantile(0.7)
        df['trending_regime'] = abs(df['trend_strength_medium']) > 0.01
        
        print("✅ אינדיקטורים מקיפים מחושבים")
    
    def diagnose_market_patterns(self):
        """אבחון דפוסי שוק"""
        print("\n🔍 מבצע אבחון דפוסי שוק...")
        
        df = self.df_2024
        
        # זיהוי תקופות רווחיות
        profitable_hours = df.groupby('hour')['returns'].mean().sort_values(ascending=False)
        print(f"🕐 שעות הכי רווחיות: {profitable_hours.head(3).index.tolist()}")
        
        # זיהוי תנאי RSI רווחיים
        df['rsi_bins'] = pd.cut(df['rsi_14'], bins=[0, 20, 30, 40, 50, 60, 70, 80, 100])
        rsi_returns = df.groupby('rsi_bins')['returns'].mean().sort_values(ascending=False)
        print(f"📊 טווחי RSI רווחיים: {rsi_returns.head(2).index.tolist()}")
        
        # זיהוי תנאי Volume רווחיים
        df['vol_bins'] = pd.cut(df['volume_ratio_20'], bins=[0, 0.5, 1, 1.5, 2, 5])
        vol_returns = df.groupby('vol_bins')['returns'].mean().sort_values(ascending=False)
        print(f"📈 טווחי Volume רווחיים: {vol_returns.head(2).index.tolist()}")
        
        return profitable_hours, rsi_returns, vol_returns
    
    def create_high_frequency_strategy(self):
        """יצירת אסטרטגיית high frequency מותאמת"""
        print("\n🎯 בונה אסטרטגיית High Frequency מותאמת...")
        
        df = self.df_2024.copy()
        
        # תנאי כניסה מרובי שכבות
        # שכבה 1: תנאי זמן ובסיסיים
        time_condition = (
            (df['is_prime_time']) &
            (df['is_weekday']) &
            (df['hour'] != 12)  # לא בשעת צהריים
        )
        
        # שכבה 2: תנאי מגמה
        trend_condition = (
            (df['ema_3'] > df['ema_8']) &  # מגמה קצרה חיובית
            (df['ema_8'] > df['ema_21']) &  # מגמה בינונית חיובית
            (df['close'] > df['ema_34'])  # מעל מגמה ארוכה
        )
        
        # שכבה 3: תנאי momentum
        momentum_condition = (
            (df['rsi_9'] > 35) & (df['rsi_9'] < 65) &  # RSI מאוזן
            (df['rsi_14'] > 40) & (df['rsi_14'] < 70) &  # RSI לא קיצוני
            (df['macd_hist_fast'] > 0) &  # MACD חיובי
            (df['macd_hist_fast'] > df['macd_hist_fast'].shift(1))  # MACD משתפר
        )
        
        # שכבה 4: תנאי volatility ונפח
        volatility_condition = (
            (df['volume_ratio_10'] > 1.1) &  # נפח מעל ממוצע
            (df['atr'] > df['atr'].rolling(50).quantile(0.3)) &  # volatility מספיק
            (df['bb_position_20'] > 0.15) & (df['bb_position_20'] < 0.7)  # לא בקצוות
        )
        
        # שכבה 5: תנאי price action
        price_action_condition = (
            (df['is_bullish']) &  # נר חיובי
            (df['body'] > df['total_range'] * 0.4) &  # body משמעותי
            (df['close'] > df['support_20'] * 1.001) &  # מעל תמיכה
            (df['close'] < df['resistance_20'] * 0.999)  # מתחת להתנגדות
        )
        
        # שכבה 6: תנאי stochastic
        stoch_condition = (
            (df['stoch_k_14'] > 25) & (df['stoch_k_14'] < 75) &
            (df['stoch_k_14'] > df['stoch_d_14'])  # K מעל D
        )
        
        # שילוב כל התנאים
        entry_conditions = (
            time_condition &
            trend_condition &
            momentum_condition &
            volatility_condition &
            price_action_condition &
            stoch_condition
        )
        
        # תנאי יציאה מרובי שכבות
        # יציאה מהירה
        quick_exit = (
            (df['rsi_9'] > 75) |  # RSI extreme
            (df['bb_position_20'] > 0.85) |  # קרוב ל-upper BB
            (df['ema_3'] < df['ema_8'])  # מגמה קצרה התהפכה
        )
        
        # יציאה רגילה
        normal_exit = (
            (df['rsi_14'] > 70) |  # RSI overbought
            (df['macd_hist_fast'] < 0) |  # MACD שלילי
            (df['stoch_k_14'] > 80) |  # Stochastic overbought
            (df['volume_ratio_10'] < 0.7)  # נפח נחלש
        )
        
        exit_conditions = quick_exit | normal_exit
        
        return self.advanced_backtest(df, entry_conditions, exit_conditions, "High Frequency Strategy")
    
    def create_conservative_scalping_strategy(self):
        """יצירת אסטרטגיית scalping שמרנית"""
        print("\n🎯 בונה אסטרטגיית Scalping שמרנית...")
        
        df = self.df_2024.copy()
        
        # תנאי כניסה שמרניים
        entry_conditions = (
            # זמן אופטימלי
            (df['hour'].isin([9, 10, 11, 13, 14])) &
            (df['is_weekday']) &
            
            # מגמה יציבה
            (df['ema_5'] > df['ema_13']) &
            (df['ema_13'] > df['ema_34']) &
            (df['close'] > df['ema_55']) &
            
            # RSI מאוזן
            (df['rsi_14'] > 45) & (df['rsi_14'] < 60) &
            
            # MACD חיובי אך לא extreme
            (df['macd_hist_fast'] > 0) &
            (df['macd_hist_fast'] < 2) &
            
            # Volume מתון
            (df['volume_ratio_20'] > 1.05) & (df['volume_ratio_20'] < 2.5) &
            
            # Bollinger Bands מרכז
            (df['bb_position_20'] > 0.3) & (df['bb_position_20'] < 0.7) &
            
            # Stochastic לא extreme
            (df['stoch_k_14'] > 30) & (df['stoch_k_14'] < 70) &
            
            # מרחק בטוח מרמות קריטיות
            (df['dist_to_support_20'] > 0.002) &
            (df['dist_to_resistance_20'] > 0.003) &
            
            # לא בתנודתיות גבוהה מדי
            (~df['high_vol_regime']) &
            
            # נר חיובי
            (df['is_bullish']) &
            (df['body'] > df['total_range'] * 0.5)
        )
        
        # תנאי יציאה שמרניים
        exit_conditions = (
            # RSI התרחק מהמרכז
            (df['rsi_14'] < 40) | (df['rsi_14'] > 65) |
            
            # MACD התדרדר
            (df['macd_hist_fast'] < 0) |
            
            # מגמה קצרה התהפכה
            (df['ema_5'] < df['ema_13']) |
            
            # Bollinger Bands קיצוני
            (df['bb_position_20'] < 0.2) | (df['bb_position_20'] > 0.8) |
            
            # Stochastic extreme
            (df['stoch_k_14'] < 25) | (df['stoch_k_14'] > 75) |
            
            # Volume חלש
            (df['volume_ratio_20'] < 0.8) |
            
            # קרוב לרמות קריטיות
            (df['dist_to_resistance_20'] < 0.001)
        )
        
        return self.advanced_backtest(df, entry_conditions, exit_conditions, "Conservative Scalping")
    
    def create_momentum_surge_strategy(self):
        """יצירת אסטרטגיית momentum surge"""
        print("\n🎯 בונה אסטרטגיית Momentum Surge...")
        
        df = self.df_2024.copy()
        
        # זיהוי momentum surge
        df['price_surge'] = (df['close'] / df['close'].shift(3) - 1) > 0.002
        df['volume_surge'] = df['volume_ratio_10'] > 1.8
        df['momentum_surge'] = df['price_surge'] & df['volume_surge']
        
        # תנאי כניסה
        entry_conditions = (
            # Momentum surge
            (df['momentum_surge']) &
            
            # זמן טוב
            (df['is_prime_time']) &
            (df['is_weekday']) &
            
            # מגמה תומכת
            (df['ema_8'] > df['ema_21']) &
            (df['close'] > df['ema_34']) &
            
            # RSI לא overbought
            (df['rsi_14'] < 75) &
            (df['rsi_9'] < 80) &
            
            # MACD תומך
            (df['macd_hist_fast'] > 0) &
            
            # לא בקצה עליון של BB
            (df['bb_position_20'] < 0.9) &
            
            # Stochastic עם מקום לעלות
            (df['stoch_k_14'] < 85) &
            
            # מרחק מהתנגדות
            (df['dist_to_resistance_20'] > 0.002) &
            
            # נר חזק
            (df['is_bullish']) &
            (df['body'] > df['total_range'] * 0.6)
        )
        
        # תנאי יציאה מהירה
        exit_conditions = (
            # Momentum נחלש
            (df['volume_ratio_10'] < 1.2) |
            
            # RSI extreme
            (df['rsi_9'] > 85) |
            (df['rsi_14'] > 80) |
            
            # MACD peak
            (df['macd_hist_fast'] < df['macd_hist_fast'].shift(1)) &
            (df['macd_hist_fast'] < df['macd_hist_fast'].shift(2)) |
            
            # BB extreme
            (df['bb_position_20'] > 0.95) |
            
            # מגמה התהפכה
            (df['ema_3'] < df['ema_8']) |
            
            # Stochastic overbought
            (df['stoch_k_14'] > 90) |
            
            # קרוב להתנגדות
            (df['dist_to_resistance_20'] < 0.0005)
        )
        
        return self.advanced_backtest(df, entry_conditions, exit_conditions, "Momentum Surge")
    
    def advanced_backtest(self, df, entry_signals, exit_signals, strategy_name):
        """Backtesting מתקדם עם stop loss ו-take profit"""
        
        position = 0
        entry_price = 0
        trades = []
        bars_in_trade = 0
        max_bars_per_trade = 20  # מגבלת זמן לעסקה
        
        # Stop loss ו-take profit דינמיים
        dynamic_stop_loss = 0.003  # 0.3%
        dynamic_take_profit = 0.008  # 0.8%
        
        for i in range(1, len(df)):
            if i >= len(df) - 1:
                break
            
            current_price = df.iloc[i]['open']  # Realistic execution
            
            # Entry
            if position == 0 and entry_signals.iloc[i-1]:
                position = 1
                entry_price = current_price
                bars_in_trade = 0
                
            # Exit
            elif position == 1:
                bars_in_trade += 1
                should_exit = False
                exit_reason = ""
                
                # Signal exit
                if exit_signals.iloc[i-1]:
                    should_exit = True
                    exit_reason = "signal"
                
                # Stop loss
                elif current_price < entry_price * (1 - dynamic_stop_loss):
                    should_exit = True
                    exit_reason = "stop_loss"
                
                # Take profit
                elif current_price > entry_price * (1 + dynamic_take_profit):
                    should_exit = True
                    exit_reason = "take_profit"
                
                # Max time
                elif bars_in_trade >= max_bars_per_trade:
                    should_exit = True
                    exit_reason = "max_time"
                
                if should_exit:
                    exit_price = current_price
                    trade_return = (exit_price - entry_price) / entry_price
                    trade_pnl = trade_return * 20000  # NQ point value
                    
                    trades.append({
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'pnl': trade_pnl,
                        'return': trade_return,
                        'bars_held': bars_in_trade,
                        'exit_reason': exit_reason,
                        'entry_time': df.index[i-1],
                        'exit_time': df.index[i]
                    })
                    
                    position = 0
                    entry_price = 0
                    bars_in_trade = 0
        
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
                'bars_held': bars_in_trade,
                'exit_reason': "final_close",
                'entry_time': df.index[-2],
                'exit_time': df.index[-1]
            })
        
        return self.comprehensive_evaluation(trades, strategy_name)
    
    def comprehensive_evaluation(self, trades, strategy_name):
        """הערכה מקיפה של אסטרטגיה"""
        
        print(f"   📊 מספר עסקאות ראשוני: {len(trades)}")
        
        if len(trades) < 200:
            print(f"   ❌ {strategy_name}: רק {len(trades)} עסקאות - פחות מ-200")
            return None
        
        # Basic metrics
        trade_returns = [t['pnl'] for t in trades]
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        
        if len(losing_trades) == 0:
            print(f"   ❌ {strategy_name}: אין עסקאות מפסידות - חשוד")
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
        
        # Drawdown calculation
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
        
        # Monthly analysis
        monthly_profits = {}
        for trade in trades:
            month = trade['exit_time'].strftime('%Y-%m')
            if month not in monthly_profits:
                monthly_profits[month] = 0
            monthly_profits[month] += trade['pnl']
        
        # Recovery time analysis
        max_recovery_months = 0
        current_recovery_months = 0
        in_drawdown = False
        
        for month, profit in sorted(monthly_profits.items()):
            if profit < 0:
                if not in_drawdown:
                    in_drawdown = True
                    current_recovery_months = 0
                current_recovery_months += 1
            else:
                if in_drawdown:
                    max_recovery_months = max(max_recovery_months, current_recovery_months)
                    in_drawdown = False
                    current_recovery_months = 0
        
        # Check all criteria
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
            'positive_monthly': all(p > 0 for p in monthly_profits.values()),
            'max_recovery_time': max_recovery_months <= 2
        }
        
        all_criteria_met = all(criteria_met.values())
        criteria_count = sum(criteria_met.values())
        
        print(f"   📈 קריטריונים: {criteria_count}/11")
        print(f"   💰 רווח: ${total_return:.0f}")
        print(f"   📊 PF: {profit_factor:.2f}")
        print(f"   📈 Sharpe: {sharpe:.2f}")
        print(f"   🎯 Win Rate: {win_rate*100:.1f}%")
        
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
            'max_recovery_months': max_recovery_months,
            'criteria_met': criteria_met,
            'all_criteria_met': all_criteria_met,
            'criteria_count': criteria_count
        }
        
        return result
    
    def run_ultimate_search(self):
        """הרצת חיפוש מתקדם ביותר"""
        
        if not self.load_data():
            return None
        
        # חישוב אינדיקטורים
        self.calculate_comprehensive_indicators()
        
        # אבחון שוק
        self.diagnose_market_patterns()
        
        print(f"\n🎯 מחפש אסטרטגיות מנצחות על 2024...")
        print(f"📈 מחיר התחלה: ${self.df_2024['close'].iloc[0]:.2f}")
        print(f"📈 מחיר סיום: ${self.df_2024['close'].iloc[-1]:.2f}")
        buy_hold = ((self.df_2024['close'].iloc[-1] / self.df_2024['close'].iloc[0]) - 1) * 100
        print(f"📊 Buy & Hold: {buy_hold:.1f}%")
        
        # רשימת אסטרטגיות מתקדמות
        strategies = [
            self.create_high_frequency_strategy,
            self.create_conservative_scalping_strategy,
            self.create_momentum_surge_strategy
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
                    elif result['criteria_count'] > best_score:
                        best_score = result['criteria_count']
                        best_partial = result
                        
            except Exception as e:
                print(f"❌ שגיאה באסטרטגיה: {e}")
        
        # תוצאות
        if winning_strategies:
            print(f"\n🏆 נמצאו {len(winning_strategies)} אסטרטגיות מנצחות!")
            
            winning_strategies.sort(key=lambda x: x['total_return'], reverse=True)
            best_strategy = winning_strategies[0]
            
            print(f"\n🥇 האסטרטגיה הטובה ביותר: {best_strategy['strategy']}")
            self.print_ultimate_report(best_strategy)
            
            return best_strategy
        
        elif best_partial:
            print(f"\n⚠️ לא נמצאה אסטרטגיה מושלמת")
            print(f"🔍 הטובה ביותר: {best_partial['strategy']} ({best_partial['criteria_count']}/11)")
            self.print_ultimate_report(best_partial)
            
            return best_partial
        
        else:
            print(f"\n❌ לא נמצאו אסטרטגיות מתאימות")
            return None
    
    def print_ultimate_report(self, result):
        """דוח מפורט ביותר"""
        print(f"\n📋 דו\"ח מפורט - {result['strategy']}")
        print("=" * 80)
        
        # Strategy description
        if "High Frequency" in result['strategy']:
            print("🎯 תיאור האסטרטגיה:")
            print("   אסטרטגיית High Frequency עם 6 שכבות תנאים:")
            print("   1. זמן: שעות מסחר אופטימליות (9-11, 13-14)")
            print("   2. מגמה: EMA 3>8>21>34 (מגמה חיובית רב-זמנית)")
            print("   3. Momentum: RSI מאוזן + MACD חיובי ומשתפר")
            print("   4. נפח: Volume ratio >1.1 + ATR מספיק + BB position 0.15-0.7")
            print("   5. Price Action: נר חיובי + body >40% + מרחק מרמות")
            print("   6. Stochastic: K בין 25-75 ומעל D")
            print()
            print("🚪 יציאה:")
            print("   מהירה: RSI>75 או BB>0.85 או EMA3<EMA8")
            print("   רגילה: RSI>70 או MACD<0 או Stoch>80 או Volume<0.7")
            print()
            print("🛡️ ניהול סיכונים:")
            print("   Stop Loss: 0.3% | Take Profit: 0.8% | Max Time: 20 bars")
        
        print(f"📊 מספר עסקאות: {result['num_trades']}")
        print(f"🎯 אחוז הצלחה: {result['win_rate']*100:.1f}%")
        print(f"💰 רווח כולל: ${result['total_return']:.0f}")
        print(f"📉 Drawdown מקסימלי: ${result['max_drawdown']:.0f}")
        print(f"💵 רווח ממוצע לעסקה: ${result['avg_trade']:.0f}")
        print(f"🔢 Profit Factor: {result['profit_factor']:.2f}")
        print(f"⚖️ יחס רווח/הפסד: {result['win_loss_ratio']:.2f}")
        print(f"📈 Sharpe Ratio: {result['sharpe_ratio']:.2f}")
        print(f"🔄 רצף הפסדים מקסימלי: {result['max_consecutive_losses']}")
        print(f"⏰ זמן התאוששות מקסימלי: {result['max_recovery_months']} חודשים")
        
        print(f"\n📅 רווח חודשי:")
        total_months = len(result['monthly_profits'])
        positive_months = sum(1 for p in result['monthly_profits'].values() if p > 0)
        print(f"   חודשים חיוביים: {positive_months}/{total_months} ({positive_months/total_months*100:.1f}%)")
        
        for month, profit in result['monthly_profits'].items():
            status = "✅" if profit > 0 else "❌"
            print(f"   {status} {month}: ${profit:.0f}")
        
        print(f"\n✅ מצב קריטריונים ({sum(result['criteria_met'].values())}/11):")
        criteria_descriptions = {
            'min_trades': f"מספר עסקאות ≥ 200: {result['num_trades']}",
            'max_drawdown': f"Drawdown ≤ $10,000: ${result['max_drawdown']:.0f}",
            'min_avg_trade': f"רווח ממוצע ≥ $30: ${result['avg_trade']:.0f}",
            'min_profit_factor': f"Profit Factor ≥ 1.7: {result['profit_factor']:.2f}",
            'min_sharpe': f"Sharpe Ratio ≥ 1.5: {result['sharpe_ratio']:.2f}",
            'min_win_loss_ratio': f"Win/Loss Ratio ≥ 1.5: {result['win_loss_ratio']:.2f}",
            'min_win_rate': f"Win Rate ≥ 50%: {result['win_rate']*100:.1f}%",
            'max_consecutive_losses': f"רצף הפסדים ≤ 6: {result['max_consecutive_losses']}",
            'positive_total_return': f"רווח כולל חיובי: ${result['total_return']:.0f}",
            'positive_monthly': f"כל החודשים חיוביים: {all(p > 0 for p in result['monthly_profits'].values())}",
            'max_recovery_time': f"התאוששות ≤ 2 חודשים: {result['max_recovery_months']}"
        }
        
        for criterion, met in result['criteria_met'].items():
            status = "✅" if met else "❌"
            description = criteria_descriptions.get(criterion, criterion)
            print(f"   {status} {description}")

def main():
    """פונקציה ראשית"""
    print("🎯 Ultimate Strategy Builder 2024")
    print("=" * 80)
    print("מערכת מתקדמת ביותר למציאת אסטרטגיות מנצחות")
    print("עם כל הקריטריונים הקשים ביותר")
    print()
    
    builder = UltimateStrategyBuilder()
    result = builder.run_ultimate_search()
    
    if result and result['all_criteria_met']:
        print(f"\n🎉 משימה הושלמה בהצלחה!")
        print(f"💎 נמצאה אסטרטגיה שעומדת בכל 11 הקריטריונים!")
        print(f"🚀 מוכנה לשימוש מיידי!")
        print(f"💰 צפויה להניב ${result['total_return']:.0f} בשנה!")
    elif result:
        print(f"\n⚠️ נמצאה אסטרטגיה חלקית")
        print(f"📊 עומדת ב-{result['criteria_count']}/11 קריטריונים")
        print(f"💡 ניתן להקל על הקריטריונים או לפתח נוסח")
    else:
        print(f"\n❌ לא נמצאו אסטרטגיות מתאימות")
        print(f"💡 יש לבחון תקופות אחרות או להתאים קריטריונים")

if __name__ == "__main__":
    main() 