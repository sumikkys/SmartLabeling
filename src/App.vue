<script setup lang="ts">
  import { onMounted, onBeforeUnmount } from 'vue';
  import MyHeader from './components/MyHeader.vue'; 
  import MyTools from './components/MyTools.vue'; 
  import MyContent from './components/MyContent.vue'; 

  // 定义防抖函数，避免窗口大小持续变化时频繁触发操作
  const debounce = (func: () => void, delay: number) => {
    let timer: NodeJS.Timeout | null = null;
    return () => {
      if (timer) {
        clearTimeout(timer);
      }
      timer = setTimeout(() => {
        func();
      }, delay);
    };
  };

  // 定义 reload 函数，用于刷新页面
  const reload = () => {
    window.location.reload();
  };

  // 使用防抖函数包装 reload 函数，设置延迟时间为 300 毫秒
  const debouncedReload = debounce(reload, 300);

  // 在组件挂载时添加 resize 事件监听器，监听窗口大小变化
  onMounted(() => {
    window.addEventListener('resize', debouncedReload);
  });

  // 在组件卸载时移除 resize 事件监听器，防止内存泄漏
  onBeforeUnmount(() => {
    window.removeEventListener('resize', debouncedReload);
  });
</script>

<template>
  <div class="grid-container">
    <div class="item1"><MyHeader></MyHeader></div>
    <div class="item2"><MyTools></MyTools></div>
    <div class="item3"><MyContent></MyContent></div>
    <div class="item4"></div>
  </div>
</template>

<style>
:root {
  font-size: 10px;
}

.item1 { 
  grid-area: header; 
}

.item2 { 
  grid-area: menu; 
}

.item3 { 
  grid-area: main; 
}

.item4 { 
  grid-area: footer; 
}

.grid-container {
  display: grid;
  grid:
  'header header header header header header'
  'menu main main main main main'
  'menu footer footer footer footer footer';
  grid-gap: 0;
  background-color: white;
  grid-template-rows: 10vh 80vh 5vh;
  grid-template-columns: repeat(6, 1fr);
  position: absolute;
}

.grid-container > div {
  text-align: center;
  padding: 0;
  font-size: 3rem;
}
</style>
