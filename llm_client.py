"""Спільний модуль для всіх завдань лабораторної роботи №3.

Функція send_prompt() надсилає запит до Gemini API, за потреби з системною
роллю та temperature, і зберігає prompt разом із відповіддю у файл
results/<task>.json. З цих файлів потім формується звіт (make_report.py).
"""
import json
import os
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
RESULTS = Path(__file__).parent / "results"
RESULTS.mkdir(exist_ok=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise SystemExit("Не знайдено GEMINI_API_KEY. Створіть файл .env за зразком .env.example")

client = genai.Client(api_key=api_key)


def send_prompt(task, title, prompt, system=None, temperature=0.0, retries=4):
    """Надсилає prompt моделі й повертає текст відповіді.

    task        -- назва файлу з результатами (наприклад, "task1")
    title       -- підпис запиту у звіті
    prompt      -- текст запиту користувача
    system      -- системна інструкція (роль моделі) або None
    temperature -- випадковість генерації (0 = найпередбачуваніша відповідь)
    """
    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=temperature,
    )

    print(f"-> {title}")
    for attempt in range(1, retries + 1):
        try:
            response = client.models.generate_content(
                model=MODEL, contents=prompt, config=config
            )
            break
        except Exception as error:  # ліміт запитів, мережа тощо
            wait = 20 * attempt
            print(f"   помилка ({error.__class__.__name__}), повтор через {wait} с")
            time.sleep(wait)
    else:
        raise RuntimeError(f"Запит «{title}» не вдався після {retries} спроб")

    record = {
        "title": title,
        "model": response.model_version or MODEL,
        "temperature": temperature,
        "system": system,
        "prompt": prompt,
        "answer": response.text,
        "words": len(response.text.split()),
        "time": datetime.now().isoformat(timespec="seconds"),
    }

    path = RESULTS / f"{task}.json"
    records = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    records = [r for r in records if r["title"] != title]  # повторний запуск перезаписує
    records.append(record)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"   отримано відповідь: {record['words']} слів\n")
    time.sleep(6)  # пауза, щоб не перевищити безкоштовний ліміт запитів
    return response.text


if __name__ == "__main__":
    # Швидка перевірка, що ключ і модель працюють
    print(send_prompt("check", "Перевірка", "Скажи одним реченням, яка ти модель."))
