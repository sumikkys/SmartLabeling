<script setup lang="ts">
  import { ref, watch, onMounted } from 'vue'
  import { selection } from '../js/selection'
  import { Dots, isDotMasked } from '../js/Dots'
  import { Boxes } from '../js/Boxes'
  import { path } from '../js/path'

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

  onMounted(() => {
    draw_Image(url.value) // 初始绘制图片
  })

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
    }
    else if (newVal === 3) {
      redoDot()
    }
    else if (newVal === 4) {
      removeAllDots()
    }
  })

  watch(Boxes.operation, (newVal) => {
    if (newVal === 1) {
      undoBox()
    }
    else if (newVal === 3) {
      redoBox()
    }
    else if (newVal === 4) {
      removeBox()
    }
  })


  watch(path,(newVal)=> {
      if (newVal != null) {
        url.value = newVal
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
