#!/bin/bash

# Define the directory where your Python apps are located
FLASK_DIR="./flask"
TELEGRAM_DIR="./telegram_bot"

# Install dependencies for Flask app
echo "Installing dependencies for Flask app..."
cd $FLASK_DIR
pip install -r requirements.txt

# Install dependencies for Telegram bot
echo "Installing dependencies for Telegram bot..."
cd $TELEGRAM_DIR
pip install -r requirements.txt

# Run Flask app and Telegram bot in the background
echo "Running Flask app..."
cd $FLASK_DIR
nohup python app.py &

echo "Running Telegram bot..."
cd $TELEGRAM_DIR
nohup python telegram_bot.py &

echo "Both services are running."
