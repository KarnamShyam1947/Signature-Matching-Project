from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import signature
import Database
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = ['.png', '.jpg', '.jpeg']

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index1.html')

@app.route('/result', methods = ['GET', 'POST'])
def result():
    data = ''

    username = request.form['username']
    file = request.files['image']

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    extension = os.path.splitext(filename)[1].lower()

    uploaded_img_path = 'uploaded_img.png'

    if extension in app.config['ALLOWED_EXTENSIONS'] :
        file.save(filepath)

        flag = Database.read_image(username, uploaded_img_path)

        if flag:
            result = signature.match(filepath, uploaded_img_path)
            data = fuzzy_logic(result)

        else :
            data = 'The user with username {} doesn\'t found in database'.format(username)

    else :
        data = 'Please select a image file'
        
    return render_template('result1.html', data = data, fn1 = filename)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST' :
        data = ''

        username = request.form['username']
        file = request.files['image']

        filename = secure_filename(file.filename) 
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        extension = os.path.splitext(filename)[1].lower()

        if extension in app.config['ALLOWED_EXTENSIONS'] :
            file.save(filepath)

            flag = Database.insert_image(username, filepath)

            if flag:
                data = 'Signature add successfully'

            else :
                data = 'Already user present in data base'

        else :
            data = 'please select an image file'

        return render_template('register.html', data = data)

    return render_template('register.html')

@app.route('/display-image/<filename>')
def display_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def fuzzy_logic(result):
    if result <= 50:
        return "The signature is not same.\n{}% is matching".format(result)

    elif result > 50 and result < 80:
        return "The signature is almost same.\n{}% is matching".format(result)

    else:
        return "The signature is same.\n{}% is matching".format(result)

if __name__ == '__main__' : 
    app.run(debug=True)