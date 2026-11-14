#!/usr/bin/env python3
"""Вирізає паузи (тишу) з відео: шукає їх через silencedetect і склеює решту.

Приклад:
    python3 cut_silence.py input.mp4 out/tight.mp4 --noise -35 --min-silence 0.6 --pad 0.15
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    out = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
        "-of", "default=noprint_wrappers=1", path,
    ])
    if out.returncode != 0:
        sys.exit(f"ffprobe не зміг прочитати файл: {out.stderr.strip()}")
    duration = None
    kinds = set()
    for line in out.stdout.splitlines():
        key, _, value = line.partition("=")
        if key == "duration" and value not in ("", "N/A"):
            duration = float(value)
        elif key == "codec_type":
            kinds.add(value)
    if duration is None:
        sys.exit("Не вдалося визначити тривалість файлу.")
    return duration, "video" in kinds, "audio" in kinds


def find_silences(path, noise_db, min_silence):
    out = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vn",
        "-af", f"silencedetect=noise={noise_db}dB:d={min_silence}", "-f", "null", "-",
    ])
    if out.returncode != 0:
        sys.exit(f"ffmpeg завершився з помилкою:\n{out.stderr[-2000:]}")
    silences = []
    start = None
    for line in out.stderr.splitlines():
        m = re.search(r"silence_start: (-?[0-9.]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
            continue
        m = re.search(r"silence_end: (-?[0-9.]+)", line)
        if m and start is not None:
            silences.append((start, float(m.group(1))))
            start = None
    if start is not None:
        silences.append((start, None))  # тиша до кінця файлу
    return silences


def keep_segments(silences, duration, pad, min_keep=0.05):
    segments = []
    cursor = 0.0
    for start, end in silences:
        end = duration if end is None else end
        cut_from = start + pad
        cut_to = end - pad
        if cut_to <= cut_from:
            continue  # пауза коротша за подвійний відступ — лишаємо
        if cut_from - cursor >= min_keep:
            segments.append((cursor, cut_from))
        cursor = cut_to
    if duration - cursor >= min_keep:
        segments.append((cursor, duration))
    return segments


def main():
    p = argparse.ArgumentParser(description="Вирізати тишу з відео або аудіо")
    p.add_argument("input")
    p.add_argument("output")
    p.add_argument("--noise", type=float, default=-35.0, help="поріг тиші, дБ (типово -35)")
    p.add_argument("--min-silence", type=float, default=0.6, help="мінімальна довжина паузи, с (типово 0.6)")
    p.add_argument("--pad", type=float, default=0.15, help="скільки тиші лишити з кожного боку, с (типово 0.15)")
    p.add_argument("--crf", type=int, default=20)
    p.add_argument("--dry-run", action="store_true", help="лише показати фрагменти, нічого не записувати")
    args = p.parse_args()

    if os.path.abspath(args.input) == os.path.abspath(args.output):
        sys.exit("Вихідний файл збігається з вхідним — вкажи інший шлях.")

    duration, has_video, has_audio = probe(args.input)
    if not has_audio:
        sys.exit("У файлі немає аудіодоріжки — тишу шукати ніде.")

    silences = find_silences(args.input, args.noise, args.min_silence)
    segments = keep_segments(silences, duration, args.pad)
    kept = sum(b - a for a, b in segments)

    print(f"Тривалість: {duration:.2f} с, знайдено пауз: {len(silences)}")
    for a, b in segments:
        print(f"  лишити {a:8.2f} – {b:8.2f}")
    print(f"Залишиться {kept:.2f} с, вирізано {duration - kept:.2f} с")

    if not segments:
        sys.exit("Увесь файл розпізнано як тишу — знизь поріг --noise (наприклад, -45).")
    if duration - kept < 0.01:
        print("Пауз для вирізання не знайдено — файл не створено.")
        return
    if args.dry_run:
        return

    parts = []
    labels = []
    for i, (a, b) in enumerate(segments):
        if has_video:
            parts.append(f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{i}]")
            labels.append(f"[v{i}]")
        parts.append(f"[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS[a{i}]")
        labels.append(f"[a{i}]")
    v = 1 if has_video else 0
    outs = "[v][a]" if has_video else "[a]"
    parts.append(f"{''.join(labels)}concat=n={len(segments)}:v={v}:a=1{outs}")

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        f.write(";\n".join(parts))
        script = f.name
    try:
        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", args.input,
               "-filter_complex_script", script]
        if has_video:
            cmd += ["-map", "[v]", "-c:v", "libx264", "-crf", str(args.crf),
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
        cmd += ["-map", "[a]"]
        if has_video:
            cmd += ["-c:a", "aac", "-b:a", "192k"]
        cmd.append(args.output)
        res = subprocess.run(cmd)
    finally:
        os.unlink(script)
    if res.returncode != 0:
        sys.exit("ffmpeg не зміг зібрати файл.")
    print(f"Готово: {args.output}")


if __name__ == "__main__":
    main()
