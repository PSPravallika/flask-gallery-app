from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # change this to something unique

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Secure login credentials
USERNAME = 'pravallika'  # your private username
PASSWORD_HASH = 'scrypt:32768:8:1$dbF15Ti4slUapnxF$5bfcaf9cccde79ffb546341d9544414be864c36b40dfc040a3e7175a08f068577e47dd5bc74707ef582a99936df0d63c09b298fa31040a57c54233d2193dc220'

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('gallery'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
        session['user'] = username
        return redirect(url_for('gallery'))
    else:
        return "<h3>Invalid credentials! Try again.</h3>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('home'))

    if 'file[]' not in request.files:
        return "No file part"

    files = request.files.getlist('file[]')
    for file in files:
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('gallery'))

@app.route('/gallery')
def gallery():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    username = session.get('user', 'User')  # fetch logged-in user
    image_list = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', images=image_list, username=username)


@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    if 'user' not in session:
        return redirect(url_for('home'))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('gallery'))

if __name__ == '__main__':
    app.run(debug=True)
