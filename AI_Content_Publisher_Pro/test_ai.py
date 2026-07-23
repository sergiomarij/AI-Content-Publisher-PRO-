print("=== Старт ===")

from app.ai.manager import AIManager

print("Импорт AIManager OK")

ai = AIManager()

print("AIManager создан")

response = ai.generate("Напиши 3 идеи SEO-статей про искусственный интеллект.")

print(response)

print("=== Конец ===")