#!/bin/bash
echo "Stopping Flask app..."
pkill -f app.py

echo "Stopping Telegram bot..."
pkill -f telegram_bot.py

echo "Both services have been stopped."
