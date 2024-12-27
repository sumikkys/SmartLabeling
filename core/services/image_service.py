import os
from fastapi import HTTPException
from PIL import Image

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
        # 如果图像是 RGBA 模式，则转换为 RGB 模式
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(target_path)  # Save the image to the target path
        return target_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving the image: {str(e)}")
