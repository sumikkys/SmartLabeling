<script setup lang="ts">
  import { ref , watch} from 'vue'
  import { selection } from '../../ts/selection'

  let color = ref('#000000')

  watch(selection, (newVal) => {
    if (newVal === 2) {
      color.value = '#409eff'
    } else {
      color.value = '#000000'
    }
  })
</script>

<template>
    <svg width="18" height="18" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-3 mr-2">
        <path d="M17.7778 0H2.22222C1.63285 0 1.06762 0.234126 0.650874 0.650874C0.234126 1.06762 0 1.63285 0 2.22222V17.7778C0 18.3671 0.234126 18.9324 0.650874 19.3491C1.06762 19.7659 1.63285 20 2.22222 20H17.7778C18.3671 20 18.9324 19.7659 19.3491 19.3491C19.7659 18.9324 20 18.3671 20 17.7778V2.22222C20 1.63285 19.7659 1.06762 19.3491 0.650874C18.9324 0.234126 18.3671 0 17.7778 0ZM17.7778 17.7778H2.22222V2.22222H17.7778V17.7778ZM15.5556 15.5556H4.44444V4.44444H15.5556V15.5556Z" :fill="color"></path>
    </svg>
</template>