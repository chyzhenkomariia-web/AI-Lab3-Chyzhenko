"""Збирає всі результати з папки results/ в один файл results.md,
з якого зручно переносити prompt і відповіді у звіт."""
import json
from pathlib import Path

RESULTS = Path(__file__).parent / "results"
TITLES = {
    "task1": "Завдання 1. Взаємодія з великою мовною моделлю",
    "task2": "Завдання 2. Zero-shot і few-shot prompting",
    "task3": "Завдання 3. Удосконалення prompt",
    "task4": "Завдання 4. Системна роль",
}

parts = ["# Результати запитів до LLM\n"]
for task, heading in TITLES.items():
    path = RESULTS / f"{task}.json"
    if not path.exists():
        continue
    parts.append(f"\n## {heading}\n")
    for r in json.loads(path.read_text(encoding="utf-8")):
        parts.append(f"\n### {r['title']}\n")
        parts.append(f"*Модель: {r['model']}, temperature = {r['temperature']}, "
                     f"обсяг відповіді: {r['words']} слів*\n")
        if r["system"]:
            parts.append(f"**System:** {r['system']}\n")
        parts.append(f"**Prompt:**\n\n```\n{r['prompt']}\n```\n")
        parts.append(f"**Відповідь:**\n\n{r['answer']}\n")

(Path(__file__).parent / "results.md").write_text("\n".join(parts), encoding="utf-8")
print("Створено results.md")
