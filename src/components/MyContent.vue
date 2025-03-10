<script setup lang="ts">
  import { ref, watch, onMounted, computed } from 'vue'
  import { selection } from '../ts/Selection'
  import { Dots, isDotMasked } from '../ts/Dots'
  import { Boxes } from '../ts/Boxes'
  import { imgPath, imgURL, myFiles } from '../ts/Files'
  import { projectPath, projectName } from '../ts/Projects'
  import { tempMaskMatrix, isWindowChange } from '../ts/Masks'
  import { api, handleError, isSwitch } from '../ts/Telegram'
  import { checkBackendReady, sendSwitchImage } from '../ts/Telegram'
  import AwaitBackend from '../components/AwaitBackend.vue'

  let send_pos = ref({
    x: 0,
    y: 0    
  })

  let box_flag = false

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
  const AnnotationMask = computed(() => myFiles.getVisibleMaskfromPathList(myFiles.getPathIdfromPathList(imgPath.value)))

  onMounted(() => {
    draw_Image(imgURL.value) // 初始绘制图片
    checkBackendReady()
  })

  // 绘制图片
  function draw_Image(imageSrc: string) {
    // 确保图片清晰度，并初始化 canvas
    const canvas = myCanvas.value
    canvas.width = canvas.clientWidth * window.devicePixelRatio
    canvas.height = canvas.clientHeight * window.devicePixelRatio
    const ctx = canvas.getContext('2d')
    ctx?.scale(window.devicePixelRatio, window.devicePixelRatio)

    let img = document.getElementById("bg") as HTMLImageElement;
    img.src = imageSrc

    img.onload = function() {
      pos_x = (canvas.offsetWidth-img.width)/2
      pos_y = (canvas.offsetHeight-img.height)/2
      zoom_x = img.width / img.naturalWidth
      zoom_y = img.height / img.naturalHeight
      img_size_x = img.naturalWidth
      img_size_y = img.naturalHeight
      if (!isWindowChange || tempMaskMatrix.value.length === 0) {
        tempMaskMatrix.value = new Array(img_size_x).fill(null).map(() => new Array(img_size_y).fill(0))
      }
      else if (isWindowChange) {
        drawMask(tempMaskMatrix.value)
      }
    }

    canvas.addEventListener('mousedown', function(e: MouseEvent) {
      if (selection.value === 1) {
        if (e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) {
          return
        }
        send_pos.value = {
            x: (e.offsetX - pos_x) / zoom_x,
            y: (e.offsetY - pos_y) / zoom_y
        }
        drawPoint(e)
        if (!Dots.isDotted.value) {
            Dots.isDotted.value = true
        }
      }
      else if (selection.value === 2 && !box_flag) {
        if (e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) {
          return
        }
        box_flag = true;
        send_box.value.start_x = (e.offsetX - pos_x) / zoom_x
        send_box.value.start_y = (e.offsetY - pos_y) / zoom_y
      }
    })

    canvas.addEventListener('mouseup', function(e: MouseEvent) {
      if (selection.value === 2 && box_flag) {
        if ((e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) 
          || (e.offsetX-send_box.value.start_x*zoom_x-pos_x <= 1 && e.offsetY-send_box.value.start_y*zoom_y-pos_y <= 1)) {
          box_flag = false
          ctx.beginPath()
          ctx.clearRect(0,0,canvas.width,canvas.height)
          return
        }
        box_flag = false
        send_box.value.end_x = (e.offsetX - pos_x) / zoom_x
        send_box.value.end_y = (e.offsetY - pos_y) / zoom_y
        Boxes.setBox(send_box.value.start_x, send_box.value.start_y, send_box.value.end_x, send_box.value.end_y)
        sendBoxData()
      }
    })

    canvas.addEventListener('mousemove', function(e: MouseEvent) {
      if (selection.value === 2 && box_flag) {
        if (e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) {
          box_flag = false
          return
        }
        drawBox(e)
        if (!Boxes.isBoxed.value) {
            Boxes.isBoxed.value = true
        }
      }
    })
  }

  // 画点
  function drawPoint(e: MouseEvent) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    if (Dots.posIsDotted(send_pos.value.x, send_pos.value.y) === true) {
      return
    }
    ctx.arc(e.offsetX, e.offsetY, 5, 0, 2 * Math.PI)
    ctx.globalAlpha = 1
    if (isDotMasked.value) {
      ctx.fillStyle = '#EE00EE'
      ctx.fill()
      Dots.addDot(send_pos.value.x, send_pos.value.y, 0)
    } 
    else {
      ctx.fillStyle = '#00BFFF'
      ctx.fill()
      Dots.addDot(send_pos.value.x, send_pos.value.y, 1)
    }
    sendPointData()
  }

  // 仅用于绘制数组里点（undo操作删除的点）
  function drawPointByXY(x: number, y: number, dot_type: number) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    ctx.arc(x*zoom_x+pos_x, y*zoom_y+pos_y, 5, 0, 2 * Math.PI)
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
    if (last_dot) {
      send_pos.value.x = last_dot.x
      send_pos.value.y = last_dot.y
    }
    sendUndoPointData()
  }

  // 反撤销点
  function redoDot() {
    let last_dot_redo = Dots.redoDot()
    Dots.operation.value = 0
    if (last_dot_redo) {
      send_pos.value.x = last_dot_redo.x
      send_pos.value.y = last_dot_redo.y
    }
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
    ctx.strokeRect(send_box.value.start_x*zoom_x+pos_x, send_box.value.start_y*zoom_y+pos_y,
       e.offsetX-send_box.value.start_x*zoom_x-pos_x, e.offsetY-send_box.value.start_y*zoom_y-pos_y)
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
  function drawMask(mask : Array<Array<number>>) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    ctx.clearRect(0,0,canvas.width,canvas.height)
    ctx.strokeStyle = '#EE00EE'
    ctx.lineWidth = 2
    ctx.globalAlpha = 1
    ctx.strokeRect(Boxes.box.start_x*zoom_x+pos_x, Boxes.box.start_y*zoom_y+pos_y, 
        (Boxes.box.end_x-Boxes.box.start_x)*zoom_x, (Boxes.box.end_y-Boxes.box.start_y)*zoom_y)
    Dots.dots.forEach(dot => {
      drawPointByXY(dot.x, dot.y, dot.dot_type)
    })
    drawAnnotationMasks()
    if (mask.length === 0) {
      tempMaskMatrix.value = new Array(img_size_x).fill(null).map(() => new Array(img_size_y).fill(0))
      return
    }
    drawMaskHelp(mask, '#00BFFF', false)
  }

  // 绘制遮罩的具体实现函数
  function drawMaskHelp(mask : Array<Array<number>>, color: string, isAnnotation: boolean) {
    const canvas = myCanvas.value
    const ctx = canvas.getContext('2d')
    ctx.beginPath()
    ctx.globalCompositeOperation="source-over"
    ctx.globalAlpha = 0.1
    ctx.fillStyle = color
    for (let j = 0; j < mask.length; j++) {
      for (let i = 0; i < mask[j].length; i++) {
        if (mask[j][i] === 1) {
          if (!isAnnotation) tempMaskMatrix.value[j][i] = 1
          ctx.beginPath()
          ctx.arc(i*zoom_x+pos_x, j*zoom_y+pos_y, 1, 0 ,2 * Math.PI)
          ctx.fill()
        }
        else if (mask[j][i] === 0 && !isAnnotation) {
          tempMaskMatrix.value[j][i] = 0
        }
      }
    }
  }

  function drawAnnotationMasks() {
    AnnotationMask.value?.forEach(tempMask => {
      drawMaskHelp(tempMask.mask_matrix, tempMask.mask_color, true)
    })
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

  watch(isWindowChange, async(newVal) => {
    if (newVal) {
      draw_Image(imgURL.value)  // 重新加载并绘制图片
      isWindowChange.value = false
    }
  })

  watch(imgPath, async(newVal)=> {
      if (newVal != null) {
        Dots.resetDots()
        Boxes.resetBox()
        imgURL.value = `file://${newVal}`
        isDotMasked.value = true
        draw_Image(imgURL.value)  // 重新加载并绘制图片
        if (isSwitch.value) {
          await sendResetData()
          sendSwitchImage()
        }
      }
  })

  watch(AnnotationMask, ()=> {
    drawMask(tempMaskMatrix.value)
  })
</script>

<template>
  <div class="myContent">
    <div class="content">
      <canvas ref="myCanvas" class="content-canvas"></canvas>
      <img :src=imgURL id="bg" alt="请上传图片" />
    </div>
    <AwaitBackend></AwaitBackend>
  </div>
</template>

<style scoped>
    .myContent {
        height: 100%;
        border: 0.1rem #D3D3D3;
        border-top-style: solid;
        border-right-style: none;
        border-bottom-style: solid;
        border-left-style: none;
        padding: 1.5rem;
        margin: 0rem;
        display: flex;
        list-style-type: none;
        flex-direction: column;
        justify-content: start;
        align-items: center;
        text-align: center;
        position: relative;
    }

    .content {
        width: 100%;
        height: 100%;
        padding: 0rem;
        margin: 0rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        flex: 1;
    }

    .content .content-canvas {
        width: 100%;
        height: 100%;
        padding: 0rem;
        margin: 0rem;
        z-index: 1;
        position: absolute;
    }

    .content #bg {
        width: auto;
        height: auto;
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
        margin: 0;
        z-index: 0;
        position: absolute;
    }
</style>
