// // isDotted.js
import { ref } from 'vue'

export const isDotMasked = ref(true)

export class Dots {
    static isDotted = ref(false);
    static isDotted_redo = ref(false);
    static dots = [];
    static dots_redo = [];
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

    static addDot(x, y, dot_type) {
        this.dots.push({
            x: x,
            y: y,
            dot_type: dot_type
        })
    }

    static addDotMatrix(tempInt2DArr) {
        this.dots_matrix.push(tempInt2DArr)
    }

    static undoDot() {
        let last_dot = this.dots.pop();
        this.dots_redo.push(last_dot);
        if (this.dots.length == 0) {
            this.isDotted.value = false;
        }
        if (this.dots_redo.length > 0) {
            this.isDotted_redo.value = true;
        }
        this.getDots()
        return last_dot;
    }

    static redoDot() {
        let last_dot_redo = this.dots_redo.pop();
        this.dots.push(last_dot_redo);
        if (this.dots_redo.length == 0) {
            this.isDotted_redo.value = false;
        }
        if (this.dots.length > 0) {
            this.isDotted.value = true;
        }
        this.getDots()
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

    static posIsDotted(x, y) { 
        for (let element of this.dots) {
            if (Math.sqrt((x - element.x) ** 2 + (y - element.y) ** 2) < 5) {
                return true; 
            }
        }
        return false;
    }
}