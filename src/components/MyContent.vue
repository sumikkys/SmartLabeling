<script setup lang="ts">
  import { ref, watch, onMounted } from 'vue'
  import { selection } from '../js/selection'
  import { Dots, isDotMasked } from '../js/Dots'
  import { Boxes } from '../js/Boxes'
  import { path } from '../js/path'
  import axios from 'axios'
  import type { AxiosError } from 'axios'

  let url = ref('https://segment-anything.com/assets/gallery/AdobeStock_94274587_welsh_corgi_pembroke_CD.jpg')

  let pos = ref({
    x: 0,
    y: 0
  })

  let send_pos = ref({
    x: 0,
    y: 0    
  })

  let box_flag = false

  let box = ref({
      start_x: 0,
      start_y: 0,
      end_x: 0,
      end_y: 0
  })

  let send_box = ref({
      start_x: 0,
      start_y: 0,
      end_x: 0,
      end_y: 0
  })

  let zoom_x = 0
  let zoom_y = 0
  let pos_x = 0
  let pos_y = 0

  const myCanvas = ref()
  // Axios 实例配置
  const api = axios.create({
    headers: {
      'Content-Type': 'application/json'
    }
  })

  // 定义 error 变量
const error = ref<string | null>(null)

  // 定义增强型错误类型
type EnhancedError = 
  | AxiosError<{ message?: string }>  // 包含响应数据的Axios错误
  | Error                              // 标准错误对象
  | string                             // 字符串类型的错误消息

// 统一错误处理函数
const handleError = (err: EnhancedError) => {
  // 处理字符串类型错误
  if (typeof err === 'string') {
    error.value = err
    console.error('API Error:', err)
    return
  }

  // 处理Error对象
  if (err instanceof Error) {
    // 类型断言为AxiosError
    const axiosError = err as AxiosError<{ message?: string }>
    
    // 处理带响应的错误
    if (axiosError.response) {
      // 状态码映射
      const statusMessage = (() => {
        switch (axiosError.response.status) {
          case 400: return '请求参数错误'
          case 404: return '资源不存在'
          case 415: return '不支持的媒体类型'
          case 500: return '服务器内部错误'
          default: return `请求失败 (${axiosError.response.status})`
        }
      })()

      error.value = axiosError.response.data?.message || statusMessage
      console.error('API Error:', {
        status: axiosError.response.status,
        message: axiosError.message,
        url: axiosError.config?.url,
        data: axiosError.response.data
      })
    } 
    // 处理无响应的网络错误
    else if (axiosError.request) {
      error.value = '网络连接异常，请检查网络'
      console.error('Network Error:', axiosError.message)
    }
    // 处理其他Error类型
    else {
      error.value = err.message
      console.error('Runtime Error:', err)
    }
  }
}  

  onMounted(() => {
    draw_Image(url.value) // 初始绘制图片
    checkBackendReady();
  })

  function checkBackendReady() {
    const interval = setInterval(async() => {
        try {
          const response = await api.get('/api/status') 
          if(response.data.initialized){
            clearInterval(interval);
            console.log("后端初始化完成！");
            // 这里可以执行后续逻辑
        }
      }catch (err: unknown) {
        // 类型安全的错误转换
      if (err instanceof Error) {
        handleError(err)
      } else {
        handleError(String(err))
      }
    }
    }, 1000);  // 每秒检查一次
}



  function draw_Image(imageSrc: string) {
    // 确保图片清晰度，并初始化 canvas
    const canvas = myCanvas.value
    canvas.width = canvas.clientWidth * window.devicePixelRatio
    canvas.height = canvas.clientHeight * window.devicePixelRatio
    const ctx = canvas.getContext('2d')
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio)

    let img = document.getElementById("bg") as HTMLImageElement;
    img.src = imageSrc

    img.onload = function() {
      pos_x = (canvas.offsetWidth-img.width)/2
      pos_y = (canvas.offsetHeight-img.height)/2
      zoom_x = img.width / img.naturalWidth
      zoom_y = img.height / img.naturalHeight
      ctx.beginPath()
    }

    canvas.addEventListener('mousedown', function(e: MouseEvent) {
      if (selection.value === 1) {
        if (e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) {
          return
        }
        pos.value = {
            x: e.offsetX,
            y: e.offsetY
        }
        send_pos.value = {
            x: (pos.value.x - pos_x) / zoom_x,
            y: (pos.value.y - pos_y) / zoom_y
        }
        drawPoint(e)
        sendPointData()
        if (!Dots.isDotted.value) {
            Dots.isDotted.value = true
        }
      }
      else if (selection.value === 2) {
        if (e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) {
          return
        }
        box_flag = true;
        box.value.start_x = e.offsetX
        box.value.start_y = e.offsetY
      }
    })

    canvas.addEventListener('mouseup', function(e: MouseEvent) {
      if (selection.value === 2) {
        if (e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) {
          return
        }
        box_flag = false
        box.value.end_x = e.offsetX
        box.value.end_y = e.offsetY
        send_box.value.start_x = (box.value.start_x - pos_x) / zoom_x
        send_box.value.start_y = (box.value.start_y - pos_y) / zoom_y
        send_box.value.end_x = (box.value.end_x - pos_x) / zoom_x
        send_box.value.end_y = (box.value.end_y - pos_y) / zoom_y
        Boxes.setBox(box.value.start_x, box.value.start_y, box.value.end_x, box.value.end_y)
        sendBoxData()
      }
    })

    canvas.addEventListener('mousemove', function(e: MouseEvent) {
      if (selection.value === 2 && box_flag) {
        if (e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) {
          return
        }
        drawBox(e)
        if (!Boxes.isBoxed.value) {
            Boxes.isBoxed.value = true
        }
      }
    })
  }


    // 发送点
const sendPointData = async() => {
    try {
      const response = await api.post('/api/prompt',{
      "operation": 0,
      "type": isDotMasked.value ? 0 : 1,
      "position": [[Math.floor(send_pos.value.x),Math.floor(send_pos.value.y)]]
        }
      ) 
      //在这里处理数据
      console.log('sendPoint 操作结果:', response.data)
    }  catch (err: unknown) {
  // 类型安全的错误转换
  if (err instanceof Error) {
    handleError(err)
  } else {
    handleError(String(err))
  }
}  
}
//发送框
const sendBoxData = async() => {
    try {
      const response = await api.post('/api/prompt',{
      "operation": 0,
      "type": 2,
      "position": [Math.floor(send_box.value.start_x),Math.floor(send_box.value.start_y),Math.floor(send_box.value.end_x),Math.floor(send_box.value.end_y)]
        }
      ) 
      //在这里处理数据
      console.log('sendBox 操作结果:', response.data)
      
    }  catch (err: unknown) {
  // 类型安全的错误转换
  if (err instanceof Error) {
    handleError(err)
  } else {
    handleError(String(err))
  }
}  
}
//发送图片
const sendImageData = async () => {
  try {
      const response = await api.post('/api/uploadimage',{
        "image_path": "D:/webcode/test_image_jpeg.jpeg"//这里改为文件地址
      }
      ) 
      //在这里处理数据
      console.log('upLoadImage 操作结果:', response.data)
      
    }catch (err: unknown) {
  // 类型安全的错误转换
  if (err instanceof Error) {
    handleError(err)
  } else {
    handleError(String(err))
  }
}      
};
const sendundoDot = async() => {
    try {
      const response = await api.post('/api/prompt',{
      "operation": 1,
      "type": 0,
      "position": [[120,120]]
        }
      ) 
      //在这里处理数据
      console.log('undoDot 操作结果:', response.data)
    }  catch (err: unknown) {
  // 类型安全的错误转换
  if (err instanceof Error) {
    handleError(err)
  } else {
    handleError(String(err))
  }
}
}
const sendredoDot = async() => {
    try {
      const response = await api.post('/api/prompt',{
      "operation": 3,
      "type": 0,
      "position": [[120,120]]
        }
      ) 
      //在这里处理数据
      console.log('redoDot 操作结果:', response.data)
    }  catch (err: unknown) {
  // 类型安全的错误转换
  if (err instanceof Error) {
    handleError(err)
  } else {
    handleError(String(err))
  }
}
}
const sendremoveAllDots = async() => {
    try {
      const response = await api.post('/api/prompt',{
      "operation": 2,
      "type": 0,
      "position": [[120,120]]
        }
      ) 
      //在这里处理数据
      console.log('removeAllDots 操作结果:', response.data)
    }  catch (err: unknown) {
  // 类型安全的错误转换
  if (err instanceof Error) {
    handleError(err)
  } else {
    handleError(String(err))
  }
}
}
const sendundoBox = async() => {
    try {
      const response = await api.post('/api/prompt',{
      "operation": 1,
      "type": 2,
      "position": [[120,120]]
        }
      ) 
      //在这里处理数据
      console.log('undoBox 操作结果:', response.data)
    }  catch (err: unknown) {
  // 类型安全的错误转换
  if (err instanceof Error) {
    handleError(err)
  } else {
    handleError(String(err))
  }
}
}
const sendredoBox = async() => {
    try {
      const response = await api.post('/api/prompt',{
      "operation": 3,
      "type": 2,
      "position": [[120,120]]
        }
      ) 
      //在这里处理数据
      console.log('redoBox 操作结果:', response.data)
    }  catch (err: unknown) {
  // 类型安全的错误转换
  if (err instanceof Error) {
    handleError(err)
  } else {
    handleError(String(err))
  }
}
}
const sendremoveBox = async() => {
    try {
      const response = await api.post('/api/prompt',{
      "operation": 2,
      "type": 2,
      "position": [[120,120]]
        }
      ) 
      //在这里处理数据
      console.log('removeBox 操作结果:', response.data)
    }  catch (err: unknown) {
  // 类型安全的错误转换
  if (err instanceof Error) {
    handleError(err)
  } else {
    handleError(String(err))
}
}
}

  // 画点
  function drawPoint(e: MouseEvent) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    if (Dots.posIsDotted(e.offsetX, e.offsetY) == true) {
      return
    }
    ctx.arc(e.offsetX, e.offsetY, 5, 0, 2 * Math.PI)
    if (isDotMasked.value) {
      ctx.fillStyle = '#EE00EE'
      ctx.fill()
      Dots.addDot(e.offsetX, e.offsetY, 0)
    } 
    else {
      ctx.fillStyle = '#00BFFF'
      ctx.fill()
      Dots.addDot(e.offsetX, e.offsetY, 1)
    }
  }
  

  

  // 仅用于绘制数组里点（画矩形和undo操作删除的点）
  function drawPointByXY(x: number, y: number, dot_type: number) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    ctx.arc(x, y, 5, 0, 2 * Math.PI)
    if (dot_type == 0) {
      ctx.fillStyle = '#EE00EE'
      ctx.fill()
    } 
    else if (dot_type == 1) {
      ctx.fillStyle = '#00BFFF'
      ctx.fill()
    }
  }

  function undoDot() {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    let last_dot = Dots.undoDot()
    ctx.beginPath()
    ctx.clearRect(last_dot.x-5,last_dot.y-5,10,10)
    Dots.operation.value = 0
  }

  function redoDot() {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    let last_dot_redo = Dots.redoDot()
    ctx.beginPath()
    ctx.arc(last_dot_redo.x, last_dot_redo.y, 5, 0, 2 * Math.PI)
    if (last_dot_redo.dot_type == 0) {
      ctx.fillStyle = '#EE00EE'
      ctx.fill()
    } 
    else if (last_dot_redo.dot_type == 1) {
      ctx.fillStyle = '#00BFFF'
      ctx.fill()
    }
    Dots.operation.value = 0
  }

  function removeAllDots() {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    ctx.clearRect(0,0,canvas.width,canvas.height)
    if (Boxes.isBoxed.value){
      ctx.clearRect(0,0,canvas.width,canvas.height)
      ctx.strokeStyle = '#EE00EE'
      ctx.lineWidth = 2
      ctx.strokeRect(Boxes.box.start_x, Boxes.box.start_y, Boxes.box.end_x - Boxes.box.start_x, Boxes.box.end_y - Boxes.box.start_y)
    }
    Dots.removeDots()
    Dots.operation.value = 0
  }

  // 画框
  function drawBox(e: MouseEvent) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    Boxes.removeBox()
    ctx.clearRect(0,0,canvas.width,canvas.height)
    ctx.strokeStyle = '#EE00EE'
    ctx.lineWidth = 2
    ctx.strokeRect(box.value.start_x, box.value.start_y, e.offsetX - box.value.start_x, e.offsetY - box.value.start_y)
    Dots.dots.forEach(dot => {
      drawPointByXY(dot.x, dot.y, dot.dot_type)
    })
  }

  function undoBox() {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    Boxes.undoBox()
    ctx.beginPath()
    ctx.clearRect(0,0,canvas.width,canvas.height)
    Dots.dots.forEach(dot => {
      drawPointByXY(dot.x, dot.y, dot.dot_type)
    })
  }

  function redoBox() {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    Boxes.redoBox()
    ctx.beginPath()
    ctx.clearRect(0,0,canvas.width,canvas.height)
    ctx.strokeStyle = '#EE00EE'
    ctx.lineWidth = 2
    ctx.strokeRect(Boxes.box.start_x, Boxes.box.start_y, Boxes.box.end_x - Boxes.box.start_x, Boxes.box.end_y - Boxes.box.start_y)
    Dots.dots.forEach(dot => {
      drawPointByXY(dot.x, dot.y, dot.dot_type)
    })
  }

  function removeBox() {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    Boxes.removeBox()
    ctx.beginPath()
    ctx.clearRect(0,0,canvas.width,canvas.height)
    Dots.dots.forEach(dot => {
      drawPointByXY(dot.x, dot.y, dot.dot_type)
    })
  }

  watch(Dots.operation, (newVal) => {
    if (newVal === 1) {
      undoDot()
      sendundoDot()
    }
    else if (newVal === 3) {
      redoDot()
      sendredoDot()
    }
    else if (newVal === 4) {
      removeAllDots()
      sendremoveAllDots()
    }
  })

  watch(Boxes.operation, (newVal) => {
    if (newVal === 1) {
      undoBox()
      sendundoBox()
    }
    else if (newVal === 3) {
      redoBox()
      sendredoBox()
    }
    else if (newVal === 4) {
      removeBox()
      sendremoveBox()
    }
  })

  watch(path,(newVal)=> {
      if (newVal != null) {
        url.value = newVal
        sendImageData()
        Dots.removeDots()
        isDotMasked.value = true
        Boxes.removeBox()
        draw_Image(url.value);  // 重新加载并绘制新图片
      }
  })

</script>

<template>
  <div class="content">
    <canvas ref="myCanvas" class="content-canvas"></canvas>
    <img :src=url id="bg" alt="图片加载失败" />
  </div>
</template>

<style scoped>
    .content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 70vh;
        width: 70vw;
        padding: 2rem;
        position: relative;
        top: 5vh;
        left: 2vw;
    }

    .content .content-canvas {
        width: 100%;
        height: 100%;
        margin: 0;
        border: 1px solid #ccc;
        z-index: 1;
        position: absolute;
    }

    .content #bg {
        width: auto;
        height: auto;
        max-width: 80%;
        max-height: 100%;
        margin: 0;
        position: absolute;
    }
</style>
