import { ref } from 'vue';
import { Masks } from './Masks'

export const imgPath = ref()
export const imgURL = ref()
export const projectPath = ref()
export const projectName = ref()

export class Paths {
    static list : Array<{path: string, mask: Masks, class: Array<string>}> = [];
    static list_num  = ref(0)

    static getPath() {
        this.list.forEach(temppath => {
            console.log(temppath)
        });
    }

    static addPath(path: string) {
        this.list.push({
            path: path,
            mask: new Masks(),
            class: new Array<string>
        });
        this.list_num.value++;
    }

    static findPath(id: number) {
        return this.list.at(id)?.path;
    }

    static addMaskstoPath(path_id: number, maskId: string, maskName: string) {
        return this.list.at(path_id)?.mask.addMasks(maskId, maskName);
    }

    static addClasstoPath(path_id: number, class_name: string) {
        this.list.at(path_id)?.class.push(class_name);
    }

    static getAllPathsfromPaths() {
        const filename_list = new Array();
        for (let i = 0; i < this.list.length; i++) {
            filename_list.push(i);
        }
        return filename_list;
    }

    static getMaskfromPath(path_id: number, index_id: number) {
        return this.list.at(path_id)?.mask.getMaskfromMaskList(index_id);
    }

    static getAllClassfromPath(path_id: number) {
        return this.list.at(path_id)?.class;
    }

    static getAllMaskNamefromPath(path_id: number) {
        return this.list.at(path_id)?.mask.getAllMaskName();
    }

    static getMaskIdfromMasks(path_id: number, index_id: number) {
        return this.list.at(path_id)?.mask.getMaskIdfromMaskList(index_id);
    }

    static removeMaskfromMasks(path_id: number, index_id: number) {
        this.list.at(path_id)?.mask.removeMaskfromMaskList(index_id);
    }
}

// export function getDirname() {
//     const filename = projectPath.value.split('\\').pop().split('/').pop()
//     return projectPath.value.slice(0, projectPath.value.length-filename.length-1)
// }