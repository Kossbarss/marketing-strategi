# Субтитри, текст, накладки

## Вшити субтитри з .srt

```bash
ffmpeg -hide_banner -y -i input.mp4 -vf "subtitles=subs.srt:force_style='FontName=Inter,FontSize=14,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=60'" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy -movflags +faststart out/subbed.mp4
```

- `FontName` — шрифт має бути встановлений і мати кирилицю. Перевір: `fc-list | grep -i inter`. Запасні варіанти: `DejaVu Sans`, `Arial`.
- `FontSize` рахується відносно умовної висоти кадру 288, а не в пікселях: `14` на вертикальному 1080×1920 — це великий читабельний текст. Підбирай по кадру.
- Кольори у форматі `&HAABBGGRR` (порядок синій-зелений-червоний): жовтий — `&H0000FFFF`.
- `Alignment`: `2` — знизу по центру, `8` — зверху, `5` — по центру кадру. `MarginV` — відступ від краю.
- Плашка замість обводки: `BorderStyle=3,BackColour=&H80000000`.
- `MarginV` теж рахується від висоти 288: `60` піднімає текст приблизно на п'яту частину кадру. Це добре для вертикального відео, де низ закриває інтерфейс соцмережі; для горизонтального став `MarginV=20` і `FontSize=18`.
- Шлях до `.srt` з пробілами, двокрапкою чи апострофом ламає фільтр — скопіюй файл поруч під простою назвою.

Після рендеру обовʼязково витягни кадр із субтитром і подивись на нього.

Субтитри окремою доріжкою, яку можна вимкнути (не вшиваються в картинку):

```bash
ffmpeg -hide_banner -y -i input.mp4 -i subs.srt -c copy -c:s mov_text -metadata:s:s:0 language=ukr out/softsub.mp4
```

## Транскрипція (Whisper)

Потрібен пакет `faster-whisper` (`pip install faster-whisper`); модель при першому запуску качається з Hugging Face, тож потрібен доступ до `huggingface.co`.

```bash
ffmpeg -hide_banner -y -i input.mp4 -vn -ac 1 -ar 16000 out/audio.wav
```

```python
from faster_whisper import WhisperModel

def ts(t):
    h, rem = divmod(int(t * 1000), 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe("out/audio.wav", language="uk", vad_filter=True)
with open("out/subs.srt", "w", encoding="utf-8") as f:
    for i, seg in enumerate(segments, 1):
        f.write(f"{i}\n{ts(seg.start)} --> {ts(seg.end)}\n{seg.text.strip()}\n\n")
```

Моделі: `small` — швидко, `medium` або `large-v3` — точніше для української. Розпізнаний текст треба вичитати: імена, бренди й терміни Whisper часто перекручує.

Анімовані субтитри «слово за словом» роби в Remotion — скіл `remotion-captions`.

## Текст на відео

Заголовок на плашці, показується з 1-ї по 4-ту секунду:

```bash
ffmpeg -hide_banner -y -i input.mp4 -vf "drawtext=font='Inter':text='Заголовок ролика':fontsize=64:fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=24:x=(w-text_w)/2:y=h*0.12:enable='between(t,1,4)'" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy out/titled.mp4
```

Текст із двокрапкою, комою, апострофом чи відсотком клади у файл і підставляй `textfile=title.txt` замість `text=...` — так не треба нічого екранувати. Якщо `font=` не знаходить шрифт, вкажи файл: `fontfile=/шлях/до/шрифту.ttf`.

## Лого або водяний знак

У правому верхньому куті, ширина 160 px, прозорість 80%, відступ 40 px:

```bash
ffmpeg -hide_banner -y -i input.mp4 -i logo.png -filter_complex "[1:v]scale=160:-1,format=rgba,colorchannelmixer=aa=0.8[logo];[0:v][logo]overlay=W-w-40:40[v]" -map "[v]" -map 0:a? -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy out/branded.mp4
```

Позиції `overlay`: зліва зверху `40:40`, знизу справа `W-w-40:H-h-40`, по центру `(W-w)/2:(H-h)/2`.

## Картинка в картинці

Друге відео (наприклад, вебкамера) у правому нижньому куті; звук береться з основного:

```bash
ffmpeg -hide_banner -y -i screen.mp4 -i camera.mp4 -filter_complex "[1:v]scale=360:-1[pip];[0:v][pip]overlay=W-w-40:H-h-40:shortest=1[v]" -map "[v]" -map 0:a? -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac out/pip.mp4
```

## Розмити ділянку кадру

Наприклад, закрити номер чи обличчя в прямокутнику 300×200 з координатами 100:150:

```bash
ffmpeg -hide_banner -y -i input.mp4 -filter_complex "[0:v]split[base][tmp];[tmp]crop=300:200:100:150,boxblur=15[blur];[base][blur]overlay=100:150[v]" -map "[v]" -map 0:a? -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy out/blurred.mp4
```
