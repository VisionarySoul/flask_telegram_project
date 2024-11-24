import aiohttp
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask server URL
load_dotenv()
api_key = os.getenv("API_KEY")
flask_url = os.getenv("FLASK_URL")


async def handle_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Extracting user ID from the command
        if len(context.args) != 1:
            await update.message.reply_text("Usage: /total_spent <id>")
            return

        user_id = context.args[0]
        if not user_id.isdigit():
            await update.message.reply_text("User ID must be numeric!")
            return

        # Send GET request to Flask app
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{flask_url}/total_spent/{user_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    await update.message.reply_text(f"User total spent: {data}")
                else:
                    await update.message.reply_text(f"Error: {response.status}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def handle_spenders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Send GET request to Flask app
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{flask_url}/average_spending_by_age") as response:
                if response.status == 200:
                    data = await response.json()
                    response_message = "\n".join(
                        [f"{age_range}: ${average:.2f}" for age_range, average in data.items()]
                    )
                    await update.message.reply_text(f"Average Spending by Age:\n{response_message}")

                else:
                    await update.message.reply_text(f"Error: API responded with status {response.status}")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def get_high_spending_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{flask_url}/write_high_spending_user") as response:
                if response.status == 200:
                    data = await response.json()
                    response_message = "\n".join(
                        [f"User ID: {row['user_id']}, Total Spending: ${row['total_spending']:.2f}" for row in data]
                    )
                    await update.message.reply_text(f"High Spending Users:\n{response_message}")
                else:
                    error_message = await response.text()
                    await update.message.reply_text(f"Error: {response.status} - {error_message}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


async def write_high_spending_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Ensure correct usage
        if len(context.args) != 2:
            await update.message.reply_text("Usage: /write_user <user_id> <total_spending>")
            return

        # Extract arguments
        user_id, total_spending = context.args

        # Validate inputs
        if not user_id.isdigit() or not total_spending.replace('.', '', 1).isdigit():
            await update.message.reply_text("Error: Both user_id and total_spending must be numeric!")
            return

        # Prepare data payload
        payload = {
            "user_id": int(user_id),
            "total_spending": float(total_spending)
        }

        # Send POST request to Flask app
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{flask_url}/write_high_spending_user", json=payload) as response:
                if response.status == 201:  # Success response
                    data = await response.json()
                    await update.message.reply_text(f"Success: {data['message']}")
                else:
                    error_message = await response.text()
                    await update.message.reply_text(f"Error: {response.status} - {error_message}")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")


def main():
    # Replace 'YOUR_TOKEN' with your Telegram bot token
    application = Application.builder().token(api_key).build()

    # Adding handler for /user command
    application.add_handler(CommandHandler("user", handle_user))
    # Adding handler for /average command
    application.add_handler(CommandHandler("average", handle_spenders))
    # Adding handler for /get_user command for GET method
    application.add_handler(CommandHandler("get_users", get_high_spending_users))
    # Adding handler for /write_user command for POST method
    application.add_handler(CommandHandler("write_user", write_high_spending_user))
    # Execute command for running the bot application
    application.run_polling()


if __name__ == '__main__':
    main()
