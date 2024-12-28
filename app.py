from flask import Flask, request, render_template, send_file, redirect, url_for, send_from_directory
from image_encryption_decryption.manipulate import manipulate_image

import os

app = Flask(__name__)

# Folder to store uploaded and processed files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']
    
    if file.filename == '':
        return "No file selected", 400

    try:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        encrypted_image_io = manipulate_image(image_path)
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], f'encrypted_{file.filename}')

        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_image_io.getvalue())

        # Redirect to the page that displays images
        return render_template('image_display.html', input_image=file.filename, output_image=f'encrypted_{file.filename}')

    except Exception as e:
        return f"Error during encryption: {str(e)}", 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']

    if file.filename == '':
        return "No file selected", 400

    try:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(image_path)

        decrypted_image_io = manipulate_image(image_path)
        decrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], f'decrypted_{file.filename}')

        with open(decrypted_path, 'wb') as f:
            f.write(decrypted_image_io.getvalue())

        # Redirect to the page that displays images
        return render_template('image_display.html', input_image=file.filename, output_image=f'decrypted_{file.filename}')

    except Exception as e:
        return f"Error during decryption: {str(e)}", 500



@app.route('/show_images')
def show_images():
    input_image = request.args.get('input_image')
    output_image = request.args.get('output_image')
    
    return render_template('image_display.html', input_image=file.filename, output_image=f'encrypted_{file.filename}')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/download_image/<filename>')
def download_image(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
