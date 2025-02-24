import {ref} from 'vue';
import { Dots } from './Dots'

export const tempMaskMatrix = ref([[0]])

export class Masks {
    mask_list = []

    addMasks(maskId, maskName) {
        this.mask_list.push({
            mask_matrix: tempMaskMatrix.value,
            mask_id: maskId,
            mask_name: maskName
        })
        Dots.operation.value = 2
        this.mask_list.forEach(element => {
            console.log(element.mask_id)
        })
    }

    getMaskfromMaskList(index_id) {
        return this.mask_list.at(index_id).mask_matrix
    }

    getMaskIdfromMaskList(index_id) {
        return this.mask_list.at(index_id).mask_id
    }

    getAllMaskName() {
        const maskname_list = new Array()
        this.mask_list.forEach(tempmask => {
            maskname_list.push(tempmask.mask_name)
        })
        return maskname_list
    }

    removeMaskfromMaskList(index_id) {
        this.mask_list.splice(index_id, 1)
    }
}