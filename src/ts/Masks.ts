import {ref} from 'vue';
import { Dots } from './Dots'

export const isWindowChange = ref(false)
export const tempMaskMatrix = ref<Array<Array<number>>>([])

export class Masks {
    mask_list : Array<{mask_matrix: Array<Array<number>>, mask_id: string, mask_name: string}> = [];

    addMasks(maskId: string, maskName: string) {
        this.mask_list.push({
            mask_matrix: tempMaskMatrix.value,
            mask_id: maskId,
            mask_name: maskName
        });
        Dots.operation.value = 2;
        console.log(tempMaskMatrix)
        this.mask_list.forEach(element => {
            console.log(element.mask_id);
        });
    }

    getMaskList() {
        return this.mask_list;
    }

    getMaskfromMaskList(index_id: number) {
        return this.mask_list.at(index_id)?.mask_matrix;
    }

    getMaskIdfromMaskList(index_id: number) {
        return this.mask_list.at(index_id)?.mask_id;
    }

    getAllMaskName() {
        const maskname_list = new Array();
        this.mask_list.forEach(tempmask => {
            maskname_list.push(tempmask.mask_name)
        });
        return maskname_list;
    }

    removeMaskfromMaskList(index_id: number) {
        this.mask_list.splice(index_id, 1);
    }
}