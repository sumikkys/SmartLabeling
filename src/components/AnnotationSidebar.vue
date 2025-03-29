<script setup lang="ts">
    import { ref, computed, watch, nextTick }  from 'vue'
    import { imgPath, myFiles, ClassColor } from '../ts/Files'
    import { tempMaskMatrix } from '../ts/Masks'
    import { AllClassList } from '../ts/Classes'
    import { isSwitch } from '../ts/Telegram'
    import { sendAddMaskAnnotation, sendRemoveMaskAnnotation, 
        sendAddCategoryAnnotation, sendExportCurrentImage, sendExoprtAllImage } from '../ts/Telegram'
    import MyLeftImage from './icons/MyLeftImageIcon.vue'
    import MyRightImage from './icons/MyRightImageIcon.vue'
    import MyDownIcon from './icons/MyDownIcon.vue'
    import MyClassIcon from './icons/MyClassIcon.vue'
    import MyUpIcon from './icons/MyUpIcon.vue'
    import MyVisibleIcon from './icons/MyVisibleIcon.vue'
    import MyInvisibleIcon from './icons/MyInvisibleIcon.vue'

    let CurrentImageName = ref('')
    let showSearchBar = ref(false)
    let showAddOneClass = ref(false)
    let showAllClass = ref(false)
    let showSelect = ref(false)
    let CurrentClass = ref('')
    let searchQuery = ref('')
    let searchQueryImage = ref('')
    let AddOneClassName = ref('')
    const classInput = ref<HTMLInputElement | null>(null)

    // 定义数据列表
    const ImageList = computed(() => myFiles.getAllPathNamefromPathList())
    const MaskItems = computed(() => myFiles.getMaskItemsFromPath(ImageList.value.indexOf(CurrentImageName.value)))
    const CurrentClassItems = computed(() => myFiles.getClassItemsFromPath(ImageList.value.indexOf(CurrentImageName.value)))

    // 切换图片
    const SwitchImage = (id : number) => {
        isSwitch.value = true
        imgPath.value = myFiles.getPathfromPathList(id)
    }

    // 切换上一张Image
    const prevImage =()=> {
        const currentIndex = ImageList.value.indexOf(CurrentImageName.value)
        if (currentIndex > 0) {
            CurrentImageName.value = ImageList.value[currentIndex - 1]
        } else {
            CurrentImageName.value = ImageList.value[ImageList.value.length - 1]
        }
        SwitchImage(ImageList.value.indexOf(CurrentImageName.value))
    }
    
    // 切换下一张Image
    const nextImage = () => {
        const currentIndex = ImageList.value.indexOf(CurrentImageName.value)
        if (currentIndex < ImageList.value.length - 1) {
            CurrentImageName.value = ImageList.value[currentIndex + 1]
        } else {
            CurrentImageName.value = ImageList.value[0]
        }
        SwitchImage(ImageList.value.indexOf(CurrentImageName.value))
    }

    // 显示Image选择栏
    const showSelectImageBar = () => {
        showSearchBar.value = !showSearchBar.value
    }

    // 数据集和当前class的切换
    const showClass =()=>{
        showAllClass.value =!showAllClass.value
    }

    // 显示Class选择栏
    const showSelectClassBar =()=> {
        showSelect.value = !showSelect.value
    }

    // 显示Class添加栏
    const AddOneClass =()=>{
        showAddOneClass.value = !showAddOneClass.value
    }

    // 从Classes当中选择Class
    const selectionClass =(option:string)=> {
        CurrentClass.value = option
        showSelect.value = !showSelect.value
        searchQuery.value = ''
    }

    // 从Images当中选择Image
    const selectionImage =(option:string)=> {
        CurrentImageName.value = option
        SwitchImage(ImageList.value.indexOf(CurrentImageName.value))
        showSearchBar.value = !showSearchBar.value
        searchQueryImage.value = ''
    }

    // 确认并添加Class
    const handleConfirm = () => {
        showAddOneClass.value = !showAddOneClass.value
        if(!AllClassList.value.includes(AddOneClassName.value)){
            sendAddCategoryAnnotation(AddOneClassName.value)
            AllClassList.value.push(AddOneClassName.value)
            AddOneClassName.value = ''      // 清除输入框内的文字残留
        }
    }

    // Class搜索栏功能实现
    const AllClassFilter = computed(() => {
        return AllClassList.value.filter((item) => {
            return item.toLowerCase().includes(searchQuery.value.toLowerCase())
        })
    })

    // Image搜索栏功能实现
    const ImageFilter = computed(()=>{
        return ImageList.value.filter((item) =>{
            return item.toLowerCase().includes((searchQueryImage.value.toLowerCase()))
        })
    })

    // 设置已标注Mask的可见性
    const setMaskVisible = (index: number) => {
        myFiles.setMaskVisiblefromPathList(ImageList.value.indexOf(CurrentImageName.value), index)
    }

    // 添加Mask
    const AddMaskAnnotation = async() => {
        const mask_id = await sendAddMaskAnnotation(AllClassList.value.indexOf(CurrentClass.value)+1, tempMaskMatrix.value)
        const maskName = CurrentClass.value+'_'+ mask_id.split('_').pop()
        const index = CurrentClassItems.value.findIndex(tempClass => tempClass.class_name === CurrentClass.value)
        let colorNum = 0
        if (index === -1) {
            colorNum = CurrentClassItems.value.length
        }
        myFiles.addClasstoPathList(ImageList.value.indexOf(CurrentImageName.value), CurrentClass.value, ClassColor[colorNum])
        myFiles.addMasktoPathList(ImageList.value.indexOf(CurrentImageName.value), mask_id, maskName)
    }

    // 删除Mask
    const RemoveMaskAnnotation = async (index: number, item: string) => {
        sendRemoveMaskAnnotation(myFiles.getMaskIdfromPathList(ImageList.value.indexOf(CurrentImageName.value), index)!)
        const className = item.substring(0, item.lastIndexOf('_'))
        myFiles.removeMaskfromPathList(ImageList.value.indexOf(CurrentImageName.value), index)
        myFiles.removeClassfromPathList(ImageList.value.indexOf(CurrentImageName.value), className)
    }

    watch(showAddOneClass, async (newVal) => {
        if (newVal) {
            await nextTick()  // 等待更新
            classInput.value?.focus()
        }
    })

    watch(imgPath, async(newVal) => {
        const imgName = newVal.split('\\').pop().split('/').pop()
        CurrentImageName.value = imgName
        await nextTick()
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
            <button @click="showSelectImageBar" class="SearchButton ArrowButton" ><MyRightImage v-if="!showSearchBar"></MyRightImage><MyDownIcon v-else></MyDownIcon></button>
        </div>
        <div v-if="showSearchBar">
            <div class="select-menu-Image">
                <div>
                    <input class="search-Bar" v-model="searchQueryImage" type="text" placeholder="搜索Image"/>
                    <hr style="FILTER: progid:DXImageTransform.Microsoft.Glow(color=lightgray,strength=10); margin: 0" width="100%" color=lightgray SIZE=1 />
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
            <div class="data-item" v-for="(maskItem, index) in MaskItems" :key="index" style="padding-left: 2rem;">
                <div style="width: 90%; display: flex; justify-content: start; padding: 0rem;">
                    <MyVisibleIcon v-if="maskItem.isVisible" @click="setMaskVisible(index)" style="cursor: pointer;"></MyVisibleIcon>
                    <MyInvisibleIcon v-else @click="setMaskVisible(index)" style="cursor: pointer;"></MyInvisibleIcon>&nbsp;&nbsp;
                    <span style="text-align: center;">{{ maskItem.mask_name }}</span>
                </div>
                <button @click="RemoveMaskAnnotation(index, maskItem.mask_name)" class="MyMask">-</button>
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
            <input v-model="AddOneClassName" ref="classInput" class="InputContent" type="text" @keyup.enter="handleConfirm" placeholder="请输入Class">
        </div>
      </li>
      <li class="Box">
        <div class = "scroll-container">
            <div v-if="!showAllClass" class="data-item" v-for="(classItem, index) in CurrentClassItems" :key="index" style="padding-left: 2rem;">
                <span class="ClassColor" :style="{ backgroundColor: classItem.class_color }"></span>&nbsp;&nbsp;
                <span>{{ classItem.class_name }}</span>
            </div>
            <div v-else class="data-item" v-for="(item, index1) in AllClassList" :key="index1" style="justify-content: center;">{{ item }}</div>
        </div>
      </li>
      <li class="Tipli">
        <div>新建标注</div>
      </li>
      <li class="TipBox">
        <div class="Box1">
            <span class="CurrentClass">{{ CurrentClass }}</span>
            <button class="ClassButton ArrowButton" @click="showSelectClassBar"><MyRightImage v-if="!showSelect"></MyRightImage><MyUpIcon v-else></MyUpIcon></button>
            <div v-if="showSelect" >
                <div class="select-menu">
                    <div>
                        <input v-model="searchQuery" class="select-Bar" type="text" placeholder="搜索Class" />
                        <hr style="FILTER: progid:DXImageTransform.Microsoft.Glow(color=lightgray,strength=10); margin: 0" width="100%" color=lightgray SIZE=1 />
                    </div>
                    <button class ="select-element" v-for="(item, index1) in AllClassFilter" :key="index1" @click="selectionClass(item)">
                        <span class="ClassElement">{{ item }}</span>
                    </button>
                </div>
            </div>
        </div>
        <button class="AddClass" @click="AddMaskAnnotation">+</button>
      </li>
      <li class="Exportli">
        <button class="Exportlabeldatabutton" @click="sendExportCurrentImage([ImageList.indexOf(CurrentImageName)])">导出当前图片</button>
        <button class="Exportlabeldatabutton" @click="sendExoprtAllImage(myFiles.getAllPathIdfromPathList())">导出所有图片</button>
      </li>
    </ul>
</template>

<style scoped>
    .MyAnothertools {
        height: 100%;
        color: #000000;
        font: bold 1.5rem Arial, sans-serif;
        border: 0.1rem solid #D3D3D3;
        padding: 0rem 1.5rem;
        margin: 0rem;
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
        padding: 0rem;
        margin: 1.5rem 0rem 0rem 0rem;
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
        border-radius: 0.6rem;
        border: 0.1rem solid #D3D3D3;
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
        height: 1rem;
        position: absolute;
        right: 1rem;
        cursor: pointer;
    }
    .Box .select-menu-Image {
        position: absolute;
        top:  100%;
        left: 0;
        width: 100%;
        height: 14rem;
        background-color: #FFFFFF;
        border: 0.1rem solid #D3D3D3;
        border-radius: 0.6rem;
        padding: 0rem;
        z-index: 1;
        transition: all 0.3s ease;
        overflow-y: auto;
        overflow-x: hidden;        
    }
    .Box .select-menu-Image .search-Bar {
        width: 100%;
        height: 100%;
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        border: none;
        outline: none;
        margin: 0.8rem;
        padding: 0rem;
    }
    .Box .select-menu-Image .select-element{
        width: 100%;
        height: 20%;
        border: 0.1rem #D3D3D3;
        border-top-style: none;
        border-right-style: none;
        border-bottom-style: solid;
        border-left-style: none;
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
        padding: 0rem;
        margin: 0rem;
        /* border: 1px solid #ccc; */
        overflow-y: auto;
    }
    .data-item {
        padding: 0.5rem;
        margin: 0rem;
        border-bottom: 0.1rem solid #D3D3D3;
        display: flex;
        justify-content: start;
        vertical-align: baseline;
    }
    .data-item .MyMask {
        width: 2rem;
        height: 2rem;
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.5rem Arial, sans-serif;
        border: 0.1rem solid #000000;
        border-radius: 0.5rem;
        text-align: top;
        cursor: pointer;
    }
    .data-item .ClassColor {
        width: 1.5rem;
        height: 1.5rem;
        border: none;
        border-radius: 0.5rem;
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
        left: 0.5vw;
    }
    .Classli .InputContent {
        width: 12vw;
        height: 2rem;
        border-radius: 0.6rem;
        border: 0.1rem solid #D3D3D3;
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
        border-radius: 0.6rem;
        border: 0.1rem solid #D3D3D3;
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
        height: 1rem;
        position: absolute;
        right: 1rem;
        cursor: pointer;
    }
    .select-menu {
        position: absolute;
        bottom: 100%;
        left: 0;
        width: 100%;
        height: 15rem;
        background-color: #FFFFFF;
        border: 0.1rem solid #D3D3D3;
        border-radius: 0.6rem;
        padding: 0rem;
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
        margin: 0.8rem;
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
        font: bold 1.2rem Arial, sans-serif;
        height: 3rem;
        width: 100%;
    }
    .Exportli .Exportlabeldatabutton:active {
        color: #B0B0B0;
    }
</style>
