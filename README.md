# Лабораторна робота №3. Робота з LLM через API

Модель: Google Gemini (через бібліотеку `google-genai`).
Предметна область запитів: штучний інтелект і програмування.

## Структура

| Файл | Призначення |
|---|---|
| `llm_client.py` | функція `send_prompt()`: надсилає запит і зберігає prompt та відповідь у `results/<task>.json` |
| `task1.py` | Завдання 1 — 5 типів запитів |
| `task2.py` | Завдання 2 — zero-shot і few-shot (3 тестові випадки) |
| `task3.py` | Завдання 3 — початковий і вдосконалений prompt |
| `task4.py` | Завдання 4 — три ролі через `system_instruction` |
| `make_report.py` | збирає всі результати в `results.md` |

## Запуск

```bash
pip install -r requirements.txt
```

1. Отримайте безкоштовний ключ: https://aistudio.google.com/apikey
2. Скопіюйте `.env.example` у файл `.env` і вставте ключ.
3. Перевірте, що все працює: `python llm_client.py`
4. Запустіть завдання по черзі:

```bash
python task1.py
python task2.py
python task3.py
python task4.py
python make_report.py
```

Результати з'являться в папці `results/`, а зведення — у файлі `results.md`.

Temperature: 0 для всіх запитів, крім генерації тексту (0.7), щоб різниця між
відповідями залежала від prompt, а не від випадковості.
