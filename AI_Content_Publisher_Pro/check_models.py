from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.gemini_key)

models = [
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-3.1-flash-lite",
    "gemini-2.0-flash",
]

for model in models:
    try:
        print(f"\nПроверяем {model}...")
        response = client.models.generate_content(
            model=model,
            contents="Ответь одним словом: OK"
        )
        print("УСПЕХ:", response.text)

    except Exception as e:
        print("ОШИБКА:", type(e).__name__)
        print(e)