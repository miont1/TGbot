from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler
import os
from openai import OpenAI
from dotenv import load_dotenv

from GPT import GPT
from utils import send_message, send_message_with_buttons, load_message, load_prompt

load_dotenv()
chat_gpt = GPT(token=os.getenv("OPENAI_API_KEY"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = load_message("main")
    await send_message(update, context, message)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, context, "Sorry, this command is not available.")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Хочу ще факт!":
        await random(update, context)
    elif text == "Закінчити":
        await start(update, context)


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wait_message = await send_message(update, context, "Думаю над цікавим фактом...")

    try:
        prompt = load_prompt("random")
        random_fact = await chat_gpt.send_question(prompt, "Напиши цікавий факт")

        await send_message_with_buttons(update, context, random_fact, "Бажаєте ще один факт?",
                                        ("Закінчити", "Хочу ще факт!"))
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
    except Exception as error:
        print(f"Помилка при оброці запита - {error}")
        await send_message(update, context, "Сталася помилка при обробці запита, спробуйте пізніше.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    random_handler = CommandHandler('random', random)
    button_handler = MessageHandler(filters.TEXT, button_handler)

    application.add_handler(start_handler)
    application.add_handler(random_handler)
    application.add_handler(button_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    print("Bot started.")
    application.run_polling()
