"""
NQ Strategy Hunter - Web Interface
ממשק אתר לניהול מערכת מציאת אסטרטגיות
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
import os
import subprocess
import signal
import time
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.utils

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # במציאות - שנה את זה!

# Global variables
autonomous_process = None
process_pid = None

class WebInterface:
    def __init__(self):
        self.data_dir = '../data'
        self.results_dir = '../results'
        self.autonomous_dir = '../autonomous'
        
    def get_system_status(self):
        """בדיקת מצב המערכת"""
        try:
            # בדיקה אם יש קבצי תוצאות
            results_exist = os.path.exists(f"{self.results_dir}/best_strategies.json")
            
            # בדיקה אם המערכת רצה
            is_running = self.check_autonomous_running()
            
            return {
                'results_exist': results_exist,
                'is_running': is_running,
                'last_update': self.get_last_update(),
                'status': 'running' if is_running else 'stopped'
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }
    
    def check_autonomous_running(self):
        """בדיקה אם המערכת האוטונומית רצה"""
        try:
            result = subprocess.run(['pgrep', '-f', 'autonomous_strategy_hunter.py'], 
                                  capture_output=True, text=True)
            return len(result.stdout.strip()) > 0
        except:
            return False
    
    def get_last_update(self):
        """קבלת זמן עדכון אחרון"""
        try:
            if os.path.exists(f"{self.results_dir}/best_strategies.json"):
                mtime = os.path.getmtime(f"{self.results_dir}/best_strategies.json")
                return datetime.fromtimestamp(mtime).strftime('%H:%M:%S')
            return "אין עדכון"
        except:
            return "שגיאה"
    
    def load_results(self):
        """טעינת תוצאות"""
        try:
            if not os.path.exists(f"{self.results_dir}/best_strategies.json"):
                return None
                
            with open(f"{self.results_dir}/best_strategies.json", 'r') as f:
                strategies = json.load(f)
                
            if not strategies:
                return None
                
            # עיבוד התוצאות להצגה
            processed = []
            for strategy in strategies[-10:]:  # 10 האחרונות
                processed.append({
                    'generation': strategy['generation'],
                    'timestamp': strategy['timestamp'],
                    'fitness': round(strategy['fitness'], 1),
                    'trades': strategy['num_trades'],
                    'return': round(strategy['total_return'], 0),
                    'win_rate': round(strategy['win_rate'] * 100, 1),
                    'dna': strategy['dna']
                })
            
            return processed
        except Exception as e:
            return {'error': str(e)}
    
    def start_autonomous(self):
        """הפעלת המערכת האוטונומית"""
        global autonomous_process, process_pid
        
        try:
            if self.check_autonomous_running():
                return {'status': 'already_running', 'message': 'המערכת כבר רצה'}
            
            # הפעלת המערכת ברקע
            autonomous_process = subprocess.Popen(
                ['python3', 'autonomous_strategy_hunter.py'],
                cwd=self.autonomous_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
            
            process_pid = autonomous_process.pid
            time.sleep(2)  # המתנה קצרה
            
            if autonomous_process.poll() is None:
                return {'status': 'started', 'message': 'המערכת הופעלה בהצלחה', 'pid': process_pid}
            else:
                return {'status': 'error', 'message': 'שגיאה בהפעלת המערכת'}
                
        except Exception as e:
            return {'status': 'error', 'message': f'שגיאה: {str(e)}'}
    
    def stop_autonomous(self):
        """עצירת המערכת האוטונומית"""
        global autonomous_process, process_pid
        
        try:
            # עצירה של התהליך הנוכחי
            if autonomous_process and autonomous_process.poll() is None:
                autonomous_process.terminate()
                autonomous_process.wait(timeout=5)
                autonomous_process = None
                process_pid = None
            
            # עצירה של תהליכים נוספים
            try:
                result = subprocess.run(['pgrep', '-f', 'autonomous_strategy_hunter.py'], 
                                      capture_output=True, text=True)
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    if pid.strip():
                        os.kill(int(pid), signal.SIGTERM)
            except:
                pass
            
            return {'status': 'stopped', 'message': 'המערכת נעצרה בהצלחה'}
            
        except Exception as e:
            return {'status': 'error', 'message': f'שגיאה: {str(e)}'}
    
    def create_charts(self, strategies):
        """יצירת גרפים"""
        if not strategies or 'error' in strategies:
            return None
        
        # גרף התפתחות Fitness
        generations = [s['generation'] for s in strategies]
        fitness_scores = [s['fitness'] for s in strategies]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=generations,
            y=fitness_scores,
            mode='lines+markers',
            name='Fitness Score',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='התפתחות ביצועי האסטרטגיות',
            xaxis_title='דור',
            yaxis_title='ציון Fitness',
            template='plotly_white',
            height=400
        )
        
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# יצירת אובייקט הממשק
interface = WebInterface()

@app.route('/')
def index():
    """דף הבית"""
    status = interface.get_system_status()
    return render_template('index.html', status=status)

@app.route('/results')
def results():
    """דף תוצאות"""
    strategies = interface.load_results()
    charts = interface.create_charts(strategies) if strategies else None
    return render_template('results.html', strategies=strategies, charts=charts)

@app.route('/api/status')
def api_status():
    """API לבדיקת מצב"""
    return jsonify(interface.get_system_status())

@app.route('/api/start', methods=['POST'])
def api_start():
    """API להפעלת המערכת"""
    result = interface.start_autonomous()
    return jsonify(result)

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """API לעצירת המערכת"""
    result = interface.stop_autonomous()
    return jsonify(result)

@app.route('/api/results')
def api_results():
    """API לקבלת תוצאות"""
    strategies = interface.load_results()
    return jsonify(strategies)

if __name__ == '__main__':
    # יצירת תיקיות אם לא קיימות
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # הפעלה מקומית
    app.run(debug=True, host='0.0.0.0', port=5001)

# עבור Vercel - זה חייב להיות בסוף
app = app 