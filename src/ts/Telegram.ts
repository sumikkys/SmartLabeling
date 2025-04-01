// Telegram.ts
import { ref } from 'vue'
import axios, { AxiosError } from 'axios'
import { send_dot, isDotMasked } from './Dots'
import { send_box } from './Boxes'
import { AllClassItem } from './Types'
import { imgPath } from './Files'
import { tempMaskMatrix } from './Masks'
import { myAllClassList } from './Classes'
import { projectPath, projectName } from './Projects'

// 判断是否是选择图片或上传图片
export const isSwitch = ref(false)

// 是否初始化加载
export const initialized = ref(false)

// Axios 实例配置
export const api = axios.create({
  baseURL: import.meta.env.PROD
    ? 'http://localhost:8232' // 生产环境直接访问
    : '/api', // 开发环境由Vite代理
  headers: { 'Content-Type': 'application/json' }
})

// 定义 error 变量
const error = ref<string | null>(null)

// 定义增强型错误类型
type EnhancedError = 
  | AxiosError<{ message?: string }>  // 包含响应数据的Axios错误
  | Error                              // 标准错误对象
  | string                             // 字符串类型的错误消息

// 统一错误处理函数
export const handleError = (err: EnhancedError) => {
  // 处理字符串类型错误
  if (typeof err === 'string') {
    error.value = err
    console.error('API Error:', err)
    return
  }

  // 处理Error对象
  if (err instanceof Error) {
    // 类型断言为AxiosError
    const axiosError = err as AxiosError<{ message?: string }>
    
    // 处理带响应的错误
    if (axiosError.response) {
      // 状态码映射
      const statusMessage = (() => {
        switch (axiosError.response.status) {
          case 400: return '请求参数错误'
          case 404: return '资源不存在'
          case 415: return '不支持的媒体类型'
          case 500: return '服务器内部错误'
          default: return `请求失败 (${axiosError.response.status})`
        }
      })()

      error.value = axiosError.response.data?.message || statusMessage
      console.error('API Error:', {
        status: axiosError.response.status,
        message: axiosError.message,
        url: axiosError.config?.url,
        data: axiosError.response.data
      })
    } 
    // 处理无响应的网络错误
    else if (axiosError.request) {
      error.value = '网络连接异常，请检查网络'
      console.error('Network Error:', axiosError.message)
    }
    // 处理其他Error类型
    else {
      error.value = err.message
      console.error('Runtime Error:', err)
    }
  }
}

export const checkBackendReady = () => {
  const interval = setInterval(async() => {
    try {
      const response = await api.get('/status') 
      if(response.data.initialized){
        clearInterval(interval)
        console.log("后端初始化完成！")
        initialized.value = response.data.initialized
      }
    }catch (err: unknown) {
      // 类型安全的错误转换
      if (err instanceof Error) {
        handleError(err)
      } else {
        handleError(String(err))
      }
    }
  }, 1000);  // 每秒检查一次
}

// 发送图片
export const sendImageData = async (path : string) => {
  try {
      const response = await api.post('/uploadimage',{
        "image_path": path,
        "project_name": projectName.value,
        "storage_path": projectPath.value,
      })
      //在这里处理数据
      console.log('upLoadImage 操作结果:', response.data)
  }catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }      
};

// 创建新项目
export const sendCreateNewProject = async () => {
  try {
    const response = await api.post('/create-project', {
      "project_name": projectName.value,
      "storage_path": projectPath.value
    })
    console.log('create-project 操作结果:', response.data)
  } catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 打开项目
export const sendOpenProject = async (): Promise<string> => {
  try {
    const response = await api.post<{ cache_path: string}>('/read-project', {
      "project_path": projectPath.value
    })
    console.log('read-project 操作结果:', response.data)
    return response.data.cache_path
  } catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
    throw err
  }
}

// 切换图片
export const sendSwitchImage = async () => {
  try {
    const response = await api.post('/switch_image', {
      "image_name": imgPath.value.split('\\').pop().split('/').pop(),
      "project_name": projectName.value,
      "project_path": projectPath.value 
    })
    console.log('switch_image 操作结果:', response.data)
  } catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 发送点请求
export const sendPointData = async() => {
  try {
    const response = await api.post('/prompt',{
      "operation": 0,
      "type": isDotMasked.value ? 0 : 1,
      "position": [[Math.floor(send_dot.value.x),Math.floor(send_dot.value.y)]],
      "project_name": projectName.value,
      "storage_path": projectPath.value,
      "image_name": imgPath.value.split('\\').pop().split('/').pop()
    })
    console.log('Prompt 操作结果:', response.data)
    tempMaskMatrix.value = response.data.masks
    if (!response.data.clip_result) return
    myAllClassList.updateClassesProbability(Object.values(response.data.clip_result) as Array<AllClassItem>)
  }  catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 发送撤销点请求
export const sendUndoPointData = async() => {
  try {
    const response = await api.post('/prompt',{
      "operation": 1,
      "type": isDotMasked.value ? 0 : 1,
      "position": [[Math.floor(send_dot.value.x),Math.floor(send_dot.value.y)]],
      "project_name": projectName.value,
      "storage_path": projectPath.value,
      "image_name": imgPath.value.split('\\').pop().split('/').pop()
    })
    console.log('Prompt 操作结果:', response.data)
    tempMaskMatrix.value = response.data.masks
    if (!response.data.clip_result) return
    myAllClassList.updateClassesProbability(Object.values(response.data.clip_result) as Array<AllClassItem>)
  }  catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 发送反撤销点请求
export const sendRedoPointData = async() => {
  try {
    const response = await api.post('/prompt',{
      "operation": 3,
      "type": isDotMasked.value ? 0 : 1,
      "position": [[Math.floor(send_dot.value.x),Math.floor(send_dot.value.y)]],
      "project_name": projectName.value,
      "storage_path": projectPath.value,
      "image_name": imgPath.value.split('\\').pop().split('/').pop()
    })
    console.log('Prompt 操作结果:', response.data)
    tempMaskMatrix.value = response.data.masks
    if (!response.data.clip_result) return
    myAllClassList.updateClassesProbability(Object.values(response.data.clip_result) as Array<AllClassItem>)
  }  catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 发送框
export const sendBoxData = async() => {
  try {
    const response = await api.post('/prompt',{
      "operation": 0,
      "type": 2,
      "position": [Math.floor(send_box.value.start_x),Math.floor(send_box.value.start_y),Math.floor(send_box.value.end_x),Math.floor(send_box.value.end_y)],
      "project_name": projectName.value,
      "storage_path": projectPath.value,
      "image_name": imgPath.value.split('\\').pop().split('/').pop()
    })
    console.log('Prompt 操作结果:', response.data)
    tempMaskMatrix.value = response.data.masks
    if (!response.data.clip_result) return
    myAllClassList.updateClassesProbability(Object.values(response.data.clip_result) as Array<AllClassItem>)
  }  catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 发送撤销框
export const sendUndoBoxData = async() => {
  try {
    const response = await api.post('/prompt',{
      "operation": 1,
      "type": 2,
      "position": [Math.floor(send_box.value.start_x),Math.floor(send_box.value.start_y),Math.floor(send_box.value.end_x),Math.floor(send_box.value.end_y)],
      "project_name": projectName.value,
      "storage_path": projectPath.value,
      "image_name": imgPath.value.split('\\').pop().split('/').pop()
    })
    console.log('Prompt 操作结果:', response.data)
    tempMaskMatrix.value = response.data.masks
    if (!response.data.clip_result) return
    myAllClassList.updateClassesProbability(Object.values(response.data.clip_result) as Array<AllClassItem>)
  }  catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }  
}

// 发送反撤销框
export const sendRedoBoxData = async() => {
  try {
    const response = await api.post('/prompt',{
      "operation": 3,
      "type": 2,
      "position": [Math.floor(send_box.value.start_x),Math.floor(send_box.value.start_y),Math.floor(send_box.value.end_x),Math.floor(send_box.value.end_y)],
      "project_name": projectName.value,
      "storage_path": projectPath.value,
      "image_name": imgPath.value.split('\\').pop().split('/').pop()
    }) 
    console.log('Prompt 操作结果:', response.data)
    tempMaskMatrix.value = response.data.masks
    if (!response.data.clip_result) return
    myAllClassList.updateClassesProbability(Object.values(response.data.clip_result) as Array<AllClassItem>)
  }  catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }  
}

// 发送清空请求
export const sendResetData = async() => {
  try {
    const response = await api.post('/prompt',{
      "operation": 2,
      "type": 0,
      "position": [[0, 0]],
      "project_name": projectName.value,
      "storage_path": projectPath.value,
      "image_name": imgPath.value.split('\\').pop().split('/').pop()
    })
    console.log('Prompt 操作结果:', response.data)
    tempMaskMatrix.value = response.data.masks
    if (!response.data.clip_result) return
    myAllClassList.updateClassesProbability(Object.values(response.data.clip_result) as Array<AllClassItem>)
  }  catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 增加mask
export const sendAddMaskAnnotation = async (classId: string, masks: Array<Array<number>>) : Promise<string> => {
  try {
    const response = await api.post<{ mask_id: string }>('/annotation-tools/prompt', {
      "operation": 0,
      "mask_data": {
        "class_id": classId,
        "masks": masks
      }
    })
    console.log('annotation-tools/prompt 操作结果:', response.data)
    return response.data.mask_id
  } catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
    throw err
  }
}

// 删除mask
export const sendRemoveMaskAnnotation = async (maskId: string) => {
  try {
    const response = await api.post('/annotation-tools/prompt', {
      "operation": 1,
      "mask_id": maskId
    })
    console.log('annotation-tools/prompt 操作结果:', response.data)
  } catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 获取类别
export const sendGetCategoryAnnotation = async () => {
  try {
    const response = await api.post('/annotation-tools/prompt', {
      "operation": 3
    })
    console.log('annotation-tools/prompt 操作结果:', response.data)
  } catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 增加类别
export const sendAddCategoryAnnotation = async (className: string): Promise<string> => {
  try {
    const response = await api.post<{ mask_data: { class_id: string, masks: Array<Array<number>>} }>('/annotation-tools/prompt', {
      "operation": 4,
      "class_name": className
    })
    console.log('annotation-tools/prompt 操作结果:', response.data)
    return response.data.mask_data.class_id
  } catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
    throw err
  }
}

// 导出当前图片Mask
export const sendExportCurrentImage = async (imageId: Array<string>) => {
  try {
    const response = await api.post('/export', {
      "image_id": imageId,
      "project_name": projectName.value,
      "project_path": projectPath.value
    })
    console.log('export 操作结果:', response.data)
  } catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}

// 导出所有图片Mask
export const sendExoprtAllImage = async (imageIdList: Array<string>) => {
  try {
    const response = await api.post('/export', {
      "image_id": imageIdList,
      "project_name": projectName.value,
      "project_path": projectPath.value
    })
    console.log('export 操作结果:', response.data)
  } catch (err: unknown) {
    // 类型安全的错误转换
    if (err instanceof Error) {
      handleError(err)
    } else {
      handleError(String(err))
    }
  }
}