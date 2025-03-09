<script setup lang="ts">
    import { onMounted, ref, watch } from 'vue'
    import { initialized } from '../ts/Telegram'

    const isVisible = ref(true)
    const isVisibleCanvas = ref(true)

    const myCanvas = ref()
    let canvasAlpha = 10

    // 初始化画布
    function initialCanvas() {
        const canvas = myCanvas.value
        const ctx = canvas.getContext('2d')
        ctx.beginPath()
        ctx.clearRect(0,0,canvas.width,canvas.height)
        ctx.beginPath()
        ctx.fillStyle = '#409eff'
        ctx.globalAlpha = canvasAlpha / 10
        ctx.fillRect(0,0,canvas.width,canvas.height)
    }

    function modifyAlpha() {
        if (canvasAlpha > 0) {
            canvasAlpha--
        }
        initialCanvas()
    }

    onMounted(() => {
        initialCanvas()
    })
    
    watch(initialized, async(newVal)=>{
        if (newVal === true) {
            isVisible.value = false
            const interval = setInterval(async() => {
                modifyAlpha()
                if (canvasAlpha === 0) {
                    clearInterval(interval)
                    isVisibleCanvas.value = false
                }
            }, 50)
        }
    })
</script>

<template>
    <canvas ref="myCanvas" class="canvas" v-if="isVisibleCanvas"></canvas>
    <div id="loader-wrapper" v-if="isVisible">
        <div id="loader"></div>
            <div class="loader-section section-left"></div>
            <div class="loader-section section-right"></div>
            <div class="load_title">正在加载模型,请耐心等待
            <br>
            <span>V0.0.1</span>
        </div>
    </div>
</template>

<style scoped>
    html,body,#app {
        height:100%;
        margin:0px;
        padding:0px;
    }
    
    .chromeframe {
        margin:0.2em 0;
        background:#CCCCCC;
        color:#000000;
        padding:0.2em 0;
    }

    .canvas {
        position:fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        margin: 0;
        border: 1px solid #CCCCCC;
        z-index: 999;
    }
        
    #loader-wrapper {
        position:fixed;
        top:0;
        left:0;
        width:100%;
        height:100%;
        z-index:999999;
    }

    #loader {
        display:block;
        position:relative;
        left:50%;
        top:50%;
        width:150px;
        height:150px;
        margin:-75px 0 0 -75px;
        border-radius:50%;
        border:3px solid transparent;
        border-top-color:#FFFFFF;
        -webkit-animation:spin 2s linear infinite;
        -ms-animation:spin 2s linear infinite;
        -moz-animation:spin 2s linear infinite;
        -o-animation:spin 2s linear infinite;
        animation:spin 2s linear infinite;
        z-index:1001;
    }
    
    #loader:before {
        content:"";
        position:absolute;
        top:5px;
        left:5px;
        right:5px;
        bottom:5px;
        border-radius:50%;
        border:3px solid transparent;
        border-top-color:#FFFFFF;
        -webkit-animation:spin 3s linear infinite;
        -moz-animation:spin 3s linear infinite;
        -o-animation:spin 3s linear infinite;
        -ms-animation:spin 3s linear infinite;
        animation:spin 3s linear infinite;
    }
        
    #loader:after {
        content:"";
        position:absolute;
        top:15px;
        left:15px;
        right:15px;
        bottom:15px;
        border-radius:50%;
        border:3px solid transparent;
        border-top-color:#FFFFFF;
        -moz-animation:spin 1.5s linear infinite;
        -o-animation:spin 1.5s linear infinite;
        -ms-animation:spin 1.5s linear infinite;
        -webkit-animation:spin 1.5s linear infinite;
        animation:spin 1.5s linear infinite;
    }
    
    @-webkit-keyframes spin {
        0% {
            -webkit-transform:rotate(0deg);
            -ms-transform:rotate(0deg);
            transform:rotate(0deg);
        }
        100% {
            -webkit-transform:rotate(360deg);
            -ms-transform:rotate(360deg);
            transform:rotate(360deg);
        }
    }
    
    @keyframes spin { 
        0% {
            -webkit-transform:rotate(0deg);
            -ms-transform:rotate(0deg);
            transform:rotate(0deg);
        } 
        
        100% { 
            -webkit-transform:rotate(360deg);
            -ms-transform:rotate(360deg);
            transform:rotate(360deg);
        }
    } 
    
    #loader-wrapper .loader-section {
        position:fixed;
        top:0;
        width:51%;
        height:100%;
        /* background:#409eff; */
        z-index:1000;
        -webkit-transform:translateX(0);
        -ms-transform:translateX(0);
        transform:translateX(0);
    } 
    
    #loader-wrapper .loader-section.section-left {
        left:0;
    }
    
    #loader-wrapper .loader-section.section-right {
        right:0;
    }
    
    .loaded #loader-wrapper .loader-section.section-left {
        -webkit-transform:translateX(-100%);
        -ms-transform:translateX(-100%);
        transform:translateX(-100%);
        -webkit-transition:all 0.7s 0.3s cubic-bezier(0.645,0.045,0.355,1.000);
        transition:all 0.7s 0.3s cubic-bezier(0.645,0.045,0.355,1.000);
    }
    
    .loaded #loader-wrapper .loader-section.section-right {
        -webkit-transform:translateX(100%);
        -ms-transform:translateX(100%);
        transform:translateX(100%);
        -webkit-transition:all 0.7s 0.3s cubic-bezier(0.645,0.045,0.355,1.000);
        transition:all 0.7s 0.3s cubic-bezier(0.645,0.045,0.355,1.000);
    }
    
    .loaded #loader {
        opacity:0;
        -webkit-transition:all 0.3s ease-out;
        transition:all 0.3s ease-out;
    }
    
    .loaded #loader-wrapper {
        visibility:hidden;
        -webkit-transform:translateY(-100%);
        -ms-transform:translateY(-100%);
        transform:translateY(-100%);
        -webkit-transition:all 0.3s 1s ease-out;transition:all 0.3s 1s ease-out;
    }
    
    .no-js #loader-wrapper {
        display:none;
    } 
    
    .no-js h1 {
        color:#222222;
    } 
    
    #loader-wrapper .load_title{
        font-family:'Open Sans';
        color:#FFF;
        font-size:19px;
        width:100%;
        text-align:center;
        z-index:9999999999999;
        position:absolute;
        top:80%;
        opacity:1;
        line-height:30px;
    }
    
    #loader-wrapper .load_title span {
        font-weight:normal;
        font-style:italic;
        font-size:13px;
        color:#FFF;
        opacity:0.5;
    }
</style>