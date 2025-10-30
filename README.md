# 🤖 Telegram Bot

This is a Telegram bot written in **Python** that uses the **OpenAI API (GPT)** to provide a variety of interactive services.
The bot uses a **mode system** to manage different functionalities, such as chatting, quizzes, conversations with famous people, and more.

## 🌟 Main Features

The bot has **6 main modes**, accessible via commands:

* **`/gpt`** — General chat mode. Allows free conversation with AI.
* **`/talk`** — Conversation simulator. Lets you “talk” to one of five famous personalities (Kurt Cobain, Queen Elizabeth II, J.R.R. Tolkien, Friedrich Nietzsche, Stephen Hawking).
* **`/quiz`** — Quiz mode. The bot generates a question on a chosen topic (Python, Math, Biology) and checks your answer.
* **`/image_describe`** — Image description. Send a photo, and the bot will describe what’s in it (powered by GPT-Vision).
* **`/translate`** — Translator. Instantly translates your text between English and Ukrainian.
* **`/random`** — Random fact. The bot sends one interesting fact.

You can use `/start` at any time to reset the current mode and return to the main menu.

## 🛠️ Installation and Setup

To run this bot locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/miont1/TGbot.git
cd TGbot
```

### 2. Create a virtual environment (recommended)

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

All required libraries are listed in the **`requirements.txt`** file.
To install them, run:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a **`.env`** file in the project’s root directory and add your API keys:

```.env
OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE
```

* **`BOT_TOKEN`** — Obtain it from [@BotFather](https://t.me/BotFather) on Telegram.
* **`OPENAI_API_KEY`** — Get it from your [OpenAI Dashboard](https://platform.openai.com/account/api-keys).

### 5. Project structure (important!)

This bot loads resources (prompt texts, messages, and images) from the `resources` folder using helper functions in `utils.py`.
Make sure your directory structure looks like this:

```
TGbot/
├── resources/
│   ├── messages/
│   │   ├── main.txt
│   │   ├── gpt.txt
│   │   ├── talk.txt
│   │   └── ... (other .txt message files)
│   ├── prompts/
│   │   ├── gpt.txt
│   │   ├── talk_cobain.txt
│   │   ├── quiz.txt
│   │   └── ... (other GPT prompt files)
│   └── photos/
│       ├── main.jpg
│       ├── gpt.jpg
│       ├── talk.jpg
│       └── ... (other image files)
├── bot.py
├── GPT.py
├── utils.py
└── .env
```

## 🚀 Running the bot

After installing dependencies and configuring your keys, run the main file:

```bash
python bot.py
```

If everything is set up correctly, you’ll see **“Bot started.”** in your console.

## 💬 How to use

1. Find your bot on Telegram and press `/start`.
2. Use commands like `/gpt`, `/talk`, `/quiz`, etc., to switch between modes.
3. Follow the bot’s prompts and use the provided buttons.
4. To exit modes like “Talk,” “Quiz,” or “Translate,” press the **“Finish”** button or simply type `/start` again.
