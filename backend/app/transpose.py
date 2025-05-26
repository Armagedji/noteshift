import subprocess
import os
from music21 import converter, stream, note, environment
from music21 import note, chord


from pdf2image import convert_from_path

environment.set('musicxmlPath', r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe')
environment.set('musescoreDirectPNGPath', r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe')

from music21 import stream, note, chord



def save_as_pdf_and_png(score, filename_base):
    """Сохраняет партитуру в PDF и PNG"""
    pdf_path = f"{filename_base}.pdf"
    png_path = f"{filename_base}.png"

    print(f"Сохраняю как PDF: {pdf_path}")
    score.write('musicxml.pdf', fp=pdf_path)

    print(f"Конвертирую PDF в PNG: {png_path}")
    images = convert_from_path(pdf_path)
    if images:
        images[0].save(png_path, 'PNG')
        print(f"PNG сохранён: {png_path}")
        return png_path, pdf_path
    else:
        print("Ошибка при конвертации PDF в PNG")

def load_from_image_via_audiveris(image_path, output_folder="output_xml"):
    """Распознать ноты с изображения с помощью Audiveris.exe и вернуть объект score."""
    print("Запуск Audiveris (EXE)...")
    result = subprocess.run([
    r"M:\Programs\Audiveris\Audiveris.exe",
    "-batch", "-export",
    "-output", output_folder,
    image_path
], capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode != 0:
        raise RuntimeError("Ошибка при запуске Audiveris.exe")

    for root, _, files in os.walk(output_folder):
        for file in files:
            if file.endswith(".xml") or file.endswith(".mxl"):
                xml_path = os.path.join(root, file)
                return converter.parse(xml_path)

    raise FileNotFoundError("MusicXML не найден после обработки изображения.")

def process_png_file(image_path, uid, semitones, results_folder='results'):
    """
    Обрабатывает изображение нот: распознаёт, транспонирует, сохраняет PDF и PNG.
    Возвращает пути к результатам.
    """
    score = load_from_image_via_audiveris(image_path)
    transposed = score.transpose(semitones)

    filename_base = os.path.join(results_folder, uid)
    png_path, pdf_path = save_as_pdf_and_png(transposed, filename_base)

    return png_path, pdf_path

def transpose_file(filepath, uid, semitones, results_folder='results'):
    """
    Транспонирует MIDI или MusicXML, сохраняет PDF и PNG.
    Для PNG используется отдельная логика.
    Возвращает пути к файлам (png_path, pdf_path).
    """
    ext = os.path.splitext(filepath)[1].lower()
    filename_base = os.path.join(results_folder, uid)
    print("Hello!")
    if ext in ['.mid', '.midi', '.xml', '.musicxml']:
        print("Hello1")
        score = converter.parse(filepath)
        print("KOBENI12")
        transposed = score.transpose(semitones)
        print("KOBENI1")
        png_path, pdf_path = save_as_pdf_and_png(transposed, filename_base)
        print("KOBENI", png_path, pdf_path)
        return png_path, pdf_path

    elif ext in ['.png', '.jpg', '.jpeg']:
        print("Hello2")
        score = load_from_image_via_audiveris(filepath)
        print("hello3")
        return process_png_file(filepath, uid, semitones, results_folder)

    else:
        raise ValueError(f"Неподдерживаемый формат файла: {ext}")



if __name__ == "__main__":
    main()