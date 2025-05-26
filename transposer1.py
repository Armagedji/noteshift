import subprocess
import os
from music21 import converter, stream, note, environment
from music21 import note, chord


from pdf2image import convert_from_path

environment.set('musicxmlPath', r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe')
environment.set('musescoreDirectPNGPath', r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe')

from music21 import stream, note, chord


def normalize_voices(score):
    # Создаем один поток голоса
    voice = stream.Voice()

    # Добавляем все ноты и аккорды в этот голос
    for el in score.recurse():
        if isinstance(el, note.Note) or isinstance(el, chord.Chord):
            voice.append(el)

    # Удаляем все ноты и аккорды из исходного score
    for el in list(score.recurse().getElementsByClass(note.Note)) + list(
            score.recurse().getElementsByClass(chord.Chord)):
        el.activeSite.remove(el)

    # Добавляем голос в score
    score.append(voice)


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
    else:
        print("Ошибка при конвертации PDF в PNG")


def load_from_midi(file_path):
    """Загрузить ноты из MIDI-файла"""
    return converter.parse(file_path)

def load_from_musicxml(file_path):
    """Загрузить ноты из MusicXML"""
    return converter.parse(file_path)

def load_from_image_via_audiveris(image_path, audiveris_exe_path, output_folder="output_xml"):
    """Распознать ноты с изображения с помощью Audiveris.exe"""
    print("Запуск Audiveris (EXE)...")
    result = subprocess.run([
        audiveris_exe_path,
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
                return converter.parse(os.path.join(root, file))
    raise FileNotFoundError("MusicXML не найден после обработки изображения.")

def transpose_score(score, semitones):
    """Транспонирует всю партитуру"""
    return score.transpose(semitones)

def show_score(score):
    """Открывает партитуру"""
    normalize_voices(score)
    score.show()

def main():
    print("Выберите источник нот:")
    print("1 - MIDI")
    print("2 - MusicXML")
    print("3 - Изображение через Audiveris")
    choice = input("Ваш выбор (1/2/3): ")

    if choice == "1":
        path = input("Путь к MIDI-файлу: ")
        score = load_from_midi(path)

    elif choice == "2":
        path = input("Путь к MusicXML-файлу: ")
        score = load_from_musicxml(path)

    elif choice == "3":
        image_path = input("Путь к изображению с нотами (png/jpg): ")
        audiveris_path = input("Путь к audiveris.jar: ")
        score = load_from_image_via_audiveris(image_path, audiveris_path)

    else:
        print("Неверный выбор.")
        return

    # Проверка, есть ли темп в партитуре
    print("\n🎼 Проверка темпа в партитуре:")
    for el in score.recurse().getElementsByClass('MetronomeMark'):
        print(el)

    semitones = int(input("На сколько полутонов транспонировать (например -6): "))
    transposed = transpose_score(score, semitones)

    print("Открываю транспонированную партитуру...")
    show_score(transposed)

    save_option = input("Сохранить в PDF и PNG? (y/n): ").lower()
    if save_option == "y":
        out_name = input("Введите имя выходного файла (без расширения): ")
        save_as_pdf_and_png(transposed, out_name)




if __name__ == "__main__":
    main()