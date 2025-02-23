<script setup lang="ts">
  import AnnotationSidebar from '../components/AnnotationSidebar.vue'
  import { ref, watch, onMounted } from 'vue'
  import { selection } from '../js/selection'
  import { Dots, isDotMasked } from '../js/Dots'
  import { Boxes } from '../js/Boxes'
  import { imgPath, imgURL, projectPath, projectName } from '../js/file'
  import { tempMaskMatrix } from '../js/Masks'
  import axios from 'axios'
  import type { AxiosError } from 'axios'

  let url = ref('')

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

  let img_size_x = 0
  let img_size_y = 0
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

  // 绘制图片
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
      img_size_x = img.naturalWidth
      img_size_y = img.naturalHeight
      ctx.beginPath()
      tempMaskMatrix.value = new Array(img_size_x).fill(null).map(() => new Array(img_size_y).fill(0))
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

  // 发送图片
  const sendImageData = async () => {
    try {
        const response = await api.post('/api/uploadimage',{
          "image_path": imgPath.value,
          "project_name": projectName.value,
          "storage_path": projectPath.value,
        })
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

  // 画点
  function drawPoint(e: MouseEvent) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    if (Dots.posIsDotted(e.offsetX, e.offsetY) == true) {
      return
    }
    ctx.arc(e.offsetX, e.offsetY, 5, 0, 2 * Math.PI)
    ctx.globalAlpha = 1
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
    sendPointData()
  }

  // 仅用于绘制数组里点（undo操作删除的点）
  function drawPointByXY(x: number, y: number, dot_type: number) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    ctx.arc(x, y, 5, 0, 2 * Math.PI)
    ctx.globalAlpha = 1
    if (dot_type == 0) {
      ctx.fillStyle = '#EE00EE'
      ctx.fill()
    } 
    else if (dot_type == 1) {
      ctx.fillStyle = '#00BFFF'
      ctx.fill()
    }
  }

  // 撤销点
  function undoDot() {
    let last_dot = Dots.undoDot()
    Dots.operation.value = 0
    send_pos.value.x = (last_dot.x - pos_x) / zoom_x
    send_pos.value.y = (last_dot.y - pos_y) / zoom_y
    sendUndoPointData()
  }

  // 反撤销点
  function redoDot() {
    let last_dot_redo = Dots.redoDot()
    Dots.operation.value = 0
    send_pos.value.x = (last_dot_redo.x - pos_x) / zoom_x
    send_pos.value.y = (last_dot_redo.y - pos_y) / zoom_y
    sendRedoPointData()
  }

  // 发送点请求
  const sendPointData = async() => {
      try {
        const response = await api.post('/api/prompt',{
          "operation": 0,
          "type": isDotMasked.value ? 0 : 1,
          "position": [[Math.floor(send_pos.value.x),Math.floor(send_pos.value.y)]],
          "project_name": projectName.value,
          "storage_path": projectPath.value,
          "image_name": imgPath.value.split('\\').pop().split('/').pop()
        })
        const maskMatrix = response.data.masks
        drawMask(maskMatrix)
        console.log('Prompt 操作结果:', response.data)
      }  catch (err: unknown) {
      // 类型安全的错误转换
      if (err instanceof Error) {
        handleError(err)
      } else {
        handleError(String(err))
      }
    }
  }

  // 发送撤销点请求
  const sendUndoPointData = async() => {
      try {
        const response = await api.post('/api/prompt',{
          "operation": 1,
          "type": isDotMasked.value ? 0 : 1,
          "position": [[Math.floor(send_pos.value.x),Math.floor(send_pos.value.y)]],
          "project_name": projectName.value,
          "storage_path": projectPath.value,
          "image_name": imgPath.value.split('\\').pop().split('/').pop()
        })
        const maskMatrix = response.data.masks
        drawMask(maskMatrix)
        console.log('Prompt 操作结果:', response.data)
      }  catch (err: unknown) {
      // 类型安全的错误转换
      if (err instanceof Error) {
        handleError(err)
      } else {
        handleError(String(err))
      }
    }
  }

  // 发送反撤销点请求
  const sendRedoPointData = async() => {
      try {
        const response = await api.post('/api/prompt',{
          "operation": 3,
          "type": isDotMasked.value ? 0 : 1,
          "position": [[Math.floor(send_pos.value.x),Math.floor(send_pos.value.y)]],
          "project_name": projectName.value,
          "storage_path": projectPath.value,
          "image_name": imgPath.value.split('\\').pop().split('/').pop()
        })
        const maskMatrix = response.data.masks
        drawMask(maskMatrix)
        console.log('Prompt 操作结果:', response.data)
      }  catch (err: unknown) {
      // 类型安全的错误转换
      if (err instanceof Error) {
        handleError(err)
      } else {
        handleError(String(err))
      }
    }
  }

  // 画框
  function drawBox(e: MouseEvent) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    Boxes.resetBox()
    Dots.resetDots()
    tempMaskMatrix.value = new Array(img_size_x).fill(null).map(() => new Array(img_size_y).fill(0))
    ctx.clearRect(0,0,canvas.width,canvas.height)
    ctx.strokeStyle = '#EE00EE'
    ctx.lineWidth = 2
    ctx.globalAlpha = 1
    ctx.strokeRect(box.value.start_x, box.value.start_y, e.offsetX - box.value.start_x, e.offsetY - box.value.start_y)
  }

  // 撤销框
  function undoBox() {
    Boxes.undoBox()
    Dots.resetDots()
    sendUndoBoxData()
  }

  // 反撤销框
  function redoBox() {
    Boxes.redoBox()
    sendRedoBoxData()
  }

  // 发送框
  const sendBoxData = async() => {
      try {
        const response = await api.post('/api/prompt',{
          "operation": 0,
          "type": 2,
          "position": [Math.floor(send_box.value.start_x),Math.floor(send_box.value.start_y),Math.floor(send_box.value.end_x),Math.floor(send_box.value.end_y)],
          "project_name": projectName.value,
          "storage_path": projectPath.value,
          "image_name": imgPath.value.split('\\').pop().split('/').pop()
        }
        ) 
        const maskMatrix = response.data.masks
        drawMask(maskMatrix)
        console.log('Prompt 操作结果:', response.data)
        
      }  catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }  
  }

  // 发送撤销框
  const sendUndoBoxData = async() => {
    try {
      const response = await api.post('/api/prompt',{
          "operation": 1,
          "type": 2,
          "position": [Math.floor(send_box.value.start_x),Math.floor(send_box.value.start_y),Math.floor(send_box.value.end_x),Math.floor(send_box.value.end_y)],
          "project_name": projectName.value,
          "storage_path": projectPath.value,
          "image_name": imgPath.value.split('\\').pop().split('/').pop()
        }
      )
      const maskMatrix = response.data.masks
      drawMask(maskMatrix)
      console.log('Prompt 操作结果:', response.data)
      
    }  catch (err: unknown) {
      // 类型安全的错误转换
      if (err instanceof Error) {
        handleError(err)
      } else {
        handleError(String(err))
      }
    }  
  }

  // 发送反撤销框
  const sendRedoBoxData = async() => {
    try {
      const response = await api.post('/api/prompt',{
        "operation": 3,
        "type": 2,
        "position": [Math.floor(send_box.value.start_x),Math.floor(send_box.value.start_y),Math.floor(send_box.value.end_x),Math.floor(send_box.value.end_y)],
        "project_name": projectName.value,
        "storage_path": projectPath.value,
        "image_name": imgPath.value.split('\\').pop().split('/').pop()
      }
      ) 
      const maskMatrix = response.data.masks
      drawMask(maskMatrix)
      console.log('Prompt 操作结果:', response.data)
      
    }  catch (err: unknown) {
      // 类型安全的错误转换
      if (err instanceof Error) {
        handleError(err)
      } else {
        handleError(String(err))
      }
    }  
  }

  // 发送清空请求
  const sendResetData = async() => {
      try {
        const response = await api.post('/api/prompt',{
          "operation": 2,
          "type": 0,
          "position": [[0, 0]],
          "project_name": projectName.value,
          "storage_path": projectPath.value,
          "image_name": imgPath.value.split('\\').pop().split('/').pop()
        })
        const maskMatrix = response.data.masks
        drawMask(maskMatrix)
        console.log('Prompt 操作结果:', response.data)
      }  catch (err: unknown) {
      // 类型安全的错误转换
      if (err instanceof Error) {
        handleError(err)
      } else {
        handleError(String(err))
      }
    }
  }

  // 绘制遮罩
  function drawMask(masks : Array<Array<number>>) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    ctx.clearRect(0,0,canvas.width,canvas.height)
    ctx.strokeStyle = '#EE00EE'
    ctx.lineWidth = 2
    ctx.globalAlpha = 1
    ctx.strokeRect(Boxes.box.start_x, Boxes.box.start_y, Boxes.box.end_x - Boxes.box.start_x, Boxes.box.end_y - Boxes.box.start_y)
    Dots.dots.forEach(dot => {
      drawPointByXY(dot.x, dot.y, dot.dot_type)
    })
    ctx.globalCompositeOperation="source-over"
    ctx.globalAlpha = 0.1
    ctx.fillStyle = '#00BFFF'
    if (!masks) {
      tempMaskMatrix.value = new Array(img_size_x).fill(null).map(() => new Array(img_size_y).fill(0))
    }
    for (let j = 0; j < masks.length; j++) {
      for (let i = 0; i < masks[j].length; i++) {
        if (masks[j][i] === 1) {
          tempMaskMatrix.value[j][i] = 1
          ctx.beginPath()
          ctx.arc(i*zoom_x+pos_x, j*zoom_y+pos_y, 1, 0 ,2 * Math.PI)
          ctx.fill()
        }
      }
    }
  }

  watch(Dots.operation, (newVal) => {
    if (newVal === 1) {
      undoDot()
    }
    else if (newVal === 2) {
      Dots.resetDots()
      Boxes.resetBox()
      Dots.operation.value = 0
      Boxes.operation.value = 0
      sendResetData()
    }
    else if (newVal === 3) {
      redoDot()
    }
  })

  watch(Boxes.operation, (newVal) => {
    if (newVal === 1) {
      undoBox()
    }
    else if (newVal === 2) {
      // 在Dots.operation里处理，故留空
    }
    else if (newVal === 3) {
      redoBox()
    }
  })

  watch(imgURL,(newVal)=> {
      if (newVal != null) {
        url.value = newVal
        sendImageData()
        Dots.resetDots()
        isDotMasked.value = true
        Boxes.resetBox()
        draw_Image(url.value);  // 重新加载并绘制新图片
      }
  })

</script>

<template>
  <div style="display: flex; flex-direction: row;">
    <div class="content">
      <canvas ref="myCanvas" class="content-canvas"></canvas>
      <img :src=url id="bg" alt="请上传图片" />
    </div>
    <AnnotationSidebar></AnnotationSidebar>
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
        padding: 0rem;
        position: relative;
        top: 5vh;
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
        max-width: 100%;
        max-height: 100%;
        margin: 0;
        position: absolute;
    }
</style>
