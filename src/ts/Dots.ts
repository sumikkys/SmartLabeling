// // Dots.js
import { ref } from 'vue'
import { DotItem } from './Types'

export const isDotMasked = ref(true)

export const send_dot = ref({ x: 0, y: 0 })

export class Dots {
    static isDotted = ref(false);
    static isDotted_redo = ref(false);
    static dots : Array<DotItem> = [];
    static dots_redo : Array<DotItem> = [];
    static operation = ref(0);  /* 0:add 1:undo 撤销 2:reset 清空当前操作 3:redo 反撤销 4:remove */

    // 测试用可删
    static getDots() {
        console.log('\n');
        this.dots.forEach(element => {
            console.log(element.x, element.y, element.dot_type, 'dot');
        });
        this.dots_redo.forEach(element => {
            console.log(element.x, element.y, element.dot_type, 'dot_redo');
        });
    }

    static addDot(x: number, y: number, dot_type: number) {
        this.dots.push({
            x: x,
            y: y,
            dot_type: dot_type
        });
    }

    static undoDot() {
        let last_dot = this.dots.pop();
        if (last_dot) {
            this.dots_redo.push(last_dot);
        }
        if (this.dots.length == 0) {
            this.isDotted.value = false;
        }
        if (this.dots_redo.length > 0) {
            this.isDotted_redo.value = true;
        }
        return last_dot;
    }

    static redoDot() {
        let last_dot_redo = this.dots_redo.pop();
        if (last_dot_redo) {
            this.dots.push(last_dot_redo);
        }
        if (this.dots_redo.length == 0) {
            this.isDotted_redo.value = false;
        }
        if (this.dots.length > 0) {
            this.isDotted.value = true;
        }
        return last_dot_redo;
    }

    static resetDots() {
        for ( ;this.dots.length > 0; ) {
            this.dots.pop();
        }
        for ( ;this.dots_redo.length > 0; ) {
            this.dots_redo.pop();
        }
        this.isDotted.value = false;
        this.isDotted_redo.value = false;
        isDotMasked.value = true;
    }

    static posIsDotted(x: number, y: number) { 
        for (let element of this.dots) {
            if (Math.sqrt((x - element.x) ** 2 + (y - element.y) ** 2) < 5) {
                return true; 
            }
        }
        return false;
    }
}