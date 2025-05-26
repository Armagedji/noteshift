import os
import time
from music21 import converter, interval

def transpose_score(score, semitones):
    if semitones == 0:
        return score
    i = interval.Interval(semitones)
    return score.transpose(i)

def process_midi(midi_path, semitones, working_dir):
    os.makedirs(working_dir, exist_ok=True)
    score = converter.parse(midi_path)
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
