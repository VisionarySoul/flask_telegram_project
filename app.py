import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, request, jsonify

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("API_KEY")


def get_db():
    conn = sqlite3.connect("users_vouchers.db")
    conn.row_factory = sqlite3.Row  # Allows dictionary-like row access
    return conn


@app.route("/")
def index():
    return "Welcome to Flask Project"


@app.route("/total_spent/<user_id>")
def get_user(user_id):
    conn = get_db()
    user = conn.execute(
        "SELECT user_id, sum(money_spent) AS total_spent, year FROM user_spending WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    if user and user["user_id"] is not None:
        result = dict(user)
        return jsonify(result)
    return jsonify({"error": f"User:{user_id} spending not found"}), 404


@app.route("/average_spending_by_age")
def average_spending():
    conn = get_db()
    user_age = [(18, 24), (25, 30), (31, 36), (37, 47), (48, None)]
    list_spenders = []
    for age in user_age:
        if age[1]:  # Check if we have a max age limit in the range
            user_average = conn.execute(
                "SELECT sum(money_spent) FROM user_info "
                "JOIN user_spending ON user_info.user_id = user_spending.user_id "
                "WHERE user_info.age >= ? AND user_info.age <= ?", (age[0], age[1])
            ).fetchone()[0]
            user_count = conn.execute(
                "SELECT count(*) FROM user_info "
                "JOIN user_spending ON user_info.user_id = user_spending.user_id "
                "WHERE user_info.age >= ? AND user_info.age <= ?", (age[0], age[1])
            ).fetchone()[0]  # Avoid division by zero
        else:
            user_average = conn.execute(
                "SELECT sum(money_spent) FROM user_info "
                "JOIN user_spending ON user_info.user_id = user_spending.user_id "
                "WHERE user_info.age >= 48 "
            ).fetchone()[0]
            user_count = conn.execute(
                "SELECT count(*) FROM user_info "
                "JOIN user_spending ON user_info.user_id = user_spending.user_id "
                "WHERE user_info.age >= 48",
            ).fetchone()[0]
        avg_spent = float(user_average) / user_count
        list_spenders.append(avg_spent)
    conn.close()
    average_spending_list = {
        "18-24": list_spenders[0],
        "25-30": list_spenders[1],
        "31-36": list_spenders[2],
        "37-47": list_spenders[3],
        ">48": list_spenders[4]
    }
    return jsonify(average_spending_list)


@app.route("/write_high_spending_user", methods=["GET", "POST"])
def high_spending_user():
    conn = get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        data = cursor.execute("SELECT * FROM high_spenders").fetchall()
        formatted_data = [{"user_id": row["user_id"], "total_spending": row["total_spending"]} for row in data]

        conn.close()
        return jsonify(formatted_data), 200
    elif request.method == "POST":
        data = request.get_json()
        cursor.execute(
            "INSERT INTO high_spenders (user_id, total_spending) VALUES (?, ?)",
            (data['user_id'], data['total_spending'])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "User data inserted successfully"}), 201

    else:
        conn.close()
    return jsonify({"error": "Invalid HTTP method; please use GET or POST"}), 405


if __name__ == "__main__":
    app.run(debug=True)
