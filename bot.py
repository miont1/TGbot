from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, InlineQueryHandler
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    # keyboard = [
    #     ["Привіт", "Пока"],
    #     ["Допомога"],
    # ]
    # reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    # await update.message.reply_text("Вибери кнопку:", reply_markup=reply_markup)

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
#     print(update.message.from_user.username + " - " + update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    print(update.message.from_user.username + " - " + update.message.text)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, this command is not available.")

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response.output_text)
    keyboard = [
        ["Закінчити"],
        ["Хочу ще факт!"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Бажаєте ще один факт?", reply_markup=reply_markup)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    random_handler = CommandHandler('random', random)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    button_handler = MessageHandler(filters.TEXT, button_handler)
    # echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(caps_handler)
    application.add_handler(start_handler)
    application.add_handler(random_handler)
    application.add_handler(button_handler)
    # application.add_handler(echo_handler)
    application.add_handler(unknown_handler)

    application.run_polling()