// Classes.ts
import { ref } from 'vue'
import { ClassItem } from './Types'

export class Classes {
    private class_list = ref<Array<ClassItem>>([]);

    addClass(className: string, classColor: string) {
        const currentList = this.class_list.value ?? [];
        const newList = [...currentList];
        const tempClassIndex = newList.findIndex(tempClass => tempClass.class_name === className);
        if (tempClassIndex !== -1) {
            newList[tempClassIndex] = { 
                ...newList[tempClassIndex], 
                count: newList[tempClassIndex].count + 1 
            };
        } 
        else {
            newList.push({ class_name: className, class_color: classColor, count: 1 });
        }
        this.class_list.value = newList;
    }

    removeClass(className: string) {
        const currentList = this.class_list.value ?? [];
        const targetIndex = currentList.findIndex(tempClass => tempClass.class_name === className);
        if (targetIndex === -1) return;
        const newList = [...currentList];
        const tempClass = newList[targetIndex];
        if (tempClass.count > 1) {
            newList[targetIndex] = { 
                ...tempClass, 
                count: tempClass.count - 1 
            };
        } else {
            newList.splice(targetIndex, 1);
        }
        this.class_list.value = newList;
    }

    getClassList(): Array<ClassItem> {
        return this.class_list.value?.slice() ?? [];
    }

    getClassColorByClassName(className: string) {
        const currentList = this.class_list.value ?? [];
        const targetIndex = currentList.findIndex(tempClass => tempClass.class_name === className);
        return currentList.at(targetIndex)?.class_color;
    }
}

export const AllClassList = ref<Array<string>>([])