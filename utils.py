from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


def load_message(message):
    with open(f"resources/messages/{message}.txt", "r", encoding="utf8") as f:
        return f.read()


def load_prompt(prompt):
    with open(f"resources/prompts/{prompt}.txt", "r", encoding="utf8") as f:
        return f.read()


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.MARKDOWN)


async def send_message_with_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str, reply_text: str,
                                    buttons: tuple):
    await send_message(update, context, message)
    keyboard = []
    for button in buttons:
        keyboard.append((button,))
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(reply_text, reply_markup=reply_markup)
