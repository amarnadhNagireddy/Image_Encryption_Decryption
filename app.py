from flask import Flask, request, render_template, send_file, redirect, url_for
from manipulate import manipulate_image
import io
import base64
app = Flask(__name__)

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
        # Read the uploaded image into memory
        image_data = file.read()
        
        # Pass the image data for manipulation (encryption)
        encrypted_image_io = manipulate_image(io.BytesIO(image_data))

        # Convert the input and output images to Base64 for rendering
        input_image_base64 = base64.b64encode(image_data).decode('utf-8')
        output_image_base64 = base64.b64encode(encrypted_image_io.getvalue()).decode('utf-8')

        # Render the preview page with in-memory images
        return render_template(
    'image_display.html',
    input_image=f"data:image/png;base64,{input_image_base64}",
    output_image=f"data:image/png;base64,{output_image_base64}",
    operation='encrypt'  # or 'decrypt' based on the route
)


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
        # Read the uploaded image into memory
        image_data = file.read()

        # Pass the image data for manipulation (decryption)
        decrypted_image_io = manipulate_image(io.BytesIO(image_data))

        # Convert the input and output images to Base64 for rendering
        input_image_base64 = base64.b64encode(image_data).decode('utf-8')
        output_image_base64 = base64.b64encode(decrypted_image_io.getvalue()).decode('utf-8')

        # Render the preview page with in-memory images
        return render_template(
    'image_display.html',
    input_image=f"data:image/png;base64,{input_image_base64}",
    output_image=f"data:image/png;base64,{output_image_base64}",
    operation='decrypt'  # or 'decrypt' based on the route
)


    except Exception as e:
        return f"Error during decryption: {str(e)}", 500

@app.route('/download_image/<operation>', methods=['POST'])
def download_image(operation):
    try:
        if operation == 'encrypt':
            file = request.files['image']
            encrypted_image_io = manipulate_image(io.BytesIO(file.read()))
            return send_file(encrypted_image_io, as_attachment=True, download_name='encrypted_image.png')

        elif operation == 'decrypt':
            file = request.files['image']
            decrypted_image_io = manipulate_image(io.BytesIO(file.read()))
            return send_file(decrypted_image_io, as_attachment=True, download_name='decrypted_image.png')
    except Exception as e:
        return f"Error during download: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
