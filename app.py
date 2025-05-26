from flask import Flask, request, render_template, send_file, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename

# Импортируем отдельно модули
from transposes.png_transpose import process_png
from transposes.midi_transpose import process_midi
from transposes.musicxml_transpose import process_musicxml

app = Flask(__name__)
app.secret_key = 'supersecretkey'

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'mid', 'midi', 'musicxml', 'xml', 'mxl'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/output/<path:filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        flash('Нет файла в запросе')
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        flash('Файл не выбран')
        return redirect(url_for('index'))
    if not allowed_file(file.filename):
        flash('Неподдерживаемый формат файла')
        return redirect(url_for('index'))

    transpose_semitones = request.form.get('transpose', type=int, default=0)

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    ext = filename.rsplit('.', 1)[1].lower()

    try:
        if ext in {'png', 'jpg', 'jpeg', 'bmp'}:
            score, musicxml_path, midi_path, png_path = process_png(filepath, transpose_semitones, app.config['OUTPUT_FOLDER'])
        elif ext in {'mid', 'midi'}:
            score, musicxml_path, midi_path, png_path = process_midi(filepath, transpose_semitones, app.config['OUTPUT_FOLDER'])
        elif ext in {'musicxml', 'xml', 'mxl'}:
            score, musicxml_path, midi_path, png_path = process_musicxml(filepath, transpose_semitones, app.config['OUTPUT_FOLDER'])
        else:
            flash('Неподдерживаемый формат файла')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Ошибка обработки: {e}')
        return redirect(url_for('index'))

    return render_template('result.html',
                           musicxml_file=os.path.basename(musicxml_path),
                           midi_file=os.path.basename(midi_path),
                           png_file=os.path.basename(png_path[:-4]+"-1.png") if png_path else None)


@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
