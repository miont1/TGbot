from openai import AsyncOpenAI
from telegram.ext import ContextTypes

from utils import load_prompt


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
        self.messages.clear()
        return message

    async def send_question(self, prompt_text, question_text):
        self.messages.clear()
        self.messages.append({"role": "system", "content": prompt_text})
        self.messages.append({"role": "user", "content": question_text})
        return await self.send_messages()

    async def set_prompt(self, prompt):
        self.messages.clear()
        self.messages.append({"role": "system", "content": prompt})

    async def send_answer(self, answer):
        self.messages.append({"role": "system", "content": answer})

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
        context.user_data["history"].clear()
        context.user_data["history"].append({"role": "system", "content": prompt_text})

    @staticmethod
    async def add_user_question(context, question_text):
        context.user_data["history"].append({"role": "user", "content": question_text})

    async def send_user_question(self, context, question_text):
        context.user_data["history"].append({"role": "user", "content": question_text})
        return await self.send_messages_contex(context)

    async def create_photo(self, file_obj):
        result = await self.client.files.create(
            file=("photo.jpg", file_obj),
            purpose="vision",
        )
        return result.id

    async def send_question_with_photo(self, prompt_text, file_id):
        user_input = [
            {
                "role": "system",
                "content": prompt_text},
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "file_id": file_id,
                    },
                ],
            }]

        result = await self.client.responses.create(
            model="o4-mini",
            input=user_input,
            max_output_tokens=3000,
        )
        return result.output_text
