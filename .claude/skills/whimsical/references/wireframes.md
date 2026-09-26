# Wireframe (лендинги, екрани, дашборди)

**Обовʼязково** `how_to('wireframe')` перед створенням і `how_to('wireframe-edit')` перед редагуванням. Wireframe вимагає `board_id` — спершу створи дошку (`create({type:'board', title})`).

## Формат — hiccup-масив

`[tag, attrs?, ...children]`. Діти можуть бути лише в `"div"`. Стилі розкладки — в `"layout/style"` (flexbox: `flex-direction`, `gap`, `padding`, `align-items`, `justify-content`, `flex`, `width`, `height`).

```json
create({
  "type": "wireframe",
  "board_id": "<board_id>",
  "title": "Лендинг — перший екран",
  "data": {
    "frame_type": "desktop",
    "layout": ["div", {"layout/style": {"flex-direction": "column", "padding": 40, "gap": 24}},
      ["div", {"layout/style": {"flex-direction": "row", "justify-content": "space-between", "align-items": "center"}},
        ["text", {"text": "**Logo**", "font-size": "l0"}],
        ["w-h-tabs", {"items": ["Послуги", "Кейси", "Ціни", "Контакти"], "size": "s"}],
        ["w-button", {"text": "Консультація", "color": "blue"}]],
      ["text", {"text": "**AI-маркетинг, який приносить лідів**", "font-size": "l2"}],
      ["text", {"text": "Налаштуємо рекламу і воронку за 14 днів"}],
      ["div", {"layout/style": {"flex-direction": "row", "gap": 12}},
        ["w-button", {"text": "Отримати аудит", "color": "blue"}],
        ["w-link", {"text": "Дивитись кейси", "icon-name": "chevron-right", "icon-placement": "right"}]],
      ["w-shape", {"layout/style": {"height": 280}}]]
  }
})
```

## Frame types

`desktop` (1080×960), `plain` (960×600), `iphone-14`, `iphone-x`, `iphone-8`, `ipad`, `android`, `android-tablet`, `apple-watch`.

## Елементи

- Форми (мають `label`): `w-input`, `w-textarea`, `w-dropdown`, `w-checkbox`, `w-radio-button`, `w-slider`, `w-progress-bar`, `w-stars`
- Інтерактив: `w-button`, `w-link`, `w-toggle`, `w-h-tabs`, `w-v-tabs`, `w-tag`, `w-tooltip`, `w-annotation`
- Візуал: `w-shape` (плейсхолдер картинки/відео), `w-divider`, `w-overlay`, `w-pattern`, `w-lorem`, `w-block-font`, `w-icon` (завжди з `icon-name`)
- Текст і заголовки — тільки `text` з `font-size` (`xs`…`l2`). `w-lorem`/`w-block-font` — нечитабельні плейсхолдери.

## Правила

- Кнопка на всю ширину: `"layout/style": {"align-self": "stretch"}`.
- Не задавай вузьку `width` елементам `text` — обрізається текст.
- Кілька екранів — кілька `create` на одній дошці; вони самі стають праворуч.
- Стрілки переходів між екранами — `edit` → `conn` між елементами.
- Після створення — `fetch image:true` і перевірка: нічого не обрізано, ієрархія читається.
