@echo off
echo Starting Auto-Completion Daemon...
echo This will automatically complete demo payments after 30 seconds
echo Press Ctrl+C to stop
echo.
python manage.py auto_complete_daemon --interval 10 --timeout 30