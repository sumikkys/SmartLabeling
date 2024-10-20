<script setup lang="ts">
  import { ref, watch } from 'vue'
  import { selection } from '../js/selection'
  import { isDotted } from '../js/isDotted'
  import { isBoxed } from '../js/isBoxed'

  let url = ref('https://segment-anything.com/assets/gallery/AdobeStock_94274587_welsh_corgi_pembroke_CD.jpg')
  let img = document.querySelector('.content-img') as HTMLImageElement

  let pos = ref({
    x: 0,
    y: 0
  })

  let send_pos = ref({
    x: 0,
    y: 0    
  })

  let box = ref({
    start_pos:{
      x: 0,
      y: 0
    },
    end_pos:{
      x: 0,
      y: 0
    }
  })

  let send_box = ref({
    start_pos:{
      x: 0,
      y: 0
    },
    end_pos:{
      x: 0,
      y: 0
    }
  })

  function MouseOverPicture() {
    let tip = document.querySelector('.tip-text') as HTMLElement
    let tipContent : string = ''
    if (tip != null) {
        tip.style.backgroundColor = '#B0E0E6'
        if (selection.value === 1) {
            tipContent = 'When hovering over the image, SAM is running in the browser'
        }
        else if (selection.value === 2) {
            tipContent = 'Draw a box around on object.'
        }
        tip.innerHTML = `&nbsp;&nbsp;${ tipContent }&nbsp;&nbsp;`
    }
  }

  function MouseOutPicture() {
    let tip = document.querySelector('.tip-text') as HTMLElement
    if (tip != null) {
        tip.style.backgroundColor = '#FFFFFF'
        tip.innerHTML = ''
    }
  }

  function MouseClickPictrue(event: MouseEvent) {
    pos.value = {
        x: event.offsetX,
        y: event.offsetY
    }
    send_pos.value = {
        x: pos.value.x / img.width * img.naturalWidth,
        y: pos.value.y / img.height * img.naturalHeight
    }
    console.log(pos.value)
    console.log(send_pos.value)
    if (isDotted.value === false) {
        isDotted.value = true
    }
  }

  function MouseDownBoxPictrue(event: MouseEvent) {
    box.value.start_pos ={
      x: event.offsetX,
      y: event.offsetY
    }
    img.addEventListener('mousemove', MouseMoveBoxPictrue)
    img.addEventListener('mouseup', MouseUpBoxPictrue)
  }

  function MouseMoveBoxPictrue(event: MouseEvent) {
    pos.value = {
      x : event.offsetX,
      y : event.offsetY
    }
  }

  function MouseUpBoxPictrue(event: MouseEvent) {
    box.value.end_pos = {
      x: event.offsetX,
      y: event.offsetY
    }
    if (box.value.start_pos.x-box.value.end_pos.x <=1 && box.value.start_pos.y-box.value.end_pos.y <=1) {
      box.value = {
        start_pos:{
          x: 0,
          y: 0
        },
        end_pos:{
          x: 0,
          y: 0
        }
      }
    }
    else {
      send_box.value = {
        start_pos:{
          x: box.value.start_pos.x / img.width * img.naturalWidth,
          y: box.value.start_pos.y / img.height * img.naturalHeight
        },
        end_pos:{
          x: box.value.end_pos.x / img.width * img.naturalWidth,
          y: box.value.end_pos.y / img.height * img.naturalHeight
        }
      }
      console.log(box.value)
      isBoxed.value = true
    }
  }

  watch(isDotted, (newVal) => {
    if (newVal === true) {
    }
    else if (newVal === false) { 
    }
  })

</script>

<template>
    <div class="content">
        <div class="tip-text"></div>
        <img :src="url" class="content-img" v-if="selection === 1"
            @mouseover="MouseOverPicture()" @mouseout="MouseOutPicture()" @click="MouseClickPictrue"/>
        <img :src="url" class="content-img" v-else-if="selection === 2"
            @mouseover="MouseOverPicture()" @mouseout="MouseOutPicture()" @mousedown="MouseDownBoxPictrue"/>
        <div v-if="selection === 1" class="dots-box">true</div>
    </div>
    <div class="boxed-box" :pos="pos">{{ pos.x }}&nbsp;{{ pos.y }}</div>
</template>

<style scoped>
    .content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        width: 100%;
    }

    .content .content-img {
        max-width: 60%;
        height: auto;
        margin: 0;
    }
    
    .content .dots-box {
      max-width: 60%;
      height: auto;
      margin: 0;
      z-index: 1;
      position: relative;
    }

    .content .tip-text {
        margin: 20px 0px;
        background-color: #FFFFFF;
        color: #000000;
        font: normal 18px Arial, sans-serif;
        border-radius: 8px;
        word-break: keep-all;
        line-height: 40px;
        text-align: center;
        width: fit-content;
        height: 40px;
    }

</style>