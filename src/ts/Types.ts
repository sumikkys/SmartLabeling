// Type.ts
import { Masks } from './Masks'
import { Classes } from './Classes'

// 点数据类型
export interface DotItem {
    x: number,
    y: number,
    dot_type: number
}

// 文件数据类型
export interface FileItem {
    path: string,
    mask: Masks, 
    class: Classes
}

// 当前图片Mask数据类型
export interface MaskItem {
    mask_matrix: Array<Array<number>>,
    mask_id: string,
    mask_name: string,
    mask_color: string,
    isVisible: boolean
}

// 当前图片Class数据类型
export interface ClassItem {
    class_name : string,
    class_color: string,
    count : number
}