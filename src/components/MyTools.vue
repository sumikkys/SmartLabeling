<script setup lang="ts">
    import { ref , watch } from 'vue'
    import { selection } from '../js/selection'
    import { isDotted } from '../js/isDotted'
    import { isBoxed } from '../js/isBoxed'
    import MyClick from './icons/MyClickIcon.vue'
    import MyBox from './icons/MyBoxIcon.vue'

    let timer: number | null = null
    let appear = ref(0)         // 0: none, 1: click, 2: box

    let clickAddClass = ref('selected-btn')
    let clickAddTextClass = ref('selected-btn-text')
    let clickRemoveClass = ref('prohibit-btn')
    let clickRemoveTextClass = ref('prohibit-btn-text')

    let boxAddClass = ref('selected-btn')
    let boxAddTextClass = ref('selected-btn-text')
    let boxRemoveClass = ref('prohibit-btn')
    let boxRemoveTextClass = ref('prohibit-btn-text')

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
        if (value === 'clickAdd' && isDotted.value === true) {
            clickAddClass.value = 'selected-btn'
            clickAddTextClass.value = 'selected-btn-text'
            clickRemoveClass.value = 'unselected-btn'
            clickRemoveTextClass.value = 'unselected-btn-text'
        }
        else if (value === 'clickRemove' && isDotted.value === true) {
            clickAddClass.value = 'unselected-btn'
            clickAddTextClass.value = 'unselected-btn-text'
            clickRemoveClass.value = 'selected-btn'
            clickRemoveTextClass.value = 'selected-btn-text'
        }
        else if (value === 'boxAdd' && isBoxed.value === true) {
            boxAddClass.value = 'selected-btn'
            boxAddTextClass.value = 'selected-btn-text'
            boxRemoveClass.value = 'unselected-btn'
            boxRemoveTextClass.value = 'unselected-btn-text'
        }
        else if (value === 'boxRemove' && isBoxed.value === true) {
            boxAddClass.value = 'unselected-btn'
            boxAddTextClass.value = 'unselected-btn-text'
            boxRemoveClass.value = 'selected-btn'
            boxRemoveTextClass.value = 'selected-btn-text'
        }
    }

    watch(selection, (newValue) => {
        if (newValue !== 1) {
            isDotted.value = false
        }
    })

    watch(isDotted, (newValue, oldValue) => {
        if (newValue === true && oldValue === false) {
            clickAddClass.value = 'selected-btn'
            clickAddTextClass.value = 'selected-btn-text'
            clickRemoveClass.value = 'unselected-btn'
            clickRemoveTextClass.value = 'unselected-btn-text'
        }
        else if (newValue === false && oldValue === true) {
            clickAddClass.value = 'selected-btn'
            clickAddTextClass.value = 'selected-btn-text'
            clickRemoveClass.value = 'prohibit-btn'
            clickRemoveTextClass.value = 'prohibit-btn-text'
        }
    })

    watch(isBoxed, (newValue, oldValue) => {
        if (newValue === true && oldValue === false) {
            boxAddClass.value = 'selected-btn'
            boxAddTextClass.value = 'selected-btn-text'
            boxRemoveClass.value = 'unselected-btn'
            boxRemoveTextClass.value = 'unselected-btn-text'
        }
        else if (newValue === false && oldValue === true) {
            boxAddClass.value = 'selected-btn'
            boxAddTextClass.value = 'selected-btn-text'
            boxRemoveClass.value = 'prohibit-btn'
            boxRemoveTextClass.value = 'prohibit-btn-text'
        }
    })
</script>

<template>
    <ul class="myTools">Tools
        <hr style="FILTER: progid:DXImageTransform.Microsoft.Glow(color=#D3D3D3,strength=10)" width="90%" color=#D3D3D3 SIZE=2 />
        <li @mouseover="MouseOverBTN('click')" @mouseout="MouseOutBTN('click')" @click="MouseClickBTN('click')" 
                :class="selection === 1 ? 'selected-tool' : 'unselected-tool'" id="click">
            <div style="text-align: left">&nbsp;<MyClick></MyClick>&nbsp;&nbsp;Hover & Click</div>
            <p v-show="appear === 1 || selection === 1">Click an object one or more times. Shift-chick to remove regions.</p>
            <div v-show="selection === 1" class="mask-btns">
                <div @click="ChangeMaskBtn('clickAdd')">
                    <p :class="clickAddClass">+</p>
                    <p :class="clickAddTextClass">Add Mask</p>
                </div>
                <div @click="ChangeMaskBtn('clickRemove')">
                    <p :class="clickRemoveClass">-</p>
                    <p :class="clickRemoveTextClass">Remove Area</p>
                </div>
            </div>
            <div v-show="selection === 1" class="operation-btns">
                <button class="disabled">Reset</button>
                <button class="disabled">Undo</button>
                <button class="disabled">Redo</button>
            </div>
        </li>
        <li @mouseover="MouseOverBTN('box')" @mouseout="MouseOutBTN('box')" @click="MouseClickBTN('box')" 
                :class="selection === 2 ? 'selected-tool' : 'unselected-tool'" id="box">
            <div style="text-align: left">&nbsp;<MyBox></MyBox>&nbsp;&nbsp;Box</div>
            <p v-show="appear === 2 || selection === 2">Rough draw a box around an object.</p>
            <div v-show="selection === 2" class="mask-btns">
                <div @click="ChangeMaskBtn('boxAdd')">
                    <p :class="boxAddClass">+</p>
                    <p :class="boxAddTextClass">Add Mask</p>
                </div>
                <div @click="ChangeMaskBtn('boxRemove')">
                    <p :class="boxRemoveClass">-</p>
                    <p :class="boxRemoveTextClass">Remove Area</p>
                </div>
            </div>
            <div v-show="selection === 2" class="operation-btns">
                <button class="disabled">Reset</button>
                <button class="disabled">Undo</button>
                <button class="disabled">Redo</button>
            </div>
        </li>
    </ul>
</template>

<style scoped>
    .myTools {
        color: #000000;
        font: bold 20px Arial, sans-serif;
        width: 200px;
        height: 500px;
        border: 1px solid #D3D3D3;
        border-radius: 15px;
        box-shadow: 0px 0px 10px 5px #D3D3D3;
        padding: 10px;
        display: flex;
        list-style-type: none;
        flex-direction: column;
        justify-content: start;
        align-items: center;
    }

    .myTools .unselected-tool {
        background-color: #FFFFFF;
        color: #000000;
        font: bold 18px Arial, sans-serif;
        border-radius: 15px;
        border: 2px solid #D3D3D3;
        padding: 5px 10px;
        width: 80%;
        margin: 10px;
        cursor: pointer;
    }

    .myTools .selected-tool {
        background-color: #FFFFFF;
        color: #2962D9;
        font: bold 18px Arial, sans-serif;
        border-radius: 15px;
        border: 2px solid #2962D9;
        padding: 5px 10px;
        width: 80%;
        margin: 10px;
        cursor: pointer;
    }

    li p {
        font: 12px Arial, sans-serif;
        color: #BEBEBE;
        margin-top: 5px;
        word-break: keep-all;
    }

    .selected-tool p {    
        font: 12px Arial, sans-serif;
        color: #2962D9;
        margin-top: 5px;
        word-break: keep-all;
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
        cursor: pointer;
    }

    .mask-btns .selected-btn {
        color: #FFFFFF;
        font: bold 28px Arial, sans-serif;
        background-color: #2962D9;
        border-radius: 5px;
        padding: 0%;
        margin: 0%;
        width: 30px;
        height: 30px;
    }

    .mask-btns .selected-btn-text {
        color: #2962D9;
        font: bold 16px Arial, sans-serif;
        word-break: keep-all;
    }

    .mask-btns .unselected-btn {
        color: #000000;
        font: bold 28px Arial, sans-serif;
        background-color: #FFFFFF;
        border: 1px solid #000000;
        border-radius: 5px; 
        padding: 0%;
        margin: 0%;
        width: 30px;
        height: 30px;
    }

    .mask-btns .unselected-btn-text {
        color: #000000;
        font: bold 16px Arial, sans-serif;
        word-break: keep-all;
    }

    .mask-btns .prohibit-btn {
        color: #D3D3D3;
        font: bold 28px Arial, sans-serif;
        background-color: #FFFFFF;
        border: 1px solid #D3D3D3;
        border-radius: 5px;
        padding: 0%;
        margin: 0%;
        width: 30px;
        height: 30px;
    }

    .mask-btns .prohibit-btn-text {
        color: #D3D3D3;
        font: bold 16px Arial, sans-serif;
        word-break: keep-all;
    }

    .operation-btns {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        background-color: #E8E8E8;
        border: 1px solid #E8E8E8;
        border-radius: 10px;
        height: 30px;
    }

    .operation-btns .disabled {
        color: #BEBEBE;
        font: bold 16px Arial, sans-serif;
        background-color: #E8E8E8;
        border: none;
        width: 30%;
        height: 20px;
        margin: 0%;
        cursor: pointer;
    }

</style>