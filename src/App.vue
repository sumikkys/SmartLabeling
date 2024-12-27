<script setup lang="ts">
  import MyHeader from './components/MyHeader.vue' 
  import MyTools from './components/MyTools.vue' 
  import MyContent from './components/MyContent.vue' 
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