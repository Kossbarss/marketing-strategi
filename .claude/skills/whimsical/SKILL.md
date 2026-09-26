---
name: whimsical
description: Будує і редагує контент у Whimsical через офіційний MCP (mcp.whimsical.com) — блок-схеми, воронки, архітектуру систем, mind map для мозкових штурмів, wireframe, стікери, kanban, таблиці, доки. Використовуй щоразу, коли треба щось намалювати, візуалізувати, структурувати, побудувати схему/воронку/таблицю/дошку у Whimsical, або перевірити/прибрати існуючу дошку. Triggers: whimsical, diagram, flowchart, mind map, brainstorm, wireframe, sticky notes, kanban, board, схема, воронка, майндмеп, дошка.
---

# Whimsical — маршрутизатор

Вхідна точка для будь-якої роботи у Whimsical. Спершу обери тип, потім відкрий відповідний файл у `references/`.

## Інструменти MCP (актуальні назви)

Сервер може називатися `whimsical` (локальний `.mcp.json`) або `Whimsical` (конектор claude.ai) — інструменти однакові:

| Інструмент | Для чого |
|---|---|
| `how_to` | Довідка по синтаксису. **Обовʼязково** перед flowchart, wireframe, board. `how_to({domain:{type:'icon'|'color'|'font-size', query}})` — пошук іконок/кольорів |
| `create` | Створити `board`, `flowchart`, `mindmap`, `sequence_diagram`, `sticky_notes`, `table`, `wireframe`, `folder`, `doc` |
| `edit` | Додати/змінити/видалити обʼєкти на дошці (shape, text, note, conn, icon, link, task, stack, table), `find_replace` у діаграмах, редагування доків |
| `fetch` | Прочитати дошку/док/папку. `image:true` — PNG-знімок для візуальної перевірки. `scope:<diagram_id>` — зайти всередину діаграми |
| `search`, `file_tree`, `list_workspaces` | Знайти файли, папки, команди |
| `doc_create` | Створити док (markdown) |
| `wireframe_edit` | Редагувати wireframe після створення |
| `auto_layout` | Перерозкласти дошку/діаграму |
| `comment_read`, `comment_edit` | Коментарі |
| `move`, `delete` | Перемістити / видалити файли |

## Який тип обрати

| Задача | Тип | Довідка |
|---|---|---|
| Процес, рішення, воронка, архітектура, ER-діаграма | `flowchart` | `references/flowcharts.md` |
| Хто кому що надсилає в часі (API, інтеграції, бот ↔ CRM) | `sequence_diagram` | `references/flowcharts.md` |
| Ієрархія, мозковий штурм, структура контенту, дерево ідей | `mindmap` | `references/mindmaps.md` |
| Екран, лендинг, дашборд, мобільний UI | `wireframe` | `references/wireframes.md` |
| Набір коротких ідей, ретро, плюси/мінуси | `sticky_notes` | `references/stickies-kanban.md` |
| Kanban, задачі з виконавцями і тегами | `edit` → `stack` + `task` | `references/stickies-kanban.md` |
| Табличні дані, контент-план, бюджет, порівняння | `table` / таблиця в доці | `references/tables-docs.md` |
| Текстовий документ, бриф, ТЗ | `doc_create` | `references/tables-docs.md` |
| Довільний макет, відтворення скетчу, кілька діаграм на одній дошці | `board` | `references/boards-layout.md` |
| «Прибери дошку», перевірка якості | — | `references/review-cleanup.md` |

Евристика: є стрілки між кроками → flowchart. Є дерево → mindmap. Є UI → wireframe. Є купа нотаток → sticky_notes. Сумніваєшся — flowchart.

## Стандартний цикл роботи

1. **Знайди місце**: `search` / `file_tree`, якщо користувач згадав існуючу дошку. Інакше створюй нову (без `board_id`).
2. **Прочитай синтаксис**: `how_to('<тип>')` для flowchart / wireframe / board.
3. **Створи одним викликом**: вся діаграма — в одному `create`. Кілька діаграм на дошці — через `placement` відносно bbox попередньої.
4. **Перевір візуально**: `fetch({id: board_id, image: true})`. Шукай накладання, обрізаний текст, хаотичні лінії.
5. **Виправ**: `edit` (update/find_replace) або `auto_layout`; для великих змін — видали і перебудуй.
6. **Віддай посилання** на дошку користувачу.

## Кольори за роллю

| Роль | Колір |
|---|---|
| Основне / вхід | `blue` |
| Успіх / конверсія / прибуток | `green` |
| Ризик / увага | `orange` |
| Помилка / втрата / відтік | `red` |
| AI / автоматизація / обробка | `purple` |
| Примітка / гіпотеза | `yellow` |
| Фон / групи / другорядне | `silver` |

Hex (`#7D82B8`) теж приймається — підганяється під найближчий колір палітри.

## Правила

- Мова підписів = мова користувача (за замовчуванням українська).
- Підписи короткі: 1–5 слів на вузол, деталі — в нотатки/док.
- Не вигадуй звʼязків, яких немає у вхідних даних.
- Великі схеми (>25 вузлів) розбивай на кілька діаграм з `placement` або групами (`groups`).
- Після кожного створення — перевірка через `fetch image:true`, потім посилання.
