<script setup lang="ts">
  import { ref } from 'vue';
  
  const props = defineProps({
    title: { type: String, default: '请输入项目名称' },
    placeholder: { type: String, default: '' }
  });
  
  const isVisible = ref(false);
  const inputValue = ref('');
  let resolvePromise: (value: string | null) => void;
  
  const show = (): Promise<string | null> => {
    isVisible.value = true;
    inputValue.value = '';
    return new Promise((resolve) => {
      resolvePromise = resolve;
    });
  };
  
  const handleConfirm = () => {
    isVisible.value = false;
    resolvePromise?.(inputValue.value);
    resolvePromise = null!;
  };
  
  const handleCancel = () => {
    isVisible.value = false;
    resolvePromise?.(null);
    resolvePromise = null!;
  };
  
  defineExpose({ show });
</script>

<template>
    <div v-if="isVisible" class="prompt-modal">
        <div class="prompt-content">
            <h3>{{ title }}</h3>
            <input v-model="inputValue" :placeholder="placeholder" @keyup.enter="handleConfirm"/>
            <div class="button-group">
                <button @click="handleConfirm">确定</button>
                <button @click="handleCancel">取消</button>
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
        padding: 20px;
        border-radius: 8px;
        width: 300px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    
    input {
        width: 95%;
        padding: 8px;
        margin: 10px 0;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    .button-group {
        display: flex;
        justify-content: flex-end;
        gap: 8px;
    }
    
    button {
        padding: 6px 12px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        background: #409eff;
        color: white;
    }
    
    button:last-child {
        background: #909399;
    }
</style>