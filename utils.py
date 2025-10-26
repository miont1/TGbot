from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


def load_photo(photo):
    with open(f"resources/images/{photo}.jpg", "rb") as f:
        return f.read()


def load_message(message):
    with open(f"resources/messages/{message}.txt", "r", encoding="utf8") as f:
        return f.read()


def load_prompt(prompt):
    with open(f"resources/prompts/{prompt}.txt", "r", encoding="utf8") as f:
        return f.read()


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    return await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.MARKDOWN)


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, photo: bytes):
    return await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)


async def send_message_with_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str,
                                    reply_text: str | None,
                                    buttons: tuple):
    if reply_text is not None:
        await send_message(update, context, message)

    keyboard = []

    for button in buttons:
        if isinstance(button, (tuple, list)):
            keyboard.append(tuple(button))  # кілька кнопок у рядку
        else:
            keyboard.append((button,))  # одна кнопка в рядку

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    if reply_text is None:
        reply_text = message
    await update.message.reply_text(reply_text, reply_markup=reply_markup)
