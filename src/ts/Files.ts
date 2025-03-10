// Files.ts
import { ref, computed } from 'vue'
import { FileItem } from './Types'
import { Masks } from './Masks'
import { Classes } from './Classes'

export const imgPath = ref()
export const imgURL = ref()

export class Files {
    list = ref<Array<FileItem>>([]);
    list_num  = computed(() => this.list.value.length);

    // 测试用
    getPath() {
        this.list.value.forEach(temppath => {
            console.log(temppath);
        });
    }

    addPathtoPathList(path: string) {
        this.list.value.push({
            path: path,
            mask: new Masks(),
            class: new Classes()
        });
    }

    addMasktoPathList(path_id: number, maskId: string, maskName: string) {
        return this.list.value.at(path_id)?.mask.addMask(maskId, maskName);
    }

    addClasstoPathList(path_id: number, className: string) {
        this.list.value.at(path_id)?.class.addClass(className);
    }

    getPathfromPathList(id: number) {
        return this.list.value.at(id)?.path;
    }

    getAllPathIdsfromPathList() {
        const filename_list = new Array();
        for (let i = 0; i < this.list_num.value; i++) {
            filename_list.push(i);
        }
        return filename_list;
    }

    getMasksfromPathList(path_id: number) {
        return this.list.value.at(path_id)?.mask.getMaskList();
    }

    getMaskMatrixfromPathList(path_id: number, index_id: number) {
        return this.list.value.at(path_id)?.mask.getMaskMatrixfromMaskList(index_id);
    }

    getMaskIdfromPathList(path_id: number, index_id: number) {
        return this.list.value.at(path_id)?.mask.getMaskIdfromMaskList(index_id);
    }

    getAllMaskNamefromPathList(path_id: number) {
        return this.list.value.at(path_id)?.mask.getMaskNameList();
    }

    getAllClassNamefromPathList(path_id: number) {
        return this.list.value.at(path_id)?.class.getClassNameList();
    }

    removeMaskfromPathList(path_id: number, index_id: number) {
        this.list.value.at(path_id)?.mask.removeMaskfromMaskList(index_id);
    }

    removeClassfromPathList(path_id: number, className: string) {
        this.list.value.at(path_id)?.class.removeClass(className);
    }
}

export const myFiles = new Files()