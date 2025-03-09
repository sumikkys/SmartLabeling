// Masks.ts
import {ref} from 'vue'
import { Dots } from './Dots'
import { MaskItem } from './Types'

export const isWindowChange = ref(false)
export const tempMaskMatrix = ref<Array<Array<number>>>([])

export class Masks {
    private mask_list = ref<Array<MaskItem>>([]);

    addMask(maskId: string, maskName: string) {
        const currentList = this.mask_list.value ?? [];
        const newList = [...currentList];
        newList.push({
            mask_matrix: tempMaskMatrix.value,
            mask_id: maskId,
            mask_name: maskName
        });
        this.mask_list.value = newList;
        Dots.operation.value = 2;
    }

    getMaskList() {
        return [...this.mask_list.value];
    }

    getMaskMatrixfromMaskList(index_id: number) {
        return this.mask_list.value[index_id]?.mask_matrix;
    }

    getMaskIdfromMaskList(index_id: number) {
        return this.mask_list.value[index_id]?.mask_id;
    }

    getMaskNameList() {
        return this.mask_list.value?.map(tempmask => tempmask.mask_name);
    }

    removeMaskfromMaskList(index_id: number) {
        const currentList = this.mask_list.value ?? [];
        const newList = [...currentList];
        newList.splice(index_id, 1);
        this.mask_list.value = newList;
    }
}