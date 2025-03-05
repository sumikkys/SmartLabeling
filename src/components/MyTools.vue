<script setup lang="ts">
    import { ref , watch } from 'vue'
    import { selection } from '../ts/selection'
    import { Dots, isDotMasked } from '../ts/Dots'
    import { Boxes } from '../ts/Boxes'
    import { imgPath, projectPath, projectName, Paths } from '../ts/file'
    import { isSwitch, CreateNewProject, sendImageData } from '../ts/telegram'
    import Prompt from '../components/Prompt.vue'
    import MyClick from './icons/MyClickIcon.vue'
    import MyBox from './icons/MyBoxIcon.vue'
    import MyUpLoad from './icons/MyUpLoadIcon.vue'
    import MyGallary from './icons/MyGallaryIcon.vue'

    let AddClass = ref('selected-btn')
    let AddTextClass = ref('selected-btn-text')
    let RemoveClass = ref('prohibit-btn')
    let RemoveTextClass = ref('prohibit-btn-text')
    let ResetClass = ref('disabled')
    let UndoClass = ref('disabled')
    let RedoClass = ref('disabled')

    // 打开文件选择对话框并获取文件的绝对路径
    const filePath = ref<string | null>(null)
    const openFileDialog = async () => {
        try {
            // 调用主进程的文件选择功能
            let paths : Array<string> | undefined = await window.electron.openFileDialog()
            if (paths) {
                isSwitch.value = false
                for (const path of paths) {
                    filePath.value = path
                    if (Paths.list.length === 0) {
                        imgPath.value = path
                    }
                    Paths.addPath(path)
                    await sendImageData(path)
                }
            } else {
                filePath.value = '未选择文件'
            }
        } catch (error) {
            console.error('文件选择失败:', error)
        }
    }

    // 打开输入项目名弹窗
    const promptRef = ref<{ show: () => Promise<string | null> }>()
    const showPrompt = async () => {
        const result = await promptRef.value?.show()
        if (result) {
            console.log('用户输入:', result)
            projectName.value = result
            CreateNewProject()
        } else {
            console.log('用户取消输入')
        }
    }

    // 其实是打开文件夹并选取
    const createDirectory = async() => {
        try {
            // 调用主进程的选取文件夹功能
            const folderPath = await window.electron.createDirectory()
            if (folderPath) {
                console.log("选择成功，文件保存路径为:", folderPath)
                projectPath.value = folderPath // 存储文件夹路径
                showPrompt()
            } else {
                console.log('未选择文件夹路径')
            }
        } catch (error) {
            console.error('保存路径选择失败:', error)
        }
    }

    function MouseClickBTN(value: string) {
        if (value === 'click') {
            selection.value = 1
        }
        else if (value === 'box') {
            selection.value = 2
        }
    }

    function ChangeMaskBtn(value: string) {
        if (selection.value === 1) {
            if (Dots.isDotted.value) {
                if (value === 'Add') {
                    AddClass.value = 'selected-btn'
                    AddTextClass.value = 'selected-btn-text'
                    RemoveClass.value = 'unselected-btn'
                    RemoveTextClass.value = 'unselected-btn-text'
                    isDotMasked.value = true
                }
                else if (value === 'Remove') {
                    AddClass.value = 'unselected-btn'
                    AddTextClass.value = 'unselected-btn-text'
                    RemoveClass.value = 'selected-btn'
                    RemoveTextClass.value = 'selected-btn-text'
                    isDotMasked.value = false
                }
                ResetClass.value = 'abled'
                UndoClass.value = 'abled'
            }
            else if (Boxes.isBoxed.value) {
                if (value === 'Add') {
                    AddClass.value = 'selected-btn'
                    AddTextClass.value = 'selected-btn-text'
                    RemoveClass.value = 'unselected-btn'
                    RemoveTextClass.value = 'unselected-btn-text'
                    isDotMasked.value = true
                }
                else if (value === 'Remove') {
                    AddClass.value = 'unselected-btn'
                    AddTextClass.value = 'unselected-btn-text'
                    RemoveClass.value = 'selected-btn'
                    RemoveTextClass.value = 'selected-btn-text'
                    isDotMasked.value = false
                }
                ResetClass.value = 'abled'
                UndoClass.value = 'abled'
            }
            else {
                AddClass.value = 'selected-btn'
                AddTextClass.value = 'selected-btn-text'
                RemoveClass.value = 'prohibit-btn'
                RemoveTextClass.value = 'prohibit-btn-text'
                ResetClass.value = 'disabled'
                UndoClass.value = 'disabled'
            }
        }
        if (selection.value === 2) {
            AddClass.value = 'selected-btn'
            AddTextClass.value = 'selected-btn-text'
            RemoveClass.value = 'prohibit-btn'
            RemoveTextClass.value = 'prohibit-btn-text'
            if (Boxes.isBoxed.value) {
                ResetClass.value = 'abled'
                UndoClass.value = 'abled'
            }
            else {
                ResetClass.value = 'disabled'
                UndoClass.value = 'disabled'
            }
        }
    }

    function Reset() {
        Dots.operation.value = 2
        Boxes.operation.value = 2
    }

    function Undo() {
        if (Dots.isDotted.value) {
            Dots.operation.value = 1
        }
        else if (!Dots.isDotted.value && Boxes.isBoxed.value) {
            Boxes.operation.value = 1
        }
    }

    function Redo() {
        if (Boxes.isBoxed_redo.value) {
            Boxes.operation.value = 3
        }
        else if (!Boxes.isBoxed_redo.value && Dots.isDotted_redo.value) {
            Dots.operation.value = 3
        }
    }

    watch(selection, (newValue) => {
        if (newValue === 1) {
            ChangeMaskBtn('Add')
        }
        else if (newValue === 2) {
            ChangeMaskBtn('Add')
        }
    })

    watch(Dots.isDotted, (newValue, oldValue) => {
        if (newValue === true && oldValue === false) {
            AddClass.value = 'selected-btn'
            AddTextClass.value = 'selected-btn-text'
            RemoveClass.value = 'unselected-btn'
            RemoveTextClass.value = 'unselected-btn-text'
            ResetClass.value = 'abled'
            UndoClass.value = 'abled'
            if (Boxes.isBoxed_redo.value === true) {
                RedoClass.value = 'disabled'
                Boxes.operation.value = 4
            }
        }
        else if (newValue === false && oldValue === true && Boxes.isBoxed.value === false) {
            AddClass.value = 'selected-btn'
            AddTextClass.value = 'selected-btn-text'
            RemoveClass.value = 'prohibit-btn'
            RemoveTextClass.value = 'prohibit-btn-text'
            ResetClass.value = 'disabled'
            UndoClass.value = 'disabled'
        }
        else if (newValue === false && oldValue === true && Boxes.isBoxed.value === true) {
            AddClass.value = 'selected-btn'
            AddTextClass.value = 'selected-btn-text'
            RemoveClass.value = 'unselected-btn'
            RemoveTextClass.value = 'unselected-btn-text'
            ResetClass.value = 'abled'
            UndoClass.value = 'abled'
        }
    })

    watch(Dots.isDotted_redo, (newValue, oldValue) => {
        if (newValue === true && oldValue === false) {
            RedoClass.value = 'abled'
        }
        else if (newValue === false && oldValue === true && Boxes.isBoxed_redo.value === false) {
            RedoClass.value = 'disabled'
        }
    })

    watch(Boxes.isBoxed, (newValue, oldValue) => {
        if (newValue === true && oldValue === false) {
            ResetClass.value = 'abled'
            UndoClass.value = 'abled'
        }
        else if (newValue === false && oldValue === true) {
            RemoveClass.value = 'prohibit-btn'
            RemoveTextClass.value = 'prohibit-btn-text'
            ResetClass.value = 'disabled'
            UndoClass.value = 'disabled'
        }
    })

    watch(Boxes.isBoxed_redo, (newValue, oldValue) => {
        if (newValue === true && oldValue === false) {
            RedoClass.value = 'abled'
        }
        else if (newValue === false && oldValue === true) {
            RedoClass.value = 'disabled'
        }
    })
</script>

<template>
    <ul class="myTools">
        <li style="text-align: left;" class="normal-btn">
            <button @click="openFileDialog" class="upload-btn"><MyUpLoad></MyUpLoad>&nbsp;&nbsp;Upload</button>
            <button @click="createDirectory" class="gallary-btn"><MyGallary></MyGallary>&nbsp;&nbsp;New</button>
            <Prompt ref="promptRef"/>
        </li>
        <li @click="MouseClickBTN('click')" 
                :class="selection === 1 ? 'selected-tool' : 'unselected-tool'" id="click">
            <div style="text-align: left">&nbsp;<MyClick></MyClick>&nbsp;&nbsp;Click</div>
        </li>
        <li @click="MouseClickBTN('box')" 
                :class="selection === 2 ? 'selected-tool' : 'unselected-tool'" id="box">
            <div style="text-align: left">&nbsp;<MyBox></MyBox>&nbsp;&nbsp;Box</div>
        </li>
        <li class="mask-btns-container">
            <div>
                <div class="mask-btns">
                    <div @click="ChangeMaskBtn('Add')">
                        <p :class="AddClass">+</p>&nbsp;&nbsp;
                        <p :class="AddTextClass">Add</p>
                    </div>
                    <div @click="ChangeMaskBtn('Remove')">
                        <p :class="RemoveClass">-</p>&nbsp;&nbsp;
                        <p :class="RemoveTextClass">Remove</p>
                    </div>
                </div>
                <div class="operation-btns">
                    <button :class="ResetClass" @click="Reset()">Reset</button>
                    <button :class="UndoClass" @click="Undo()">Undo</button>
                    <button :class="RedoClass" @click="Redo()">Redo</button>
                </div>
            </div>
        </li>
    </ul>
</template>

<style scoped>
    .myTools {
        color: #000000;
        font: bold 2.5rem Arial, sans-serif;
        width: 10vw;
        height: 70vh;
        border: 0.2rem solid #D3D3D3;
        border-radius: 0rem 1.5rem 1.5rem 0rem;
        box-shadow: 0rem 0rem 1rem 0.5rem #D3D3D3;
        padding: 1.5rem;
        margin: 1.5rem 0rem;
        display: flex;
        list-style-type: none;
        flex-direction: column;
        justify-content: start;
        align-items: center;
    }

    .myTools .normal-btn {
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.8rem Arial, sans-serif;
        border-radius: 1.5rem;
        border: 0.2rem solid #D3D3D3;
        padding: 0.5rem 1rem;
        width: 85%;
        margin: 1rem;
        justify-content: left;
        vertical-align: top;     
    }

    .normal-btn .upload-btn {
        background: none;
        border: none;
        color: inherit; 
        font: inherit; 
        padding: 0rem 0rem 0.3rem 0rem; 
        cursor: pointer; 
    }

    .myTools .gallary-btn {
        background: none;
        border: none;
        color: inherit; 
        font: inherit; 
        padding: 0rem 0rem 0.3rem 0rem; 
        cursor: pointer; 
    }

    .myTools .unselected-tool {
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.8rem Arial, sans-serif;
        border-radius: 1.5rem;
        border: 0.2rem solid #D3D3D3;
        padding: 0.5rem 1rem;
        width: 85%;
        margin: 1rem;
        cursor: pointer;
    }

    .myTools .selected-tool {
        background-color: #FFFFFF;
        color: #409eff;
        font: bold 1.8rem Arial, sans-serif;
        border-radius: 1.5rem;
        border: 0.2rem solid #409eff;
        padding: 0.5rem 1rem;
        width: 85%;
        margin: 1rem;
        cursor: pointer;
    }

    .myTools .mask-btns-container {
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.8rem Arial, sans-serif;
        border-radius: 1.5rem;
        border: 0.2rem solid #D3D3D3;
        padding: 0.5rem 1rem;
        width: 85%;
        margin: 1rem;
        cursor: pointer;
    }
    
    li .mask-btns {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }

    .mask-btns div {
        display: flex;
        flex-direction: row;
        width: 90%;
        justify-content: start;
        align-items: center;
    }

    .mask-btns .selected-btn {
        color: #FFFFFF;
        font: bold 2.5rem Arial, sans-serif;
        background-color: #409eff;
        border-radius: 0.5rem;
        padding: 0%;
        margin: 0%;
        width: 3rem;
        height: 3rem;
        cursor: pointer;
    }

    .mask-btns .selected-btn-text {
        color: #409eff;
        font: bold 1.5rem Arial, sans-serif;
        word-break: keep-all;
        cursor: pointer;
    }

    .mask-btns .unselected-btn {
        color: #000000;
        font: bold 2.5rem Arial, sans-serif;
        background-color: #FFFFFF;
        border: 0.1rem solid #000000;
        border-radius: 0.5rem;
        padding: 0%;
        margin: 0%;
        width: 3rem;
        height: 3rem;
        cursor: pointer;
    }

    .mask-btns .unselected-btn-text {
        color: #000000;
        font: bold 1.5rem Arial, sans-serif;
        word-break: keep-all;
        cursor: pointer;
    }

    .mask-btns .prohibit-btn {
        color: #D3D3D3;
        font: bold 2.5rem Arial, sans-serif;
        background-color: #FFFFFF;
        border: 0.1rem solid #D3D3D3;
        border-radius: 0.5rem;
        padding: 0%;
        margin: 0%;
        width: 3rem;
        height: 3rem;
        cursor: default;
    }

    .mask-btns .prohibit-btn-text {
        color: #D3D3D3;
        font: bold 1.5rem Arial, sans-serif;
        word-break: keep-all;
        cursor: default;
    }

    li .operation-btns {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        background-color: #E8E8E8;
        border: 0.1rem solid #E8E8E8;
        border-radius: 1rem;
        height: 9rem;
    }

    .operation-btns .abled {
        color: #000000;
        font: bold 1.5rem Arial, sans-serif;
        background-color: #E8E8E8;
        border: none;
        width: 40%;
        height: 3rem;
        margin: 0%;
        border-radius: 1rem;
        cursor: pointer;
    }

    .operation-btns .disabled {
        color: #BEBEBE;
        font: bold 1.5rem Arial, sans-serif;
        background-color: #E8E8E8;
        border: none;
        width: 40%;
        height: 3rem;
        margin: 0%;
        border-radius: 1rem;
        cursor: default;
    }
</style>