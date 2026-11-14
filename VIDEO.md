# Відео × Claude Code: Remotion і FFmpeg

Скіли для монтажу й створення відео в Claude Code. Підхоплюються автоматично, коли репозиторій відкрито в Claude Code.

## Що в репозиторії

```
.claude/skills/ffmpeg/
  SKILL.md                          — маршрутизатор: аналіз файлу, правила, пресети платформ
  references/cut-concat.md          — нарізка, склейка, переходи, вертикальний формат, швидкість
  references/audio.md               — гучність, шумодав, музика під голос, прибрати тишу
  references/subtitles-overlays.md  — субтитри, текст, лого, картинка в картинці, Whisper
  references/export-formats.md      — експорт під соцмережі, стиснення, GIF, превʼю, слайдшоу
  scripts/cut_silence.py            — вирізає паузи з відео
.claude/skills/remotion-*/          — 13 офіційних скілів Remotion (версія 4.0.543)
```

## Коли який

| Задача | Скіл |
|---|---|
| Обрізати, склеїти, стиснути, переформатувати, звук, вшити готові субтитри | `ffmpeg` |
| Анімована графіка, титри, караоке-субтитри, відео з шаблону чи даних | `remotion-best-practices` (маршрутизатор до решти) |
| Сирий матеріал + графіка | `ffmpeg` готує кліпи → Remotion збирає ролик |

## Скіли Remotion

Скопійовані без змін з [remotion-dev/skills](https://github.com/remotion-dev/skills):

| Скіл | Для чого |
|---|---|
| `remotion-best-practices` | Вхідна точка, веде до решти |
| `remotion-create` | Новий проєкт або композиція |
| `remotion-markup` | Розмітка: анімації, таймінг, шрифти, медіа, ефекти |
| `remotion-captions` | Транскрипція й анімовані субтитри |
| `remotion-studio` | Запуск превʼю |
| `remotion-render` | Рендер у відео або кадр |
| `remotion-maps` | Анімовані карти |
| `remotion-multimedia` | Метадані й обробка медіа (Mediabunny) |
| `remotion-interactivity` | Розмітка, яку можна редагувати в Studio |
| `remotion-saas` | Застосунки на Remotion |
| `remotion-docs` | Пошук по документації |
| `remotion-license` | Ліцензія |
| `remotion-upgrade` | Оновлення Remotion і самих скілів |

Оновити до свіжої версії: `npx skills add remotion-dev/skills` або скіл `remotion-upgrade`.

## Що потрібно встановити

- **FFmpeg:** `apt install ffmpeg` або `brew install ffmpeg`. Опційно `imagemagick`, `yt-dlp`, `faster-whisper`.
- **Remotion:** Node.js 18+. Проєкт створюється командою `npx create-video@latest`; при першому рендері Remotion сам завантажує браузер.

## Ліцензія Remotion

Remotion безкоштовний для приватних осіб і компаній до 3 працівників; більшим компаніям потрібна платна ліцензія. Умови: [remotion.dev/docs/license](https://www.remotion.dev/docs/license).

## Приклади запитів

- «Наріж `interview.mp4` на три кліпи по 30 секунд у форматі 9:16 і вший субтитри з `subs.srt`».
- «Прибери паузи з `talk.mp4` і вирівняй гучність до −14 LUFS».
- «Зроби в Remotion 15-секундне інтро з логотипом і анімованим заголовком».
