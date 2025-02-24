import { ref } from 'vue';
import { Masks } from './Masks'

export const imgPath = ref()
export const imgURL = ref()
export const projectPath = ref()
export const projectName = ref()

export class Paths {
    static list = []

    static getPath() {
        this.list.forEach(temppath => {
            console.log(temppath)
        })
    }

    static addPath(path) {
        this.list.push({
            path: path,
            mask: new Masks(),
            class: new Array()
        })
        this.getPath()
    }

    static findPath(id) {
        return this.list.at(id).path
    }

    static addMaskstoPath(path_id, maskId, maskName) {
        return this.list.at(path_id).mask.addMasks(maskId, maskName)
    }

    static addClasstoPath(id, class_name) {
        this.list.at(id).class.push(class_name)
    }

    static getAllPathsfromPaths() {
        const filename_list = new Array()
        for (let i = 0; i < this.list.length; i++) {
            filename_list.push(i)
        }
        return filename_list
    }

    static getMaskfromPath(path_id, index_id) {
        return this.list.at(path_id).mask.getMaskfromMaskList(index_id)
    }

    static getAllClassfromPath(path_id) {
        return this.list.at(path_id).class
    }

    static getAllMaskNamefromPath(path_id) {
        return this.list.at(path_id).mask.getAllMaskName()
    }

    static getMaskIdfromMasks(path_id, index_id) {
        return this.list.at(path_id).mask.getMaskIdfromMaskList(index_id)
    }

    static removeMaskfromMasks(path_id, index_id) {
        this.list.at(path_id).mask.removeMaskfromMaskList(index_id)
    }
}

// export function getDirname() {
//     const filename = projectPath.value.split('\\').pop().split('/').pop()
//     return projectPath.value.slice(0, projectPath.value.length-filename.length-1)
// }