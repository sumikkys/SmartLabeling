# websocket_manager.py
from fastapi import WebSocket
from typing import List
import logging

class ConnectionManager:
    """WebSocket 连接管理器"""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """建立新的WebSocket连接"""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """断开WebSocket连接"""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """广播消息给所有活跃连接"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logging.error(f"Broadcasting error: {e}")
                await self.disconnect(connection)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """发送消息给指定连接"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logging.error(f"Personal message error: {e}")
            await self.disconnect(websocket)