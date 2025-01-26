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
    # Locate the uploaded image
    uploaded_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    if not uploaded_files:
        return None, "No uploaded image found."

    uploaded_file_path = os.path.join(upload_folder, uploaded_files[0])
    
    # Open the image
    image = Image.open(uploaded_file_path)

    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(image)

    # Save the grayscale image
    base, ext = os.path.splitext(uploaded_files[0])
    transformed_name = f"{base}_gray{ext}"
    transformed_image_path = os.path.join(upload_folder, transformed_name)
    gray_image.save(transformed_image_path)

    return transformed_name, "Image converted to grayscale and saved."


def handle_face_sticker(upload_folder, stickers_folder, selected_sticker):
    uploaded_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    if not uploaded_files:
        return None, "No uploaded image found."

    uploaded_file_path = os.path.join(upload_folder, uploaded_files[0])
    image = face_recognition.load_image_file(uploaded_file_path)
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        return None, "No face detected in the uploaded image."

    pil_image = Image.open(uploaded_file_path).convert("RGBA")

    # Load the selected sticker
    sticker_path = os.path.join(stickers_folder, selected_sticker)
    if not os.path.exists(sticker_path):
        print(sticker_path)
        return None, "Selected sticker file not found123. "

    sticker = Image.open(sticker_path).convert("RGBA")

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_width = right - left
        aspect_ratio = sticker.height / sticker.width
        new_width = face_width
        new_height = int(new_width * aspect_ratio)
        resized_sticker = sticker.resize((new_width, new_height), Image.Resampling.LANCZOS)

        face_center_x = (left + right) // 2
        sticker_x = face_center_x - (new_width // 2)
        sticker_y = top - new_height - 5

        overlay = Image.new('RGBA', pil_image.size, (255, 255, 255, 0))
        overlay.paste(resized_sticker, (sticker_x, sticker_y), resized_sticker)

        pil_image = Image.alpha_composite(pil_image, overlay)

    pil_image_rgb = pil_image.convert("RGB")
    base, ext = os.path.splitext(uploaded_files[0])
    processed_name = f"{base}_with_sticker.jpg"
    processed_path = os.path.join(upload_folder, processed_name)
    pil_image_rgb.save(processed_path, "JPEG")

    return processed_name, "Now you can download your photo!"

def handle_sad_face_sticker(upload_folder, sad_stickers_folder, selected_sticker):
    uploaded_files = [f for f in os.listdir(upload_folder) if os.path.isfile(os.path.join(upload_folder, f))]
    if not uploaded_files:
        return None, "No uploaded image found."

    uploaded_file_path = os.path.join(upload_folder, uploaded_files[0])
    image = face_recognition.load_image_file(uploaded_file_path)
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        return None, "No face detected in the uploaded image."

    pil_image = Image.open(uploaded_file_path).convert("RGBA")

    # Load the selected sticker
    sticker_path = os.path.join(sad_stickers_folder, selected_sticker)
    if not os.path.exists(sticker_path):
        print(sad_stickers_folder)
        return None, "Selected sticker file not found."

    sticker = Image.open(sticker_path).convert("RGBA")

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_width = right - left
        aspect_ratio = sticker.height / sticker.width
        new_width = face_width
        new_height = int(new_width * aspect_ratio)
        resized_sticker = sticker.resize((new_width, new_height), Image.Resampling.LANCZOS)

        face_center_x = (left + right) // 2
        sticker_x = face_center_x - (new_width // 2)
        sticker_y = top - new_height - 5

        overlay = Image.new('RGBA', pil_image.size, (255, 255, 255, 0))
        overlay.paste(resized_sticker, (sticker_x, sticker_y), resized_sticker)

        pil_image = Image.alpha_composite(pil_image, overlay)

    pil_image_rgb = pil_image.convert("RGB")
    base, ext = os.path.splitext(uploaded_files[0])
    processed_name = f"{base}_with_sticker.jpg"
    processed_path = os.path.join(upload_folder, processed_name)
    pil_image_rgb.save(processed_path, "JPEG")

    return processed_name, "Now you can download your photo!"

