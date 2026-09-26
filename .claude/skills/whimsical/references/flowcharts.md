# Блок-схеми, воронки, архітектура, sequence

Перед створенням — `how_to('flowchart')`. Формат — структурований `nodes` + `edges` (Mermaid лише на прохання користувача).

## Шаблон

```json
create({
  "type": "flowchart",
  "title": "Воронка Telegram → продаж",
  "data": {
    "direction": "left-right",
    "nodes": [
      {"id": "ads", "label": "Реклама Meta", "color": "blue", "deco": "fill"},
      {"id": "lead", "label": "Лід-магніт", "color": "blue"},
      {"id": "tg", "label": "Telegram-канал", "color": "purple"},
      {"id": "q", "label": "Купив?", "shape": "diamond", "color": "orange"},
      {"id": "sale", "label": "Продаж", "color": "green", "deco": "fill"},
      {"id": "warm", "label": "Прогрів\n7 днів", "color": "yellow", "deco": "dashes"}
    ],
    "edges": [
      {"from": "ads", "to": "lead", "label": "CTR 1.5%"},
      {"from": "lead", "to": "tg"},
      {"from": "tg", "to": "q"},
      {"from": "q", "to": "sale", "label": "так", "color": "green"},
      {"from": "q", "to": "warm", "label": "ні", "style": "dotted-arrow"},
      {"from": "warm", "to": "tg", "style": "dotted-arrow"}
    ],
    "groups": [
      {"id": "paid", "label": "Платний трафік", "nodes": ["ads", "lead"], "color": "silver"}
    ]
  }
})
```

## Схема

- **Вузли**: `id`, `label` (`\n` — перенос), `shape` (`rect`, `diamond`, `ellipse`, `pill`, `hexagon`, `cylinder`, `parallelogram`, `triangle`, `cloud`, `star`, `trapezoid`), `color`, `deco` (`fill`/`outline`/`dashes`), `icon` (перекриває shape).
- **Ребра**: `from`, `to`, `label`, `style` (`arrow`, `dotted-arrow`, `open`, `thick-arrow`), `color`, `from_endpoint`/`to_endpoint` (`one-one`, `zero-many`, `one-many`… — для ER).
- **Групи**: `groups: [{id, label, nodes, color, style: outline|fill}]` — зони, етапи, команди, сервіси.
- **Напрям**: `left-right` (дефолт, краще з іконками), `top-down`, `right-left`, `bottom-top`.

## Конвенції форм

| Форма | Значення |
|---|---|
| `pill` / `ellipse` | Старт / фініш |
| `rect` | Дія / етап |
| `diamond` | Рішення (підписуй гілки «так/ні») |
| `cylinder` | База даних / CRM / таблиця |
| `parallelogram` | Вхідні/вихідні дані |
| `cloud` | Зовнішній сервіс |
| `hexagon` | AI-агент / автоматизація |

Іконки сервісів: `how_to({domain:{type:'icon', query:'telegram'}})` (є AWS/Azure/GCP та 4500+ UI-іконок).

## Sequence-діаграма

Без `how_to` для простих випадків:

```json
create({"type": "sequence_diagram", "title": "Лід → CRM",
  "data": {"diagram": "Користувач -> Бот: /start\nБот -> Make: webhook\nMake -> CRM: створити лід\nCRM --> Бот: id ліда\nБот ->> Користувач: вітальне повідомлення"}})
```

`->` суцільна, `-->` пунктир (відповідь), `->>` відкрита стрілка.

## Редагування

- Спершу `fetch({id: board_id, scope: <flowchart_id>})` — отримати реальні підписи вузлів.
- `edit` з `find_replace` / `delete_by_text` для перейменування і видалення вузлів.
- Додати багато вузлів або змінити структуру — простіше видалити діаграму і створити заново одним викликом.

## Типові помилки

- Кілька `create` на одну логічну схему → розрізнені діаграми, що накладаються. Один процес = один виклик.
- Довгі підписи → роздуті вузли. Деталі винось у нотатку поруч (`edit` add `note`).
- Рішення без підписаних гілок.
