<script setup lang="ts">
  import { ref, watch, nextTick } from 'vue'

  const props = defineProps({
    title: { type: String, default: '请输入新建项目名称' },
    placeholder: { type: String, default: '' },
    successText: { type: String, default: '创建成功！' },
    openText: { type: String, default: '打开项目成功！' },
  })

  const isVisible = ref(false)
  const inputValue = ref('')
  const showSuccess = ref(false)
  const showOpen = ref(false)
  let resolvePromise: (value: string | null) => void
  const projectInput = ref<HTMLInputElement | null>(null)

  const show = (isOpen: boolean): Promise<string | null> => {
    isVisible.value = true
    inputValue.value = ''
    showSuccess.value = false
    showOpen.value = isOpen
    return new Promise((resolve) => {
      resolvePromise = resolve
    })
  }

  const handleConfirm = () => {
    if (!showSuccess.value) {
      showSuccess.value = true
    } else {
      isVisible.value = false
      resolvePromise?.(inputValue.value)
      console.log(props)
      resolvePromise = null!
    }
  }

  const handleCancel = () => {
    isVisible.value = false
    resolvePromise?.(null)
    resolvePromise = null!
  }

  defineExpose({ show })

  watch(isVisible, async(newVal) => {
    if (newVal) {
      await nextTick()  // 等待更新
      projectInput.value?.focus()
    }
  })
</script>

<template>
  <div v-if="isVisible" class="prompt-modal">
    <div class="prompt-content">
      <div v-if="showOpen">
        <div>
          <h3 style="color: #67c23a; font-size: 2.5rem;">{{ openText }}</h3>
        </div>
        <div class="button-group">
          <button v-if="!showSuccess" @click="handleCancel">确定</button>
        </div>
      </div>
      <div v-else>
        <div v-if="!showSuccess">
          <h3>{{ title }}</h3>
          <input v-model="inputValue" ref="projectInput" :placeholder="placeholder" @keyup.enter="handleConfirm">
        </div>
        <div v-else>
          <h3 style="color: #67c23a; font-size: 2.5rem;">{{ successText }}</h3>
          <p class="success-message">新创建项目名称：{{ inputValue }}</p>
        </div>
        <div class="button-group">
          <button @click="handleConfirm">
            {{ showSuccess ? '关闭' : '确定' }}
          </button>
          <button v-if="!showSuccess" @click="handleCancel">取消</button>
        </div>
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
    
    input {
        width: 95%;
        padding: 0.8rem;
        margin: 1rem 0rem;
        border: 0.1rem solid #ddd;
        border-radius: 0.4rem;
    }
    
    .success-message {
      margin: 1rem 0rem;
      color: #606266;
    }

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