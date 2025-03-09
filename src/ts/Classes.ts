// Classes.ts
import { ref } from 'vue'
import { ClassItem } from './Types'

export class Classes {
    private class_list = ref<Array<ClassItem>>([]);

    addClass(className: string) {
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
            newList.push({ class_name: className, count: 1 });
        }
        this.class_list.value = newList;
    }

    removeClass(className: string) {
        const currentList = this.class_list.value ?? [];
        const targetIndex = currentList.findIndex(temp => temp.class_name === className);
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

    getClassNameList() {
        const currentList = this.class_list.value ?? [];
        return currentList?.map(tempClass => tempClass.class_name) || [];
    }
}