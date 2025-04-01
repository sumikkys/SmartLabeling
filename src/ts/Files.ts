// Files.ts
import { ref } from 'vue'
import { FileItem, MaskItem, ClassItem } from './Types'
import { Masks } from './Masks'
import { Classes } from './Classes'

export const imgPath = ref()
export const imgURL = ref()
export const isLoading = ref(false)

export class Files {
    list = ref<Array<FileItem>>([]);

    // 测试用
    getPath() {
        this.list.value.forEach(temppath => {
            console.log(temppath);
        });
    }

    // 添加path
    addPathtoPathList(path: string) {
        this.list.value.push({
            path: path,
            mask: new Masks(),
            class: new Classes()
        });
    }

    // 添加mask
    addMasktoPathList(path_id: number, maskId: string, maskName: string, maskMatrix?: Array<Array<number>>) {
        const className = maskName.substring(0, maskName.lastIndexOf("_"));
        const maskColor = this.list.value.at(path_id)?.class.getClassColorByClassName(className) ?? "";
        if (maskMatrix) {
            return this.list.value.at(path_id)?.mask.addMask(maskId, maskName, maskColor, maskMatrix);
        }
        else {
            return this.list.value.at(path_id)?.mask.addMask(maskId, maskName, maskColor);
        }
    }

    // 添加class
    addClasstoPathList(path_id: number, className: string, classColor: string) {
        this.list.value.at(path_id)?.class.addClass(className, classColor);
    }

    // 设置通过索引获取的某一张图片的mask的可见性
    setMaskVisiblefromPathList(path_id: number, index_id: number) {
        this.list.value.at(path_id)?.mask.setMaskVisiblefromMaskList(index_id)
    }

    // 获取list长度
    getListLength() {
        return this.list.value.length;
    }

    // 根据索引获取图片文件
    getPathfromPathList(id: number) {
        return this.list.value.at(id)?.path;
    }

    // 根据文件名获取图片文件id
    getPathIdfromPathList(path: string) {
        return this.list.value.findIndex(tempFile => tempFile.path === path);
    }

    // 获取所有文件名
    getAllPathNamefromPathList() {
        return this.list.value.map(tempFile => tempFile.path.split('\\').pop()?.split('/').pop() ?? "") ?? [];
    }

    // 获取所有文件id
    getAllPathIdfromPathList(): Array<string> {
        const filename_list = new Array();
        for (let i = 0; i < this.list.value.length; i++) {
            filename_list.push(i.toString());
        }
        return filename_list;
    }

    // 根据索引获取某一张图片的mask数组
    getMaskItemsFromPath(path_id: number) {
        return this.list.value.at(path_id)?.mask.getMaskList()?.slice() ?? [];
    }

    // 根据索引获取某一张图片的某一个mask矩阵
    getMaskMatrixfromPathList(path_id: number, index_id: number) {
        return this.list.value.at(path_id)?.mask.getMaskMatrixfromMaskList(index_id);
    }

    // 根据索引获取某一张图片的某一个maskid
    getMaskIdfromPathList(path_id: number, index_id: number) {
        return this.list.value.at(path_id)?.mask.getMaskIdfromMaskList(index_id);
    }

    // 根据索引获取某一张图片的所有可见的mask
    getVisibleMaskfromPathList(path_id: number): Array<MaskItem> {
        return this.list.value.at(path_id)?.mask.getVisibleMaskList() ?? [];
    }

    // 根据索引获取某一张图片的所有maskname
    getAllMaskNamefromPathList(path_id: number) {
        return this.list.value.at(path_id)?.mask.getMaskNameList()?.slice ?? [];
    }

    // 根据索引获取某一张图片的所有class
    getClassItemsFromPath(path_id: number): Array<ClassItem> {
        return this.list.value.at(path_id)?.class.getClassList()?.slice() ?? [];
    }

    // 清空内存
    removeAll() {
        this.list.value = []
    }

    // 根据索引删除某一张图片的某一个mask
    removeMaskfromPathList(path_id: number, index_id: number) {
        this.list.value.at(path_id)?.mask.removeMaskfromMaskList(index_id);
    }

    // 根据索引搜索一张图片并根据classname删除具体class
    removeClassfromPathList(path_id: number, className: string) {
        this.list.value.at(path_id)?.class.removeClass(className);
    }
}

export const myFiles = new Files()

export const ClassColor = [
    "#FF0000",
    "#FF8000",
    "#FFFF00",
    "#00FF00",
    "#0000FF",
    "#7F00FF",
    "#FF00FF",
    "#FF007F",
    "#808080"
]