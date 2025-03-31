# image_service.py
import os
from fastapi import HTTPException
from PIL import Image
from cache.image_cache import *

# allowed file extensions
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'bmp'}

def allowed_file(file_path: str) -> bool:
    """Check if the file extension is allowed"""
    return any(file_path.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def save_image_from_path(image_path: str, save_dir: str) -> str:
    """Save image from path to the server"""
    
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    if not allowed_file(image_path):
        raise HTTPException(status_code=415, detail="Unsupported media type. Only JPEG, JPG, PNG, and BMP files are allowed.")
    
    # Generate the target file location
    file_name = os.path.basename(image_path)
    target_path = os.path.join(save_dir, file_name)
    
    try:
        image = Image.open(image_path)
        # RGBA to RGB
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(target_path)  # Save the image to the target path
        return target_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving the image: {str(e)}")

def switch_image(image_id: str) -> str:
    """切换图片"""
    try:
        set_current_id(image_id)
        image_path = find_key_by_value(image_id_cache, image_id)
        if image_path is None:
            raise ValueError(f"Image ID {image_id} not found in cache.")
        image_name = os.path.basename(image_path)
        image_data = {}
        if image_id not in image_data_cache.keys():
            raise ValueError(f"Image ID {image_id} not found in image_data_cache.")
        if "masks" not in image_data_cache[image_id]:
            raise ValueError(f"Image ID {image_id} does not have 'masks' in cache.")
        for class_id in image_data_cache[image_id]["masks"].keys():
            image_data[class_id] = []
            for mask_id in image_data_cache[image_id]["masks"][class_id].keys():
                image_data[class_id].append(mask_id)
        return image_name, image_data
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")