import os
from PIL import Image, ImageOps, ImageFilter
import face_recognition
import numpy as np


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
    uploaded_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    if not uploaded_files:
        print("No uploaded image found to transform.")
        return None

    uploaded_file_path = os.path.join(upload_folder, uploaded_files[0])
    image = Image.open(uploaded_file_path)

    # Grayscale transformation
    transformed_image = ImageOps.grayscale(image)

    # Save transformed image with a new name
    base, ext = os.path.splitext(uploaded_files[0])
    transformed_name = f"{base}_transformed{ext}"
    transformed_image_path = os.path.join(upload_folder, transformed_name)
    transformed_image.save(transformed_image_path)

    print(f"Image transformed and saved as {transformed_image_path}")
    return transformed_name


def handle_face_sticker(upload_folder, stickers_folder):
    uploaded_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    if not uploaded_files:
        return None, "No uploaded image found."

    uploaded_file_path = os.path.join(upload_folder, uploaded_files[0])
    image = face_recognition.load_image_file(uploaded_file_path)
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        return None, "No face detected in the uploaded image."

    # Load the image and convert it for processing
    pil_image = Image.open(uploaded_file_path).convert("RGBA")

    # Load the sticker
    sticker_path = os.path.join(stickers_folder, 'sticker.png')
    if not os.path.exists(sticker_path):
        return None, "Sticker resource file not found."

    sticker = Image.open(sticker_path).convert("RGBA")

    # Process each detected face
    for face_location in face_locations:
        top, right, bottom, left = face_location

        # Determine where to place the sticker
        face_center_x = (left + right) // 2
        sticker_width, sticker_height = sticker.size
        sticker_x = face_center_x - (sticker_width // 2)
        sticker_y = top - sticker_height - 5  # 5 pixels above the face

        # Create a new layer for the sticker
        overlay = Image.new('RGBA', pil_image.size, (255, 255, 255, 0))
        overlay.paste(sticker, (sticker_x, sticker_y), sticker)

        # Combine the sticker with the original image
        pil_image = Image.alpha_composite(pil_image, overlay)

    # Convert the final image to RGB mode (to remove alpha transparency)
    pil_image_rgb = pil_image.convert("RGB")

    # Save the processed image
    base, ext = os.path.splitext(uploaded_files[0])
    processed_name = f"{base}_with_sticker.jpg"  # Save as JPEG
    processed_path = os.path.join(upload_folder, processed_name)
    pil_image_rgb.save(processed_path, "JPEG")

    return processed_name, "Face detected, sticker applied, and image saved."
