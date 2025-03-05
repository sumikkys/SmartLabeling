<script setup lang="ts">
    import { ref, computed, watch, nextTick }  from 'vue'
    import { api, handleError, isSwitch } from '../ts/telegram'
    import { imgPath, projectPath, projectName, Paths } from '../ts/file'
    import { tempMaskMatrix } from '../ts/Masks'
    import MyLeftImage from './icons/MyLeftImageIcon.vue'
    import MyRightImage from './icons/MyRightImageIcon.vue'
    import MyDownIcon from './icons/MyDownIcon.vue'
    import MyClassIcon from './icons/MyClassIcon.vue'
    import MyUpIcon from './icons/MyUpIcon.vue'

    let CurrentImageName = ref('')
    let showSearchBar = ref(false)
    let showAddOneClass = ref(false)
    let showAllClass = ref(false)
    let showSelect = ref(false)
    let CurrentClass = ref('')
    let searchQuery = ref('')
    let searchQueryImage = ref('')
    let AddOneClassName = ref('')

    // 定义数据列表
    const ImageList = ref<Array<string>>([])
    const MasksList = ref<Array<string>>([])
    const AllClass = ref<Array<string>>([])
    const CurrentAllClass = ref<Array<string>>([])
    CurrentClass.value = AllClass.value[0]

    const SwitchImage = (id : number) => {
        isSwitch.value = true
        imgPath.value = Paths.findPath(id)
        for (; CurrentAllClass.value.length > 0;) {
            CurrentAllClass.value.pop()
        }
        for (; MasksList.value.length > 0;) {
            MasksList.value.pop()
        }
        const tempClassList : Array<string> | undefined = Paths.getAllClassfromPath(ImageList.value.indexOf(CurrentImageName.value))
        const tempMaskNameList : Array<string> | undefined = Paths.getAllMaskNamefromPath(ImageList.value.indexOf(CurrentImageName.value))
        tempClassList?.forEach(tempClass => {
            CurrentAllClass.value.push(tempClass)
        })
        tempMaskNameList?.forEach(tempMaskName => {
            MasksList.value.push(tempMaskName)
        })
    }

    // 增加mask
    const sendAddMaskAnnotation = async () => {
        try {
            const response = await api.post('/api/annotation-tools/prompt', {
                "operation": 0,
                "mask_data": {
                    "class_id": AllClass.value.indexOf(CurrentClass.value),
                    "masks": tempMaskMatrix.value
                }
            })
            console.log(response.data)
            const maskName = CurrentClass.value+"_"+ImageList.value.length
            Paths.addMaskstoPath(ImageList.value.indexOf(CurrentImageName.value), response.data.mask_id, maskName)
            MasksList.value.push(maskName)
        } catch (err: unknown) {
            // 类型安全的错误转换
            if (err instanceof Error) {
                handleError(err)
            } else {
                handleError(String(err))
            }
        }
    }

    // 删除mask
    const sendRemoveMaskAnnotation = async (index : number) => {
        try {
            const response = await api.post('/api/annotation-tools/prompt', {
                "operation": 1,
                "mask_id": Paths.getMaskIdfromMasks(ImageList.value.indexOf(CurrentImageName.value), index)
            })
            console.log(response.data)
            Paths.removeMaskfromMasks(ImageList.value.indexOf(CurrentImageName.value), index)
            MasksList.value.splice(index, 1)
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
    const sendGetCategoryAnnotation = async () => {
        try {
            const response = await api.post('/api/annotation-tools/prompt', {
                "operation": 3
            })
            console.log(response.data)
            AllClass.value.push(AddOneClassName.value);
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
    const sendAddCategoryAnnotation = async (class_name : string) => {
        try {
            const response = await api.post('/api/annotation-tools/prompt', {
                "operation": 4,
                "class_name": class_name
            })
            console.log(response.data)
            sendGetCategoryAnnotation()
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
                "project_name": projectName.value,
                "project_path": projectPath.value
            })
            console.log(response.data)
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
                "image_id": Paths.getAllPathsfromPaths(),
                "project_name": projectName.value,
                "project_path": projectPath.value
            })
            console.log(response.data)
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
        SwitchImage(ImageList.value.indexOf(CurrentImageName.value))
    };
    
    const nextImage = () => {
        const currentIndex = ImageList.value.indexOf(CurrentImageName.value);
        if (currentIndex < ImageList.value.length - 1) {
            CurrentImageName.value = ImageList.value[currentIndex + 1];
        } else {
            CurrentImageName.value = ImageList.value[0];
        }
        SwitchImage(ImageList.value.indexOf(CurrentImageName.value))
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
        SwitchImage(ImageList.value.indexOf(CurrentImageName.value))
        showSearchBar.value = !showSearchBar.value;
    }

    const AddOneClass =()=>{
        showAddOneClass.value = !showAddOneClass.value;
    }

    const handleConfirm = () => {
        showAddOneClass.value = !showAddOneClass.value;
        if(!AllClass.value.includes(AddOneClassName.value)){
            sendAddCategoryAnnotation(AddOneClassName.value)
        }
    };

    const AddClassToMask =()=> {
        if(!CurrentAllClass.value.includes(CurrentClass.value)){
            CurrentAllClass.value.push(CurrentClass.value)
            Paths.addClasstoPath(ImageList.value.indexOf(CurrentImageName.value), CurrentClass.value)
        }
        sendAddMaskAnnotation()
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

    watch(imgPath, async(newVal) => {
        const imgName = newVal.split('\\').pop().split('/').pop()
        CurrentImageName.value = imgName
        await nextTick()
    })

    watch(Paths.list_num, async(newVal) => {
        if (newVal && newVal !== 0) {
            const tempPath = Paths.findPath(newVal - 1)
            if (tempPath){
                const tempPathName = tempPath.split('\\').pop()?.split('/').pop() ?? "unknown"
                ImageList.value.push(tempPathName)
            }
        }
    })
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
        <div>
            <span class="currentImage">{{ CurrentImageName }}</span>
            <span v-if="!CurrentImageName" class="noneImage">none</span>
            <button @click="showBar" class="SearchButton ArrowButton" ><MyRightImage v-if="!showSearchBar"></MyRightImage><MyDownIcon v-else></MyDownIcon></button></div>
            <div v-if="showSearchBar">
                <div class="select-menu-Image">
                    <div>
                    <input class="search-Bar" v-model = "searchQueryImage" type="text" placeholder="搜索Image"/>
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
            <div class="data-item" v-for="(item, index) in MasksList" :key="index">{{ item }}
                <button @click="sendRemoveMaskAnnotation(index)" class="MyClass">-</button>
            </div>
        </div>
      </li>
      <li class="Classli">
        <div v-if="!showAllClass" class="CurrentClassText">当前图片Classes</div>
        <div v-else class="CurrentClassText">数据集Class</div>
        <div>
            <button v-if="showAllClass" @click="AddOneClass" class="MyClass">+</button>
            <button @click="showClass" class="MyClass"><MyClassIcon></MyClassIcon></button>
        </div>
        <div v-if="showAddOneClass" class="InputOneClass">
            <input v-model="AddOneClassName" class="InputContent" type="text" @keyup.enter="handleConfirm" placeholder="">
        </div>
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
                        <input v-model = "searchQuery" class="select-Bar" type="text" placeholder="搜索Class" />
                    </div>
                    <button class ="select-element" v-for="(item, index1) in AllClassFilter" :key="index1" @click="selectionOption(item)">
                        <span class="ClassElement">{{ item }}</span>
                    </button>
                </div>
            </div>
        </div>
        <button class="AddClass" @click="AddClassToMask">+</button>
      </li>
      <li class="Exportli">
        <button class="Exportlabeldatabutton" @click="ExportCurrentImage">导出当前图片</button>
        <button class="Exportlabeldatabutton" @click="ExoprtAllImage">导出所有图片</button>
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
    .Box .noneImage {
        background-color: #FFFFFF;
        color: #D3D3D3;
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
        margin: 0rem;
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
        font: normal 2rem Arial, sans-serif;
        border: none;
        text-align: top;
    }
    .Classli .InputOneClass {
        position: absolute;
        bottom: 100%;
        left: 1vw;
    }
    .Classli .InputContent {
        width: 12vw;
        height: 2rem;
        border-radius: 1rem;
        border: 0.2rem solid #409eff;
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
        font: normal 2rem Arial, sans-serif;
        border: none;
        border-radius: 0.5rem;
        width: 2.8rem;
        height: 2.8rem;
        margin: 1rem 0rem;
    }
    .Exportli {
        display: flex;
        align-self: flex-end;
        justify-content: space-between;
        width: 100%;
        margin: 0.5rem;
    }
    .Exportli .Exportlabeldatabutton {
        background-color: #409eff;
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        color: #FFFFFF;
        font: bold 1.4rem Arial, sans-serif;
        height: 3rem;
        width: 100%;
    }
    .Exportli .Exportlabeldatabutton:active {
        color: #B0B0B0;
    }
</style>
