from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler
import os
from openai import OpenAI
from dotenv import load_dotenv

from utils import send_message, send_message_with_buttons, load_message

load_dotenv()
client = OpenAI()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = load_message("main")
    await send_message(update, context, message)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await send_message(update, context, text_caps)
    print(update.message.from_user.username + " - " + update.message.text)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, context, "Sorry, this command is not available.")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Хочу ще факт!":
        await random(update, context)
    elif text == "Закінчити":
        await start(update, context)


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = client.responses.create(
        model="o4-mini",
        input='Write a random fact'
    )
    await send_message_with_buttons(update, context, response.output_text, "Бажаєте ще один факт?",
                                    ("Закінчити", "Хочу ще факт!"))


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    random_handler = CommandHandler('random', random)
    button_handler = MessageHandler(filters.TEXT, button_handler)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(caps_handler)
    application.add_handler(start_handler)
    application.add_handler(random_handler)
    application.add_handler(button_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
