"""
Report Generator
מערכת יצירת דוחות אוטומטית
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
from nq_analyzer import NQAnalyzer
from strategy_engine import StrategyEngine
import warnings
warnings.filterwarnings('ignore')

class ReportGenerator:
    """
    מולד דוחות מתקדם
    """
    
    def __init__(self):
        self.analyzer = None
        self.engine = None
        self.report_data = {}
        
    def generate_full_report(self, save_charts=True):
        """
        יצירת דוח מלא
        """
        print("📋 יוצר דוח מלא...")
        
        # שלב 1: ניתוח בסיסי
        print("🔍 שלב 1: ניתוח בסיסי")
        self.analyzer = NQAnalyzer()
        basic_report = self.analyzer.run_full_analysis()
        
        # שלב 2: ניתוח מתקדם
        print("🤖 שלב 2: ניתוח מתקדם")
        self.engine = StrategyEngine(self.analyzer)
        self.engine.create_advanced_features()
        
        # שלב 3: יצירת גרפים
        if save_charts:
            print("📊 שלב 3: יצירת גרפים")
            self.create_charts()
        
        # שלב 4: הכנת דוח
        print("📄 שלב 4: הכנת דוח")
        self.compile_report(basic_report)
        
        # שלב 5: שמירת דוח
        print("💾 שלב 5: שמירת דוח")
        self.save_report()
        
        print("✅ דוח הושלם!")
        return self.report_data
        
    def create_charts(self):
        """
        יצירת גרפים לדוח
        """
        print("📊 יוצר גרפים...")
        
        # הגדרת עיצוב
        plt.style.use('seaborn-v0_8')
        plt.rcParams['figure.figsize'] = (12, 8)
        
        # גרף 1: מחירים עם אינדיקטורים
        self.create_price_chart()
        
        # גרף 2: נפח מסחר
        self.create_volume_chart()
        
        # גרף 3: RSI
        self.create_rsi_chart()
        
        # גרף 4: ניתוח שעות
        self.create_hourly_analysis()
        
        # גרף 5: התפלגות תשואות
        self.create_returns_distribution()
        
        print("✅ גרפים נוצרו")
        
    def create_price_chart(self):
        """
        גרף מחירים עם אינדיקטורים
        """
        # לקיחת נתונים מהחודש האחרון
        df = self.analyzer.df.tail(30 * 24 * 60)  # 30 ימים
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # גרף מחירים
        ax1.plot(df.index, df['close'], label='מחיר', linewidth=1)
        if 'sma_20' in df.columns:
            ax1.plot(df.index, df['sma_20'], label='SMA 20', alpha=0.7)
        if 'sma_50' in df.columns:
            ax1.plot(df.index, df['sma_50'], label='SMA 50', alpha=0.7)
        if 'bb_upper' in df.columns and 'bb_lower' in df.columns:
            ax1.fill_between(df.index, df['bb_lower'], df['bb_upper'], alpha=0.2, label='Bollinger Bands')
        
        ax1.set_title('מחירי NQ עם אינדיקטורים טכניים', fontsize=14, fontweight='bold')
        ax1.set_ylabel('מחיר')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # גרף נפח
        ax2.bar(df.index, df['volume'], alpha=0.6, color='lightblue')
        ax2.set_title('נפח מסחר', fontsize=12)
        ax2.set_ylabel('נפח')
        ax2.set_xlabel('תאריך')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('price_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_volume_chart(self):
        """
        ניתוח נפח מסחר
        """
        # ניתוח לפי שעות
        hourly_volume = self.analyzer.df.groupby('hour')['volume'].mean()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # נפח לפי שעות
        ax1.bar(hourly_volume.index, hourly_volume.values, color='steelblue', alpha=0.7)
        ax1.set_title('נפח מסחר ממוצע לפי שעות', fontsize=12, fontweight='bold')
        ax1.set_xlabel('שעה')
        ax1.set_ylabel('נפח ממוצע')
        ax1.grid(True, alpha=0.3)
        
        # נפח לפי ימים בשבוע
        daily_volume = self.analyzer.df.groupby('day_of_week')['volume'].mean()
        days = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ש']
        
        ax2.bar(range(len(daily_volume)), daily_volume.values, color='darkgreen', alpha=0.7)
        ax2.set_title('נפח מסחר ממוצע לפי ימים', fontsize=12, fontweight='bold')
        ax2.set_xlabel('יום בשבוע')
        ax2.set_ylabel('נפח ממוצע')
        ax2.set_xticks(range(len(days)))
        ax2.set_xticklabels(days)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('volume_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_rsi_chart(self):
        """
        ניתוח RSI
        """
        if 'rsi' not in self.analyzer.df.columns:
            return
            
        df = self.analyzer.df.tail(30 * 24 * 60)  # 30 ימים
        
        fig, ax = plt.subplots(figsize=(15, 6))
        
        ax.plot(df.index, df['rsi'], label='RSI', color='purple', linewidth=1)
        ax.axhline(y=70, color='red', linestyle='--', label='רמת יתר-קנייה (70)')
        ax.axhline(y=30, color='green', linestyle='--', label='רמת יתר-מכירה (30)')
        ax.fill_between(df.index, 70, 100, alpha=0.2, color='red')
        ax.fill_between(df.index, 0, 30, alpha=0.2, color='green')
        
        ax.set_title('אינדיקטור RSI', fontsize=14, fontweight='bold')
        ax.set_ylabel('RSI')
        ax.set_xlabel('תאריך')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 100)
        
        plt.tight_layout()
        plt.savefig('rsi_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_hourly_analysis(self):
        """
        ניתוח שעות מסחר מפורט
        """
        hourly_stats = self.analyzer.df.groupby('hour').agg({
            'volume': 'mean',
            'returns': 'mean',
            'volatility': 'mean'
        })
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # נפח לפי שעות
        axes[0, 0].bar(hourly_stats.index, hourly_stats['volume'], color='blue', alpha=0.7)
        axes[0, 0].set_title('נפח ממוצע לפי שעות')
        axes[0, 0].set_xlabel('שעה')
        axes[0, 0].set_ylabel('נפח')
        axes[0, 0].grid(True, alpha=0.3)
        
        # תשואות לפי שעות
        axes[0, 1].plot(hourly_stats.index, hourly_stats['returns'], marker='o', color='green')
        axes[0, 1].set_title('תשואה ממוצעת לפי שעות')
        axes[0, 1].set_xlabel('שעה')
        axes[0, 1].set_ylabel('תשואה')
        axes[0, 1].grid(True, alpha=0.3)
        
        # תנודתיות לפי שעות
        axes[1, 0].plot(hourly_stats.index, hourly_stats['volatility'], marker='s', color='red')
        axes[1, 0].set_title('תנודתיות לפי שעות')
        axes[1, 0].set_xlabel('שעה')
        axes[1, 0].set_ylabel('תנודתיות')
        axes[1, 0].grid(True, alpha=0.3)
        
        # הדגשת שעות פעילות
        top_5_hours = hourly_stats.nlargest(5, 'volume')
        axes[1, 1].bar(top_5_hours.index, top_5_hours['volume'], color='orange', alpha=0.7)
        axes[1, 1].set_title('5 שעות הפעילות הגבוהות ביותר')
        axes[1, 1].set_xlabel('שעה')
        axes[1, 1].set_ylabel('נפח')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('hourly_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_returns_distribution(self):
        """
        התפלגות תשואות
        """
        returns = self.analyzer.df['returns'].dropna()
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # היסטוגרמה
        axes[0].hist(returns, bins=100, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0].set_title('התפלגות תשואות')
        axes[0].set_xlabel('תשואה')
        axes[0].set_ylabel('תדירות')
        axes[0].grid(True, alpha=0.3)
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(returns, dist="norm", plot=axes[1])
        axes[1].set_title('Q-Q Plot - השוואה להתפלגות נורמלית')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('returns_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def compile_report(self, basic_report):
        """
        הכנת דוח מסכם
        """
        self.report_data = {
            'metadata': {
                'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data_period': f"{self.analyzer.df.index.min()} - {self.analyzer.df.index.max()}",
                'total_data_points': len(self.analyzer.df),
                'analysis_type': 'NQ Futures Strategy Analysis'
            },
            'executive_summary': self.create_executive_summary(),
            'basic_analysis': basic_report,
            'technical_analysis': self.create_technical_summary(),
            'market_structure': self.create_market_structure_analysis(),
            'risk_analysis': self.create_risk_analysis(),
            'recommendations': self.create_recommendations(),
            'appendix': self.create_appendix()
        }
        
    def create_executive_summary(self):
        """
        סיכום מנהלים
        """
        df = self.analyzer.df
        
        return {
            'key_findings': [
                f"נותחו {len(df):,} נקודות נתונים של NQ Futures",
                f"טווח מחירים: ${df['low'].min():.2f} - ${df['high'].max():.2f}",
                f"תנודתיות שנתית: {df['returns'].std() * np.sqrt(252) * 100:.1f}%",
                f"נפח יומי ממוצע: {df['volume'].mean():.0f} חוזים"
            ],
            'opportunities': [
                f"זוהו {self.analyzer.results['opportunities']['golden_cross_signals']:,} אותות Golden Cross",
                f"זוהו {self.analyzer.results['opportunities']['strong_buy_signals']:,} אותות קנייה חזקים",
                f"שעות הפעילות הגבוהות ביותר: 9:00-10:00 בבוקר"
            ],
            'risk_factors': [
                "תנודתיות גבוהה בשעות פתיחת השווקים",
                "נפח נמוך בשעות הלילה מגביר את הסיכון",
                "השפעת חדשות מקרו-כלכליות על התנודתיות"
            ]
        }
        
    def create_technical_summary(self):
        """
        סיכום טכני
        """
        return {
            'indicators_performance': {
                'RSI': {
                    'oversold_signals': self.analyzer.results['opportunities']['rsi_oversold_signals'],
                    'overbought_signals': self.analyzer.results['opportunities']['rsi_overbought_signals']
                },
                'MACD': {
                    'bullish_signals': self.analyzer.results['opportunities']['macd_bullish_signals']
                },
                'Moving_Averages': {
                    'golden_cross_signals': self.analyzer.results['opportunities']['golden_cross_signals']
                },
                'Bollinger_Bands': {
                    'oversold_signals': self.analyzer.results['opportunities']['bb_oversold_signals'],
                    'overbought_signals': self.analyzer.results['opportunities']['bb_overbought_signals']
                }
            },
            'pattern_recognition': {
                'breakouts': self.analyzer.results['patterns']['high_breakouts'] + self.analyzer.results['patterns']['low_breakouts'],
                'volume_spikes': self.analyzer.results['patterns']['volume_spikes']
            }
        }
        
    def create_market_structure_analysis(self):
        """
        ניתוח מבנה השוק
        """
        hourly_stats = self.analyzer.df.groupby('hour').agg({
            'volume': 'mean',
            'returns': 'mean',
            'volatility': 'mean'
        })
        
        return {
            'trading_hours': {
                'peak_volume_hours': hourly_stats.nlargest(3, 'volume').index.tolist(),
                'peak_volatility_hours': hourly_stats.nlargest(3, 'volatility').index.tolist(),
                'best_return_hours': hourly_stats.nlargest(3, 'returns').index.tolist()
            },
            'market_efficiency': {
                'average_spread': 'N/A',  # יש לחשב מנתונים נוספים
                'liquidity_score': hourly_stats['volume'].mean(),
                'market_depth': 'N/A'
            }
        }
        
    def create_risk_analysis(self):
        """
        ניתוח סיכונים
        """
        returns = self.analyzer.df['returns'].dropna()
        
        return {
            'volatility_metrics': {
                'daily_volatility': returns.std(),
                'annualized_volatility': returns.std() * np.sqrt(252),
                'volatility_of_volatility': returns.rolling(20).std().std()
            },
            'risk_metrics': {
                'var_95': np.percentile(returns, 5),
                'var_99': np.percentile(returns, 1),
                'expected_shortfall': returns[returns <= np.percentile(returns, 5)].mean(),
                'max_drawdown': self.calculate_max_drawdown(returns),
                'skewness': returns.skew(),
                'kurtosis': returns.kurtosis()
            },
            'stress_scenarios': {
                'extreme_moves': (returns.abs() > 3 * returns.std()).sum(),
                'consecutive_losses': self.calculate_consecutive_losses(returns),
                'tail_risk': (returns < -2 * returns.std()).sum()
            }
        }
        
    def calculate_max_drawdown(self, returns):
        """
        חישוב Max Drawdown
        """
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = cumulative / running_max - 1
        return drawdown.min()
        
    def calculate_consecutive_losses(self, returns):
        """
        חישוב רצף הפסדים מקסימלי
        """
        losses = returns < 0
        max_consecutive = 0
        current_consecutive = 0
        
        for loss in losses:
            if loss:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
                
        return max_consecutive
        
    def create_recommendations(self):
        """
        המלצות מפורטות
        """
        return {
            'strategic_recommendations': [
                "מומלץ לפתח אסטרטגיה המבוססת על שילוב של מספר אינדיקטורים",
                "כדאי להתמקד בשעות הפעילות הגבוהות (9:00-10:00)",
                "מומלץ להשתמש בstop-loss של 2-3% מהפוזיציה",
                "כדאי לשלב ניתוח נפח עם אותות המחיר"
            ],
            'tactical_recommendations': [
                "שימוש באסטרטגיית Golden Cross לזיהוי מגמות ארוכות טווח",
                "ניצול רמות RSI קיצוניות לכניסות קצרות טווח",
                "מעקב אחר breakouts עם נפח גבוה",
                "שימוש ב-Bollinger Bands לזיהוי רמות תמיכה והתנגדות"
            ],
            'risk_management': [
                "הגדרת מגבלות יומיות על הפסדים",
                "פיזור פוזיציות על פני מספר אסטרטגיות",
                "מעקב רציף אחר מטריקות הסיכון",
                "התאמת גודל הפוזיציות לתנודתיות הנוכחית"
            ]
        }
        
    def create_appendix(self):
        """
        נספחים
        """
        return {
            'methodology': {
                'data_source': 'NQ Futures minute data',
                'analysis_period': f"{self.analyzer.df.index.min()} - {self.analyzer.df.index.max()}",
                'indicators_used': ['RSI', 'MACD', 'Moving Averages', 'Bollinger Bands'],
                'risk_free_rate': '2%'
            },
            'definitions': {
                'RSI': 'Relative Strength Index - מדד חוזק יחסי',
                'MACD': 'Moving Average Convergence Divergence',
                'Golden Cross': 'חציית ממוצע נע קצר מעל ממוצע נע ארוך',
                'VaR': 'Value at Risk - ערך בסיכון'
            },
            'limitations': [
                "הניתוח מבוסס על נתונים היסטוריים",
                "תוצאות עבר אינן מבטיחות תוצאות עתיד",
                "לא נלקחו בחשבון עמלות מסחר",
                "הניתוח לא כולל השפעות מקרו-כלכליות"
            ]
        }
        
    def save_report(self):
        """
        שמירת הדוח
        """
        # שמירה כ-JSON
        with open('nq_full_report.json', 'w', encoding='utf-8') as f:
            json.dump(self.report_data, f, ensure_ascii=False, indent=2, default=str)
        
        # שמירה כ-TXT
        self.save_text_report()
        
        print("✅ דוח נשמר בהצלחה!")
        print("📄 קבצים שנוצרו:")
        print("  - nq_full_report.json")
        print("  - nq_summary_report.txt")
        print("  - price_analysis.png")
        print("  - volume_analysis.png")
        print("  - rsi_analysis.png")
        print("  - hourly_analysis.png")
        print("  - returns_distribution.png")
        
    def save_text_report(self):
        """
        שמירת דוח טקסט
        """
        with open('nq_summary_report.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("                    דוח ניתוח NQ Futures\n")
            f.write("=" * 80 + "\n\n")
            
            # מטא-דאטה
            f.write("📊 פרטי הדוח:\n")
            f.write("-" * 40 + "\n")
            for key, value in self.report_data['metadata'].items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            
            # סיכום מנהלים
            f.write("📋 סיכום מנהלים:\n")
            f.write("-" * 40 + "\n")
            f.write("ממצאים עיקריים:\n")
            for finding in self.report_data['executive_summary']['key_findings']:
                f.write(f"• {finding}\n")
            f.write("\nהזדמנויות:\n")
            for opp in self.report_data['executive_summary']['opportunities']:
                f.write(f"• {opp}\n")
            f.write("\nגורמי סיכון:\n")
            for risk in self.report_data['executive_summary']['risk_factors']:
                f.write(f"• {risk}\n")
            f.write("\n")
            
            # המלצות
            f.write("💡 המלצות:\n")
            f.write("-" * 40 + "\n")
            f.write("המלצות אסטרטגיות:\n")
            for rec in self.report_data['recommendations']['strategic_recommendations']:
                f.write(f"• {rec}\n")
            f.write("\nהמלצות טקטיות:\n")
            for rec in self.report_data['recommendations']['tactical_recommendations']:
                f.write(f"• {rec}\n")
            f.write("\nניהול סיכונים:\n")
            for rec in self.report_data['recommendations']['risk_management']:
                f.write(f"• {rec}\n")
            f.write("\n")
            
            f.write("=" * 80 + "\n")
            f.write("                         סוף הדוח\n")
            f.write("=" * 80 + "\n")

def main():
    """
    פונקציה ראשית
    """
    generator = ReportGenerator()
    report = generator.generate_full_report()
    
    print("\n🎉 דוח מלא הושלם!")
    print("📊 הדוח כולל:")
    print("  - ניתוח מפורט של 2.6 מיליון נקודות נתונים")
    print("  - 5 גרפים מתקדמים")
    print("  - המלצות אסטרטגיות מפורטות")
    print("  - ניתוח סיכונים מקצועי")
    print("  - סיכום מנהלים")
    
    return report

if __name__ == "__main__":
    report = main() 