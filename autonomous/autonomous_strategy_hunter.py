"""
Autonomous Strategy Hunter
תוחצנמ תויגטרטסא תאיצמל תימונוטוא תכרעמ
IA-ב תולת אלל תימוקמ הצר
"""

import pandas as pd
import numpy as np
import random
import time
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class AutonomousStrategyHunter:
    def __init__(self):
        self.df = None
        self.df_2024 = None
        self.population_size = 100
        self.elite_size = 20
        self.mutation_rate = 0.15
        self.best_strategies = []
        self.generation = 0
        
    def load_data(self):
        """םינותנ תניעט"""
        print("🤖 ...םינותנ ןעוט - תימונוטוא תכרעמ")
        
        try:
            self.df = pd.read_csv('../data/NQ2018.csv')
            self.df['datetime'] = pd.to_datetime(self.df['datetime'])
            self.df.set_index('datetime', inplace=True)
            
            # הפרדת 2024
            self.df_2024 = self.df[self.df.index.year == 2024].copy()
            
            print(f"✅ 4202-מ םינותנ תודוקנ {len(self.df_2024):,} ונעטנ")
            self.calculate_indicators()
            
            return True
            
        except Exception as e:
            print(f"❌ {e} :האיגש")
            return False
    
    def calculate_indicators(self):
        """םירוטקידניא בושיח"""
        print("📊 ...םירוטקידניא בשחמ")
        
        df = self.df_2024
        
        # Basic
        df['hour'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['is_market_open'] = df['hour'].between(9, 15)
        df['is_weekday'] = df['day_of_week'] < 5
        
        # Price action
        df['is_green'] = df['close'] > df['open']
        df['body'] = abs(df['close'] - df['open'])
        df['range'] = df['high'] - df['low']
        df['body_ratio'] = df['body'] / df['range']
        
        # Moving averages
        for period in [5, 10, 20, 50]:
            df[f'ma_{period}'] = df['close'].rolling(window=period).mean()
            df[f'above_ma_{period}'] = df['close'] > df[f'ma_{period}']
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Volume
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        df['high_volume'] = df['volume_ratio'] > 1.5
        
        # Price momentum
        for period in [3, 5, 10]:
            df[f'momentum_{period}'] = (df['close'] / df['close'].shift(period) - 1) * 100
            df[f'positive_momentum_{period}'] = df[f'momentum_{period}'] > 0
        
        # Support/Resistance
        df['recent_high'] = df['high'].rolling(window=20).max()
        df['recent_low'] = df['low'].rolling(window=20).min()
        df['near_resistance'] = df['close'] > df['recent_high'] * 0.995
        df['near_support'] = df['close'] < df['recent_low'] * 1.005
        
        print("✅ םיבושחמ םירוטקידניא")
    
    def create_random_dna(self):
        """יצירת DNA רנדומלי לאסטרטגיה"""
        return {
            # Entry conditions
            'use_trend': random.choice([True, False]),
            'ma_period': random.choice([5, 10, 20, 50]),
            'use_rsi': random.choice([True, False]),
            'rsi_low': random.randint(20, 40),
            'rsi_high': random.randint(60, 80),
            'use_volume': random.choice([True, False]),
            'volume_threshold': random.uniform(1.0, 2.0),
            'use_momentum': random.choice([True, False]),
            'momentum_period': random.choice([3, 5, 10]),
            'use_price_action': random.choice([True, False]),
            'min_body_ratio': random.uniform(0.3, 0.8),
            'use_time_filter': random.choice([True, False]),
            'allowed_hours': random.sample([9, 10, 11, 12, 13, 14, 15], random.randint(3, 7)),
            
            # Exit conditions
            'use_profit_target': random.choice([True, False]),
            'profit_target': random.uniform(0.003, 0.015),
            'use_stop_loss': random.choice([True, False]),
            'stop_loss': random.uniform(0.002, 0.008),
            'use_time_exit': random.choice([True, False]),
            'max_bars': random.randint(5, 50),
            'use_rsi_exit': random.choice([True, False]),
            'rsi_exit_high': random.randint(70, 85),
            'use_trend_exit': random.choice([True, False]),
            'use_resistance_exit': random.choice([True, False])
        }
    
    def apply_strategy(self, dna):
        """הפעלת אסטרטגיה על הנתונים"""
        df = self.df_2024.copy()
        
        # Build entry conditions
        entry_condition = pd.Series(True, index=df.index)
        
        # Market hours
        entry_condition &= df['is_market_open'] & df['is_weekday']
        
        # Time filter
        if dna['use_time_filter']:
            entry_condition &= df['hour'].isin(dna['allowed_hours'])
        
        # Trend filter
        if dna['use_trend']:
            ma_col = f"above_ma_{dna['ma_period']}"
            entry_condition &= df[ma_col]
        
        # RSI filter
        if dna['use_rsi']:
            entry_condition &= (df['rsi'] > dna['rsi_low']) & (df['rsi'] < dna['rsi_high'])
        
        # Volume filter
        if dna['use_volume']:
            entry_condition &= df['volume_ratio'] > dna['volume_threshold']
        
        # Momentum filter
        if dna['use_momentum']:
            momentum_col = f"positive_momentum_{dna['momentum_period']}"
            entry_condition &= df[momentum_col]
        
        # Price action filter
        if dna['use_price_action']:
            entry_condition &= df['is_green'] & (df['body_ratio'] > dna['min_body_ratio'])
        
        return self.backtest_strategy(df, entry_condition, dna)
    
    def backtest_strategy(self, df, entry_signals, dna):
        """Backtesting אסטרטגיה"""
        position = 0
        entry_price = 0
        trades = []
        bars_in_trade = 0
        
        for i in range(1, len(df)):
            if i >= len(df) - 1:
                break
            
            current_price = df.iloc[i]['open']
            
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
                
                # Profit target
                if dna['use_profit_target']:
                    if current_price >= entry_price * (1 + dna['profit_target']):
                        should_exit = True
                        exit_reason = "profit_target"
                
                # Stop loss
                if dna['use_stop_loss'] and not should_exit:
                    if current_price <= entry_price * (1 - dna['stop_loss']):
                        should_exit = True
                        exit_reason = "stop_loss"
                
                # Time exit
                if dna['use_time_exit'] and not should_exit:
                    if bars_in_trade >= dna['max_bars']:
                        should_exit = True
                        exit_reason = "time_exit"
                
                # RSI exit
                if dna['use_rsi_exit'] and not should_exit:
                    if df.iloc[i]['rsi'] > dna['rsi_exit_high']:
                        should_exit = True
                        exit_reason = "rsi_exit"
                
                # Trend exit
                if dna['use_trend_exit'] and not should_exit:
                    ma_col = f"above_ma_{dna['ma_period']}"
                    if not df.iloc[i][ma_col]:
                        should_exit = True
                        exit_reason = "trend_exit"
                
                # Resistance exit
                if dna['use_resistance_exit'] and not should_exit:
                    if df.iloc[i]['near_resistance']:
                        should_exit = True
                        exit_reason = "resistance_exit"
                
                if should_exit:
                    exit_price = current_price
                    trade_return = (exit_price - entry_price) / entry_price
                    trade_pnl = trade_return * 20000
                    
                    trades.append({
                        'pnl': trade_pnl,
                        'return': trade_return,
                        'bars_held': bars_in_trade,
                        'exit_reason': exit_reason
                    })
                    
                    position = 0
                    entry_price = 0
                    bars_in_trade = 0
        
        return trades
    
    def evaluate_fitness(self, trades):
        """הערכת כושר אסטרטגיה"""
        if len(trades) < 50:  # Minimum trades for evaluation
            return 0
        
        trade_pnls = [t['pnl'] for t in trades]
        total_return = sum(trade_pnls)
        
        if total_return <= 0:
            return 0
        
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        
        if len(losing_trades) == 0 or len(winning_trades) == 0:
            return 0
        
        win_rate = len(winning_trades) / len(trades)
        avg_trade = total_return / len(trades)
        
        # Profit Factor
        gross_profit = sum([t['pnl'] for t in winning_trades])
        gross_loss = abs(sum([t['pnl'] for t in losing_trades]))
        profit_factor = gross_profit / gross_loss
        
        # Sharpe-like metric
        returns_std = np.std(trade_pnls)
        sharpe_like = avg_trade / returns_std if returns_std > 0 else 0
        
        # Max consecutive losses
        consecutive_losses = 0
        max_consecutive_losses = 0
        for trade in trades:
            if trade['pnl'] < 0:
                consecutive_losses += 1
                max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
            else:
                consecutive_losses = 0
        
        # Fitness calculation - prioritize strategies that meet criteria
        fitness = 0
        
        # Base fitness from return
        fitness += total_return * 0.001
        
        # Bonus for meeting criteria
        if len(trades) >= 200:
            fitness += 100
        if avg_trade >= 30:
            fitness += 100
        if profit_factor >= 1.7:
            fitness += 100
        if win_rate >= 0.5:
            fitness += 100
        if max_consecutive_losses <= 6:
            fitness += 100
        if sharpe_like >= 1.0:
            fitness += 100
        
        return max(0, fitness)
    
    def crossover(self, parent1, parent2):
        """הכלאה בין שני הורים"""
        child = {}
        for key in parent1:
            if random.random() < 0.5:
                child[key] = parent1[key]
            else:
                child[key] = parent2[key]
        return child
    
    def mutate(self, dna):
        """מוטציה ב-DNA"""
        mutated = dna.copy()
        
        for key, value in mutated.items():
            if random.random() < self.mutation_rate:
                if isinstance(value, bool):
                    mutated[key] = random.choice([True, False])
                elif isinstance(value, int):
                    if key == 'rsi_low':
                        mutated[key] = random.randint(20, 40)
                    elif key == 'rsi_high':
                        mutated[key] = random.randint(60, 80)
                    elif key == 'ma_period':
                        mutated[key] = random.choice([5, 10, 20, 50])
                    elif key == 'momentum_period':
                        mutated[key] = random.choice([3, 5, 10])
                    elif key == 'max_bars':
                        mutated[key] = random.randint(5, 50)
                    elif key == 'rsi_exit_high':
                        mutated[key] = random.randint(70, 85)
                elif isinstance(value, float):
                    if key == 'volume_threshold':
                        mutated[key] = random.uniform(1.0, 2.0)
                    elif key == 'profit_target':
                        mutated[key] = random.uniform(0.003, 0.015)
                    elif key == 'stop_loss':
                        mutated[key] = random.uniform(0.002, 0.008)
                    elif key == 'min_body_ratio':
                        mutated[key] = random.uniform(0.3, 0.8)
                elif isinstance(value, list):
                    mutated[key] = random.sample([9, 10, 11, 12, 13, 14, 15], random.randint(3, 7))
        
        return mutated
    
    def save_best_strategy(self, dna, fitness, trades):
        """שמירת אסטרטגיה טובה"""
        strategy_data = {
            'generation': self.generation,
            'timestamp': datetime.now().isoformat(),
            'dna': dna,
            'fitness': fitness,
            'num_trades': len(trades),
            'total_return': sum([t['pnl'] for t in trades]),
            'win_rate': len([t for t in trades if t['pnl'] > 0]) / len(trades) if trades else 0
        }
        
        self.best_strategies.append(strategy_data)
        
        # שמירה לקובץ
        with open('../results/../results/best_strategies.json', 'w') as f:
            json.dump(self.best_strategies, f, indent=2)
        
        print(f"💾 {fitness:.1f} :ssintf ,{self.generation} רוד - הבוט היגטרטסא הרמשנ")
    
    def check_winning_criteria(self, trades):
        """בדיקת קריטריונים מנצחים"""
        if len(trades) < 200:
            return False, "עסקאות < 200"
        
        trade_pnls = [t['pnl'] for t in trades]
        total_return = sum(trade_pnls)
        winning_trades = [t for t in trades if t['pnl'] > 0]
        losing_trades = [t for t in trades if t['pnl'] < 0]
        
        if len(losing_trades) == 0:
            return False, "אין עסקאות מפסידות"
        
        avg_trade = total_return / len(trades)
        win_rate = len(winning_trades) / len(trades)
        
        gross_profit = sum([t['pnl'] for t in winning_trades])
        gross_loss = abs(sum([t['pnl'] for t in losing_trades]))
        profit_factor = gross_profit / gross_loss
        
        avg_win = gross_profit / len(winning_trades)
        avg_loss = gross_loss / len(losing_trades)
        win_loss_ratio = avg_win / avg_loss
        
        returns_std = np.std(trade_pnls)
        sharpe = (avg_trade / returns_std) * np.sqrt(252*24) if returns_std > 0 else 0
        
        # Max consecutive losses
        consecutive_losses = 0
        max_consecutive_losses = 0
        for trade in trades:
            if trade['pnl'] < 0:
                consecutive_losses += 1
                max_consecutive_losses = max(max_consecutive_losses, consecutive_losses)
            else:
                consecutive_losses = 0
        
        # Drawdown
        equity_curve = np.cumsum(trade_pnls) + 100000
        peak = np.maximum.accumulate(equity_curve)
        drawdown = equity_curve - peak
        max_drawdown = np.min(drawdown)
        
        criteria = {
            'min_trades': len(trades) >= 200,
            'max_drawdown': max_drawdown >= -10000,
            'min_avg_trade': avg_trade >= 30,
            'min_profit_factor': profit_factor >= 1.7,
            'min_sharpe': sharpe >= 1.5,
            'min_win_loss_ratio': win_loss_ratio >= 1.5,
            'min_win_rate': win_rate >= 0.5,
            'max_consecutive_losses': max_consecutive_losses <= 6,
            'positive_total_return': total_return > 0
        }
        
        all_met = all(criteria.values())
        failed = [k for k, v in criteria.items() if not v]
        
        if all_met:
            return True, "כל הקריטריונים מתקיימים!"
        else:
            return False, f"נכשל ב: {failed}"
    
    def run_autonomous_evolution(self):
        """הרצת אבולוציה אוטונומית"""
        if not self.load_data():
            return
        
        print(f"\n🤖 !תימונוטוא היצולובא ליחתמ")
        print(f"📊 {self.population_size} :הייסולכוא לדוג")
        print(f"🧬 {self.mutation_rate} :היצטומ רועיש")
        print(f"🎯 םינוירטירקה לכ םע היגטרטסא תאיצמ :הרטמ")
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')} :ןמזה")
        print("🔄 הריצעל C+lrtC ץחל")
        print("-" * 60)
        
        # יצירת אוכלוסיה ראשונית
        population = []
        for _ in range(self.population_size):
            population.append(self.create_random_dna())
        
        try:
            while True:
                self.generation += 1
                
                # הערכת אוכלוסיה
                fitness_scores = []
                for individual in population:
                    trades = self.apply_strategy(individual)
                    fitness = self.evaluate_fitness(trades)
                    fitness_scores.append((fitness, individual, trades))
                
                # מיון לפי fitness
                fitness_scores.sort(key=lambda x: x[0], reverse=True)
                
                # הצגת תוצאות
                best_fitness, best_individual, best_trades = fitness_scores[0]
                avg_fitness = np.mean([f[0] for f in fitness_scores])
                
                print(f"🔄 {len(best_trades):3d} :sedart | {avg_fitness:6.1f} :gvA | {best_fitness:8.1f} :tseB | {self.generation:4d} רוד")
                
                # בדיקת קריטריונים מנצחים
                is_winner, criteria_status = self.check_winning_criteria(best_trades)
                
                if is_winner:
                    print(f"\n🎉 !{self.generation} רודב תחצנמ היגטרטסא האצמנ")
                    print(f"✅ {criteria_status}")
                    self.save_winning_strategy(best_individual, best_trades)
                    break
                
                # שמירת אסטרטגיות טובות
                if best_fitness > 300:  # Threshold for good strategies (lowered)
                    self.save_best_strategy(best_individual, best_fitness, best_trades)
                
                # שמירת סטטוס כל 10 דורות
                if self.generation % 10 == 0:
                    self.save_best_strategy(best_individual, best_fitness, best_trades)
                
                # יצירת דור חדש
                new_population = []
                
                # Elitism - שמירת הטובים ביותר
                for i in range(self.elite_size):
                    new_population.append(fitness_scores[i][1])
                
                # הכלאה ומוטציה
                while len(new_population) < self.population_size:
                    # בחירת הורים מהטובים ביותר
                    parent1 = random.choice(fitness_scores[:self.population_size//2])[1]
                    parent2 = random.choice(fitness_scores[:self.population_size//2])[1]
                    
                    # הכלאה ומוטציה
                    child = self.crossover(parent1, parent2)
                    child = self.mutate(child)
                    
                    new_population.append(child)
                
                population = new_population
                
                # עצירה כל 100 דורות לבדיקה
                if self.generation % 100 == 0:
                    print(f"\n📊 סיכום ביניים - דור {self.generation}")
                    print(f"🏆 הטובה ביותר עד כה: {best_fitness:.1f}")
                    print(f"📈 עסקאות: {len(best_trades)}")
                    if best_trades:
                        total_return = sum([t['pnl'] for t in best_trades])
                        print(f"💰 תשואה: ${total_return:.0f}")
                    print(f"❌ {criteria_status}")
                    print("-" * 60)
        
        except KeyboardInterrupt:
            print(f"\n⏹️  {self.generation} רודב תינדי הריצע")
            print(f"🏆 {best_fitness:.1f} :רתוי הבוטה")
            if self.best_strategies:
                print(f"💾 תובוט תויגטרטסא {len(self.best_strategies)} ורמשנ")
    
    def save_winning_strategy(self, dna, trades):
        """שמירת אסטרטגיה מנצחת"""
        trade_pnls = [t['pnl'] for t in trades]
        total_return = sum(trade_pnls)
        winning_trades = [t for t in trades if t['pnl'] > 0]
        win_rate = len(winning_trades) / len(trades)
        
        winning_strategy = {
            'timestamp': datetime.now().isoformat(),
            'generation': self.generation,
            'dna': dna,
            'num_trades': len(trades),
            'total_return': total_return,
            'win_rate': win_rate,
            'avg_trade': total_return / len(trades)
        }
        
        # שמירה לקובץ
        with open('../results/../results/winning_strategy_2024.json', 'w') as f:
            json.dump(winning_strategy, f, indent=2)
        
        print(f"\n💎 אסטרטגיה מנצחת נשמרה!")
        print(f"📁 קובץ: ../results/../results/winning_strategy_2024.json")
        print(f"📊 עסקאות: {len(trades)}")
        print(f"💰 תשואה: ${total_return:.0f}")
        print(f"🎯 אחוז הצלחה: {win_rate*100:.1f}%")

def main():
    """תישאר היצקנופ"""
    print("🤖 Autonomous Strategy Hunter")
    print("=" * 60)
    print("תוחצנמ תויגטרטסא תאיצמל תימונוטוא תכרעמ")
    print("IA-ב תולת אלל תימוקמ הצר")
    print("םלשומ ןורתפ תאיצמל דע 7/42 תויגטרטסא שפחמ")
    print()
    
    hunter = AutonomousStrategyHunter()
    hunter.run_autonomous_evolution()

if __name__ == "__main__":
    main() 