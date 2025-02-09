<script setup lang="ts">
    import { ref , watch } from 'vue'
    import { selection } from '../js/selection'
    import { Dots, isDotMasked } from '../js/Dots'
    import { Boxes } from '../js/Boxes'
    import { path } from '../js/path'
    import MyClick from './icons/MyClickIcon.vue'
    import MyBox from './icons/MyBoxIcon.vue'
    import MyUpLoad from './icons/MyUpLoadIcon.vue'
    import MyGallary from './icons/MyGallaryIcon.vue'


    let timer: number | null = null
    let appear = ref(0)         // 0: none, 1: click, 2: box

    let AddClass = ref('selected-btn')
    let AddTextClass = ref('selected-btn-text')
    let RemoveClass = ref('prohibit-btn')
    let RemoveTextClass = ref('prohibit-btn-text')
    let ResetClass = ref('disabled')
    let UndoClass = ref('disabled')
    let RedoClass = ref('disabled')

    const fileInput = ref<HTMLInputElement | null>(null);

    const selectFile = () => {
        if (fileInput.value) {
            fileInput.value.click();
        }
    };

    const readFile = (event: Event) => {
        const target = event.target as HTMLInputElement;
        const file = target.files?.[0];
        if (file && (file.type === 'image/jpeg' || file.type === 'image/jpg')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                if (e.target?.result) { // 使用可选链
                   path.value = e.target.result as string; // 获取文件的 URL
                }
        };
        reader.readAsDataURL(file); // 读取为 Data URL
      } else {
        alert('请选择一个 JPG 文件！');
      }
    }

    function ChangeOver(isOvered: boolean, value: string) {
        if (!isOvered) {
            if (value === 'click') {
                appear.value = 1
            }
            else if (value === 'box') {
                appear.value = 2
            }
        }
        else {
            appear.value = 0
        }
    }

    function MouseOverBTN(value: string) {
        if (timer != null) {
            clearTimeout(timer)
        }

        timer = setTimeout(() => {
            if (value === 'click' && selection.value != 1) {
                ChangeOver(false,'click')
            }
            else if (value === 'box' && selection.value != 2) {
                ChangeOver(false,'box')
            }
        },1000) as any
    }

    function MouseOutBTN(value: string) {
        if (timer != null) {
            clearTimeout(timer)
        }
        if (value === 'click' && selection.value != 1) {
            ChangeOver(true,'click')
        }
        else if (value === 'box' && selection.value != 2) {
            ChangeOver(true,'box')
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
        if (selection.value === 1) {
            Dots.operation.value = 4;
        }
        else if (selection.value === 2) {
            Boxes.operation.value = 4;
        }
    }

    function Undo() {
        if (selection.value === 1) {
            Dots.operation.value = 1;
        }
        else if (selection.value === 2) {
            Boxes.operation.value = 1;
        }
    }

    function Redo() {
        if (selection.value === 1) {
            Dots.operation.value = 3;
        }
        else if (selection.value === 2) {
            Boxes.operation.value = 3;
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
        }
        else if (newValue === false && oldValue === true) {
            AddClass.value = 'selected-btn'
            AddTextClass.value = 'selected-btn-text'
            RemoveClass.value = 'prohibit-btn'
            RemoveTextClass.value = 'prohibit-btn-text'
            ResetClass.value = 'disabled'
            UndoClass.value = 'disabled'
        }
    })

    watch(Dots.isDotted_redo, (newValue, oldValue) => {
        if (newValue === true && oldValue === false) {
            RedoClass.value = 'abled'
        }
        else if (newValue === false && oldValue === true) {
            RedoClass.value = 'disabled'
        }
    })

    watch(Boxes.isBoxed, (newValue, oldValue) => {
        if (newValue === true && oldValue === false) {
            ResetClass.value = 'abled'
            UndoClass.value = 'abled'
        }
        else if (newValue === false && oldValue === true) {
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
    <ul class="myTools">Tools
        <hr style="FILTER: progid:DXImageTransform.Microsoft.Glow(color=#D3D3D3,strength=10)" width="90%" color=#D3D3D3 SIZE=2 />
        <li style="text-align: left;" class="normal-btn"><input type="file" ref="fileInput" @change="readFile" accept=".jpg,.jpeg" style="display: none;" />
            <button @click = "selectFile" class="upload-btn">&nbsp;&nbsp;<MyUpLoad></MyUpLoad>Upload</button>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<button class="gallary-btn"><MyGallary></MyGallary>Gallary</button>
        </li>
        <li @mouseover="MouseOverBTN('click')" @mouseout="MouseOutBTN('click')" @click="MouseClickBTN('click')" 
                :class="selection === 1 ? 'selected-tool' : 'unselected-tool'" id="click">
            <div style="text-align: left">&nbsp;<MyClick></MyClick>&nbsp;&nbsp;Hover & Click</div>
            <p v-show="appear === 1 || selection === 1">Click an object one or more times. Shift-chick to remove regions.</p>
        </li>
        <li @mouseover="MouseOverBTN('box')" @mouseout="MouseOutBTN('box')" @click="MouseClickBTN('box')" 
                :class="selection === 2 ? 'selected-tool' : 'unselected-tool'" id="box">
            <div style="text-align: left">&nbsp;<MyBox></MyBox>&nbsp;&nbsp;Box</div>
            <p v-show="appear === 2 || selection === 2">Rough draw a box around an object.</p>
        </li>
        <li class="mask-btns-container">
            <div>
                <div class="mask-btns">
                    <div @click="ChangeMaskBtn('Add')">
                        <p :class="AddClass">+</p>
                        <p :class="AddTextClass">Add Mask</p>
                    </div>
                    <div @click="ChangeMaskBtn('Remove')">
                        <p :class="RemoveClass">-</p>
                        <p :class="RemoveTextClass">Remove Area</p>
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
    }

    .myTools .normal-btn {
        background-color: #FFFFFF;
        color: #000000;
        font: bold 1.4rem Arial, sans-serif;
        border-radius: 1.5rem;
        border: 0.2rem solid #D3D3D3;
        padding: 0.5rem 1rem;
        width: 85%;
        margin: 1rem;
        justify-content: left;
        vertical-align: top;     
    }

    .myTools .upload-btn {
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
        color: #2962D9;
        font: bold 1.8rem Arial, sans-serif;
        border-radius: 1.5rem;
        border: 0.2rem solid #2962D9;
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

    li p {
        font: 1.2rem Arial, sans-serif;
        color: #BEBEBE;
        margin-top: 0.5rem;
        word-break: keep-all;
    }

    .selected-tool p {    
        color: #2962D9;
    }
    
    li .mask-btns {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: center;
    }

    .mask-btns div {
        display: flex;
        flex-direction: column;
        justify-content: start;
        align-items: center;
    }

    .mask-btns .selected-btn {
        color: #FFFFFF;
        font: bold 2.5rem Arial, sans-serif;
        background-color: #2962D9;
        border-radius: 0.5rem;
        padding: 0%;
        margin: 0%;
        width: 3rem;
        height: 3rem;
        cursor: pointer;
    }

    .mask-btns .selected-btn-text {
        color: #2962D9;
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
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        background-color: #E8E8E8;
        border: 0.1rem solid #E8E8E8;
        border-radius: 1rem;
        height: 3rem;
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