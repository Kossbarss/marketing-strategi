# Нарізка, склейка, кадр

Усі приклади пишуть у `out/`. Заміни `input.mp4` на свій файл.

## Обрізати фрагмент

Точно до кадру (з перекодуванням) — з 00:00:05, тривалість 10 с:

```bash
ffmpeg -hide_banner -y -ss 00:00:05 -i input.mp4 -t 10 -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart out/clip.mp4
```

Швидко, без перекодування (ріже по ключових кадрах, початок може зсунутися на 1–2 с):

```bash
ffmpeg -hide_banner -y -ss 00:00:05 -i input.mp4 -t 10 -c copy out/clip_fast.mp4
```

`-ss` перед `-i` — швидкий пошук. `-t` — тривалість, `-to` — кінцева позначка (відлік від початку вихідного файлу, якщо `-ss` стоїть перед `-i`).

## Нарізати на рівні частини

По 30 с без перекодування (межі — по ключових кадрах):

```bash
ffmpeg -hide_banner -y -i input.mp4 -c copy -map 0 -f segment -segment_time 30 -reset_timestamps 1 out/part_%03d.mp4
```

## Склеїти

Файли з однаковими кодеком, розміром і fps — без перекодування. Шляхи у списку відносні до самого списку:

```bash
printf "file '%s'\n" a.mp4 b.mp4 c.mp4 > list.txt
ffmpeg -hide_banner -y -f concat -safe 0 -i list.txt -c copy out/joined.mp4
```

Різні файли — привести до одного вигляду і склеїти фільтром (тут 1080×1920, 30 fps; в обох має бути звук):

```bash
ffmpeg -hide_banner -y -i a.mp4 -i b.mp4 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v0];[1:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v1];[0:a]aresample=48000[a0];[1:a]aresample=48000[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -movflags +faststart out/joined.mp4
```

Якщо в кліпі немає звуку, додай тишу входом `-f lavfi -t <тривалість> -i anullsrc=r=48000:cl=stereo`.

## Перехід між двома кліпами

`offset` = тривалість першого кліпу мінус тривалість переходу. Кліпи мають бути одного розміру і fps.

```bash
ffmpeg -hide_banner -y -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5[v];[0:a][1:a]acrossfade=d=0.5[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac out/xfade.mp4
```

Інші значення `transition`: `wipeleft`, `slideup`, `circleopen`, `dissolve`, `smoothleft`, `zoomin`.

## Вертикальний формат 9:16

Кроп по центру (втрачаються боки):

```bash
ffmpeg -hide_banner -y -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy -movflags +faststart out/vertical_crop.mp4
```

Кроп зі зсувом: `crop=1080:1920:X:0`, де `X` — відступ зліва у вже масштабованому кадрі.

Ціле відео на розмитому фоні (нічого не обрізається):

```bash
ffmpeg -hide_banner -y -i input.mp4 -filter_complex "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg];[b]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[v]" -map "[v]" -map 0:a? -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -movflags +faststart out/vertical_blur.mp4
```

Для 4:5 підстав `1080:1350`, для квадрата — `1080:1080`.

## Швидкість

Удвічі швидше (відео і звук). `atempo` приймає 0.5–100; для сповільнення вдвічі — `setpts=2*PTS` і `atempo=0.5`:

```bash
ffmpeg -hide_banner -y -i input.mp4 -filter_complex "[0:v]setpts=PTS/2[v];[0:a]atempo=2[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac out/fast.mp4
```

## Поворот, дзеркало, fps

```bash
ffmpeg -hide_banner -y -i input.mp4 -vf "transpose=1" -c:a copy out/rot90.mp4
```

`transpose=1` — на 90° за годинниковою, `2` — проти, `hflip` — дзеркало, `fps=30` — змінити частоту кадрів.

## Плавна поява і зникнення

Фейд 0.5 с на початку і в кінці ролика тривалістю 10 с (`st` кінцевого фейду = тривалість − 0.5):

```bash
ffmpeg -hide_banner -y -i input.mp4 -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=9.5:d=0.5" -af "afade=t=in:st=0:d=0.5,afade=t=out:st=9.5:d=0.5" -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac out/faded.mp4
```

## Стабілізація

Два проходи; потрібна збірка ffmpeg з `vidstab` (перевір: `ffmpeg -filters | grep vidstab`):

```bash
ffmpeg -hide_banner -y -i input.mp4 -vf vidstabdetect=shakiness=5:result=transforms.trf -f null -
ffmpeg -hide_banner -y -i input.mp4 -vf vidstabtransform=input=transforms.trf:smoothing=20,unsharp=5:5:0.8 -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a copy out/stable.mp4
```

## Знайти зміни сцен

Друкує час кожної склейки; `0.3` — чутливість (менше — більше спрацювань). Порожній вивід означає, що склейок не знайдено:

```bash
ffmpeg -hide_banner -i input.mp4 -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*"
```
