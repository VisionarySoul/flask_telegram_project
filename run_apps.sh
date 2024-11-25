#!/bin/bash

# Run Flask app and redirect output to flask.log
echo "Starting Flask app..."
nohup python app.py > flask.log 2>&1 &

# Run Telegram bot and redirect output to telegram_bot.log
echo "Starting Telegram bot..."
nohup python telegram_bot.py > telegram_bot.log 2>&1 &

echo "Both services are running. Check flask.log and telegram_bot.log for logs."
