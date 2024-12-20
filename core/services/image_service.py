from fastapi import HTTPException
from schemas.image_schema import*

def allowed_file(filename: str) -> bool:
    """����ļ���ʽ�Ƿ�֧��"""
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

async def save_uploaded_file(file, filename: str):
    """�����ϴ����ļ���ָ��Ŀ¼"""
    try:
        file_location = UPLOAD_DIR / filename
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
        return file_location
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")