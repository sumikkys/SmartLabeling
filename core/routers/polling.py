# polling.py
from fastapi import APIRouter
import threading

router = APIRouter()
initialized = False
def initialize():
    global initialized
@router.get("/status")
def get_status():
    return {"initialized": initialized}

threading.Thread(target=initialize, daemon=True).start()