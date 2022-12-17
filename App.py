from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import signature

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = ['.png', '.jpg', 'jpeg']

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    data = ''
    file1 = request.files['image1']
    file2 = request.files['image2']

    filename1 = secure_filename(file1.filename)
    filename2 = secure_filename(file2.filename)

    extension1 = os.path.splitext(filename1)[1].lower()
    extension2 = os.path.splitext(filename2)[1].lower()

    filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
    filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

    if extension1 in app.config['ALLOWED_EXTENSIONS'] and extension2 in app.config['ALLOWED_EXTENSIONS']:
        file1.save(filepath1)
        file2.save(filepath2)

        print('path1 = ', filepath1)
        print('path2 = ', filepath2)

        result = signature.match(filepath1, filepath2)

        data = f'They are {result}% same'

    else:
        data = 'uploaded file is not an image'
    return render_template('result.html', data = data, fp1 = filename1, fp2 = filename2)

@app.route('/display-image/<filename>', methods=['GET'])
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__' : 
    app.run(debug=True)