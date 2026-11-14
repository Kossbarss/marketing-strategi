# Експорт, стиснення, формати

## Універсальний експорт під соцмережі

H.264 + AAC, 30 fps — приймають Instagram, TikTok, YouTube, LinkedIn, Telegram:

```bash
ffmpeg -hide_banner -y -i input.mp4 -c:v libx264 -crf 20 -preset medium -profile:v high -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 -movflags +faststart out/final.mp4
```

`-crf` керує якістю: 18 — майже без втрат, 20–23 — стандарт, 26–28 — помітно менший файл. `-preset slow` дає менший файл за ту саму якість, але рендерить довше.

## Зменшити файл

Найпростіше — вищий CRF і менший кадр (тут до 720 px по висоті):

```bash
ffmpeg -hide_banner -y -i input.mp4 -vf "scale=-2:720" -c:v libx264 -crf 26 -preset slow -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart out/small.mp4
```

У заданий розмір — два проходи. Бітрейт відео в кбіт/с = `розмір_МБ × 8000 / тривалість_с − бітрейт_аудіо`, і відніми ще ~3% запасу. Приклад: 20 МБ на 60 с → 20×8000/60 − 128 ≈ 2538, беремо 2450k:

```bash
ffmpeg -hide_banner -y -i input.mp4 -c:v libx264 -b:v 2450k -preset slow -pix_fmt yuv420p -pass 1 -passlogfile out/pass -an -f null /dev/null
ffmpeg -hide_banner -y -i input.mp4 -c:v libx264 -b:v 2450k -preset slow -pix_fmt yuv420p -pass 2 -passlogfile out/pass -c:a aac -b:a 128k -movflags +faststart out/sized.mp4
```

Після цього прибери файли `out/pass-0.log*`.

## GIF

З власною палітрою (без неї кольори «сиплються»). 3 с із 2-ї секунди, 12 fps, ширина 480:

```bash
ffmpeg -hide_banner -y -ss 2 -t 3 -i input.mp4 -vf "fps=12,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" out/clip.gif
```

GIF швидко росте: тримай до 5 с, 10–15 fps, ширину до 480–600 px. Для сайту краще WebM або MP4 без звуку.

## WebM для сайту

```bash
ffmpeg -hide_banner -y -i input.mp4 -c:v libvpx-vp9 -crf 32 -b:v 0 -row-mt 1 -c:a libopus -b:a 96k out/web.webm
```

## Превʼю і розкадрування

Один кадр як обкладинка:

```bash
ffmpeg -hide_banner -y -ss 3 -i input.mp4 -frames:v 1 -q:v 2 out/cover.jpg
```

Кадр кожні 5 с:

```bash
ffmpeg -hide_banner -y -i input.mp4 -vf "fps=1/5" -q:v 2 out/frame_%03d.jpg
```

Контактний лист 4×3 одним файлом — зручно швидко оглянути довге відео:

```bash
ffmpeg -hide_banner -y -i input.mp4 -vf "fps=1/5,scale=320:-1,tile=4x3" -frames:v 1 -q:v 3 out/sheet.jpg
```

Підбери `fps` так, щоб кадрів вистачило на сітку: для 12 клітинок на 60 с — `fps=1/5`.

## Відео з фото

Одне фото на 5 с з повільним наближенням (Ken Burns), вертикальний кадр:

```bash
ffmpeg -hide_banner -y -loop 1 -i photo.jpg -vf "scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='min(zoom+0.0008,1.15)':d=150:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30" -t 5 -c:v libx264 -crf 20 -pix_fmt yuv420p out/photo_zoom.mp4
```

`d` = тривалість × fps. Попереднє збільшення вдвічі прибирає тремтіння зуму.

Слайдшоу з нумерованих фото `img_001.jpg, img_002.jpg…`, по 3 с на кадр:

```bash
ffmpeg -hide_banner -y -framerate 1/3 -i img_%03d.jpg -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30" -c:v libx264 -crf 20 -pix_fmt yuv420p out/slideshow.mp4
```

Кілька кліпів з фото потім зʼєднуються через `xfade` (див. `cut-concat.md`).

## Зображення (ImageMagick)

Обкладинка YouTube 1280×720 з кадру:

```bash
convert out/cover.jpg -resize 1280x720^ -gravity center -extent 1280x720 -quality 90 out/thumb.jpg
```

## Майстер для подальшого монтажу

ProRes 422 HQ — великий файл без помітних втрат, для передачі монтажеру:

```bash
ffmpeg -hide_banner -y -i input.mp4 -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le -c:a pcm_s16le out/master.mov
```

## Завантажити відео за посиланням

Потрібен `yt-dlp` (`pip install yt-dlp`). Найкраща якість до 1080p у MP4:

```bash
yt-dlp -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[ext=mp4]" -o "src/%(title)s.%(ext)s" "URL"
```

Тільки звук: `yt-dlp -x --audio-format mp3 "URL"`. Завантажуй лише те, на використання чого є права.
