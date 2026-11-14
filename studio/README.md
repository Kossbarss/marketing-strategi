# Студія — памʼять і структура

Тут лежать тексти: профілі авторів, розбори референсів, сценарії та історія проєктів. Медіафайли (відео, аудіо, фото) в репозиторій не кладемо.

## Структура репозиторію

```
studio/
  authors/<автор>/profile.md  voice.md  look.md
  references/<платформа>_<назва>/analysis.md
  projects/<дата_назва>/brief.md  script.md  shotlist.md  edit.md
```

Проєкт посилається на автора й референси, але нічого з них не копіює.

## Google Drive

Коренева папка: [Studio](https://drive.google.com/drive/folders/1cH9qX7RAEllK_iLBlgAGOrUMWPio9QwN)

| Папка | Вміст | ID |
|---|---|---|
| `01_Authors/<автор>/voice, photos, video` | Матеріали авторів | `15thrTgqBu-I74N1O3GF6vq7nLtEQ67Rw` |
| `02_References/youtube, instagram, tiktok, threads` | Відео-референси | `1q-uTIo5KT7QOLKeH0vhvdB3VYxSJWsa4` |
| `03_Projects/<дата_назва>/source, generations, edit, final` | Файли проєктів | `1QdSR1fEpzpSOhP1MLh2RfbCWbQXcxk1T` |
| `04_Assets/music, sfx, fonts, logos` | Спільні ресурси | `1ykYhKhuksrB0Blotc6BHpMBnleV4IPaS` |

## Перевірені обмеження хмарної сесії (2026-11-14)

- **Запис на Drive:** не більше ~3 МБ на файл. Тестове відео 9 МБ і 20 МБ не завантажилось. Готові ролики на Drive з хмарної сесії покласти не можна.
- **Читання відео з Drive:** не перевірено.
- **Мережа:** YouTube, Instagram, TikTok, Threads і Hugging Face заблоковані правилами середовища `Default Cloud Environment`. Завантаження референсів через `yt-dlp` і моделі Whisper недоступні, доки хости не додано.
- **Відеокарта:** немає, 4 ядра CPU, 15 ГБ памʼяті.
- **Встановлюється без проблем:** `yt-dlp`, `faster-whisper`, `scenedetect` (з PyPI); `ffmpeg` є в системі.
