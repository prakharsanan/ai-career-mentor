import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.3-70b-versatile"


def generate_response(messages):

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.5
    )

    return response.choices[0].message.content