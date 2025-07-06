# 🌐 מדריך העלאה לשרת - NQ Strategy Hunter

## 📖 תוכן עניינים
1. [הכנה לפרויקט](#הכנה-לפרויקט)
2. [הרצה מקומית](#הרצה-מקומית)
3. [העלאה לשרת](#העלאה-לשרת)
4. [הגדרות אבטחה](#הגדרות-אבטחה)
5. [Nginx Configuration](#nginx-configuration)
6. [Domain Setup](#domain-setup)

## 🚀 הכנה לפרויקט

### דרישות מערכת
- Python 3.8+
- pip
- Git
- 2GB RAM מינימום
- 5GB דיסק

### התקנה מקומית
```bash
# שכפול הפרויקט
git clone YOUR_REPO_URL
cd nq-strategy-hunter

# יצירת סביבה וירטואלית
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# או
venv\Scripts\activate  # Windows

# התקנת חבילות
pip install -r web/requirements.txt

# הפעלת האתר
python3 run_website.py
```

## 🏠 הרצה מקומית

### דרך 1: סקריפט אוטומטי
```bash
python3 run_website.py
```

### דרך 2: הפעלה ידנית
```bash
cd web
python3 app.py
```

האתר יהיה זמין בכתובת: `http://localhost:5000`

## 🌍 העלאה לשרת

### שלב 1: בחירת שרת
מומלץ:
- **VPS/Dedicated Server**: DigitalOcean, AWS, Linode
- **Cloud Platform**: Heroku, Railway, Render
- **Shared Hosting**: לא מומלץ (מגבלות זמן ריצה)

### שלב 2: הכנת השרת (Ubuntu/Debian)
```bash
# עדכון מערכת
sudo apt update && sudo apt upgrade -y

# התקנת Python ו-pip
sudo apt install python3 python3-pip python3-venv git nginx -y

# יצירת משתמש לפרויקט
sudo useradd -m -s /bin/bash nqstrategy
sudo su - nqstrategy
```

### שלב 3: העלאת הפרויקט
```bash
# העלאת הקוד
git clone YOUR_REPO_URL
cd nq-strategy-hunter

# הגדרת סביבה
python3 -m venv venv
source venv/bin/activate
pip install -r web/requirements.txt

# הרצת בדיקה
python3 run_website.py
```

### שלב 4: הפעלה עם Gunicorn
```bash
# התקנה
pip install gunicorn

# הרצת השרת
cd web
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### שלב 5: יצירת Systemd Service
```bash
# יצירת קובץ שירות
sudo nano /etc/systemd/system/nqstrategy.service
```

תוכן הקובץ:
```ini
[Unit]
Description=NQ Strategy Hunter Web App
After=network.target

[Service]
Type=simple
User=nqstrategy
WorkingDirectory=/home/nqstrategy/nq-strategy-hunter/web
Environment=PATH=/home/nqstrategy/nq-strategy-hunter/venv/bin
ExecStart=/home/nqstrategy/nq-strategy-hunter/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

הפעלת השירות:
```bash
sudo systemctl daemon-reload
sudo systemctl enable nqstrategy
sudo systemctl start nqstrategy
sudo systemctl status nqstrategy
```

## 🔒 הגדרות אבטחה

### שלב 1: חומת אש
```bash
# הפעלת UFW
sudo ufw enable

# הרשאות בסיסיות
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw deny 5000/tcp  # חסימת גישה ישירה לפורט
```

### שלב 2: SSL Certificate
```bash
# התקנת Certbot
sudo apt install certbot python3-certbot-nginx -y

# קבלת תעודה
sudo certbot --nginx -d your-domain.com
```

### שלב 3: עדכון הגדרות Flask
עריכת `web/app.py`:
```python
app.secret_key = 'your-very-secret-key-here-change-this-in-production'
# או טוב יותר:
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')
```

## 🌐 Nginx Configuration

יצירת קובץ הגדרות:
```bash
sudo nano /etc/nginx/sites-available/nqstrategy
```

תוכן הקובץ:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /home/nqstrategy/nq-strategy-hunter/web/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

הפעלת האתר:
```bash
sudo ln -s /etc/nginx/sites-available/nqstrategy /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 📡 Domain Setup

### שלב 1: קניית דומיין
- Namecheap, GoDaddy, Google Domains
- מומלץ: .com, .net, .org

### שלב 2: הגדרת DNS
```
A Record: your-domain.com → IP השרת
A Record: www.your-domain.com → IP השרת
```

### שלב 3: בדיקת התחברות
```bash
# בדיקת DNS
nslookup your-domain.com

# בדיקת חיבור
curl -I http://your-domain.com
```

## 🚀 אופציות פרישה מהירות

### 1. Heroku (קל ומהיר)
```bash
# התקנת Heroku CLI
# יצירת Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT app:app" > web/Procfile

# פרישה
heroku create your-app-name
git push heroku main
```

### 2. Railway (חדש וטוב)
```bash
# התחברות לרכבת
railway login
railway init
railway up
```

### 3. Render (בחינם לתחילת דרך)
1. חבר את הפרויקט לגיטהאב
2. הרשם ל-Render
3. צור Web Service חדש
4. הגדר: `pip install -r web/requirements.txt && cd web && gunicorn app:app`

## 🔧 פתרון בעיות נפוצות

### בעיה: האתר לא נטען
```bash
# בדיקת לוגים
sudo journalctl -u nqstrategy -f
sudo tail -f /var/log/nginx/error.log
```

### בעיה: שגיאות Python
```bash
# בדיקת חבילות
pip list
pip install -r web/requirements.txt --upgrade
```

### בעיה: בעיות הרשאות
```bash
# תיקון הרשאות
sudo chown -R nqstrategy:nqstrategy /home/nqstrategy/nq-strategy-hunter
chmod +x run_website.py
```

## 📊 מניטורינג ותחזוקה

### בדיקת מצב השרת
```bash
# בדיקת שירותים
sudo systemctl status nqstrategy
sudo systemctl status nginx

# בדיקת זיכרון וCPU
htop
df -h
```

### גיבוי אוטומטי
```bash
# יצירת סקריפט גיבוי
nano backup.sh
```

תוכן הסקריפט:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /home/nqstrategy/backups/backup_$DATE.tar.gz /home/nqstrategy/nq-strategy-hunter/
```

## 🎯 טיפים להצלחה

1. **בדיקות לפני העלאה**: תמיד תבדוק מקומית
2. **גיבויים**: צור גיבויים קבועים
3. **מניטורינג**: השתמש ב-logs למעקב
4. **עדכונים**: עדכן את המערכת באופן קבוע
5. **אבטחה**: שמור על סיסמאות חזקות

## 📞 תמיכה

אם נתקלת בבעיות:
1. בדוק את הלוגים
2. ודא שכל השירותים רצים
3. בדוק את הרשאות הקבצים
4. ודא שהחבילות מותקנות

**זכור**: האתר הזה מיועד לריצה מקומית או על שרת פרטי. אל תשתף גישה לאתר עם משתמשים לא מורשים! 