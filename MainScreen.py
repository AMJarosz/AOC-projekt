import os
from PIL import Image, ImageOps, ImageFilter

def handle_upload(file, upload_folder):
    if file and file.filename:
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)
        print(f"Image saved at {filepath}")

def handle_delete(upload_folder):
    for file_name in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file_name)
        if os.path.isfile(file_path):
            os.unlink(file_path)
            print(f"Deleted {file_path}")

def handle_transform(upload_folder, resources_folder):
    # Locate the uploaded image (assuming one upload at a time)
    uploaded_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    if not uploaded_files:
        print("No uploaded image found to transform.")
        return

    uploaded_file_path = os.path.join(upload_folder, uploaded_files[0])
    image = Image.open(uploaded_file_path)

    # Example transformation: Convert to grayscale
    transformed_image = ImageOps.grayscale(image)

    # Optional: Add an overlay from resources
    overlay_path = os.path.join(resources_folder, 'sticker.png')  # Example sticker
    if os.path.exists(overlay_path):
        sticker = Image.open(overlay_path).convert("RGBA")
        image_with_sticker = Image.alpha_composite(image.convert("RGBA"), sticker)
        transformed_image = image_with_sticker

    # Save the transformed image
    transformed_image.save(uploaded_file_path)
    print("Image transformed and saved.")