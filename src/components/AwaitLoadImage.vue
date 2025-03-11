<script setup lang="ts">
    import { onMounted, ref } from 'vue'

    const myCanvasLoading = ref()

    function drawAwaitLoading() {
        const canvasLoading = myCanvasLoading.value
        const ctxLoading= canvasLoading?.getContext('2d')
        ctxLoading.beginPath()
        ctxLoading.globalAlpha = 0.8
        ctxLoading.fillStyle = "#696969"
        ctxLoading.fillRect(0,0,canvasLoading.width,canvasLoading.height)
    }

    onMounted(() => {
        drawAwaitLoading()
    })
</script>

<template>
    <canvas ref="myCanvasLoading" class="loading-canvas"></canvas>
    <div id="loading-mask">
        <div class="loading-wrapper">
            <span class="loading-dot loading-dot-spin"><i></i><i></i><i></i><i></i></span>
        </div>
        <span class="loading-text">正在加载图片</span>
    </div>
</template>

<style>
    .loading-canvas {
        top: 10vh;
        left: 0vw;
        width: 100vw;
        height: 80vh;
        padding: 0rem;
        margin: 0rem;
        position: fixed;
        z-index: 9998;
    }

    #loading-mask { 
        position:relative;
        left:0;
        top:0;
        height:100%;
        width:100%;
        background:none;
        user-select:none;
        padding: 0rem;
        margin: 0rem;
        z-index:9999;
        overflow:hidden
    }

    .loading-wrapper { 
        position:absolute;
        top:55%;
        left:50%;
        transform:translate(-50%,-100%)
    }

    .loading-text {
        position:absolute;
        top:90%;
        left:50%;
        color: #409eff;
        font: bold 2rem Arial, sans-serif;
        word-break: keep-all;
        transform:translate(-50%,-100%)
    }
    
    .loading-dot {
        animation:antRotate 1.2s infinite linear;
        transform:rotate(45deg);
        position:relative;
        display:inline-block;
        font-size:6.4rem;
        width:6.4rem;
        height:6.4rem;
        box-sizing:border-box
    }
    
    .loading-dot i {
        width:2.2rem;
        height:2.2rem;
        position:absolute;
        display:block;
        background-color:#409eff;
        border-radius:100%;
        transform:scale(.75);
        transform-origin:50% 50%;
        opacity:.3;
        animation:antSpinMove 1s infinite linear alternate
    }
    
    .loading-dot i:nth-child(1) {
        top:0;
        left:0
    }
    
    .loading-dot i:nth-child(2) {
        top:0;
        right:0;
        -webkit-animation-delay:.4s;
        animation-delay:.4s
    }
    
    .loading-dot i:nth-child(3) {
        right:0;
        bottom:0;
        -webkit-animation-delay:.8s;
        animation-delay:.8s
    }
    
    .loading-dot i:nth-child(4) {
        bottom:0;
        left:0;
        -webkit-animation-delay:1.2s;
        animation-delay:1.2s
    }
    
    @keyframes antRotate {
        to {
            -webkit-transform:rotate(405deg);
            transform:rotate(405deg)
        }
    }
    
    @-webkit-keyframes antRotate {
        to {
            -webkit-transform:rotate(405deg);
            transform:rotate(405deg)
        }
    }
    
    @keyframes antSpinMove {
        to {
            opacity:1
        }
    }
    
    @-webkit-keyframes antSpinMove {
        to {
            opacity:1
        }
    }
</style>
