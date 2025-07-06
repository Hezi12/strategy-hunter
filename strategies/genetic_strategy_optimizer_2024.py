"""
Genetic Strategy Optimizer 2024
אלגוריתם גנטי למציאת אסטרטגיות מנצחות
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class GeneticStrategyOptimizer:
    def __init__(self):
        self.df = None
        self.df_2024 = None
        self.population_size = 50
        self.generations = 20
        self.mutation_rate = 0.1
        
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
            
            # חישוב אינדיקטורים בסיסיים
            self.calculate_indicators()
            
            return True
            
        except Exception as e:
            print(f"❌ שגיאה: {e}")
            return False
    
    def calculate_indicators(self):
        """חישוב אינדיקטורים"""
        print("📊 מחשב אינדיקטורים...")
        
        df = self.df_2024
        
        # Basic
        df['returns'] = df['close'].pct_change()
        df['hour'] = df.index.hour
        df['is_market_open'] = df['hour'].between(9, 15)
        
        # Moving averages
        periods = [5, 8, 13, 21, 34, 55, 89]
        for period in periods:
            df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
            df[f'ema_{period}'] = df['close'].ewm(span=period).mean()
        
        # RSI
        for period in [14, 21]:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            df[f'rsi_{period}'] = 100 - (100 / (1 + rs))
        
        # MACD
        df['macd'] = df['ema_13'] - df['ema_21']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # Bollinger Bands
        df['bb_middle'] = df['close'].rolling(window=20).mean()
        bb_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        
        # Volume
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        # Stochastic
        df['stoch_k'] = self.calculate_stochastic(df, 14)
        
        # ATR
        df['atr'] = self.calculate_atr(df, 14)
        
        # Price position
        df['price_position'] = (df['close'] - df['low']) / (df['high'] - df['low'])
        
    def calculate_stochastic(self, df, period):
        """חישוב Stochastic"""
        lowest_low = df['low'].rolling(window=period).min()
        highest_high = df['high'].rolling(window=period).max()
        return 100 * (df['close'] - lowest_low) / (highest_high - lowest_low)
    
    def calculate_atr(self, df, period):
        """חישוב ATR"""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()
    
    def create_random_strategy(self):
        """יצירת אסטרטגיה רנדומלית"""
        
        # Parameters for entry
        entry_params = {
            'rsi_period': random.choice([14, 21]),
            'rsi_lower': random.uniform(25, 45),
            'rsi_upper': random.uniform(55, 75),
            'bb_position': random.uniform(0.1, 0.4),
            'volume_threshold': random.uniform(1.0, 2.0),
            'ema_short': random.choice([8, 13, 21]),
            'ema_long': random.choice([21, 34, 55]),
            'macd_threshold': random.uniform(-1, 1),
            'stoch_lower': random.uniform(10, 40),
            'stoch_upper': random.uniform(60, 90),
            'hour_start': random.choice([9, 10]),
            'hour_end': random.choice([14, 15, 16]),
            'use_volume': random.choice([True, False]),
            'use_macd': random.choice([True, False]),
            'use_stoch': random.choice([True, False]),
            'use_bb': random.choice([True, False])
        }
        
        # Parameters for exit
        exit_params = {
            'rsi_exit_high': random.uniform(60, 80),
            'rsi_exit_low': random.uniform(20, 40),
            'bb_exit_position': random.uniform(0.7, 0.95),
            'macd_exit_threshold': random.uniform(-1, 1),
            'stoch_exit_high': random.uniform(70, 90),
            'profit_target': random.uniform(0.005, 0.02),
            'stop_loss': random.uniform(0.005, 0.02),
            'max_bars': random.randint(5, 100),
            'use_profit_target': random.choice([True, False]),
            'use_stop_loss': random.choice([True, False]),
            'use_max_bars': random.choice([True, False])
        }
        
        return {'entry': entry_params, 'exit': exit_params}
    
    def apply_strategy(self, strategy):
        """הפעלת אסטרטגיה על הנתונים"""
        df = self.df_2024.copy()
        
        entry_params = strategy['entry']
        exit_params = strategy['exit']
        
        # Entry conditions
        entry_conditions = pd.Series(True, index=df.index)
        
        # RSI condition
        rsi_col = f"rsi_{entry_params['rsi_period']}"
        entry_conditions &= (df[rsi_col] > entry_params['rsi_lower']) & (df[rsi_col] < entry_params['rsi_upper'])
        
        # EMA condition
        ema_short_col = f"ema_{entry_params['ema_short']}"
        ema_long_col = f"ema_{entry_params['ema_long']}"
        entry_conditions &= df[ema_short_col] > df[ema_long_col]
        
        # Bollinger Bands
        if entry_params['use_bb']:
            bb_position = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
            entry_conditions &= bb_position < entry_params['bb_position']
        
        # Volume
        if entry_params['use_volume']:
            entry_conditions &= df['volume_ratio'] > entry_params['volume_threshold']
        
        # MACD
        if entry_params['use_macd']:
            entry_conditions &= df['macd_hist'] > entry_params['macd_threshold']
        
        # Stochastic
        if entry_params['use_stoch']:
            entry_conditions &= (df['stoch_k'] > entry_params['stoch_lower']) & (df['stoch_k'] < entry_params['stoch_upper'])
        
        # Time filter
        entry_conditions &= df['hour'].between(entry_params['hour_start'], entry_params['hour_end'])
        entry_conditions &= df['is_market_open']
        
        # Exit conditions
        exit_conditions = pd.Series(False, index=df.index)
        
        # RSI exit
        rsi_col = f"rsi_{entry_params['rsi_period']}"
        exit_conditions |= df[rsi_col] > exit_params['rsi_exit_high']
        
        # EMA exit
        exit_conditions |= df[ema_short_col] < df[ema_long_col]
        
        # Bollinger Bands exit
        bb_position = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        exit_conditions |= bb_position > exit_params['bb_exit_position']
        
        # MACD exit
        exit_conditions |= df['macd_hist'] < exit_params['macd_exit_threshold']
        
        # Stochastic exit
        exit_conditions |= df['stoch_k'] > exit_params['stoch_exit_high']
        
        return self.backtest_strategy(df, entry_conditions, exit_conditions, strategy)
    
    def backtest_strategy(self, df, entry_signals, exit_signals, strategy):
        """Backtesting מהיר"""
        
        position = 0
        entry_price = 0
        trades = []
        bars_in_trade = 0
        
        for i in range(1, len(df)):
            current_price = df.iloc[i]['open']  # Realistic execution
            
            # Entry
            if position == 0 and entry_signals.iloc[i-1] and i < len(df) - 1:
                position = 1
                entry_price = current_price
                bars_in_trade = 0
                
            # Exit
            elif position == 1:
                bars_in_trade += 1
                should_exit = False
                
                # Signal exit
                if exit_signals.iloc[i-1]:
                    should_exit = True
                
                # Profit target
                if strategy['exit']['use_profit_target']:
                    if current_price > entry_price * (1 + strategy['exit']['profit_target']):
                        should_exit = True
                
                # Stop loss
                if strategy['exit']['use_stop_loss']:
                    if current_price < entry_price * (1 - strategy['exit']['stop_loss']):
                        should_exit = True
                
                # Max bars
                if strategy['exit']['use_max_bars']:
                    if bars_in_trade >= strategy['exit']['max_bars']:
                        should_exit = True
                
                if should_exit:
                    exit_price = current_price
                    trade_return = (exit_price - entry_price) / entry_price
                    trade_pnl = trade_return * 20000  # NQ point value
                    
                    trades.append({
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'pnl': trade_pnl,
                        'bars_held': bars_in_trade,
                        'return': trade_return
                    })
                    
                    position = 0
                    entry_price = 0
                    bars_in_trade = 0
        
        return trades
    
    def evaluate_strategy(self, trades):
        """הערכת אסטרטגיה"""
        
        if len(trades) < 200:
            return 0  # לא עומד בקריטריון
        
        # חישוב מדדים
        trade_returns = [t['pnl'] for t in trades]
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        
        if len(losing_trades) == 0:
            return 0  # חשוד
        
        total_return = sum(trade_returns)
        num_trades = len(trades)
        win_rate = len(winning_trades) / num_trades
        avg_trade = total_return / num_trades
        
        # Profit Factor
        gross_profit = sum([t['pnl'] for t in winning_trades])
        gross_loss = abs(sum([t['pnl'] for t in losing_trades]))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Win/Loss ratio
        avg_win = gross_profit / len(winning_trades) if len(winning_trades) > 0 else 0
        avg_loss = gross_loss / len(losing_trades) if len(losing_trades) > 0 else 0
        win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0
        
        # Sharpe Ratio
        returns_std = np.std(trade_returns) if len(trade_returns) > 1 else 1
        sharpe = (avg_trade / returns_std) * np.sqrt(252) if returns_std > 0 else 0
        
        # Drawdown (simplified)
        equity_curve = np.cumsum(trade_returns)
        peak = np.maximum.accumulate(equity_curve)
        drawdown = equity_curve - peak
        max_drawdown = np.min(drawdown)
        
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
        criteria_score = 0
        
        if num_trades >= 200:
            criteria_score += 1
        if max_drawdown >= -10000:
            criteria_score += 1
        if avg_trade >= 30:
            criteria_score += 1
        if profit_factor >= 1.7:
            criteria_score += 1
        if sharpe >= 1.5:
            criteria_score += 1
        if win_loss_ratio >= 1.5:
            criteria_score += 1
        if win_rate >= 0.5:
            criteria_score += 1
        if max_consecutive_losses <= 6:
            criteria_score += 1
        if total_return > 0:
            criteria_score += 1
        
        # ציון משוקלל
        if criteria_score == 9:  # כל הקריטריונים
            fitness = total_return * profit_factor * sharpe * 100
        else:
            fitness = criteria_score * total_return * 0.1  # ציון חלקי
        
        return fitness, {
            'num_trades': num_trades,
            'win_rate': win_rate,
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'avg_trade': avg_trade,
            'profit_factor': profit_factor,
            'win_loss_ratio': win_loss_ratio,
            'sharpe_ratio': sharpe,
            'max_consecutive_losses': max_consecutive_losses,
            'criteria_score': criteria_score
        }
    
    def crossover(self, parent1, parent2):
        """הכלאה בין שתי אסטרטגיות"""
        child = {}
        
        # Entry parameters
        child['entry'] = {}
        for key in parent1['entry']:
            if random.random() < 0.5:
                child['entry'][key] = parent1['entry'][key]
            else:
                child['entry'][key] = parent2['entry'][key]
        
        # Exit parameters
        child['exit'] = {}
        for key in parent1['exit']:
            if random.random() < 0.5:
                child['exit'][key] = parent1['exit'][key]
            else:
                child['exit'][key] = parent2['exit'][key]
        
        return child
    
    def mutate(self, strategy):
        """מוטציה באסטרטגיה"""
        mutated = strategy.copy()
        
        # Entry mutations
        if random.random() < self.mutation_rate:
            mutated['entry']['rsi_lower'] = random.uniform(25, 45)
        if random.random() < self.mutation_rate:
            mutated['entry']['rsi_upper'] = random.uniform(55, 75)
        if random.random() < self.mutation_rate:
            mutated['entry']['volume_threshold'] = random.uniform(1.0, 2.0)
        if random.random() < self.mutation_rate:
            mutated['entry']['bb_position'] = random.uniform(0.1, 0.4)
        
        # Exit mutations
        if random.random() < self.mutation_rate:
            mutated['exit']['rsi_exit_high'] = random.uniform(60, 80)
        if random.random() < self.mutation_rate:
            mutated['exit']['profit_target'] = random.uniform(0.005, 0.02)
        if random.random() < self.mutation_rate:
            mutated['exit']['stop_loss'] = random.uniform(0.005, 0.02)
        
        return mutated
    
    def run_genetic_optimization(self):
        """הרצת אופטימיזציה גנטית"""
        
        if not self.load_data():
            return None
        
        print(f"\n🧬 מתחיל אופטימיזציה גנטית...")
        print(f"📊 גודל אוכלוסיה: {self.population_size}")
        print(f"🔄 מספר דורות: {self.generations}")
        
        # יצירת אוכלוסיה ראשונית
        population = []
        for _ in range(self.population_size):
            strategy = self.create_random_strategy()
            population.append(strategy)
        
        best_strategy = None
        best_fitness = 0
        best_stats = None
        
        for generation in range(self.generations):
            print(f"\n🔄 דור {generation + 1}/{self.generations}")
            
            # הערכת אוכלוסיה
            fitness_scores = []
            stats_list = []
            
            for i, strategy in enumerate(population):
                try:
                    trades = self.apply_strategy(strategy)
                    result = self.evaluate_strategy(trades)
                    
                    if isinstance(result, tuple):
                        fitness, stats = result
                    else:
                        fitness = result
                        stats = {'criteria_score': 0}
                    
                    fitness_scores.append(fitness)
                    stats_list.append(stats)
                    
                    if fitness > best_fitness:
                        best_fitness = fitness
                        best_strategy = strategy.copy()
                        best_stats = stats.copy()
                        
                        if stats['criteria_score'] == 9:
                            print(f"✅ נמצאה אסטרטגיה מושלמת! דור {generation + 1}, אינדיבידואל {i + 1}")
                            print(f"   💰 רווח: ${stats['total_return']:.0f}")
                            print(f"   📊 PF: {stats['profit_factor']:.2f}")
                            print(f"   📈 Sharpe: {stats['sharpe_ratio']:.2f}")
                            
                except Exception as e:
                    fitness_scores.append(0)
                    stats_list.append({'criteria_score': 0})
            
            # מיון לפי fitness
            sorted_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)
            
            # הצגת הטובים ביותר
            top_5 = sorted_indices[:5]
            print(f"   🏆 5 הטובים ביותר: fitness = {[fitness_scores[i] for i in top_5]}")
            print(f"   📊 קריטריונים: {[stats_list[i]['criteria_score'] for i in top_5]}")
            
            # אם מצאנו אסטרטגיה מושלמת
            if best_stats and best_stats['criteria_score'] == 9:
                print(f"\n🎉 נמצאה אסטרטגיה מושלמת!")
                break
            
            # יצירת דור חדש
            new_population = []
            
            # שמירת הטובים ביותר (elitism)
            elite_size = self.population_size // 5
            for i in range(elite_size):
                new_population.append(population[sorted_indices[i]])
            
            # הכלאה
            while len(new_population) < self.population_size:
                # בחירת הורים
                parent1_idx = random.choice(sorted_indices[:self.population_size//2])
                parent2_idx = random.choice(sorted_indices[:self.population_size//2])
                
                parent1 = population[parent1_idx]
                parent2 = population[parent2_idx]
                
                # הכלאה ומוטציה
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                
                new_population.append(child)
            
            population = new_population
        
        return best_strategy, best_stats
    
    def print_final_report(self, strategy, stats):
        """הדפסת דוח סופי"""
        print(f"\n📋 דו\"ח סופי - אסטרטגיה מנצחת")
        print("=" * 60)
        
        if stats:
            print(f"📊 מספר עסקאות: {stats['num_trades']}")
            print(f"🎯 אחוז הצלחה: {stats['win_rate']*100:.1f}%")
            print(f"💰 רווח כולל: ${stats['total_return']:.0f}")
            print(f"📉 Drawdown מקסימלי: ${stats['max_drawdown']:.0f}")
            print(f"💵 רווח ממוצע לעסקה: ${stats['avg_trade']:.0f}")
            print(f"🔢 Profit Factor: {stats['profit_factor']:.2f}")
            print(f"⚖️ יחס רווח/הפסד: {stats['win_loss_ratio']:.2f}")
            print(f"📈 Sharpe Ratio: {stats['sharpe_ratio']:.2f}")
            print(f"🔄 רצף הפסדים מקסימלי: {stats['max_consecutive_losses']}")
            print(f"✅ קריטריונים שנענו: {stats['criteria_score']}/9")
        
        print(f"\n🎯 פרמטרי האסטרטגיה:")
        print("כניסה:")
        for key, value in strategy['entry'].items():
            print(f"  {key}: {value}")
        
        print("יציאה:")
        for key, value in strategy['exit'].items():
            print(f"  {key}: {value}")

def main():
    """פונקציה ראשית"""
    print("🧬 Genetic Strategy Optimizer 2024")
    print("=" * 60)
    print("אופטימיזציה גנטית למציאת אסטרטגיות מנצחות")
    print()
    
    optimizer = GeneticStrategyOptimizer()
    result = optimizer.run_genetic_optimization()
    
    if result:
        strategy, stats = result
        optimizer.print_final_report(strategy, stats)
        
        if stats and stats['criteria_score'] == 9:
            print(f"\n🎉 משימה הושלמה בהצלחה!")
            print(f"💎 נמצאה אסטרטגיה שעומדת בכל הקריטריונים!")
        else:
            print(f"\n⚠️ לא נמצאה אסטרטגיה מושלמת")
            print(f"🔍 הטובה ביותר: {stats['criteria_score']}/9 קריטריונים")
    else:
        print(f"\n❌ לא נמצאו אסטרטגיות מתאימות")

if __name__ == "__main__":
    main() 