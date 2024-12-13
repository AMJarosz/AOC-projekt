from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from MainScreen import handle_upload, handle_delete, handle_transform
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def main_screen():
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
            handle_transform(app.config['UPLOAD_FOLDER'], 'resources')
    
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
