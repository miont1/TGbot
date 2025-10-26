from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import os
from dotenv import load_dotenv

from GPT import GPT
from utils import send_message, send_message_with_buttons, load_message, load_prompt, send_photo, load_photo

load_dotenv()
chat_gpt = GPT(token=os.getenv("OPENAI_API_KEY"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = ""
    context.user_data["history"] = []
    message = load_message("main")
    photo = load_photo("main")
    await send_photo(update, context, photo)
    await send_message(update, context, message)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "mode" not in context.user_data:
        context.user_data["mode"] = ""
    if "history" not in context.user_data:
        context.user_data["history"] = []

    text = update.message.text
    if text == "Хочу ще факт!":
        await random(update, context)
    elif text == "Закінчити":
        await start(update, context)
    elif context.user_data["mode"] == "chat":
        wait_message = await send_message(update, context, "Даю відповідь на питання...")
        try:
            answer = await chat_gpt.add_user_question(context, text)
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
            await send_message_with_buttons(update, context, answer, None, ("Закінчити",))
        except Exception as error:
            print(f"Помилка при обробці запита - {error}")
            await send_message(update, context, "Сталася помилка при обробці запита, спробуйте пізніше.")


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = load_photo("random")
    await send_photo(update, context, photo)
    wait_message = await send_message(update, context, "Думаю над цікавим фактом...")

    try:
        prompt = load_prompt("random")
        random_fact = await chat_gpt.send_question(prompt, "Напиши цікавий факт")

        await send_message_with_buttons(update, context, random_fact, "Бажаєте ще один факт?",
                                        ("Закінчити", "Хочу ще факт!"))
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
    except Exception as error:
        print(f"Помилка при обробці запита - {error}")
        await send_message(update, context, "Сталася помилка при обробці запита, спробуйте пізніше.")


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "chat"
    context.user_data["history"] = []

    photo = load_photo("gpt")
    await send_photo(update, context, photo)
    message = load_message("gpt")
    await chat_gpt.set_user_prompt(context, load_prompt("gpt"))
    await send_message(update, context, message)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, context, "Вибачте, такої команди немає :(")


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    random_handler = CommandHandler('random', random)
    button_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    gpt_handler = CommandHandler('gpt', gpt)

    application.add_handler(start_handler)
    application.add_handler(random_handler)
    application.add_handler(button_handler)
    application.add_handler(gpt_handler)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    print("Bot started.")
    application.run_polling()
