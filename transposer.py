import os
import subprocess
import time

from music21 import converter, interval
from music21 import environment

us = environment.UserSettings()
us['musescoreDirectPNGPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'  # обнови путь при необходимости

AUDIVERIS_PATH = r'M:\Programs\Audiveris\Audiveris.exe'  # путь к Audiveris

def run_audiveris(image_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    cmd = [
        AUDIVERIS_PATH,
        '-batch',
        '-export',
        '-output', output_dir,
        image_path
    ]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ошибка запуска Audiveris: {e}")

    # Ищем результат в output_dir с разными расширениями
    possible_exts = ['.musicxml', '.xml', '.mxl']
    for ext in possible_exts:
        musicxml_path = os.path.join(output_dir, base_name + ext)
        if os.path.exists(musicxml_path):
            return musicxml_path

    raise FileNotFoundError(f"MusicXML файл не найден в {output_dir} после обработки Audiveris.")

def transpose_score(score, semitones):
    if semitones == 0:
        return score
    i = interval.Interval(semitones)
    return score.transpose(i)


def process_image(image_path, transpose_semitones, working_dir='output'):
    os.makedirs(working_dir, exist_ok=True)
    musicxml_path = run_audiveris(image_path, working_dir)

    score = converter.parse(musicxml_path)
    score = transpose_score(score, transpose_semitones)
    timestamp = int(time.time())
    base_name = f'transposed_{timestamp}'
    # Пути к финальным файлам
    musicxml_out = os.path.join(working_dir, base_name + '.musicxml')
    midi_out = os.path.join(working_dir, base_name + '.mid')
    png_out = os.path.join(working_dir, base_name + '.png')

    # Сохраняем MusicXML и MIDI
    score.write('musicxml', fp=musicxml_out)
    score.write('midi', fp=midi_out)

    # Сохраняем PNG с помощью MuseScore
    try:
        score.write('musicxml.png', fp=png_out)
    except Exception as e:
        print(f"⚠️ Ошибка при сохранении PNG: {e}")
        png_out = None
    png_out = png_out[:-4] + "-1.png"
    print("GOOD_OUT:", png_out)
    return score, musicxml_out, midi_out, png_out
