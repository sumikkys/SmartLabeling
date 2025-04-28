import { initialized } from './Telegram';

export const checkBackendReady_WebSocket = () => {
  // 使用 WebSocket 监听后端状态
  if ((window as any).electron && (window as any).electron.onWebSocketMessage) {
    (window as any).electron.onWebSocketMessage((message: string) => {
      try {
        const data = JSON.parse(message);
        if (data.SAM && data.CLIP) {
          console.log('后端初始化完成！');
          initialized.value = true;
        } else {
          console.log('后端未完全初始化:', data);
        }
      } catch (error) {
        console.error('解析 WebSocket 消息失败:', error);
      }
    });
  } else {
    console.error('WebSocket 功能未正确暴露到渲染进程');
  }
};