// Classes.ts
import { ref } from 'vue'
import { ClassItem, AllClassItem } from './Types'

export class Classes {
    private class_list = ref<Array<ClassItem>>([]);

    addClass(className: string, classColor: string): void {
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

    removeClass(className: string): void {
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

    getClassColorByClassName(className: string): string {
        const currentList = this.class_list.value ?? [];
        const targetIndex = currentList.findIndex(tempClass => tempClass.class_name === className);
        return currentList.at(targetIndex)?.class_color ?? "";
    }
}

export class AllClasses {
    private all_class_list = ref<Array<AllClassItem>>([]);

    // 添加一个Class
    addOneClass(className: string, classId: string, probability?: number): void {
        const currentList = this.all_class_list.value ?? [];
        const newList = [...currentList];
        newList.push({ class_name: className, class_id: classId, probability: probability ?? 0 });
        this.all_class_list.value = newList;
    }

    // 添加多个Class
    addClasses(classIds: Array<string>, classNames: Array<string>): void {
        const currentList = this.all_class_list.value ?? [];
        const newList = [...currentList];
        for (let i = 0; i < Math.min(classIds.length, classNames.length); i++) {
            newList.push({ class_name: classNames[i], class_id: classIds[i], probability: 0 });
        }
        this.all_class_list.value = newList;
    }

    // 更新Class的概率
    updateClassesProbability(classes: Array<AllClassItem>): void {
        const currentList = this.all_class_list.value ?? [];
        const newList = [...currentList];
        classes.forEach(classItem => {
            const targetIndex = newList.findIndex(tempClass => tempClass.class_id === classItem.class_id);
            if (targetIndex === -1) return;
            newList[targetIndex].probability = classItem.probability;
        });
        this.all_class_list.value = newList;
    }

    // 获取所有按class_id排序的Class列表
    getAllClassListBySortId(): Array<AllClassItem> {
        const currentList = this.all_class_list.value ?? [];
        const newList = currentList.slice().sort((a, b) => parseInt(a.class_id) - parseInt(b.class_id));
        return newList ?? [];
    }

    // 获取所有按probability排序的Class列表
    getAllClassListBySortProbability(): Array<AllClassItem> {
        const currentList = this.all_class_list.value ?? [];
        const newList = currentList.slice().sort((a, b) => b.probability - a.probability);
        return newList ?? [];
    }

    // 寻找该Class是否存在
    isExistedClassByClassProperty(classProperty: string, type: string): boolean {
        const currentList = this.all_class_list.value ?? [];
        let targetIndex : number;
        if (type === "Name") targetIndex = currentList.findIndex(tempClass => tempClass.class_name === classProperty);
        else if (type === "Id") targetIndex = currentList.findIndex(tempClass => tempClass.class_id === classProperty);
        else targetIndex = -1;

        if (targetIndex === -1) return false;
        else return true;
    }

    // 寻找该Class的属性
    findClassProperty(classProperty: string, type: string): string {
        const currentList = this.all_class_list.value ?? [];
        let targetIndex : number;
        if (type === "Name") {
            targetIndex = currentList.findIndex(tempClass => tempClass.class_name === classProperty);
            return currentList.at(targetIndex)?.class_id ?? "";
        }
        else if (type === "Id") {
            targetIndex = currentList.findIndex(tempClass => tempClass.class_id === classProperty);
            return currentList.at(targetIndex)?.class_name ?? "";
        }
        else return "";
    }

    // 移除所有Class
    removeAll(): void {
        this.all_class_list.value = [];
    }
}

export const myAllClassList = new AllClasses()