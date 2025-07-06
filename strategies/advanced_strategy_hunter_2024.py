"""
Advanced Strategy Hunter 2024
מערכת מתקדמת לחיפוש אסטרטגיות מנצחות
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AdvancedStrategyHunter:
    def __init__(self):
        self.df = None
        self.df_2024 = None
        
    def load_data(self):
        """טעינת נתונים והפרדת 2024"""
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
    
    def calculate_advanced_indicators(self, df):
        """חישוב אינדיקטורים מתקדמים"""
        print("📊 מחשב אינדיקטורים מתקדמים...")
        
        # Basic indicators
        df['returns'] = df['close'].pct_change()
        df['hl2'] = (df['high'] + df['low']) / 2
        df['hlc3'] = (df['high'] + df['low'] + df['close']) / 3
        df['ohlc4'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
        
        # Moving Averages - multiple timeframes
        for period in [5, 8, 12, 13, 21, 26, 34, 55, 89, 144]:
            df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
            df[f'ema_{period}'] = df['close'].ewm(span=period).mean()
        
        # RSI with different periods
        for period in [14, 21, 28]:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            df[f'rsi_{period}'] = 100 - (100 / (1 + rs))
        
        # MACD variants
        df['macd_12_26'] = df['ema_12'] - df['ema_26']
        df['macd_signal_12_26'] = df['macd_12_26'].ewm(span=9).mean()
        df['macd_hist_12_26'] = df['macd_12_26'] - df['macd_signal_12_26']
        
        # Bollinger Bands
        for period in [20, 50]:
            df[f'bb_middle_{period}'] = df['close'].rolling(window=period).mean()
            bb_std = df['close'].rolling(window=period).std()
            df[f'bb_upper_{period}'] = df[f'bb_middle_{period}'] + (bb_std * 2)
            df[f'bb_lower_{period}'] = df[f'bb_middle_{period}'] - (bb_std * 2)
            df[f'bb_width_{period}'] = df[f'bb_upper_{period}'] - df[f'bb_lower_{period}']
            df[f'bb_position_{period}'] = (df['close'] - df[f'bb_lower_{period}']) / df[f'bb_width_{period}']
        
        # Stochastic
        df['lowest_low_14'] = df['low'].rolling(window=14).min()
        df['highest_high_14'] = df['high'].rolling(window=14).max()
        df['stoch_k'] = 100 * (df['close'] - df['lowest_low_14']) / (df['highest_high_14'] - df['lowest_low_14'])
        df['stoch_d'] = df['stoch_k'].rolling(window=3).mean()
        
        # Volume indicators
        df['volume_ma_20'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma_20']
        df['volume_spike'] = df['volume_ratio'] > 1.5
        
        # Price action indicators
        df['body_size'] = abs(df['close'] - df['open'])
        df['upper_shadow'] = df['high'] - np.maximum(df['open'], df['close'])
        df['lower_shadow'] = np.minimum(df['open'], df['close']) - df['low']
        df['total_range'] = df['high'] - df['low']
        
        # Volatility
        df['atr_14'] = df['total_range'].rolling(window=14).mean()
        df['volatility_20'] = df['returns'].rolling(window=20).std()
        
        # Time-based features
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month
        df['is_market_open'] = df['hour'].between(9, 15)
        
        # Trend strength
        df['trend_strength_20'] = df['close'].rolling(window=20).apply(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0])
        
        # Support/Resistance levels
        df['resistance_20'] = df['high'].rolling(window=20).max()
        df['support_20'] = df['low'].rolling(window=20).min()
        df['distance_to_resistance'] = (df['resistance_20'] - df['close']) / df['close']
        df['distance_to_support'] = (df['close'] - df['support_20']) / df['close']
        
        return df
    
    def realistic_backtest(self, df, entry_signals, exit_signals, strategy_name):
        """Backtesting מתקדם עם ביצוע realistic"""
        print(f"🧪 מבצע backtesting מתקדם עבור {strategy_name}...")
        
        # Initialize
        df = df.copy()
        df['signal'] = 0
        df['position'] = 0
        df['entry_price'] = 0
        df['exit_price'] = 0
        df['trade_return'] = 0
        df['cumulative_return'] = 0
        df['drawdown'] = 0
        
        position = 0
        entry_price = 0
        trades = []
        equity_curve = []
        current_equity = 100000  # starting capital
        peak_equity = 100000
        
        for i in range(1, len(df)):
            current_bar = df.iloc[i]
            prev_bar = df.iloc[i-1]
            
            # Entry logic (signal on close, execute on next open)
            if position == 0 and entry_signals.iloc[i-1]:
                if i < len(df) - 1:  # Make sure we have next bar
                    position = 1
                    entry_price = current_bar['open']  # Execute on current open (next bar after signal)
                    df.iloc[i, df.columns.get_loc('signal')] = 1
                    df.iloc[i, df.columns.get_loc('position')] = 1
                    df.iloc[i, df.columns.get_loc('entry_price')] = entry_price
            
            # Exit logic (signal on close, execute on next open)
            elif position == 1 and exit_signals.iloc[i-1]:
                if i < len(df) - 1:  # Make sure we have next bar
                    exit_price = current_bar['open']  # Execute on current open
                    
                    # Calculate trade return
                    trade_return = (exit_price - entry_price) / entry_price
                    trade_pnl = trade_return * 20000  # NQ point value
                    
                    # Record trade
                    trades.append({
                        'entry_time': df.index[i-1],
                        'exit_time': df.index[i],
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'return': trade_return,
                        'pnl': trade_pnl,
                        'bars_held': 1
                    })
                    
                    # Update equity
                    current_equity += trade_pnl
                    peak_equity = max(peak_equity, current_equity)
                    
                    # Update dataframe
                    df.iloc[i, df.columns.get_loc('signal')] = -1
                    df.iloc[i, df.columns.get_loc('position')] = 0
                    df.iloc[i, df.columns.get_loc('exit_price')] = exit_price
                    df.iloc[i, df.columns.get_loc('trade_return')] = trade_return
                    
                    position = 0
                    entry_price = 0
            
            # Update position
            df.iloc[i, df.columns.get_loc('position')] = position
            
            # Update equity curve
            if position == 1:
                unrealized_pnl = (current_bar['close'] - entry_price) / entry_price * 20000
                current_unrealized_equity = 100000 + sum([t['pnl'] for t in trades]) + unrealized_pnl
            else:
                current_unrealized_equity = current_equity
            
            equity_curve.append(current_unrealized_equity)
            
            # Update drawdown
            peak_equity = max(peak_equity, current_unrealized_equity)
            drawdown = current_unrealized_equity - peak_equity
            df.iloc[i, df.columns.get_loc('drawdown')] = drawdown
        
        # Close final position if still open
        if position == 1 and len(df) > 1:
            exit_price = df.iloc[-1]['close']
            trade_return = (exit_price - entry_price) / entry_price
            trade_pnl = trade_return * 20000
            
            trades.append({
                'entry_time': df.index[-2],
                'exit_time': df.index[-1],
                'entry_price': entry_price,
                'exit_price': exit_price,
                'return': trade_return,
                'pnl': trade_pnl,
                'bars_held': 1
            })
        
        return df, trades, equity_curve
    
    def evaluate_strategy(self, trades, equity_curve, strategy_name):
        """הערכת ביצועי אסטרטגיה לפי הקריטריונים"""
        
        if len(trades) < 200:
            return None  # לא עומד בקריטריון מספר עסקאות
        
        # חישוב מדדים בסיסיים
        trade_returns = [t['pnl'] for t in trades]
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        
        total_return = sum(trade_returns)
        num_trades = len(trades)
        win_rate = len(winning_trades) / num_trades if num_trades > 0 else 0
        avg_trade = total_return / num_trades if num_trades > 0 else 0
        
        # Profit Factor
        gross_profit = sum([t['pnl'] for t in winning_trades])
        gross_loss = abs(sum([t['pnl'] for t in losing_trades]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Win/Loss ratio
        avg_win = gross_profit / len(winning_trades) if len(winning_trades) > 0 else 0
        avg_loss = gross_loss / len(losing_trades) if len(losing_trades) > 0 else 0
        win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0
        
        # Drawdown
        max_drawdown = min(equity_curve) - max(equity_curve) if equity_curve else 0
        
        # Sharpe Ratio
        if len(trade_returns) > 1:
            returns_mean = np.mean(trade_returns)
            returns_std = np.std(trade_returns)
            sharpe = returns_mean / returns_std * np.sqrt(252) if returns_std > 0 else 0
        else:
            sharpe = 0
        
        # רצף הפסדים
        consecutive_losses = 0
        max_consecutive_losses = 0
        for trade in trades:
            if trade['pnl'] < 0:
                consecutive_losses += 1
                max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
            else:
                consecutive_losses = 0
        
        # בדיקת קריטריונים
        criteria_met = {
            'min_trades': num_trades >= 200,
            'max_drawdown': max_drawdown >= -10000,
            'min_avg_trade': avg_trade >= 30,
            'min_profit_factor': profit_factor >= 1.7,
            'min_sharpe': sharpe >= 1.5,
            'min_win_loss_ratio': win_loss_ratio >= 1.5,
            'min_win_rate': win_rate >= 0.5,
            'max_consecutive_losses': max_consecutive_losses <= 6,
            'positive_total_return': total_return > 0
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
            'criteria_met': criteria_met,
            'all_criteria_met': all_criteria_met,
            'monthly_profits': self.calculate_monthly_profits(trades)
        }
        
        return result
    
    def calculate_monthly_profits(self, trades):
        """חישוב רווחים חודשיים"""
        monthly_profits = {}
        
        for trade in trades:
            month = trade['exit_time'].strftime('%Y-%m')
            if month not in monthly_profits:
                monthly_profits[month] = 0
            monthly_profits[month] += trade['pnl']
        
        return monthly_profits
    
    def strategy_advanced_rsi_momentum(self, df):
        """אסטרטגיית RSI מתקדמת עם מומנטום"""
        
        # תנאי כניסה מתקדמים
        entry_conditions = (
            (df['rsi_14'] < 35) &  # RSI oversold but not extreme
            (df['rsi_14'] > 25) &  # Not too oversold
            (df['close'] > df['ema_21']) &  # Above medium-term trend
            (df['close'] > df['bb_lower_20']) &  # Above BB lower
            (df['volume_ratio'] > 1.2) &  # Volume confirmation
            (df['is_market_open']) &  # Market hours only
            (df['hour'].isin([9, 10, 11, 13, 14])) &  # Best trading hours
            (df['macd_hist_12_26'] > 0) &  # MACD bullish
            (df['stoch_k'] < 40) &  # Stochastic oversold
            (df['trend_strength_20'] > -0.02)  # Not in strong downtrend
        )
        
        # תנאי יציאה
        exit_conditions = (
            (df['rsi_14'] > 65) |  # RSI overbought
            (df['close'] < df['ema_13']) |  # Below short-term trend
            (df['macd_hist_12_26'] < -0.5) |  # MACD bearish
            (df['stoch_k'] > 80)  # Stochastic overbought
        )
        
        return entry_conditions, exit_conditions
    
    def strategy_bb_breakout_refined(self, df):
        """אסטרטגיית Bollinger Bands מתקדמת"""
        
        # תנאי כניסה
        entry_conditions = (
            (df['close'] > df['bb_lower_20']) &  # Above BB lower
            (df['close'] < df['bb_middle_20']) &  # Below BB middle
            (df['bb_position_20'] > 0.1) &  # Not at extreme bottom
            (df['bb_position_20'] < 0.4) &  # Not too high
            (df['volume_ratio'] > 1.3) &  # Volume confirmation
            (df['rsi_14'] > 30) &  # RSI not extreme
            (df['rsi_14'] < 50) &  # RSI in lower half
            (df['ema_13'] > df['ema_21']) &  # Short-term bullish
            (df['is_market_open']) &
            (df['hour'].isin([9, 10, 11, 13, 14])) &
            (df['bb_width_20'] > df['bb_width_20'].rolling(20).mean())  # Sufficient volatility
        )
        
        # תנאי יציאה
        exit_conditions = (
            (df['close'] > df['bb_upper_20']) |  # Hit upper BB
            (df['bb_position_20'] > 0.85) |  # Near upper BB
            (df['rsi_14'] > 70) |  # RSI overbought
            (df['ema_13'] < df['ema_21'])  # Trend change
        )
        
        return entry_conditions, exit_conditions
    
    def strategy_multi_timeframe_momentum(self, df):
        """אסטרטגיית מומנטום רב-זמנית"""
        
        # תנאי כניסה
        entry_conditions = (
            (df['ema_8'] > df['ema_13']) &  # Short-term bullish
            (df['ema_13'] > df['ema_21']) &  # Medium-term bullish
            (df['close'] > df['ema_34']) &  # Above longer-term trend
            (df['rsi_14'] > 40) &  # RSI not oversold
            (df['rsi_14'] < 60) &  # RSI not overbought
            (df['macd_12_26'] > df['macd_signal_12_26']) &  # MACD bullish
            (df['macd_hist_12_26'] > df['macd_hist_12_26'].shift(1)) &  # MACD improving
            (df['stoch_k'] > 20) &  # Stochastic above extreme
            (df['stoch_k'] < 80) &  # Stochastic below extreme
            (df['volume_ratio'] > 1.1) &  # Volume confirmation
            (df['is_market_open']) &
            (df['hour'].isin([9, 10, 11, 13, 14])) &
            (df['volatility_20'] > df['volatility_20'].rolling(50).quantile(0.3))  # Sufficient volatility
        )
        
        # תנאי יציאה
        exit_conditions = (
            (df['ema_8'] < df['ema_13']) |  # Short-term bearish
            (df['rsi_14'] > 75) |  # RSI overbought
            (df['macd_hist_12_26'] < 0) |  # MACD bearish
            (df['stoch_k'] > 85)  # Stochastic overbought
        )
        
        return entry_conditions, exit_conditions
    
    def strategy_volume_price_action(self, df):
        """אסטרטגיית Volume Price Action"""
        
        # תנאי כניסה
        entry_conditions = (
            (df['volume_ratio'] > 1.5) &  # Strong volume
            (df['close'] > df['open']) &  # Bullish bar
            (df['body_size'] > df['total_range'] * 0.6) &  # Strong body
            (df['lower_shadow'] > df['upper_shadow']) &  # Support visible
            (df['close'] > df['ema_21']) &  # Above trend
            (df['rsi_14'] > 35) &  # RSI not extreme
            (df['rsi_14'] < 65) &  # RSI not overbought
            (df['distance_to_support'] > 0.002) &  # Not at support
            (df['distance_to_resistance'] > 0.005) &  # Room to resistance
            (df['is_market_open']) &
            (df['hour'].isin([9, 10, 11, 13, 14])) &
            (df['atr_14'] > df['atr_14'].rolling(50).quantile(0.4))  # Sufficient volatility
        )
        
        # תנאי יציאה
        exit_conditions = (
            (df['volume_ratio'] < 0.8) |  # Volume drying up
            (df['close'] < df['open']) |  # Bearish bar
            (df['rsi_14'] > 70) |  # RSI overbought
            (df['close'] < df['ema_13']) |  # Below short-term trend
            (df['distance_to_resistance'] < 0.002)  # Near resistance
        )
        
        return entry_conditions, exit_conditions
    
    def strategy_adaptive_mean_reversion(self, df):
        """אסטרטגיית Mean Reversion אדפטיבית"""
        
        # חישוב רמת volatility
        df['vol_regime'] = df['volatility_20'] > df['volatility_20'].rolling(100).median()
        
        # תנאי כניסה - מותאמים לרמת volatility
        low_vol_entry = (
            (df['rsi_14'] < 30) &
            (df['bb_position_20'] < 0.2) &
            (df['stoch_k'] < 25)
        )
        
        high_vol_entry = (
            (df['rsi_14'] < 40) &
            (df['bb_position_20'] < 0.3) &
            (df['stoch_k'] < 35)
        )
        
        entry_conditions = (
            (
                (~df['vol_regime'] & low_vol_entry) |
                (df['vol_regime'] & high_vol_entry)
            ) &
            (df['close'] > df['ema_55']) &  # Above long-term trend
            (df['volume_ratio'] > 1.1) &  # Volume confirmation
            (df['is_market_open']) &
            (df['hour'].isin([9, 10, 11, 13, 14])) &
            (df['trend_strength_20'] > -0.03)  # Not in strong downtrend
        )
        
        # תנאי יציאה - מותאמים לרמת volatility
        low_vol_exit = (
            (df['rsi_14'] > 70) |
            (df['bb_position_20'] > 0.8)
        )
        
        high_vol_exit = (
            (df['rsi_14'] > 65) |
            (df['bb_position_20'] > 0.75)
        )
        
        exit_conditions = (
            (~df['vol_regime'] & low_vol_exit) |
            (df['vol_regime'] & high_vol_exit) |
            (df['close'] < df['ema_21'])  # Below medium-term trend
        )
        
        return entry_conditions, exit_conditions
    
    def run_strategy_hunt(self):
        """הרצת חיפוש אסטרטגיות"""
        
        if not self.load_data():
            return
        
        # חישוב אינדיקטורים
        self.df_2024 = self.calculate_advanced_indicators(self.df_2024)
        
        print(f"\n🎯 חיפוש אסטרטגיות מנצחות על 2024...")
        print(f"📊 תקופה: {self.df_2024.index.min()} עד {self.df_2024.index.max()}")
        print(f"📈 מחיר התחלה: ${self.df_2024['close'].iloc[0]:.2f}")
        print(f"📈 מחיר סיום: ${self.df_2024['close'].iloc[-1]:.2f}")
        
        # רשימת אסטרטגיות לבדיקה
        strategies = [
            ('Advanced RSI Momentum', self.strategy_advanced_rsi_momentum),
            ('BB Breakout Refined', self.strategy_bb_breakout_refined),
            ('Multi-Timeframe Momentum', self.strategy_multi_timeframe_momentum),
            ('Volume Price Action', self.strategy_volume_price_action),
            ('Adaptive Mean Reversion', self.strategy_adaptive_mean_reversion)
        ]
        
        winning_strategies = []
        
        for name, strategy_func in strategies:
            print(f"\n🔍 בודק: {name}")
            
            try:
                # הרצת האסטרטגיה
                entry_signals, exit_signals = strategy_func(self.df_2024)
                
                # Backtesting
                df_result, trades, equity_curve = self.realistic_backtest(
                    self.df_2024, entry_signals, exit_signals, name
                )
                
                # הערכת תוצאות
                result = self.evaluate_strategy(trades, equity_curve, name)
                
                if result and result['all_criteria_met']:
                    winning_strategies.append(result)
                    print(f"✅ {name} - עומד בכל הקריטריונים!")
                    self.print_strategy_results(result)
                elif result:
                    print(f"❌ {name} - לא עומד בקריטריונים")
                    failed_criteria = [k for k, v in result['criteria_met'].items() if not v]
                    print(f"   נכשל ב: {', '.join(failed_criteria)}")
                else:
                    print(f"❌ {name} - פחות מ-200 עסקאות")
                    
            except Exception as e:
                print(f"❌ {name} - שגיאה: {e}")
        
        # דווח על התוצאות
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
            print(f"💡 ממשיך לחיפוש מתקדם...")
            
            # חיפוש מתקדם עם פרמטרים מותאמים
            return self.advanced_parameter_search()
    
    def advanced_parameter_search(self):
        """חיפוש מתקדם עם אופטימיזציה של פרמטרים"""
        print(f"\n🔬 מבצע חיפוש מתקדם עם אופטימיזציה...")
        
        # נסיון עם פרמטרים שונים
        rsi_periods = [12, 14, 16, 18, 21]
        bb_periods = [15, 20, 25, 30]
        volume_thresholds = [1.1, 1.2, 1.3, 1.4, 1.5]
        
        best_strategy = None
        best_score = 0
        
        for rsi_period in rsi_periods:
            for bb_period in bb_periods:
                for vol_threshold in volume_thresholds:
                    
                    try:
                        # חישוב אינדיקטורים עם פרמטרים מותאמים
                        df_test = self.df_2024.copy()
                        
                        # RSI מותאם
                        delta = df_test['close'].diff()
                        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
                        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
                        rs = gain / loss
                        df_test['rsi_custom'] = 100 - (100 / (1 + rs))
                        
                        # BB מותאם
                        df_test['bb_middle_custom'] = df_test['close'].rolling(window=bb_period).mean()
                        bb_std = df_test['close'].rolling(window=bb_period).std()
                        df_test['bb_upper_custom'] = df_test['bb_middle_custom'] + (bb_std * 2)
                        df_test['bb_lower_custom'] = df_test['bb_middle_custom'] - (bb_std * 2)
                        
                        # אסטרטגיה מותאמת
                        entry_conditions = (
                            (df_test['rsi_custom'] < 38) &
                            (df_test['rsi_custom'] > 28) &
                            (df_test['close'] > df_test['bb_lower_custom']) &
                            (df_test['close'] < df_test['bb_middle_custom']) &
                            (df_test['volume_ratio'] > vol_threshold) &
                            (df_test['ema_13'] > df_test['ema_21']) &
                            (df_test['is_market_open']) &
                            (df_test['hour'].isin([9, 10, 11, 13, 14]))
                        )
                        
                        exit_conditions = (
                            (df_test['rsi_custom'] > 68) |
                            (df_test['close'] > df_test['bb_upper_custom']) |
                            (df_test['ema_13'] < df_test['ema_21'])
                        )
                        
                        # Backtesting
                        df_result, trades, equity_curve = self.realistic_backtest(
                            df_test, entry_conditions, exit_conditions, 
                            f"Optimized RSI{rsi_period}_BB{bb_period}_Vol{vol_threshold}"
                        )
                        
                        # הערכה
                        result = self.evaluate_strategy(trades, equity_curve, 
                                                      f"Optimized RSI{rsi_period}_BB{bb_period}_Vol{vol_threshold}")
                        
                        if result and result['all_criteria_met']:
                            score = result['total_return'] * result['sharpe_ratio'] * result['profit_factor']
                            if score > best_score:
                                best_score = score
                                best_strategy = result
                                print(f"✅ נמצאה אסטרטגיה מנצחת: RSI{rsi_period}_BB{bb_period}_Vol{vol_threshold}")
                                print(f"   תשואה: ${result['total_return']:.0f}, Sharpe: {result['sharpe_ratio']:.2f}")
                    
                    except Exception as e:
                        continue
        
        if best_strategy:
            print(f"\n🏆 האסטרטגיה הטובה ביותר נמצאה!")
            self.print_detailed_report(best_strategy)
            return best_strategy
        else:
            print(f"\n❌ לא נמצאו אסטרטגיות מנצחות גם בחיפוש המתקדם")
            return None
    
    def print_strategy_results(self, result):
        """הדפסת תוצאות בסיסיות"""
        print(f"  📊 מספר עסקאות: {result['num_trades']}")
        print(f"  💰 תשואה כוללת: ${result['total_return']:.0f}")
        print(f"  🎯 אחוז הצלחה: {result['win_rate']*100:.1f}%")
        print(f"  📈 Sharpe Ratio: {result['sharpe_ratio']:.2f}")
        print(f"  🔢 Profit Factor: {result['profit_factor']:.2f}")
    
    def print_detailed_report(self, result):
        """הדפסת דו"ח מפורט"""
        print(f"\n📋 דו\"ח מפורט - {result['strategy']}")
        print("=" * 60)
        print(f"📊 מספר עסקאות: {result['num_trades']}")
        print(f"🎯 אחוז הצלחה: {result['win_rate']*100:.1f}%")
        print(f"💰 רווח כולל: ${result['total_return']:.0f}")
        print(f"📉 Drawdown מקסימלי: ${result['max_drawdown']:.0f}")
        print(f"💵 רווח ממוצע לעסקה: ${result['avg_trade']:.0f}")
        print(f"🔢 Profit Factor: {result['profit_factor']:.2f}")
        print(f"⚖️ יחס רווח/הפסד: {result['win_loss_ratio']:.2f}")
        print(f"📈 Sharpe Ratio: {result['sharpe_ratio']:.2f}")
        print(f"🔄 רצף הפסדים מקסימלי: {result['max_consecutive_losses']}")
        
        # רווחים חודשיים
        print(f"\n📅 רווחים חודשיים:")
        for month, profit in result['monthly_profits'].items():
            print(f"  {month}: ${profit:.0f}")
        
        # סטטוס קריטריונים
        print(f"\n✅ עמידה בקריטריונים:")
        criteria_names = {
            'min_trades': 'מספר עסקאות מינימלי',
            'max_drawdown': 'Drawdown מקסימלי',
            'min_avg_trade': 'רווח ממוצע לעסקה',
            'min_profit_factor': 'Profit Factor מינימלי',
            'min_sharpe': 'Sharpe Ratio מינימלי',
            'min_win_loss_ratio': 'יחס רווח/הפסד מינימלי',
            'min_win_rate': 'אחוז הצלחה מינימלי',
            'max_consecutive_losses': 'רצף הפסדים מקסימלי',
            'positive_total_return': 'רווח כולל חיובי'
        }
        
        for criterion, met in result['criteria_met'].items():
            status = "✅" if met else "❌"
            print(f"  {status} {criteria_names.get(criterion, criterion)}")

def main():
    """פונקציה ראשית"""
    print("🎯 Advanced Strategy Hunter 2024")
    print("=" * 60)
    print("מחפש אסטרטגיות מנצחות עם קריטריונים מחמירים")
    print()
    
    hunter = AdvancedStrategyHunter()
    result = hunter.run_strategy_hunt()
    
    if result:
        print(f"\n🎉 משימה הושלמה בהצלחה!")
        print(f"💎 נמצאה אסטרטגיה מנצחת: {result['strategy']}")
    else:
        print(f"\n🔍 לא נמצאו אסטרטגיות שעומדות בכל הקריטריונים")
        print(f"💡 ייתכן שצריך להקל על הקריטריונים או לבדוק תקופות אחרות")

if __name__ == "__main__":
    main() 