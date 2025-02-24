// isBoxed.js
import { ref } from 'vue'

export class Boxes {
    static isBoxed = ref(false)
    static isBoxed_redo = ref(false)
    static box = {
        start_x: 0,
        start_y: 0,
        end_x: 0,
        end_y: 0
    }
    static box_redo = {
        start_x: 0,
        start_y: 0,
        end_x: 0,
        end_y: 0
    }
    static operation = ref(0)   /* 0:add 1:undo 撤销 2:reset 清空当前操作 3:redo 反撤销 4:remove */

    static getBoxes() {
        console.log('\n')
        console.log(box.start_x, box.start_y, box.end_x, box.end_y)
    }

    static setBox(start_x, start_y, end_x, end_y) {
        this.box = {
            start_x,
            start_y,
            end_x,
            end_y
        }
    }

    static undoBox() {
        this.box_redo = this.box
        this.box = {
            start_x: 0,
            start_y: 0,
            end_x: 0,
            end_y: 0
        }
        this.isBoxed_redo.value = true
        this.isBoxed.value = false
    }

    static redoBox() {
        this.box = this.box_redo
        this.box_redo = {
            start_x: 0,
            start_y: 0,
            end_x: 0,
            end_y: 0
        }
        this.isBoxed.value = true
        this.isBoxed_redo.value = false
    }

    static resetBox() {
        this.box = {
            start_x: 0,
            start_y: 0,
            end_x: 0,
            end_y: 0
        }
        this.box_redo = {
            start_x: 0,
            start_y: 0,
            end_x: 0,
            end_y: 0
        }
        this.isBoxed.value = false
        this.isBoxed_redo.value = false
    }
}