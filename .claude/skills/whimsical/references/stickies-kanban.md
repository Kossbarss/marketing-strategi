# Стікери, ретро, kanban

## Sticky notes (нова дошка, сітка 4 колонки)

```json
create({
  "type": "sticky_notes",
  "title": "Ретро кампанії вересня",
  "data": {"notes": [
    {"content": "## Спрацювало\nUGC-креативи: CTR 2.1%", "color": "green"},
    {"content": "## Не спрацювало\nLookalike 5% — дорогий лід", "color": "red"},
    {"content": "## Дія\nТестувати 3 нових хуки", "color": "blue"}
  ]}
})
```

`content` — markdown. Кольори: `yellow` (дефолт), `blue`, `green`, `red`, `orange`, `purple`, `white`, `dark-purple`, `dark-green`, `brown`, `pale-red`.

Колір = категорія. Сортуй нотатки за категорією — сітка йде по порядку.

Готові шаблони:
- **Ретро**: Спрацювало (green) / Не спрацювало (red) / Ідеї (yellow) / Дії (blue)
- **SWOT**: Сильні (green) / Слабкі (orange) / Можливості (blue) / Загрози (red)
- **Плюси/мінуси**: green / red
- **Гіпотези для тестів**: yellow, у тексті «Якщо… то… бо…»

## Нотатки на існуючій дошці

```json
edit({"id": "<board_id>", "operations": [
  {"op": "add", "type": "note", "text": "Перевірити UTM", "color": "yellow"}
]})
```

## Kanban (stack + task)

```json
edit({"id": "<board_id>", "operations": [
  {"op": "add", "type": "stack", "temp_id": "todo", "label": "To do"},
  {"op": "add", "type": "stack", "temp_id": "doing", "label": "В роботі"},
  {"op": "add", "type": "stack", "temp_id": "done", "label": "Готово"},
  {"op": "add", "type": "task", "title": "Зібрати 10 креативів", "parent": "todo", "color": "blue"},
  {"op": "add", "type": "task", "title": "Налаштувати пікселі", "parent": "doing", "tags": ["urgent"]}
]})
```

- `assignee` — імʼя учасника робочого простору (невідоме → помилка зі списком кандидатів).
- `tags` — лише існуючі теги робочого простору.
- Перемістити картку: `{"op": "update", "id": "<task_id>", "parent": "<stack_id>"}`.
- Стікери всередині stack через MCP не підтримуються — лише `task`.
