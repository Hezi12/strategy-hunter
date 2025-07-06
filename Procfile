web: cd web && gunicorn -w 4 -b 0.0.0.0:$PORT app:app
worker: cd autonomous && python3 autonomous_strategy_hunter.py 