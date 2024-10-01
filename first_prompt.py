import os

from groq import Groq

client = Groq(
    api_key="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",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What is groq?",
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)