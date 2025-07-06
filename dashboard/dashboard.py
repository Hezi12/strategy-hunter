"""
NQ Trading Dashboard
דשבורד ויזואלי מתקדם לאסטרטגיות מסחר
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'analysis'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'strategies'))

from nq_analyzer import NQAnalyzer
from strategy_engine import StrategyEngine

# הגדרת הדף
st.set_page_config(
    page_title="NQ Strategy Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# עיצוב CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .success-metric {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .warning-metric {
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
    }
    .sidebar .sidebar-content {
        background: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

class NQDashboard:
    """
    דשבורד מתקדם לאסטרטגיות NQ
    """
    
    def __init__(self):
        self.analyzer = None
        self.engine = None
        self.data_loaded = False
        
    def load_data(self):
        """
        טעינת נתונים
        """
        if not self.data_loaded:
            with st.spinner("טוען נתונים..."):
                self.analyzer = NQAnalyzer()
                success = self.analyzer.load_data()
                if success:
                    self.data_loaded = True
                    st.success("✅ נתונים נטענו בהצלחה!")
                else:
                    st.error("❌ שגיאה בטעינת נתונים")
                    return False
        return True
        
    def run_analysis(self):
        """
        הרצת ניתוח מתקדם
        """
        if not self.data_loaded:
            st.error("יש לטעון נתונים תחילה")
            return
            
        with st.spinner("מבצע ניתוח מתקדם..."):
            # ניתוח בסיסי
            self.analyzer.basic_analysis()
            self.analyzer.identify_patterns()
            self.analyzer.find_trading_opportunities()
            
            # מנוע אסטרטגיות
            self.engine = StrategyEngine(self.analyzer)
            self.engine.create_advanced_features()
            
            st.success("✅ ניתוח הושלם!")
            
    def show_overview(self):
        """
        הצגת סקירה כללית
        """
        st.markdown('<div class="main-header">📈 דשבורד אסטרטגיות NQ</div>', unsafe_allow_html=True)
        
        if not self.data_loaded:
            st.warning("יש לטעון נתונים תחילה")
            return
            
        # מטריקות עיקריות
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "נקודות נתונים",
                f"{len(self.analyzer.df):,}",
                help="מספר כל נקודות הנתונים"
            )
            
        with col2:
            st.metric(
                "מחיר ממוצע",
                f"${self.analyzer.df['close'].mean():.2f}",
                help="מחיר ממוצע בתקופה"
            )
            
        with col3:
            st.metric(
                "נפח ממוצע",
                f"{self.analyzer.df['volume'].mean():.0f}",
                help="נפח מסחר ממוצע"
            )
            
        with col4:
            volatility = self.analyzer.df['returns'].std() * np.sqrt(252) * 100
            st.metric(
                "תנודתיות שנתית",
                f"{volatility:.1f}%",
                help="תנודתיות שנתית"
            )
    
    def show_price_analysis(self):
        """
        ניתוח מחירים
        """
        st.header("📊 ניתוח מחירים")
        
        if not self.data_loaded:
            return
            
        # בחירת תקופה
        col1, col2 = st.columns(2)
        
        with col1:
            days_back = st.selectbox(
                "תקופת הצגה",
                [7, 30, 90, 180, 365],
                index=2,
                help="כמה ימים אחורה להציג"
            )
            
        with col2:
            show_indicators = st.checkbox("הצגת אינדיקטורים", value=True)
        
        # חישוב תאריך התחלה
        end_date = self.analyzer.df.index.max()
        start_date = end_date - timedelta(days=days_back)
        
        # סינון נתונים
        df_filtered = self.analyzer.df[self.analyzer.df.index >= start_date].copy()
        
        if len(df_filtered) == 0:
            st.warning("אין נתונים לתקופה זו")
            return
            
        # יצירת גרף
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=["מחיר ואינדיקטורים", "נפח", "RSI"],
            vertical_spacing=0.05,
            row_heights=[0.6, 0.2, 0.2]
        )
        
        # גרף מחיר
        fig.add_trace(
            go.Candlestick(
                x=df_filtered.index,
                open=df_filtered['open'],
                high=df_filtered['high'],
                low=df_filtered['low'],
                close=df_filtered['close'],
                name="מחיר"
            ),
            row=1, col=1
        )
        
        # אינדיקטורים
        if show_indicators:
            if 'sma_20' in df_filtered.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df_filtered.index,
                        y=df_filtered['sma_20'],
                        name="SMA 20",
                        line=dict(color='blue', width=1)
                    ),
                    row=1, col=1
                )
                
            if 'sma_50' in df_filtered.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df_filtered.index,
                        y=df_filtered['sma_50'],
                        name="SMA 50",
                        line=dict(color='red', width=1)
                    ),
                    row=1, col=1
                )
                
            if 'bb_upper' in df_filtered.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df_filtered.index,
                        y=df_filtered['bb_upper'],
                        name="Bollinger Upper",
                        line=dict(color='gray', width=1, dash='dash')
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=df_filtered.index,
                        y=df_filtered['bb_lower'],
                        name="Bollinger Lower",
                        line=dict(color='gray', width=1, dash='dash')
                    ),
                    row=1, col=1
                )
        
        # גרף נפח
        fig.add_trace(
            go.Bar(
                x=df_filtered.index,
                y=df_filtered['volume'],
                name="נפח",
                marker_color='lightblue'
            ),
            row=2, col=1
        )
        
        # RSI
        if 'rsi' in df_filtered.columns:
            fig.add_trace(
                go.Scatter(
                    x=df_filtered.index,
                    y=df_filtered['rsi'],
                    name="RSI",
                    line=dict(color='purple')
                ),
                row=3, col=1
            )
            
            # קווי RSI
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
        
        fig.update_layout(
            title="ניתוח מחירים מתקדם",
            xaxis_title="תאריך",
            height=800,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def show_strategy_analysis(self):
        """
        ניתוח אסטרטגיות
        """
        st.header("🎯 ניתוח אסטרטגיות")
        
        if not self.data_loaded:
            return
            
        # בדיקה אם יש תוצאות
        if not hasattr(self.analyzer, 'results') or 'opportunities' not in self.analyzer.results:
            st.warning("יש להריץ ניתוח מתקדם תחילה")
            return
            
        opportunities = self.analyzer.results['opportunities']
        
        # הצגת אותות מסחר
        st.subheader("📈 אותות מסחר")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # אותות קנייה
            st.markdown("### 🟢 אותות קנייה")
            buy_signals = {
                'Golden Cross': opportunities.get('golden_cross_signals', 0),
                'RSI Oversold': opportunities.get('rsi_oversold_signals', 0),
                'MACD Bullish': opportunities.get('macd_bullish_signals', 0),
                'BB Oversold': opportunities.get('bb_oversold_signals', 0)
            }
            
            for signal, count in buy_signals.items():
                st.metric(signal, f"{count:,}")
        
        with col2:
            # אותות מכירה
            st.markdown("### 🔴 אותות מכירה")
            sell_signals = {
                'RSI Overbought': opportunities.get('rsi_overbought_signals', 0),
                'BB Overbought': opportunities.get('bb_overbought_signals', 0)
            }
            
            for signal, count in sell_signals.items():
                st.metric(signal, f"{count:,}")
        
        # גרף אותות
        signals_data = {**buy_signals, **sell_signals}
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(signals_data.keys()),
                y=list(signals_data.values()),
                marker_color=['green' if 'Oversold' in k or 'Cross' in k or 'Bullish' in k 
                             else 'red' for k in signals_data.keys()]
            )
        ])
        
        fig.update_layout(
            title="התפלגות אותות מסחר",
            xaxis_title="סוג אות",
            yaxis_title="מספר אותות"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def show_market_hours_analysis(self):
        """
        ניתוח שעות מסחר
        """
        st.header("🕐 ניתוח שעות מסחר")
        
        if not self.data_loaded:
            return
            
        # ניתוח לפי שעות
        hourly_stats = self.analyzer.df.groupby('hour').agg({
            'volume': 'mean',
            'returns': 'mean',
            'volatility': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # נפח לפי שעות
            fig = px.bar(
                hourly_stats,
                x='hour',
                y='volume',
                title="נפח ממוצע לפי שעות",
                labels={'hour': 'שעה', 'volume': 'נפח ממוצע'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # תנודתיות לפי שעות
            fig = px.line(
                hourly_stats,
                x='hour',
                y='volatility',
                title="תנודתיות לפי שעות",
                labels={'hour': 'שעה', 'volatility': 'תנודתיות'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # טבלת שעות מובילות
        st.subheader("🏆 שעות מובילות")
        top_hours = hourly_stats.nlargest(5, 'volume')[['hour', 'volume', 'volatility']]
        top_hours.columns = ['שעה', 'נפח ממוצע', 'תנודתיות']
        st.dataframe(top_hours, use_container_width=True)
    
    def show_advanced_analytics(self):
        """
        אנליטיקה מתקדמת
        """
        st.header("🧠 אנליטיקה מתקדמת")
        
        if not self.data_loaded:
            return
            
        # סטטיסטיקות מתקדמות
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 סטטיסטיקות תשואות")
            
            returns_stats = {
                'תשואה ממוצעת': f"{self.analyzer.df['returns'].mean():.4f}",
                'סטיית תקן': f"{self.analyzer.df['returns'].std():.4f}",
                'תשואה מקסימלית': f"{self.analyzer.df['returns'].max():.4f}",
                'תשואה מינימלית': f"{self.analyzer.df['returns'].min():.4f}",
                'Skewness': f"{self.analyzer.df['returns'].skew():.4f}",
                'Kurtosis': f"{self.analyzer.df['returns'].kurtosis():.4f}"
            }
            
            for key, value in returns_stats.items():
                st.metric(key, value)
        
        with col2:
            st.subheader("📈 היסטוגרמת תשואות")
            
            fig = px.histogram(
                self.analyzer.df,
                x='returns',
                nbins=100,
                title="התפלגות תשואות"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # מטריקות סיכון
        st.subheader("⚠️ מטריקות סיכון")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            var_95 = np.percentile(self.analyzer.df['returns'].dropna(), 5)
            st.metric("VaR 95%", f"{var_95:.4f}")
        
        with col2:
            var_99 = np.percentile(self.analyzer.df['returns'].dropna(), 1)
            st.metric("VaR 99%", f"{var_99:.4f}")
        
        with col3:
            max_drawdown = self.calculate_max_drawdown()
            st.metric("Max Drawdown", f"{max_drawdown:.2%}")
    
    def calculate_max_drawdown(self):
        """
        חישוב Max Drawdown
        """
        cumulative_returns = (1 + self.analyzer.df['returns']).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdown = cumulative_returns / running_max - 1
        return drawdown.min()
    
    def show_recommendations(self):
        """
        הצגת המלצות
        """
        st.header("💡 המלצות")
        
        if not self.data_loaded:
            return
            
        # המלצות בסיסיות
        recommendations = [
            "מומלץ לעקוב אחר אותות Golden Cross לזיהוי מגמות חזקות",
            "שעות 8-10 בבוקר מציגות נפח גבוה - מומלץ לסחור בזמנים אלו",
            "שימוש ב-RSI עם רמות 30/70 יכול לזהות נקודות כניסה טובות",
            "Bollinger Bands מספקים אותות טובים בתנאי שוק רגיל",
            "מומלץ לשלב מספר אינדיקטורים לאישור האותות"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
        
        # המלצות מתקדמות
        if hasattr(self.analyzer, 'results') and 'opportunities' in self.analyzer.results:
            opportunities = self.analyzer.results['opportunities']
            
            st.subheader("🎯 המלצות מותאמות")
            
            if opportunities.get('golden_cross_signals', 0) > 100:
                st.success("✅ אסטרטגיית Golden Cross מציגה פוטנציאל גבוה")
            
            if opportunities.get('volume_spikes', 0) > 500:
                st.info("ℹ️ זוהו עליות נפח רבות - מומלץ לחקור הקשר למחירים")
            
            if opportunities.get('strong_buy_signals', 0) > 1000:
                st.warning("⚠️ מספר רב של אותות קנייה - יש לבדוק איכות האותות")

def main():
    """
    פונקציה ראשית
    """
    dashboard = NQDashboard()
    
    # Sidebar
    st.sidebar.title("🎛️ בקרה")
    
    # טעינת נתונים
    if st.sidebar.button("טעינת נתונים"):
        dashboard.load_data()
    
    # ניתוח מתקדם
    if st.sidebar.button("ניתוח מתקדם"):
        if dashboard.data_loaded:
            dashboard.run_analysis()
        else:
            st.sidebar.error("יש לטעון נתונים תחילה")
    
    # תפריט ניווט
    page = st.sidebar.selectbox(
        "בחר עמוד",
        ["סקירה כללית", "ניתוח מחירים", "אסטרטגיות", "שעות מסחר", "אנליטיקה מתקדמת", "המלצות"]
    )
    
    # הצגת עמודים
    if page == "סקירה כללית":
        dashboard.show_overview()
    elif page == "ניתוח מחירים":
        dashboard.show_price_analysis()
    elif page == "אסטרטגיות":
        dashboard.show_strategy_analysis()
    elif page == "שעות מסחר":
        dashboard.show_market_hours_analysis()
    elif page == "אנליטיקה מתקדמת":
        dashboard.show_advanced_analytics()
    elif page == "המלצות":
        dashboard.show_recommendations()
    
    # מידע בסרגל צד
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ מידע על המערכת")
    st.sidebar.markdown("""
    - **נתונים**: NQ Futures 
    - **תקופה**: 2018-2025
    - **רזולוציה**: דקה
    - **אינדיקטורים**: RSI, MACD, Bollinger Bands
    """)

if __name__ == "__main__":
    main() 