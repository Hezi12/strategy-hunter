#!/usr/bin/env python3
"""
NQ Strategy Hunter - GitHub Preparation Script
מכין את הפרויקט לגיט האב באופן אוטומטי
"""

import os
import subprocess
import shutil
import sys
from datetime import datetime

class GitHubPreparation:
    def __init__(self):
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self.cleaned_files = []
        self.issues = []
        
    def print_header(self):
        """הצגת כותרת"""
        print("🚀 הכנת פרויקט NQ Strategy Hunter לגיט האב")
        print("=" * 60)
        print(f"📍 נתיב פרויקט: {self.project_root}")
        print(f"🕐 זמן: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def clean_unwanted_files(self):
        """ניקוי קבצים לא רצויים"""
        print("🧹 מנקה קבצים לא רצויים...")
        
        # קבצים ותיקיות לניקוי
        unwanted_patterns = [
            '__pycache__',
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '.DS_Store',
            '*.log',
            '.pytest_cache',
            '.coverage',
            '*.backup',
            '*.bak',
            '*.tmp',
            '*.temp'
        ]
        
        for root, dirs, files in os.walk(self.project_root):
            # ניקוי תיקיות
            dirs_to_remove = [d for d in dirs if d in ['__pycache__', '.pytest_cache']]
            for dir_name in dirs_to_remove:
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    self.cleaned_files.append(f"📁 {dir_path}")
                    print(f"  ❌ הוסרה תיקייה: {dir_path}")
                except Exception as e:
                    self.issues.append(f"שגיאה בהסרת {dir_path}: {e}")
            
            # ניקוי קבצים
            for file_name in files:
                if (file_name.endswith(('.pyc', '.pyo', '.pyd', '.log', '.backup', '.bak', '.tmp', '.temp')) or
                    file_name == '.DS_Store'):
                    file_path = os.path.join(root, file_name)
                    try:
                        os.remove(file_path)
                        self.cleaned_files.append(f"📄 {file_path}")
                        print(f"  ❌ הוסר קובץ: {file_path}")
                    except Exception as e:
                        self.issues.append(f"שגיאה בהסרת {file_path}: {e}")
        
        if not self.cleaned_files:
            print("  ✅ אין קבצים לניקוי")
        print()
    
    def check_required_files(self):
        """בדיקת קבצים נדרשים"""
        print("📋 בודק קבצים נדרשים...")
        
        required_files = [
            '.gitignore',
            'PROJECT_README.md',
            'LICENSE',
            'requirements.txt',
            'Dockerfile',
            'docker-compose.yml',
            'Procfile',
            'app.json',
            'web/app.py',
            'web/requirements.txt',
            'web/templates/index.html',
            'web/templates/results.html'
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = os.path.join(self.project_root, file_path)
            if os.path.exists(full_path):
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} - חסר!")
                missing_files.append(file_path)
        
        if missing_files:
            self.issues.extend([f"קובץ חסר: {f}" for f in missing_files])
        print()
        
    def check_git_status(self):
        """בדיקת מצב Git"""
        print("🔍 בודק מצב Git...")
        
        try:
            # בדיקה אם זה Git repository
            result = subprocess.run(['git', 'status'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                print("  ✅ Git repository קיים")
                
                # בדיקת שינויים לא committed
                if "nothing to commit" in result.stdout:
                    print("  ✅ אין שינויים לא שמורים")
                else:
                    print("  ⚠️  יש שינויים שלא נשמרו")
                    print("     הפעל: git add . && git commit -m 'הכנה לגיט האב'")
                
                # בדיקת remote
                remote_result = subprocess.run(['git', 'remote', '-v'], 
                                            capture_output=True, text=True, cwd=self.project_root)
                if remote_result.stdout.strip():
                    print("  ✅ Git remote מוגדר")
                else:
                    print("  ⚠️  Git remote לא מוגדר")
                    print("     הוסף: git remote add origin https://github.com/USERNAME/nq-strategy-hunter.git")
                    
            else:
                print("  ❌ לא Git repository")
                print("     הפעל: git init")
                self.issues.append("Git repository לא מאותחל")
                
        except FileNotFoundError:
            print("  ❌ Git לא מותקן")
            self.issues.append("Git לא מותקן במערכת")
        
        print()
    
    def check_dependencies(self):
        """בדיקת dependencies"""
        print("📦 בודק dependencies...")
        
        try:
            # בדיקת Python
            python_version = sys.version_info
            if python_version.major >= 3 and python_version.minor >= 8:
                print(f"  ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
            else:
                print(f"  ⚠️  Python {python_version.major}.{python_version.minor} - מומלץ 3.8+")
            
            # בדיקת חבילות חשובות
            important_packages = ['flask', 'pandas', 'numpy', 'plotly']
            missing_packages = []
            
            for package in important_packages:
                try:
                    __import__(package)
                    print(f"  ✅ {package}")
                except ImportError:
                    print(f"  ❌ {package} - חסר")
                    missing_packages.append(package)
            
            if missing_packages:
                print(f"  📦 התקן חבילות חסרות: pip install {' '.join(missing_packages)}")
                
        except Exception as e:
            self.issues.append(f"שגיאה בבדיקת dependencies: {e}")
        
        print()
    
    def create_github_commands(self):
        """יצירת פקודות Git לגיט האב"""
        print("📝 פקודות Git להעלאה לגיט האב:")
        print("-" * 40)
        
        commands = [
            "# הכנה בסיסית",
            "git init",
            "git add .",
            'git commit -m "🚀 Initial commit: NQ Strategy Hunter - AI-Powered Trading Strategy Discovery"',
            "",
            "# חיבור לגיט האב (שנה USERNAME לשם שלך)",
            "git remote add origin https://github.com/USERNAME/nq-strategy-hunter.git",
            "git branch -M main",
            "git push -u origin main",
            "",
            "# אחרי ההעלאה - עדכון README",
            "rm README.md",
            "mv PROJECT_README.md README.md",
            "# ערוך את README.md עם הקישורים הנכונים",
            'git add .',
            'git commit -m "📖 עדכון README מקצועי"',
            'git push origin main'
        ]
        
        for cmd in commands:
            if cmd.startswith('#'):
                print(f"\033[92m{cmd}\033[0m")  # ירוק לתגובות
            elif cmd == "":
                print()
            else:
                print(f"  {cmd}")
        
        print()
    
    def generate_summary(self):
        """סיכום הבדיקה"""
        print("📊 סיכום הכנה לגיט האב")
        print("=" * 40)
        
        if self.cleaned_files:
            print(f"🧹 נוקו {len(self.cleaned_files)} קבצים")
        
        if self.issues:
            print("⚠️  בעיות שנמצאו:")
            for issue in self.issues:
                print(f"  • {issue}")
        else:
            print("✅ הפרויקט מוכן להעלאה לגיט האב!")
        
        print("\n🔗 קישורים שימושיים:")
        print("  • מדריך מלא: GITHUB_DEPLOYMENT.md")
        print("  • יצירת repository: https://github.com/new")
        print("  • הוראות Heroku: https://devcenter.heroku.com/articles/getting-started-with-python")
        
    def run_preparation(self):
        """הרצת כל התהליך"""
        self.print_header()
        self.clean_unwanted_files()
        self.check_required_files()
        self.check_git_status()
        self.check_dependencies()
        self.create_github_commands()
        self.generate_summary()

def main():
    """פונקציה ראשית"""
    try:
        prep = GitHubPreparation()
        prep.run_preparation()
    except KeyboardInterrupt:
        print("\n⏹️  הופסק על ידי המשתמש")
    except Exception as e:
        print(f"\n❌ שגיאה כללית: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 