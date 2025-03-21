// Type.ts
import { Masks } from './Masks'
import { Classes } from './Classes'

export interface DotItem {
    x: number,
    y: number,
    dot_type: number
}

export interface FileItem {
    path: string,
    mask: Masks, 
    class: Classes
}

export interface MaskItem {
    mask_matrix: Array<Array<number>>,
    mask_id: string,
    mask_name: string,
    mask_color: string,
    isVisible: boolean
}

export interface ClassItem {
    class_name : string,
    class_color: string,
    count : number
}