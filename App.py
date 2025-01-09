from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from MainScreen import handle_upload, handle_delete, handle_transform, handle_face_sticker
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def main_screen():
    uploaded_image_name = None
    uploaded_image_path = None
    message = None
    processed_image_name = None

    if request.method == 'POST':
        if 'image' in request.files:
            # Handle image upload
            file = request.files['image']
            handle_upload(file, app.config['UPLOAD_FOLDER'])

        elif 'delete' in request.form:
            # Handle image deletion
            handle_delete(app.config['UPLOAD_FOLDER'])

        elif 'transform' in request.form:
            # Handle image transformation
            handle_transform(app.config['UPLOAD_FOLDER'], 'stickers')

        elif 'face-sticker' in request.form:
            # Handle face detection and sticker placement
            processed_image_name, message = handle_face_sticker(
                app.config['UPLOAD_FOLDER'], 'stickers'
            )

    # Get the uploaded image name (assume the last uploaded image)
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    if uploaded_files:
        uploaded_image_name = uploaded_files[0]  # First uploaded file
        uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image_name)

    return render_template(
        'main.html',
        image_name=uploaded_image_name,
        image_path=uploaded_image_path,
        message=message,
        processed_image_name=processed_image_name,
    )

if __name__ == '__main__':
    app.run(debug=True)
