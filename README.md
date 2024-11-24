# Flask Telegram Project

This project is a Flask web application integrated with a Telegram bot that interacts with the Flask API. The Flask application serves data about user spending and can accept both GET and POST requests, while the Telegram bot fetches and posts information from the Flask app.

## Project Structure

```
flask_telegram_project/
├── .venv/                  # Python virtual environment
├── .env                    # Environment variables (API keys, etc.)
├── .env_example            # Example env file
├── .gitignore              # Git ignore file
├── app.py                  # Flask application
├── LICENSE                 # Project License
├── README.md               # Project README
├── requirements.txt        # Python dependencies
├── run_apps.sh             # Shell script to run the apps
├── telegram_bot.py         # Telegram bot logic
├── test_app.py             # Test cases for Flask app
├── users_vouchers.db       # SQLite database
├── users_vouchers.db-journal # SQLite journal (temporary)
```

## Requirements

- Python 3.8 or higher
- `pip` for managing Python packages

## Setting up the environment

Follow these steps to set up the project:

### 1. Clone the repository

Clone the project repository to your local machine:

```bash
git clone https://github.com/yourusername/flask_telegram_project.git
cd flask_telegram_project
```

### 2. Set up the virtual environment

Create and activate a virtual environment to manage dependencies:

#### On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Install all the required Python dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file (or copy the `.env_example` and rename it) and set your environment variables:

```bash
cp .env_example .env
```

Edit the `.env` file to add your values for the following:

```
API_KEY=your_telegram_bot_api_key
FLASK_URL=http://127.0.0.1:5000  # URL of your Flask app (can be local)
```

### 5. Running the application

You can start both the Flask app and the Telegram bot simultaneously using the provided shell script `run_apps.sh`.

#### On Windows (Git Bash or WSL):
```bash
bash run_apps.sh
```

This script does the following:
1. Installs the dependencies from the `requirements.txt` for both the Flask app and Telegram bot.
2. Runs both the Flask app (`app.py`) and the Telegram bot (`telegram_bot.py`) in the background.

Alternatively, you can run the apps manually by executing the following commands:

#### For Flask app (`app.py`):

```bash
python app.py
```

#### For Telegram bot (`telegram_bot.py`):

```bash
python telegram_bot.py
```

### 6. Accessing the Flask app

Once the Flask app is running, you can access the following endpoints:

- `GET /`: A simple welcome message.
- `GET /total_spent/<user_id>`: Returns the total spending for a given user ID.
- `GET /average_spending_by_age`: Returns average spending by age ranges.
- `GET /write_high_spending_user`: Retrieves high-spending users.
- `POST /write_high_spending_user`: Adds a high-spending user.

### 7. Testing the Flask app

Run the test cases for the Flask app using the following command:

```bash
python -m unittest test_app.py
```

This will execute the tests and validate that the API works as expected.

## License

This project is licensed under the [GPL-3.0 license](LICENSE).

---

### Key Notes:

- The shell script `run_apps.sh` makes it easy to start both services simultaneously without manual intervention.
- The `.env` file holds your environment variables, ensuring sensitive data (like API keys) are not exposed in the code.
