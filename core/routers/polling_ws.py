from fastapi import APIRouter, WebSocket
import logging
from websocket_manager import ConnectionManager
from cache.initialize_cache import initialize_manager
router = APIRouter()
manager = ConnectionManager()

async def update_status():
    """广播当前初始化状态"""
    await manager.broadcast({
        "SAM": initialize_manager.get_SAM_initialized(),
        "CLIP": initialize_manager.get_CLIP_initialized()
    })

@router.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点用于监听初始化状态"""
    await manager.connect(websocket)
    try:
        # 连接建立后立即发送当前状态
        await manager.send_personal_message({
            "SAM": initialize_manager.get_SAM_initialized(),
            "CLIP": initialize_manager.get_CLIP_initialized()
        }, websocket)
        
        while True:
            await websocket.receive_text()
            # 每次收到消息都返回最新状态
            await manager.send_personal_message({
                "SAM": initialize_manager.get_SAM_initialized(),
                "CLIP": initialize_manager.get_CLIP_initialized()
            }, websocket)
            
    except Exception as e:
        logging.error(f"WebSocket错误: {e}")
    finally:
        manager.disconnect(websocket)