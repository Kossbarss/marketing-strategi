# Звук

## Витягти, прибрати, замінити

Аудіо в MP3:

```bash
ffmpeg -hide_banner -y -i input.mp4 -vn -c:a libmp3lame -q:a 2 out/audio.mp3
```

WAV 16 кГц моно — формат для транскрипції:

```bash
ffmpeg -hide_banner -y -i input.mp4 -vn -ac 1 -ar 16000 out/audio.wav
```

Відео без звуку:

```bash
ffmpeg -hide_banner -y -i input.mp4 -an -c:v copy out/silent.mp4
```

Замінити доріжку (відео не перекодовується, довжина — за коротшим входом):

```bash
ffmpeg -hide_banner -y -i input.mp4 -i voice.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out/replaced.mp4
```

## Гучність

Нормалізація до −14 LUFS (стандарт YouTube і більшості соцмереж), один прохід:

```bash
ffmpeg -hide_banner -y -i input.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:v copy -c:a aac -b:a 192k -ar 48000 out/normalized.mp4
```

Виміряти поточну гучність, нічого не записуючи (дивись `input_i` у JSON наприкінці):

```bash
ffmpeg -hide_banner -i input.mp4 -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | tail -15
```

Просто тихіше або голосніше: `-af "volume=0.5"` чи `-af "volume=6dB"`.

## Чистка голосу

Зріз низьких частот, шумодав і легка компресія:

```bash
ffmpeg -hide_banner -y -i input.mp4 -af "highpass=f=80,afftdn=nr=12:nf=-30,acompressor=threshold=-18dB:ratio=3:attack=5:release=120" -c:v copy -c:a aac -b:a 192k out/clean.mp4
```

`nr` — сила шумодаву в дБ: 6–12 мʼяко, понад 20 звук стає «металевим». Нормалізацію гучності роби окремим кроком після чистки.

## Музика під голос (ducking)

Музика зациклена на всю довжину ролика і притишується, коли звучить голос:

```bash
ffmpeg -hide_banner -y -i input.mp4 -stream_loop -1 -i music.mp3 -filter_complex "[0:a]asplit[voice][key];[1:a]volume=0.4[music];[music][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[ducked];[voice][ducked]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest out/with_music.mp4
```

Крутилки: `volume` — базова гучність музики, `ratio` — наскільки сильно вона сідає під голосом, `release` — як швидко повертається (мс).

Музика на відео без власного звуку:

```bash
ffmpeg -hide_banner -y -i input.mp4 -stream_loop -1 -i music.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out/music_only.mp4
```

## Фейди звуку

Для ролика 10 с: поява 1 с, зникнення останні 2 с:

```bash
ffmpeg -hide_banner -y -i input.mp4 -af "afade=t=in:st=0:d=1,afade=t=out:st=8:d=2" -c:v copy -c:a aac out/afade.mp4
```

## Прибрати тишу

Знайти паузи (тихіше −35 дБ і довше 0.6 с):

```bash
ffmpeg -hide_banner -i input.mp4 -af "silencedetect=noise=-35dB:d=0.6" -vn -f null - 2>&1 | grep silence_
```

Вирізати паузи з відео і звуку разом — скрипт зі скіла (шлях від кореня репозиторію):

```bash
python3 .claude/skills/ffmpeg/scripts/cut_silence.py input.mp4 out/tight.mp4 --noise -35 --min-silence 0.6 --pad 0.15
```

- `--noise` — поріг тиші в дБ. Шумний запис: −30, студійний: −40.
- `--min-silence` — паузи коротші за це значення лишаються.
- `--pad` — скільки секунд тиші залишити з кожного боку фрази, щоб мова не звучала рубано.
- `--dry-run` — лише показати, які фрагменти залишаться.

Скрипт перекодовує відео (libx264, CRF 20) і друкує, скільки секунд вирізано. Якщо тиші не знайдено, файл не створюється.
