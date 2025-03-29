<script setup lang="ts">
  import { ref, watch, onMounted, computed, nextTick } from 'vue'
  import { selection } from '../ts/Selection'
  import { Dots, send_dot, isDotMasked } from '../ts/Dots'
  import { Boxes, send_box } from '../ts/Boxes'
  import { imgPath, imgURL, isLoading, myFiles } from '../ts/Files'
  import { tempMaskMatrix, isWindowChange } from '../ts/Masks'
  import { isSwitch, checkBackendReady, sendSwitchImage, sendResetData } from '../ts/Telegram'
  import { sendPointData, sendUndoPointData, sendRedoPointData } from '../ts/Telegram'
  import { sendBoxData, sendUndoBoxData, sendRedoBoxData } from '../ts/Telegram'
  import AwaitBackend from '../components/AwaitBackend.vue'
  import AwaitLoadImage from '../components/AwaitLoadImage.vue'

  let box_flag = false
  let img_size_x = 0
  let img_size_y = 0
  let zoom_x = 0
  let zoom_y = 0
  let pos_x = 0
  let pos_y = 0

  const myMaskCanvas = ref()
  const myOperationCanvas = ref()
  const AnnotationMask = computed(() => myFiles.getVisibleMaskfromPathList(myFiles.getPathIdfromPathList(imgPath.value)))

  onMounted(() => {
    draw_Image(imgURL.value) // 初始绘制图片
    checkBackendReady()
  })

  // 异步初始化临时遮罩矩阵
  function initializeTempMaskAsync(width: number, height: number): Promise<Array<Array<number>>> {
    return new Promise((resolve) => {
      const matrix: Array<Array<number>> = []
      let i = 0
      const chunkSize = 100 // 每次处理100行
      function processChunk() {
        const end = Math.min(i + chunkSize, height)
        for (; i < end; i++) {
          matrix[i] = new Array(width).fill(0)
        }
        if (i < height) {
          setTimeout(processChunk, 0)
        } else {
          resolve(matrix)
        }
      }
      processChunk()
    })
  }

  // 初始化图片
  function draw_Image(imageSrc: string) {
    // 确保图片清晰度，并初始化 canvas
    const maskCanvas = myMaskCanvas.value
    const operationCanvas = myOperationCanvas.value
    const maskCtx = maskCanvas.getContext('2d')!
    const operationCtx = operationCanvas.getContext('2d')!

    maskCanvas.width = maskCanvas.clientWidth * window.devicePixelRatio
    maskCanvas.height = maskCanvas.clientHeight * window.devicePixelRatio
    operationCanvas.width = maskCanvas.width
    operationCanvas.height = maskCanvas.height

    maskCtx.scale(window.devicePixelRatio, window.devicePixelRatio)
    operationCtx.scale(window.devicePixelRatio, window.devicePixelRatio)

    let img = document.getElementById("bg") as HTMLImageElement
    img.src = imageSrc

    img.onload = async function() {
      pos_x = (maskCanvas.clientWidth-img.width)/2
      pos_y = (maskCanvas.clientHeight-img.height)/2
      zoom_x = img.width / img.naturalWidth
      zoom_y = img.height / img.naturalHeight
      img_size_x = img.naturalWidth
      img_size_y = img.naturalHeight

      requestIdleCallback(async () => {
        if (!isWindowChange || tempMaskMatrix.value.length === 0) {
          tempMaskMatrix.value = await initializeTempMaskAsync(img_size_x, img_size_y)
        } else if (isWindowChange) {
          drawPointAndBox()
          drawMask()
        }
      })
    }

    maskCanvas.addEventListener('mousedown', async function(e: MouseEvent) {
      if (selection.value === 1) {
        if (e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) {
          return
        }
        send_dot.value = {
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

    maskCanvas.addEventListener('mouseup', async function(e: MouseEvent) {
      if (selection.value === 2 && box_flag) {
        if ((e.offsetX < pos_x || e.offsetY < pos_y || e.offsetX > pos_x+img.width || e.offsetY > pos_y+img.height) 
          || (e.offsetX-send_box.value.start_x*zoom_x-pos_x <= 1 && e.offsetY-send_box.value.start_y*zoom_y-pos_y <= 1)) {
          box_flag = false
          maskCtx.beginPath()
          maskCtx.clearRect(0,0,maskCanvas.width,maskCanvas.height)
          return
        }
        box_flag = false
        send_box.value.end_x = (e.offsetX - pos_x) / zoom_x
        send_box.value.end_y = (e.offsetY - pos_y) / zoom_y
        Boxes.resetBox()
        Dots.resetDots()
        tempMaskMatrix.value = await initializeTempMaskAsync(img_size_x, img_size_y)
        Boxes.setBox(send_box.value.start_x, send_box.value.start_y, send_box.value.end_x, send_box.value.end_y)
        await sendBoxData()
        drawMask()
      }
    })

    maskCanvas.addEventListener('mousemove', async function(e: MouseEvent) {
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
  async function drawPoint(e: MouseEvent) {
    const operationCanvas = myOperationCanvas.value
    const operationCtx = operationCanvas.getContext('2d')!
    if (Dots.posIsDotted(send_dot.value.x, send_dot.value.y) === true) {
      return
    }
    operationCtx.beginPath()
    operationCtx.globalAlpha = 1
    operationCtx.arc(e.offsetX, e.offsetY, 5, 0, 2 * Math.PI)
    operationCtx.fillStyle = isDotMasked.value ? '#EE00EE' : '#00BFFF'
    operationCtx.fill()
    Dots.addDot(send_dot.value.x, send_dot.value.y, isDotMasked.value ? 0 : 1)
    await sendPointData()
    drawMask()
  }

  // 在OperationCanvas上绘制点
  function drawPointByXY(x: number, y: number, dot_type: number) {
    const operationCanvas = myOperationCanvas.value
    const operationCtx = operationCanvas.getContext('2d')!
    operationCtx.beginPath()
    operationCtx.globalAlpha = 1
    operationCtx.arc(x * zoom_x + pos_x, y * zoom_y + pos_y, 5, 0, 2 * Math.PI)
    operationCtx.fillStyle = dot_type === 0 ? '#EE00EE' : '#00BFFF'
    operationCtx.fill()
  }

  // 撤销点
  async function undoDot() {
    let last_dot = Dots.undoDot()
    Dots.operation.value = 0
    if (last_dot) {
      send_dot.value.x = last_dot.x
      send_dot.value.y = last_dot.y
    }
    await sendUndoPointData()
    drawMask()
    drawPointAndBox()
  }

  // 反撤销点
  async function redoDot() {
    let last_dot_redo = Dots.redoDot()
    Dots.operation.value = 0
    if (last_dot_redo) {
      send_dot.value.x = last_dot_redo.x
      send_dot.value.y = last_dot_redo.y
    }
    await sendRedoPointData()
    drawMask()
    drawPointAndBox()
  }

  // 画框
  function drawBox(e: MouseEvent) {
    const operationCanvas = myOperationCanvas.value
    const operationCtx = operationCanvas.getContext('2d')!
    operationCtx.beginPath()
    operationCtx.clearRect(0,0,operationCanvas.width,operationCanvas.height)
    operationCtx.strokeStyle = '#EE00EE'
    operationCtx.lineWidth = 2
    operationCtx.globalAlpha = 1
    operationCtx.strokeRect(send_box.value.start_x*zoom_x+pos_x, send_box.value.start_y*zoom_y+pos_y,
       e.offsetX-send_box.value.start_x*zoom_x-pos_x, e.offsetY-send_box.value.start_y*zoom_y-pos_y)
  }

  // 撤销框
  async function undoBox() {
    Boxes.undoBox()
    Boxes.operation.value = 0
    Dots.resetDots()
    await sendUndoBoxData()
    drawMask()
    drawPointAndBox()
  }

  // 反撤销框
  async function redoBox() {
    Boxes.redoBox()
    Boxes.operation.value = 0
    await sendRedoBoxData()
    drawMask()
    drawPointAndBox()
  }

  // 重绘框点
  function drawPointAndBox() {
    const operationCanvas = myOperationCanvas.value
    const operationCtx = operationCanvas.getContext('2d')!
    operationCtx.beginPath()
    operationCtx.clearRect(0,0,operationCanvas.width,operationCanvas.height)
    operationCtx.strokeStyle = '#EE00EE'
    operationCtx.lineWidth = 2
    operationCtx.globalAlpha = 1
    operationCtx.strokeRect(Boxes.box.start_x*zoom_x+pos_x, Boxes.box.start_y*zoom_y+pos_y, 
        (Boxes.box.end_x-Boxes.box.start_x)*zoom_x, (Boxes.box.end_y-Boxes.box.start_y)*zoom_y)
    Dots.dots.forEach(dot => {
      drawPointByXY(dot.x, dot.y, dot.dot_type)
    })
  }

  // 绘制遮罩
  async function drawMask() {
    const maskCanvas = myMaskCanvas.value
    const maskCtx = maskCanvas.getContext('2d')!
    maskCtx.beginPath()
    maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height)
    drawAnnotationMasks() // 绘制已标注Mask
    if (tempMaskMatrix.value.length === 0) {
      return
    }
    drawMaskHelp(tempMaskMatrix.value, '#00BFFF')  // 绘制遮罩
  }

  // 绘制已标注的可见的所有mask
  function drawAnnotationMasks() {
    for (const tempMask of AnnotationMask.value) {
      drawMaskHelp(tempMask.mask_matrix, tempMask.mask_color)
    }
  }

  // 绘制遮罩的具体实现函数
  function drawMaskHelp(mask: Array<Array<number>>, color: string) {
    const maskCanvas = myMaskCanvas.value
    const maskCtx = maskCanvas.getContext('2d')
    maskCtx.globalCompositeOperation="source-over"
    maskCtx.globalAlpha = 0.1
    maskCtx.fillStyle = color
    for (let j = 0; j < mask.length; j++) {
      for (let i = 0; i < mask[j].length; i++) {
        if (mask[j][i] === 1) {
          maskCtx.beginPath()
          maskCtx.arc(i*zoom_x+pos_x, j*zoom_y+pos_y, 1, 0 ,2 * Math.PI)
          maskCtx.fill()
        }
      }
    }
  }

  watch(Dots.operation, async(newVal) => {
    if (newVal === 1) {
      undoDot()
    }
    else if (newVal === 2) {
      Dots.resetDots()
      Boxes.resetBox()
      Dots.operation.value = 0
      Boxes.operation.value = 0
      await sendResetData()
      drawMask()
      drawPointAndBox()
    }
    else if (newVal === 3) {
      redoDot()
    }
  })

  watch(Boxes.operation, async(newVal) => {
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
      imgURL.value = `file://${newVal}`
      isDotMasked.value = true
      draw_Image(imgURL.value)  // 重新加载并绘制图片
      if (isSwitch.value) {
        Dots.resetDots()
        Boxes.resetBox()
        await sendResetData()
        drawMask()
        drawPointAndBox()
        sendSwitchImage()
        isSwitch.value = false
        await nextTick()
      }
    }
  })

  watch(AnnotationMask, async()=> {
    if (!isSwitch.value) {
      drawMask()
    }
  })
</script>

<template>
  <div class="myContent">
    <div class="content">
      <canvas ref="myMaskCanvas" class="mask-canvas"></canvas>
      <canvas ref="myOperationCanvas" class="operation-canvas"></canvas>
      <img :src=imgURL id="bg" alt="请上传图片" />
      <AwaitLoadImage v-if="isLoading"></AwaitLoadImage>
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
    padding: 0rem;
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

  .content .mask-canvas {
    width: 100%;
    height: 100%;
    padding: 0rem;
    margin: 0rem;
    z-index: 3;
    position: absolute;
  }

  .content .operation-canvas {
    width: 100%;
    height: 100%;
    padding: 0rem;
    margin: 0rem;
    z-index: 2;
    position: absolute;
  }

  .content #bg {
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    padding: 0rem;
    margin: 0rem;
    z-index: 1;
    position: absolute;
  }
</style>