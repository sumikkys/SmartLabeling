// 使用OffscreenCanvas进行离屏渲染
const ctx = self as unknown as Worker;

ctx.addEventListener('message', async (e) => {
  const { 
    maskData, 
    rows,
    cols,
    color, 
    zoomX, 
    zoomY, 
    posX, 
    posY, 
    canvasWidth, 
    canvasHeight 
  } = e.data;
  
  // 重建二维数组结构
  const mask = [];
  for (let y = 0; y < rows; y++) {
    mask.push(Array.from(maskData.slice(y * cols, (y + 1) * cols)));
  }
  
  const offscreen = new OffscreenCanvas(canvasWidth, canvasHeight);
  const context = offscreen.getContext('2d')!;

  // 创建图像数据
  const imageData = context.createImageData(offscreen.width, offscreen.height);
  const rgba = hexToRGBA(color);
  
  // 遍历mask矩阵
  for (let y = 0; y < mask.length; y++) {
    for (let x = 0; x < mask[y].length; x++) {
      if (mask[y][x] === 1) {
        const canvasX = Math.round(x * zoomX + posX);
        const canvasY = Math.round(y * zoomY + posY);
        
        // 在图像数据中设置像素
        if (canvasX >= 0 && canvasX < canvasWidth && canvasY >= 0 && canvasY < canvasHeight) {
          const index = (canvasY * canvasWidth + canvasX) * 4;
          imageData.data[index] = rgba.r;     // R
          imageData.data[index + 1] = rgba.g; // G
          imageData.data[index + 2] = rgba.b; // B
          imageData.data[index + 3] = rgba.a;    // Alpha (0.1*255)
        }
      }
    }
  }

  context.putImageData(imageData, 0, 0);
  const bitmap = await createImageBitmap(offscreen);
  ctx.postMessage(bitmap);
});

// 十六进制颜色转RGBA
function hexToRGBA(hex: string) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return { r, g, b, a: 75 };
}

export default {} as typeof Worker & { new (): Worker };