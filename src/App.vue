<script setup lang="ts">
  import { onMounted, onBeforeUnmount } from 'vue'
  import { debounce } from 'lodash'
  import { isWindowChange } from './ts/Masks'
  import MyHeader from './components/MyHeader.vue'
  import MyTools from './components/MyTools.vue'
  import MyContent from './components/MyContent.vue'
  import AnnotationSidebar from './components/AnnotationSidebar.vue'

  // 设计稿基准配置
  const designWidth = 1280  // 设计稿宽度
  const baseFontSize = 10   // 1rem = 10px
  const minFontSize = 8     // 最小字体限制
  const maxFontSize = 12    // 最大字体限制

  // 动态计算根字体大小
  const setRemScale = () => {
    const currentWidth = document.documentElement.clientWidth
    const scale = currentWidth / designWidth
    const fontSize = Math.min(maxFontSize, Math.max(minFontSize, baseFontSize * scale))
    document.documentElement.style.fontSize = `${fontSize}px`
    isWindowChange.value = true
  }

  // 防抖处理窗口变化
  const handleResize = debounce(setRemScale, 200)

  onMounted(() => {
    setRemScale() // 初始化计算
    window.addEventListener('resize', handleResize)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
  })
</script>

<template>
  <div class="grid-container">
    <div class="item1"><MyHeader></MyHeader></div>
    <div class="item2"><MyTools></MyTools></div>
    <div class="item3"><MyContent></MyContent></div>
    <div class="item4"><AnnotationSidebar></AnnotationSidebar></div>
    <div class="item5" style="height: 100%;"></div>
  </div>
</template>

<style>
  :root {
    font-size: 10px;
  }

  body {
    margin: 0;
  }

  .item1 { 
    grid-area: header; 
  }

  .item2 { 
    grid-area: left-menu; 
  }

  .item3 { 
    grid-area: main; 
  }

  .item4 { 
    grid-area: right-menu; 
  }

  .item5 {
    grid-area: footer
  }

  .grid-container {
    display: grid;
    grid:
    'header header header'
    'left-menu main right-menu'
    'footer footer footer';
    grid-gap: 0;
    background-color: white;
    grid-template-rows: 10vh 80vh 10vh;
    grid-template-columns: 14vw 70vw 16vw;
    min-height: 100vh;
  }

  .grid-container > div {
    text-align: center;
    padding: 0rem;
    margin: 0rem;
    font-size: 3rem;
  }
</style>
