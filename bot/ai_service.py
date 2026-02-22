from openai import OpenAI
from bot.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


async def generate_joke():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ти генератор коротких українських анекдотів."
                                          "НЕ використовуй теми: політика, війна, смерть, релігія, комп'ютери."
             },
            {"role": "user", "content": "Придумай один свіжий короткий анекдот українською."}
        ],
        max_tokens=150
    )

    BANNED_WORDS = ["війна", "політик", "смерть", "політіка"]

    def contains_banned(text):
        text = text.lower()
        return any(word in text for word in BANNED_WORDS)

    return response.choices[0].message.content.strip()