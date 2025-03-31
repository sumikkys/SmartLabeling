<script setup lang="ts">
  import { ref } from 'vue'

  const props = defineProps({
    title: { type: String, default: '警告' },
    message: { type: String, default: '' }
  })

  const isVisible = ref(false)
  let resolvePromise: (value: void) => void

  const show = (): Promise<void> => {
    isVisible.value = true
    return new Promise((resolve) => {
      resolvePromise = resolve
    })
  }

  const handleConfirm = () => {
    isVisible.value = false
    resolvePromise?.()
    console.log(props)
    resolvePromise = null!
  }

  defineExpose({ show })
</script>

<template>
  <div v-if="isVisible" class="prompt-modal">
    <div class="prompt-content">
      <div>
        <img src="../assets/warning-yellow.svg" style="width: 8rem; height: 8rem; margin-bottom: 1.5rem;" alt="warning" />
        <div>
          <h3 style="color: #FFD700; font-size: 2.5rem; margin: 0.5rem;">{{ title }}</h3>
          <p class="warning-message">{{ message }}</p>
        </div>
      </div>
      <div class="button-group">
        <button @click="handleConfirm">确定</button>
      </div>
    </div>
  </div>
</template>
  
<style scoped>
  .prompt-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }

  .prompt-content {
    background: white;
    padding: 2rem;
    border-radius: 0.8rem;
    width: 30rem;
    box-shadow: 0rem 0.2rem 0.8rem rgba(0, 0, 0, 0.15);
  }

  .warning-message {
    margin: 0rem;
    color: #606266;
    font-size: 1.8rem;
    line-height: 1.5;
  }
  
  /* input {
    width: 95%;
    padding: 0.8rem;
    margin: 1rem 0rem;
    border: 0.1rem solid #ddd;
    border-radius: 0.4rem;
  } */
  
  /* .success-message {
    margin: 1rem 0rem;
    color: #606266;
  } */

  .button-group {
    display: flex;
    justify-content: flex-end;
    gap: 0.8rem;
  }
  
  button {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 0.4rem;
    cursor: pointer;
    background: #409eff;
    color: white;
  }
  
  button:last-child {
    background: #909399;
  }
</style>