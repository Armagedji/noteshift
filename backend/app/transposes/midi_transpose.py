import os
from music21 import converter, environment
from pdf2image import convert_from_path

# Указать путь к MuseScore
environment.set('musicxmlPath', r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe')
environment.set('musescoreDirectPNGPath', r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe')


def save_as_pdf_and_png(score, filename_base):
    """Сохраняет партитуру в PDF и PNG"""
    pdf_path = f"{filename_base}.pdf"
    png_path = f"{filename_base}.png"

    # Сохранить как PDF с помощью MuseScore
    score.write('musicxml.pdf', fp=pdf_path)

    # Конвертация первой страницы PDF → PNG
    images = convert_from_path(pdf_path)
    if images:
        images[0].save(png_path, 'PNG')
    else:
        print("Ошибка при конвертации PDF в PNG")

    return png_path, pdf_path


def transpose_midi_file(filepath, uid, results_folder='results'):
    """Транспонирует MIDI, сохраняет PDF и PNG, возвращает пути"""
    score = converter.parse(filepath)

    semitones = -2  # можно заменить на пользовательское значение
    transposed = score.transpose(semitones)

    filename_base = os.path.join(results_folder, uid)
    png_path, pdf_path = save_as_pdf_and_png(transposed, filename_base)

    return png_path, pdf_path
