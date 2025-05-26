import os
import subprocess
import time
from music21 import converter, interval, environment

AUDIVERIS_PATH = r'M:\Programs\Audiveris\Audiveris.exe'  # путь к Audiveris

us = environment.UserSettings()
us['musescoreDirectPNGPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'  # путь к MuseScore

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
    subprocess.run(cmd, check=True)

    # Ищем MusicXML в output_dir
    possible_exts = ['.musicxml', '.xml', '.mxl']
    for ext in possible_exts:
        path = os.path.join(output_dir, base_name + ext)
        if os.path.exists(path):
            return path

    raise FileNotFoundError(f"MusicXML файл не найден в {output_dir} после Audiveris.")

def transpose_score(score, semitones):
    if semitones == 0:
        return score
    i = interval.Interval(semitones)
    return score.transpose(i)

def process_png(image_path, semitones, working_dir):
    os.makedirs(working_dir, exist_ok=True)
    musicxml_path = run_audiveris(image_path, working_dir)

    score = converter.parse(musicxml_path)
    score = transpose_score(score, semitones)

    timestamp = int(time.time())
    base_name = f'transposed_{timestamp}'

    musicxml_out = os.path.join(working_dir, base_name + '.musicxml')
    midi_out = os.path.join(working_dir, base_name + '.mid')
    png_out = os.path.join(working_dir, base_name + '.png')

    score.write('musicxml', fp=musicxml_out)
    score.write('midi', fp=midi_out)

    try:
        score.write('musicxml.png', fp=png_out)
    except Exception as e:
        print(f"Ошибка создания PNG: {e}")
        png_out = None

    return score, musicxml_out, midi_out, png_out
