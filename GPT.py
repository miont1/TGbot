from openai import AsyncOpenAI


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

    async def set_prompt(self, prompt_text):
        self.messages.clear()
        self.messages.append({"role": "system", "content": prompt_text})

    async def add_question(self, question_text):
        self.messages.append({"role": "user", "content": question_text})
        return await self.send_messages()

    async def send_question(self, prompt_text, question_text):
        self.messages.clear()
        self.messages.append({"role": "system", "content": prompt_text})
        self.messages.append({"role": "user", "content": question_text})
        return await self.send_messages()
