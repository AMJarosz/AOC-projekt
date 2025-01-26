from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from MainScreen import handle_upload, handle_delete, handle_transform, handle_face_sticker, handle_sad_face_sticker
import os
from deepface import DeepFace
import cv2

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/stickers/<filename>')
def serve_sticker(filename):
    return send_from_directory('stickers', filename)

@app.route('/', methods=['GET', 'POST'])
def main_screen():
    uploaded_image_name = None
    uploaded_image_path = None
    message = None
    processed_image_name = None
    emotion = None

    # Default sticker folder if no image is uploaded
    sticker_folder = 'stickers'  # Default to general stickers

    if request.method == 'POST':
        if 'image' in request.files:
            # Handle image upload
            file = request.files['image']
            handle_upload(file, app.config['UPLOAD_FOLDER'])

            uploaded_image_name = file.filename
            uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image_name)

            # Perform emotion recognition
            image = cv2.imread(uploaded_image_path)
            if image is not None:
                try:
                    result = DeepFace.analyze(image, actions=['emotion'])

                    # Handle result being a list of dictionaries
                    if isinstance(result, list):
                        result = result[0]  # Take the first face's result

                    emotion = result.get('dominant_emotion', None)

                    # Handle Emotion Logic
                    if emotion:
                        message = f"Detected emotion: {emotion.capitalize()}"
                    else:
                        message = "No emotion detected."
                    
                    # Set sticker folder based on the emotion detected
                    if emotion == "sad":
                        sticker_folder = 'sad_stickers'  # Update sticker folder for sad emotions

                except Exception as e:
                    message = f"Error occurred: Please upload a clear photo showing a face."

            else:
                message = "No face detected in the uploaded image."

        elif 'delete' in request.form:
            # Handle image deletion
            handle_delete(app.config['UPLOAD_FOLDER'])

        elif 'transform' in request.form:
            # Handle image transformation
            handle_transform(app.config['UPLOAD_FOLDER'], 'stickers')


        elif 'selected-sticker' in request.form:
            # Get the selected sticker name
            selected_sticker = request.form.get('sticker-name')

            # Handle emotion-specific stickers
            if emotion == "sad" and selected_sticker:
                sticker_folder = 'sad_stickers'
                processed_image_name, message = handle_sad_face_sticker(
                    app.config['UPLOAD_FOLDER'], sticker_folder, selected_sticker
                )
            else:
                processed_image_name, message = handle_face_sticker(
                    app.config['UPLOAD_FOLDER'], sticker_folder, selected_sticker
                )

    # Get the uploaded image name (assume the last uploaded image)
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    if uploaded_files:
        uploaded_image_name = uploaded_files[0]  # First uploaded file
        uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_image_name)

    # List stickers available in the selected folder
    sticker_files = [
        sticker for sticker in os.listdir(sticker_folder)
        if sticker.lower().endswith(('png', 'jpg', 'jpeg'))
    ]

    return render_template(
        'main.html',
        image_name=uploaded_image_name,
        image_path=uploaded_image_path,
        message=message,
        emotion=emotion,
        processed_image_name=processed_image_name,
        stickers=sticker_files,  # Pass sticker files to the template
        sticker_folder=sticker_folder
    )

if __name__ == '__main__':
    app.run(debug=True)
