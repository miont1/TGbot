from openai import AsyncOpenAI
from telegram.ext import ContextTypes


class GPT:
    def __init__(self, token):
        self.client = AsyncOpenAI(api_key=token)
        self.messages = []

    async def send_messages(self):
        response = await self.client.responses.create(
            model="o4-mini",
            input=self.messages,
            max_output_tokens=3000,
        )

        message = response.output_text
        self.messages.append({"role": "assistant", "content": message})
        return message

    async def send_messages_contex(self, context: ContextTypes.DEFAULT_TYPE):
        response = await self.client.responses.create(
            model="o4-mini",
            input=context.user_data["history"],
            max_output_tokens=3000,
        )

        message = response.output_text
        context.user_data["history"].append({"role": "assistant", "content": message})
        return message

    @staticmethod
    async def set_user_prompt(context, prompt_text):
        context.user_data["history"].append({"role": "system", "content": prompt_text})

    async def add_user_question(self, context, question_text):
        context.user_data["history"].append({"role": "user", "content": question_text})
        return await self.send_messages_contex(context)

    async def send_question(self, prompt_text, question_text):
        self.messages.clear()
        self.messages.append({"role": "system", "content": prompt_text})
        self.messages.append({"role": "user", "content": question_text})
        return await self.send_messages()
