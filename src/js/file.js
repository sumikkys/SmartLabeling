import {ref} from 'vue';

export const imgPath = ref()
export const imgURL = ref()
export const projectPath = ref()
export const projectName = ref()

// export function getDirname() {
//     const filename = projectPath.value.split('\\').pop().split('/').pop()
//     return projectPath.value.slice(0, projectPath.value.length-filename.length-1)
// }