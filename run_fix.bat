@echo off
REM Set DATABASE_URL for local SQLite database
set DATABASE_URL=sqlite:///D:/fiverr/Tradeprint_eco/db.sqlite3

REM Run the Django management command
python manage.py fix_shopkeepers

pause
