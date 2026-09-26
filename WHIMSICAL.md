# Whimsical × Claude Code

Набір для роботи з Whimsical у Claude Code: MCP-сервер, навичка і 5 агентів.

## Що в репозиторії

```
.mcp.json                          — офіційний Whimsical MCP (https://mcp.whimsical.com/mcp)
.claude/skills/whimsical/
  SKILL.md                         — маршрутизатор: який тип діаграми, які інструменти
  references/flowcharts.md         — блок-схеми, воронки, архітектура, ER, sequence
  references/mindmaps.md           — mind map і техніки мозкового штурму
  references/wireframes.md         — лендинги, екрани, дашборди
  references/stickies-kanban.md    — стікери, ретро, SWOT, kanban
  references/tables-docs.md        — таблиці, доки, маркетингові шаблони таблиць
  references/boards-layout.md      — довільні дошки, кілька діаграм на дошці
  references/review-cleanup.md     — чек-лист перевірки і виправлення
.claude/agents/
  whimsical-architect.md           — схеми систем, воронок, автоматизацій, коду
  whimsical-brainstorm.md          — мозкові штурми → mind map + стікери + ICE
  whimsical-reviewer.md            — перевірка і виправлення дошок, звірка з кодом
  whimsical-tables.md              — таблиці, контент-/медіаплани, kanban
  whimsical-wireframer.md          — wireframe лендингів і застосунків
```

## Встановлення

**Варіант А — працювати в цьому репозиторії.** Відкрий його в Claude Code: `.mcp.json`, навичка і агенти підхопляться автоматично. При першому запуску погодься підключити сервер `whimsical`, потім `/mcp` → увійди в акаунт Whimsical.

**Варіант Б — поставити глобально (для всіх проєктів):**

```bash
claude mcp add --transport http --scope user whimsical https://mcp.whimsical.com/mcp
git clone https://github.com/kossbarss/marketing-strategi /tmp/ms
mkdir -p ~/.claude/skills ~/.claude/agents
cp -r /tmp/ms/.claude/skills/whimsical ~/.claude/skills/
cp /tmp/ms/.claude/agents/whimsical-*.md ~/.claude/agents/
```

Потім у Claude Code: `/mcp` → авторизація Whimsical, `/agents` — перевірити, що агенти видно.

## Як користуватися

- Звичайний запит: «намалюй у Whimsical воронку для Telegram-каналу» — спрацює навичка `whimsical`.
- Явно агентом: «use whimsical-brainstorm: ідеї контенту для AI-маркетолога на жовтень».
- Фоном: агенти запускаються у фоні (Claude продовжує розмову, результат приходить сповіщенням). Можна кілька одночасно: «паралельно: architect — схема воронки, tables — медіаплан, потім reviewer — перевір обидві дошки».

## Інші джерела з GitHub

| Репозиторій | Що це |
|---|---|
| [WhimsicalCode/mcp-server-guide](https://github.com/WhimsicalCode/mcp-server-guide) | Офіційний MCP-сервер і інструкції (використаний тут) |
| [sambt94/whimsical-plugin](https://github.com/sambt94/whimsical-plugin) | 8 навичок під старий desktop-MCP (інші назви інструментів) — ідеї з нього враховані |
| [BrockReece/whimsical-mcp-server](https://github.com/BrockReece/whimsical-mcp-server) | Неофіційний MCP (Mermaid → Whimsical), запасний варіант |
| [FdezRomero/whimsical-exporter](https://github.com/FdezRomero/whimsical-exporter) | CLI: експорт дошок у PNG/PDF/SVG |
| [WhimsicalCode/obsidian-whimsical-plugin](https://github.com/WhimsicalCode/obsidian-whimsical-plugin) | Живі дошки Whimsical в Obsidian |

Документація: [whimsical.com/learn/integrations/mcp](https://whimsical.com/learn/integrations/mcp), [довідник інструментів](https://whimsical.com/learn/ai/mcp-tools).
