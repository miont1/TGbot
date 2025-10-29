from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import os
import io
from dotenv import load_dotenv

from GPT import GPT
from utils import send_message, send_message_with_buttons, load_message, load_prompt, send_photo, load_photo

load_dotenv()
chat_gpt = GPT(token=os.getenv("OPENAI_API_KEY"))


def check_context(context):
    if "mode" not in context.user_data:
        context.user_data["mode"] = ""
    if "history" not in context.user_data:
        context.user_data["history"] = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_context(context)
    context.user_data["mode"] = ""
    context.user_data["history"] = []

    message = load_message("main")
    photo = load_photo("main")
    await send_photo(update, context, photo)
    await send_message(update, context, message)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_context(context)
    text = update.message.text

    if text == "Хочу ще факт!":
        await random(update, context)
    elif text == "Закінчити":
        await start(update, context)
    elif context.user_data["mode"] == "chat":
        wait_message = await send_message(update, context, "Даю відповідь на питання...")
        try:
            answer = await chat_gpt.send_user_question(context, text)
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
            await send_message_with_buttons(update, context, answer, None, ("Закінчити",))
        except Exception as error:
            print(f"Помилка при обробці запита - {error}")
            await send_message(update, context, "Сталася помилка при обробці запита, спробуйте пізніше.")

    elif context.user_data["mode"] == "talk":

        talk_list = {
            "Курт Кобейн": ("talk_cobain", "Привіт! Курт Кобейн слухає!"),
            "Єлизавета II": ("talk_queen", "Привіт! Єлизавета II слухає!"),
            "Джон Толкін": ("talk_tolkien", "Привіт! Джон Толкін слухає!"),
            "Фрідріх Ніцше": ("talk_nietzsche", "Привіт! Джон Толкін слухає!"),
            "Стівен Гокінг": ("talk_hawking", "Привіт! Стівен Гокінг слухає!")
        }

        person = talk_list.get(text)
        if person:
            await send_photo(update, context, load_photo(person[0]))
            await send_message_with_buttons(update, context, person[1], None, ("Закінчити",))
            await chat_gpt.set_user_prompt(context, load_prompt(person[0]))
        else:
            if not context.user_data["history"]:
                await send_message(update, context,
                                   "Виберіть ім'я відомої особистості зі списку:\n Курт Кобейн\n Єлизавета II\n Джон Толкін\n Фрідріх Ніцше\n Стівен Гокінг")
            else:
                wait_message = await send_message(update, context, "Даю відповідь на питання...")
                answer = await chat_gpt.send_user_question(context, text)
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
                await send_message_with_buttons(update, context, answer, None, ("Закінчити",))

    elif context.user_data["mode"] == "quiz":
        if context.user_data["status"] == "question":
            wait_message = await send_message(update, context, "Думаю над питанням...")
            answer = await chat_gpt.send_user_question(context, text)
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
            await send_message(update, context, answer)
            context.user_data["status"] = "answer"

        elif context.user_data["status"] == "answer":
            wait_message = await send_message(update, context, "Думаю над відповіддю...")
            answer = await chat_gpt.send_user_question(context, text)
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
            await send_message(update, context, answer)
            await send_message_with_buttons(update, context, "Оберіть тему.", None,
                                            ("Python", "Математика", "Біологія", ("Попередня тема", "Закінчити")))
            context.user_data["status"] = "question"

    elif context.user_data["mode"] == "translate":

        translate_list = {
            "Українська": "translate_ua",
            "Англійська": "translate_eng",
        }

        language = translate_list.get(text)
        if language:
            await chat_gpt.set_user_prompt(context, load_prompt(language))
            await send_message(update, context, "Введіть повідомлення для перекладу:")
        else:

            wait_message = await send_message(update, context, "Перекладаю...")
            answer = await chat_gpt.send_user_question(context, text)
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
            await send_message_with_buttons(update, context, answer, load_message("translate"),
                                            (("Українська", "Англійська"), "Закінчити"))


async def photo_handler(update, context):
    if not update.message.photo:
        await send_message(update, context, "Треба скинути картинку")
        return

    photo = update.message.photo[-1]
    tg_file = await context.bot.get_file(photo.file_id)
    photo_bytes = await tg_file.download_as_bytearray()

    if context.user_data["mode"] == "image_describe":
        wait_message = await send_message(update, context, "Думаю над відповіддю...")
        file_obj = io.BytesIO(photo_bytes)
        file_obj.name = "photo.jpg"
        file_id = await chat_gpt.create_photo(file_obj)

        response = await chat_gpt.send_question_with_photo(load_prompt("image_describe"), file_id)
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=wait_message.message_id)
        await send_message(update, context, response)


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_context(context)
    context.user_data["mode"] = "quiz"
    context.user_data["status"] = "question"

    photo = load_photo("quiz")
    await send_photo(update, context, photo)
    message = load_message("quiz")
    if not context.user_data["history"]:
        await send_message_with_buttons(update, context, message, None,
                                        ("Python", "Математика", "Біологія"))
    else:
        await send_message_with_buttons(update, context, message, None,
                                        ("Python", "Математика", "Біологія", "Попередня тема"))

    await chat_gpt.set_user_prompt(context, load_prompt("quiz"))


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
    check_context(context)
    context.user_data["mode"] = "chat"

    photo = load_photo("gpt")
    await send_photo(update, context, photo)
    message = load_message("gpt")
    await chat_gpt.set_user_prompt(context, load_prompt("gpt"))
    await send_message(update, context, message)


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_context(context)
    context.user_data["mode"] = "talk"

    photo = load_photo("talk")
    await send_photo(update, context, photo)
    message = load_message("talk")
    await send_message_with_buttons(update, context, message, None,
                                    ("Курт Кобейн", "Єлизавета II", "Джон Толкін", "Фрідріх Ніцше", "Стівен Гокінг"))


async def image_describe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_context(context)
    context.user_data["mode"] = "image_describe"

    photo = load_photo("gpt")
    await send_photo(update, context, photo)
    message = load_message("image_describe")
    await send_message(update, context, message)


async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    check_context(context)
    context.user_data["mode"] = "translate"

    photo = load_photo("gpt")
    await send_photo(update, context, photo)
    message = load_message("translate")
    await send_message_with_buttons(update, context, message, None, (("Українська", "Англійська"),))


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message(update, context, "Вибачте, такої команди немає :(")


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    start_handler = CommandHandler('start', start)
    random_handler = CommandHandler('random', random)
    message_handler_ = MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    photo_handler_ = MessageHandler(filters.PHOTO, photo_handler)
    gpt_handler = CommandHandler('gpt', gpt)
    talk_handler = CommandHandler('talk', talk)
    quiz_handler = CommandHandler('quiz', quiz)
    image_describe_handler = CommandHandler('image_describe', image_describe)
    translate_handler = CommandHandler('translate', translate)

    application.add_handler(start_handler)
    application.add_handler(random_handler)
    application.add_handler(message_handler_)
    application.add_handler(photo_handler_)
    application.add_handler(gpt_handler)
    application.add_handler(talk_handler)
    application.add_handler(quiz_handler)
    application.add_handler(image_describe_handler)
    application.add_handler(translate_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    print("Bot started.")
    application.run_polling()
