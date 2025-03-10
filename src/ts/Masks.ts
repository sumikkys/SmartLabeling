// Masks.ts
import {ref} from 'vue'
import { Dots } from './Dots'
import { MaskItem } from './Types'

export const isWindowChange = ref(false)
export const tempMaskMatrix = ref<Array<Array<number>>>([])

export class Masks {
    private mask_list = ref<Array<MaskItem>>([]);

    addMask(maskId: string, maskName: string, maskColor: string) {
        const currentList = this.mask_list.value ?? [];
        const newList = [...currentList];
        newList.push({
            mask_matrix: tempMaskMatrix.value,
            mask_id: maskId,
            mask_name: maskName,
            mask_color: maskColor,
            isVisible: false
        });
        this.mask_list.value = newList;
        Dots.operation.value = 2;
    }

    setMaskVisiblefromMaskList(index_id: number) {
        const currentList = this.mask_list.value ?? [];
        const newList = [...currentList];
        if (index_id !== -1 && index_id < newList.length) {
            newList[index_id] = { 
                ...newList[index_id],
                isVisible: !newList[index_id].isVisible
            };
        } 
        else {
            console.log("没有该图片")
        }
        this.mask_list.value = newList;
    }

    getMaskList(): Array<MaskItem> {
        return this.mask_list.value?.slice() ?? [];
    }

    getMaskMatrixfromMaskList(index_id: number) {
        return this.mask_list.value[index_id]?.mask_matrix;
    }

    getMaskIdfromMaskList(index_id: number) {
        return this.mask_list.value[index_id]?.mask_id;
    }

    // 获取可见的所有mask
    getVisibleMaskList() {
        const currentList = this.mask_list.value ?? [];
        return currentList?.filter((tempMask) => tempMask.isVisible).map(tempMask => tempMask);
    }

    getMaskNameList() {
        const currentList = this.mask_list.value ?? [];
        return currentList?.map(tempMask => tempMask.mask_name) || [];
    }

    // 获取所有mask的可见性
    getMaskVisibleList() {
        const currentList = this.mask_list.value ?? [];
        return currentList?.map(tempMask => tempMask.isVisible) || [];
    }

    removeMaskfromMaskList(index_id: number) {
        const currentList = this.mask_list.value ?? [];
        const newList = [...currentList];
        newList.splice(index_id, 1);
        this.mask_list.value = newList;
    }
}