"""
Strategy Engine
מנוע אסטרטגיות מתקדם עם Machine Learning ובדיקה היסטורית
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
HAS_XGBOOST = False  # מושבת זמנית עד לתיקון בעיית OpenMP
import warnings
warnings.filterwarnings('ignore')

class StrategyEngine:
    """
    מנוע אסטרטגיות מתקדם
    """
    
    def __init__(self, analyzer):
        """
        אתחול המנוע
        """
        self.analyzer = analyzer
        self.df = analyzer.df.copy()
        self.models = {}
        self.strategies = {}
        self.backtest_results = {}
        
    def create_advanced_features(self):
        """
        יצירת פיצ'רים מתקדמים למודל ML
        """
        print("🧠 יוצר פיצ'רים מתקדמים...")
        
        # פיצ'רים בסיסיים
        self.df['price_momentum'] = self.df['close'].pct_change(5)
        self.df['volume_momentum'] = self.df['volume'].pct_change(5)
        
        # יחסי מחירים
        self.df['high_low_ratio'] = self.df['high'] / self.df['low']
        self.df['close_open_ratio'] = self.df['close'] / self.df['open']
        
        # אינדיקטורים מתקדמים
        self.df['rsi_momentum'] = self.df['rsi'].diff()
        self.df['macd_momentum'] = self.df['macd'].diff()
        
        # תנודתיות מתקדמת
        self.df['volatility_5'] = self.df['returns'].rolling(5).std()
        self.df['volatility_20'] = self.df['returns'].rolling(20).std()
        self.df['volatility_ratio'] = self.df['volatility_5'] / self.df['volatility_20']
        
        # אינדיקטורי נפח
        self.df['volume_price_trend'] = ((self.df['close'] - self.df['close'].shift(1)) / 
                                        self.df['close'].shift(1)) * self.df['volume']
        
        # זיהוי patterns
        self.df['doji'] = (abs(self.df['open'] - self.df['close']) / 
                          (self.df['high'] - self.df['low'])) < 0.1
        
        self.df['hammer'] = ((self.df['high'] - self.df['low']) > 
                           3 * abs(self.df['open'] - self.df['close'])) & \
                           ((self.df['close'] - self.df['low']) / 
                            (self.df['high'] - self.df['low']) > 0.6)
        
        # מגמות
        self.df['trend_5'] = np.where(self.df['close'] > self.df['close'].shift(5), 1, 0)
        self.df['trend_20'] = np.where(self.df['close'] > self.df['close'].shift(20), 1, 0)
        
        # פיצ'רים זמניים
        self.df['hour_sin'] = np.sin(2 * np.pi * self.df['hour'] / 24)
        self.df['hour_cos'] = np.cos(2 * np.pi * self.df['hour'] / 24)
        self.df['day_sin'] = np.sin(2 * np.pi * self.df['day_of_week'] / 7)
        self.df['day_cos'] = np.cos(2 * np.pi * self.df['day_of_week'] / 7)
        
        print("✅ פיצ'רים מתקדמים נוצרו")
        
    def prepare_ml_data(self, prediction_horizon=5):
        """
        הכנת נתונים למודל ML
        """
        print(f"📊 מכין נתונים למודל ML (תחזית ל-{prediction_horizon} דקות)...")
        
        # יצירת target - האם המחיר יעלה בדקות הבאות
        self.df['future_return'] = self.df['close'].shift(-prediction_horizon) / self.df['close'] - 1
        self.df['target'] = (self.df['future_return'] > 0.001).astype(int)  # רווח של 0.1% לפחות
        
        # רשימת פיצ'רים
        feature_columns = [
            'rsi', 'macd', 'macd_signal', 'macd_histogram',
            'bb_upper', 'bb_lower', 'bb_middle',
            'sma_20', 'sma_50', 'ema_20',
            'volatility', 'volume_ratio',
            'price_momentum', 'volume_momentum',
            'high_low_ratio', 'close_open_ratio',
            'rsi_momentum', 'macd_momentum',
            'volatility_5', 'volatility_20', 'volatility_ratio',
            'volume_price_trend',
            'doji', 'hammer',
            'trend_5', 'trend_20',
            'hour_sin', 'hour_cos', 'day_sin', 'day_cos'
        ]
        
        # הכנת datasets
        data = self.df[feature_columns + ['target']].dropna()
        
        X = data[feature_columns]
        y = data['target']
        
        print(f"📈 נתונים מוכנים: {len(X)} שורות, {len(feature_columns)} פיצ'רים")
        
        return X, y, feature_columns
    
    def train_ml_models(self):
        """
        אימון מודלי ML
        """
        print("🤖 מתחיל אימון מודלי ML...")
        
        # הכנת נתונים
        X, y, feature_columns = self.prepare_ml_data()
        
        # חלוקת נתונים
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # מודלים
        models = {
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
            'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
        }
        
        # if HAS_XGBOOST:
        #     models['XGBoost'] = xgb.XGBClassifier(n_estimators=100, random_state=42)
        
        # אימון והערכה
        for name, model in models.items():
            print(f"  🔄 מאמן {name}...")
            
            if name == 'XGBoost':
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            else:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            
            accuracy = accuracy_score(y_test, y_pred)
            
            # שמירת המודל
            self.models[name] = {
                'model': model,
                'scaler': scaler,
                'accuracy': accuracy,
                'features': feature_columns
            }
            
            print(f"  ✅ {name}: דיוק {accuracy:.3f}")
        
        print("🎯 אימון מודלים הושלם!")
        
    def generate_predictions(self, model_name='RandomForest'):
        """
        יצירת חיזויים
        """
        print(f"🔮 יוצר חיזויים עם {model_name}...")
        
        if model_name not in self.models:
            print(f"❌ מודל {model_name} לא נמצא")
            return
        
        model_data = self.models[model_name]
        model = model_data['model']
        scaler = model_data['scaler']
        features = model_data['features']
        
        # הכנת נתונים לחיזוי
        X = self.df[features].dropna()
        
        if model_name == 'XGBoost':
            predictions = model.predict_proba(X)[:, 1]
        else:
            X_scaled = scaler.transform(X)
            predictions = model.predict_proba(X_scaled)[:, 1]
        
        # שמירת התחזיות
        self.df.loc[X.index, f'{model_name}_prediction'] = predictions
        
        print(f"✅ חיזויים נוצרו עם {model_name}")
        
    def create_ml_strategy(self, model_name='RandomForest', threshold=0.6):
        """
        יצירת אסטרטגיה מבוססת ML
        """
        print(f"🎯 יוצר אסטרטגיה ML עם {model_name}...")
        
        prediction_col = f'{model_name}_prediction'
        
        if prediction_col not in self.df.columns:
            self.generate_predictions(model_name)
        
        # אותות מסחר
        self.df[f'{model_name}_buy'] = self.df[prediction_col] > threshold
        self.df[f'{model_name}_sell'] = self.df[prediction_col] < (1 - threshold)
        
        strategy = {
            'name': f'ML_{model_name}',
            'buy_signals': self.df[f'{model_name}_buy'].sum(),
            'sell_signals': self.df[f'{model_name}_sell'].sum(),
            'threshold': threshold,
            'model': model_name
        }
        
        self.strategies[f'ML_{model_name}'] = strategy
        
        print(f"✅ אסטרטגיה ML נוצרה: {strategy['buy_signals']} אותות קנייה")
        return strategy
    
    def backtest_strategy(self, strategy_name, initial_capital=10000, 
                         position_size=0.1, stop_loss=0.02, take_profit=0.04):
        """
        בדיקה היסטורית של אסטרטגיה
        """
        print(f"📈 מבצע בדיקה היסטורית עבור {strategy_name}...")
        
        if strategy_name not in self.strategies:
            print(f"❌ אסטרטגיה {strategy_name} לא נמצאה")
            return
        
        strategy = self.strategies[strategy_name]
        model_name = strategy['model']
        
        # אתחול משתנים
        capital = initial_capital
        position = 0
        entry_price = 0
        trades = []
        equity_curve = []
        
        buy_col = f'{model_name}_buy'
        sell_col = f'{model_name}_sell'
        
        # מעבר על הנתונים
        for i, (timestamp, row) in enumerate(self.df.iterrows()):
            current_price = row['close']
            
            # בדיקת stop loss / take profit
            if position != 0:
                if position > 0:  # long position
                    if (current_price <= entry_price * (1 - stop_loss) or 
                        current_price >= entry_price * (1 + take_profit)):
                        # סגירת פוזיציה
                        pnl = (current_price - entry_price) * position
                        capital += pnl
                        trades.append({
                            'entry_time': entry_time,
                            'exit_time': timestamp,
                            'entry_price': entry_price,
                            'exit_price': current_price,
                            'position': position,
                            'pnl': pnl,
                            'type': 'long'
                        })
                        position = 0
                        entry_price = 0
            
            # אותות מסחר
            if position == 0:  # אין פוזיציה
                if row[buy_col] and not pd.isna(row[buy_col]):
                    # פתיחת long position
                    position = (capital * position_size) / current_price
                    entry_price = current_price
                    entry_time = timestamp
                    capital -= position * current_price
            
            # שמירת equity curve
            total_value = capital + (position * current_price if position > 0 else 0)
            equity_curve.append({
                'timestamp': timestamp,
                'equity': total_value,
                'position': position
            })
        
        # חישוב תוצאות
        if trades:
            total_pnl = sum(trade['pnl'] for trade in trades)
            winning_trades = [t for t in trades if t['pnl'] > 0]
            losing_trades = [t for t in trades if t['pnl'] < 0]
            
            results = {
                'strategy': strategy_name,
                'initial_capital': initial_capital,
                'final_capital': capital + (position * self.df['close'].iloc[-1] if position > 0 else 0),
                'total_return': (capital + (position * self.df['close'].iloc[-1] if position > 0 else 0)) / initial_capital - 1,
                'total_trades': len(trades),
                'winning_trades': len(winning_trades),
                'losing_trades': len(losing_trades),
                'win_rate': len(winning_trades) / len(trades) if trades else 0,
                'avg_win': np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0,
                'avg_loss': np.mean([t['pnl'] for t in losing_trades]) if losing_trades else 0,
                'profit_factor': abs(sum(t['pnl'] for t in winning_trades)) / abs(sum(t['pnl'] for t in losing_trades)) if losing_trades else float('inf'),
                'max_drawdown': self.calculate_max_drawdown(equity_curve),
                'sharpe_ratio': self.calculate_sharpe_ratio(equity_curve),
                'trades': trades,
                'equity_curve': equity_curve
            }
            
            self.backtest_results[strategy_name] = results
            
            print(f"✅ בדיקה היסטורית הושלמה עבור {strategy_name}")
            print(f"  📊 תשואה כוללת: {results['total_return']:.2%}")
            print(f"  📊 מספר עסקאות: {results['total_trades']}")
            print(f"  📊 אחוז הצלחה: {results['win_rate']:.2%}")
            print(f"  📊 יחס רווח: {results['profit_factor']:.2f}")
            
            return results
        else:
            print("❌ לא נמצאו עסקאות")
            return None
    
    def calculate_max_drawdown(self, equity_curve):
        """
        חישוב max drawdown
        """
        equity_values = [point['equity'] for point in equity_curve]
        peak = equity_values[0]
        max_dd = 0
        
        for value in equity_values:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
        
        return max_dd
    
    def calculate_sharpe_ratio(self, equity_curve, risk_free_rate=0.02):
        """
        חישוב Sharpe ratio
        """
        if len(equity_curve) < 2:
            return 0
        
        equity_values = [point['equity'] for point in equity_curve]
        returns = np.diff(equity_values) / equity_values[:-1]
        
        if len(returns) == 0 or np.std(returns) == 0:
            return 0
        
        excess_return = np.mean(returns) - risk_free_rate / 252  # יומי
        return excess_return / np.std(returns) * np.sqrt(252)
    
    def compare_strategies(self):
        """
        השוואת אסטרטגיות
        """
        print("🏆 משווה אסטרטגיות...")
        
        if not self.backtest_results:
            print("❌ אין תוצאות לבדיקה")
            return
        
        comparison = []
        for strategy_name, results in self.backtest_results.items():
            comparison.append({
                'strategy': strategy_name,
                'total_return': results['total_return'],
                'win_rate': results['win_rate'],
                'profit_factor': results['profit_factor'],
                'max_drawdown': results['max_drawdown'],
                'sharpe_ratio': results['sharpe_ratio'],
                'total_trades': results['total_trades']
            })
        
        # מיון לפי תשואה
        comparison.sort(key=lambda x: x['total_return'], reverse=True)
        
        print("\n🎯 השוואת אסטרטגיות:")
        print("=" * 80)
        for i, strategy in enumerate(comparison, 1):
            print(f"{i}. {strategy['strategy']}")
            print(f"   תשואה: {strategy['total_return']:.2%}")
            print(f"   אחוז הצלחה: {strategy['win_rate']:.2%}")
            print(f"   יחס רווח: {strategy['profit_factor']:.2f}")
            print(f"   Max DD: {strategy['max_drawdown']:.2%}")
            print(f"   Sharpe: {strategy['sharpe_ratio']:.2f}")
            print(f"   עסקאות: {strategy['total_trades']}")
            print("-" * 40)
        
        return comparison
    
    def run_full_strategy_analysis(self):
        """
        הרצת ניתוח אסטרטגיות מלא
        """
        print("🚀 מתחיל ניתוח אסטרטגיות מלא...")
        
        # יצירת פיצ'רים
        self.create_advanced_features()
        
        # אימון מודלים
        self.train_ml_models()
        
        # יצירת אסטרטגיות
        model_names = ['RandomForest', 'GradientBoosting']
        if HAS_XGBOOST:
            model_names.append('XGBoost')
            
        for model_name in model_names:
            strategy = self.create_ml_strategy(model_name, threshold=0.6)
            self.backtest_strategy(f'ML_{model_name}')
        
        # השוואת אסטרטגיות
        comparison = self.compare_strategies()
        
        print("\n🎉 ניתוח אסטרטגיות הושלם!")
        return comparison

if __name__ == "__main__":
    # דמו
    print("יש להריץ את זה עם analyzer קיים")
    print("דוגמא: engine = StrategyEngine(analyzer)")
    print("        results = engine.run_full_strategy_analysis()") 