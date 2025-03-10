<script setup lang="ts">
    import { ref } from 'vue'
</script>

<template>
    <div class="myHeader">
        <div class="headerTitle">SmartLabeling</div>
    </div>
</template>

<style scoped>
    .myHeader {
        height: 100%;
        border: 0.1rem #D3D3D3;
        border-top-style: solid;
        border-right-style: solid;
        border-bottom-style: none;
        border-left-style: solid;
        padding: 0rem;
        margin: 0rem;
        display: flex;
        justify-content: start;
        flex-direction: row;
        align-items: center;
        position: relative;
    }

    .headerTitle {
        color: black;
        font: bold 3rem Arial, sans-serif;
        padding: 1rem;
        margin: 0rem;
        display: flex;
        justify-content: start;
        align-items: center;
        position: relative;
    }
</style>