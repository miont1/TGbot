from openai import OpenAI

from utils import load_prompt


class GPT:
    def __init__(self, token):
        self.client = OpenAI(api_key=token)
        self.messages = []

    async def send_messages(self):
        response = self.client.responses.create(
            model="o4-mini",
            input=self.messages,
            max_output_tokens=3000,
        )
        return response.output_text

    async def send_question(self, prompt_text, question_text):
        self.messages.clear()
        self.messages.append({"role": "system", "content": prompt_text})
        self.messages.append({"role": "user", "content": question_text})
        return await self.send_messages()
