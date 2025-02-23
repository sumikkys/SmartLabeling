<script setup lang="ts">
    import { ref,computed }  from 'vue'
    import axios, { AxiosError } from 'axios'
    import MyLeftImage from './icons/MyLeftImageIcon.vue'
    import MyRightImage from './icons/MyRightImageIcon.vue'
    import MyDownIcon from './icons/MyDownIcon.vue'
    import MyClassIcon from './icons/MyClassIcon.vue'
    import MyAddIcon from './icons/MyAddIcon.vue'
    import MyUpIcon from './icons/MyUpIcon.vue'
    import { imgPath, imgURL, projectPath, projectName } from '../js/file'

    let CurrentImageName = ref('test.png') 
    let showSearchBar = ref(false)
    let showAllClass = ref(false)
    let showSelect = ref(false)
    let CurrentClass = ref('')
    let searchQuery = ref('')
    let searchQueryImage = ref('')

    const api = axios.create({
        headers: {
            'Content-Type': 'application/json'
        }
    })

    const error = ref<string | null>(null)
    // 定义增强型错误类型
    type EnhancedError = 
    | AxiosError<{ message?: string }>  // 包含响应数据的Axios错误
    | Error                              // 标准错误对象
    | string                             // 字符串类型的错误消息

    // 统一错误处理函数
    const handleError = (err: EnhancedError) => {
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


    // 定义数据列表
    const ImageList = ref([
        'test.png',
        'test1.png',
        'test2.png',
        'test3.png',
        'test4.png',
        'test5.png',
        'test6.png',
        'test7.png',
        'test8.png'
    ])
    const MasksList = ref([
        '数据项 1',
        '数据项 2',
        '数据项 3',
        '数据项 4',
        '数据项 5',
        '数据项 6',
        '数据项 7',
        '数据项 8',
        '数据项 9',
        '数据项 10'
    ])
    const AllClass = ref([
        '数据项 0',
        '数据项 1',
        '数据项 2',
        '数据项 3',
        '数据项 4',
        '数据项 5',
        '数据项 6',
        '数据项 7',
        '数据项 8',
        '数据项 9',
        '数据项 10' 
    ])
    const CurrentAllClass = ref([
        '数据项 0',
        '数据项 1',
        '数据项 2',
        '数据项 3',
        '数据项 4',
        '数据项 5',
        '数据项 6',
        '数据项 10' 
    ])
    CurrentClass.value = AllClass.value[0]

    //网络部分
    const sendSwitchImage = async (id:number) => {
        try {
            const response = await api.post('/api/switch_image', {
                "image_id": id,
                "project_name": projectName.value,
                "project_path": projectPath.value 
            })
            //这里切换图片的地址，执行后续逻辑
        } catch (err: unknown) {
            // 类型安全的错误转换
            if (err instanceof Error) {
                handleError(err)
            } else {
                handleError(String(err))
            }
        }
    }

    const ExportCurrentImage = async () => {
        try {
            const response = await api.post('/api/export', {
                "image_id": [ImageList.value.indexOf(CurrentImageName.value)],
                "project_name": "",
                "project_path": ""
            })
            //这里导出当前图片，执行后续逻辑
        } catch (err: unknown) {
            // 类型安全的错误转换
            if (err instanceof Error) {
                handleError(err)
            } else {
                handleError(String(err))
            }
        }
    }

    const ExoprtAllImage = async () => {
        try {
            const response = await api.post('/api/export', {
                "image_id": [],
                "project_name": "",
                "project_path": ""
            })
            //这里导出所有图片，执行后续逻辑
        } catch (err: unknown) {
            // 类型安全的错误转换
            if (err instanceof Error) {
                handleError(err)
            } else {
                handleError(String(err))
            }
        }
    }

    const prevImage =()=> {
        const currentIndex = ImageList.value.indexOf(CurrentImageName.value);
        if (currentIndex > 0) {
            CurrentImageName.value = ImageList.value[currentIndex - 1];
        } else {
            CurrentImageName.value = ImageList.value[ImageList.value.length - 1];
        }
        sendSwitchImage(ImageList.value.indexOf(CurrentImageName.value))
    };
    
    const nextImage = () => {
        const currentIndex = ImageList.value.indexOf(CurrentImageName.value);
        if (currentIndex < ImageList.value.length - 1) {
            CurrentImageName.value = ImageList.value[currentIndex + 1];
        } else {
            CurrentImageName.value = ImageList.value[0];
        }
        sendSwitchImage(ImageList.value.indexOf(CurrentImageName.value))
    };

    const showBar = () => {
        showSearchBar.value = !showSearchBar.value;
    }
    const showClass =()=>{
        showAllClass.value =!showAllClass.value;
    }
    const showSelectBar =()=> {
        showSelect.value = !showSelect.value;
    }
    const selectionOption =(option:string)=> {
        CurrentClass.value = option;
        showSelect.value = !showSelect.value;
    }

    const selectionImage =(option:string)=> {
        CurrentImageName.value = option;
        sendSwitchImage(ImageList.value.indexOf(CurrentImageName.value))
        showSearchBar.value = !showSearchBar.value;
    }

    const AddClassToMask =()=> {
        if(!CurrentAllClass.value.includes(CurrentClass.value)){
            CurrentAllClass.value.push(CurrentClass.value);
        }
        if(!AllClass.value.includes(CurrentClass.value)){
            AllClass.value.push(CurrentClass.value);
        }
        MasksList.value.push('Mask' + MasksList.value.length + CurrentClass.value)
    }

    // 这里是搜索栏功能实现
    const AllClassFilter = computed(() => {
        return AllClass.value.filter((item) => {
            return item.toLowerCase().includes(searchQuery.value.toLowerCase());
        });
    });

    const ImageFilter =computed(()=>{
        return ImageList.value.filter((item) =>{
            return item.toLowerCase().includes((searchQueryImage.value.toLowerCase()));
        })
    });
    </script>

<template>
    <ul class = 'MyAnothertools'>
      <li class ='Image'>
        <div class="ImageLeft">图片选择</div>
        <div>
            <button class="ImageCenter ArrowButton" @click ="prevImage"><MyLeftImage></MyLeftImage></button>
            <button class="ImageRight ArrowButton" @click ="nextImage"><MyRightImage></MyRightImage></button>
        </div>
      </li>
      <li class="Box">
        <div><span class="currentImage">{{ CurrentImageName }}</span>
            <button @click="showBar" class="SearchButton ArrowButton" ><MyRightImage v-if="!showSearchBar"></MyRightImage><MyDownIcon v-else></MyDownIcon></button></div>
            <div v-if="showSearchBar">
                <div class="select-menu-Image">
                    <div>
                    <input class="search-Bar" v-model = "searchQueryImage" type="text" placeholder="搜索你想要标注的Image" />
                </div>
                <button class ="select-element" v-for="(item, index1) in ImageFilter" :key="index1" @click="selectionImage(item)">
                    <span class="ClassElement">{{ item }}</span>
                </button>
                </div>
            </div>
      </li>
      <li class="Masksli">
        <div>已标注Masks</div>
      </li>
      <li class="Box">
        <div class = "scroll-container">
            <div class="data-item" v-for="(item, index) in MasksList" :key="index">{{ item }}</div>
        </div>
      </li>
      <li class="Classli">
        <div v-if="!showAllClass" class="CurrentClassText">当前图片Classes</div><div v-else class="CurrentClassText">数据集Class</div>
        <div><button @click="showClass" class="MyClass"><MyClassIcon></MyClassIcon></button></div>
        <!-- <div v-if="showAddOneClass" class="InputOneClass"><input v-model="AddOneClassName" class="InputContent" type="text"placeholder="添加你想要用来标注的类">
        <button @click="FinishAdd"><MyAddIcon></MyAddIcon></button></div> -->
      </li>
      <li class="Box">
        <div class = "scroll-container">
            <div v-if="!showAllClass" class="data-item" v-for="(item, index) in CurrentAllClass" :key="index">{{ item }}</div>
            <div v-else class="data-item" v-for="(item, index1) in AllClass" :key="index1">{{ item }}</div>
        </div>
      </li>
      <li class="Tipli">
        <div>新建标注</div>
      </li>
      <li class="TipBox">
        <div class="Box1">
            <div>
                <span class="CurrentClass">{{ CurrentClass }}</span>
                <button class="ClassButton ArrowButton" @click="showSelectBar"><MyRightImage v-if="!showSelect"></MyRightImage><MyUpIcon v-else></MyUpIcon></button>
            </div>
            <div v-if="showSelect" >
                <div class="select-menu">
                    <div>
                        <input v-model = "searchQuery" class="select-Bar" type="text" placeholder="搜索你想要标注的Class" />
                    </div>
                    <button class ="select-element" v-for="(item, index1) in AllClassFilter" :key="index1" @click="selectionOption(item)">
                        <span class="ClassElement">{{ item }}</span>
                    </button>
                </div>
            </div>
        </div>
        <button class="AddClass" @click="AddClassToMask"><MyAddIcon></MyAddIcon></button>
      </li>
      <li class="Exportli">
        <div class="Exportlabeldata"><button class="Exportlabeldatabutton" @click="ExportCurrentImage"><span>导出当前图片</span></button></div>
      </li>
      <li class="Exportli">
        <div class="Exportlabeldata"><button class="Exportlabeldatabutton" @click="ExoprtAllImage"><span>导出所有图片</span></button></div>
      </li>
    </ul>
</template>

<style scoped>
    .MyAnothertools {
        color: #000000;
        font: bold 1.5rem Arial, sans-serif;
        width: 15vw;
        height: 70vh;
        border: 0.2rem solid #D3D3D3;
        border-radius: 1.5rem;
        box-shadow: 0rem 0rem 1rem 0.5rem #D3D3D3;
        padding: 1.5rem;
        margin-left: 3rem;
        display: flex;
        list-style-type: none;
        flex-direction: column;
        justify-content: start;
        align-items: center;
        text-align: center;
        position: relative;
    }

    .Image {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

    .ArrowButton {
        background-color: #FFFFFF;
        color: #000000;
        border: none;
    }

    .Image .ImageLeft {
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.5rem Arial, sans-serif;
        align-items: center;
    }
    .Image .ImageCenter {
        cursor: pointer;
    }
    .Image .ImageRight {
        margin-left: 1rem;
        cursor: pointer;
    }

    .Box {
        position: relative;
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.4rem Arial, sans-serif;
        border-radius: 1.1rem;
        border: 0.2rem solid #D3D3D3;
        padding: 0.5rem 1rem;
        width: 90%;
        margin: 1rem;
        display: flex;
        justify-content: flex-start;
    }
    .Box .currentImage{
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.4rem Arial, sans-serif;
    }
    .Box .SearchButton {
        position: absolute;
        right: 1rem;
        cursor: pointer;
    }
    .Box .select-menu-Image {
        position: absolute;
        top:  100%;
        left: 0;
        width: 90%;
        height: 15rem;
        background-color: #FFFFFF;
        border: 0.2rem solid #D3D3D3;
        border-radius: 1.1rem;
        box-shadow: 0rem 0rem 1rem 0.5rem #D3D3D3;
        padding: 0.5rem 1rem;
        z-index: 1;
        transition: all 0.3s ease;
        overflow-y: auto;
        overflow-x: hidden;        
    }
    .Box .select-menu-Image .search-Bar {
        width: 100%;
        height: 100%;
        background-color: #FFFFFF;
        border: none;
        outline: none;
        margin: 1rem;
        padding: 0;
    }
    .Box .select-menu-Image .select-element{
        width: 100%;
        height: 20%;
        border: 0.05rem solid #D3D3D3;
        background-color: #FFFFFF;
        box-shadow: 0 0.2rem 0.4rem rgba(0, 0, 0, 0.1);
        transition: all 0.1s ease;
        cursor: pointer;       
    }
    .Box .select-menu-Image .select-element:active {
        background-color: #F0F0F0;
        box-shadow: 0 0.1rem 0.2rem rgba(0, 0, 0, 0.1);
        transform: translateY(0.1rem);
        border-color: #B0B0B0;
    }
    .Masksli {
        display: flex;
        align-self: flex-start;
        width: 90%;
    }
    .scroll-container {
        width: 30rem;
        height: 10rem;
        /* border: 1px solid #ccc; */
        overflow-y: auto;
    }
    .data-item {
        padding: 1rem;
        border-bottom: 0.1rem solid #eee;
    }
    .Classli {
        position: relative;
        display: flex;
        justify-content: space-between;
        align-self: start;
        width: 100%;
    }      
    .Classli .CurrentClassText {
        margin-right: 2rem;
    }
    .Classli .MyAddIcon {
        height: 30%;
        width: 80%;
        cursor: pointer;
    }
    .Classli .MyClass {
        cursor: pointer;
        background-color: #FFFFFF;
        color: #000000;
        border: none;
    }
    .Classli .InputOneClass {
        position: absolute;
        bottom: 100%;
    }
    .Classli .InputContent {
        width: 23rem;
        height: 2rem;
        border-radius: 1.5rem;
    }
    .Tipli {
        display: flex;
        align-self: start;
        width: 100%;       
    }
    .TipBox {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    .Box1{
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.4rem Arial, sans-serif;
        border-radius: 1.1rem;
        border: 0.2rem solid #D3D3D3;
        padding: 0.5rem 1rem;
        width: 90%;
        margin: 1rem 1rem 1rem 0rem;
        display: flex;
        justify-content: start;
        text-align: center;
        position: relative;
    }
    .CurrentClass {
        font: bold 1.5rem Arial, sans-serif;
    }
    .Box1 .ClassButton {
        position: absolute;
        right: 1rem;
        cursor: pointer;
    }
    .select-menu {
        position: absolute;
        bottom: 100%;
        left: 0;
        width: 90%;
        height: 15rem;
        background-color: #FFFFFF;
        border: 0.2rem solid #D3D3D3;
        border-radius: 1.1rem;
        box-shadow: 0rem 0rem 1rem 0.5rem #D3D3D3;
        padding: 0.5rem 1rem;
        z-index: 1;
        transition: all 0.3s ease;
        overflow-y: auto;
        overflow-x: hidden;
    }
    .select-menu .select-Bar {
        width: 100%;
        height: 100%;
        background-color: #FFFFFF;
        border: none;
        outline: none;
        margin: 1rem;
        padding: 0;
    }
    .select-menu .select-element {
        width: 100%;
        height: 20%;
        border: 0.05rem solid #D3D3D3;
        background-color: #FFFFFF;
        box-shadow: 0 0.2rem 0.4rem rgba(0, 0, 0, 0.1);
        transition: all 0.1s ease;
        cursor: pointer;
    }

    .select-menu .select-element:active {
        background-color: #F0F0F0;
        box-shadow: 0 0.1rem 0.2rem rgba(0, 0, 0, 0.1);
        transform: translateY(0.1rem);
        border-color: #B0B0B0;
    }
    .ClassElement {
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.4rem Arial, sans-serif;
    }
    .AddClass {
        cursor: pointer;
        background-color: #409eff;
        color: #FFFFFF;
        border: none;
        border-radius: 0.5rem;
        height: 2.8rem;
        margin: 1rem 0rem;
    }
    .Exportli {
        display: flex;
        align-self: flex-end;
        width: 100%;
        margin: 0.5rem;
    }
    .Exportlabeldata {
        background-color: #FFFFFF;
        border: none;
        width: 100%;
        height: 100%;
    }
    .Exportlabeldata .Exportlabeldatabutton {
        cursor: pointer;
        color: #000000;
        border: 0.05rem solid #D3D3D3;
        height: 100%;
        width: 100%;
    }
    .Exportlabeldata .Exportlabeldatabutton:active {
        background-color: #409eff;
        color: #000000;
    }
</style>
