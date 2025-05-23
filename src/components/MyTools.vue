<script setup lang="ts">
	import { ref , watch, nextTick } from 'vue'
	import { selection } from '../ts/Selection'
	import { Dots, isDotMasked } from '../ts/Dots'
	import { Boxes } from '../ts/Boxes'
	import { imgPath, isLoading, myFiles, ClassColor } from '../ts/Files'
	import { tempMaskMatrix } from '../ts/Masks'
	import { myAllClassList } from '../ts/Classes'
	import { projectPath, projectName } from '../ts/Projects'
	import { isSwitch, sendCreateNewProject, sendOpenProject, 
		sendImageData, sendSwitchImage, sendExoprtAllImage } from '../ts/Telegram'
	import Prompt from '../components/Prompt.vue'
	import MyClick from './icons/MyClickIcon.vue'
	import MyBox from './icons/MyBoxIcon.vue'
	import MyUpLoad from './icons/MyUpLoadIcon.vue'
	import MyNewProjectIcon from './icons/MyNewProjectIcon.vue'
	import MyOpenProjectIcon from './icons/MyOpenProjectIcon.vue'

	let AddClass = ref('selected-btn')
	let AddTextClass = ref('selected-btn-text')
	let RemoveClass = ref('prohibit-btn')
	let RemoveTextClass = ref('prohibit-btn-text')
	let ResetClass = ref('disabled')
	let UndoClass = ref('disabled')
	let RedoClass = ref('disabled')

	// 打开文件选择对话框并获取文件的绝对路径
	const filePath = ref<string | null>(null)
	const loadFilesDialog = async () => {
		try {
			// 调用主进程的文件选择功能
			let paths : Array<string> | undefined = await (window as any).electron.loadFilesDialog()
			if (paths) {
				isLoading.value = true
				isSwitch.value = false
				for (const path of paths) {
					filePath.value = path
					if (myFiles.list.value.length === 0) {
						imgPath.value = path
					}
					myFiles.addPathtoPathList(path)
					await sendImageData(path)
				}
				await sendSwitchImage()
				await sendExoprtAllImage(myFiles.getAllPathIdfromPathList())
				isLoading.value = false
			} else {
				filePath.value = '未选择文件'
			}
		} catch (error) {
			console.error('文件选择失败:', error)
		}
	}

	// 打开输入项目名弹窗
	const promptRef = ref<{ show: (isOpen: boolean) => Promise<string | null> }>()
	const showPrompt = async (isOpen: boolean) => {
		const result = await promptRef.value?.show(isOpen)
		if (result) {
			console.log('用户输入:', result)
			projectName.value = result
			await sendCreateNewProject()

			// 清空之前项目缓存
			await removeAllData()
		}
		else if (isOpen) {
			const cachePath = await sendOpenProject()
			projectName.value = projectPath.value.split('\\').pop().split('/').pop()
			// 同时处理 Windows 和 Mac/Linux 路径分隔符
			const lastBackslashIndex = projectPath.value.lastIndexOf('\\');
			const lastForwardSlashIndex = projectPath.value.lastIndexOf('/');
			const lastSeparatorIndex = Math.max(lastBackslashIndex, lastForwardSlashIndex);
			// 如果找到了分隔符，则截取到该位置
			if (lastSeparatorIndex !== -1) {
				projectPath.value = projectPath.value.slice(0, lastSeparatorIndex);
			}

			let cacheJsonText = await (window as any).electron.readJSON(cachePath)
			console.log(cacheJsonText)

			// 清空之前项目缓存
			await removeAllData()
			isLoading.value = true
			await nextTick()
			await saveJsonText(cacheJsonText)
			cacheJsonText = null as unknown as Record<string, any> // 手动清除
		}
		else {
			console.log('用户取消输入')
		}
	}

	// 打开文件夹选择对话框并选取项目的路径
	const selectDirectoryDialog = async(isOpen: boolean) => {
		try {
			const dialogTitle = isOpen ? '打开项目' : '选择新项目的保存路径'
			// 调用主进程的选取文件夹功能
			const folderPath = await (window as any).electron.selectDirectoryDialog(dialogTitle)
			if (folderPath) {
				console.log('选择成功，文件保存路径为:', folderPath)
				projectPath.value = folderPath // 存储文件夹路径
				showPrompt(isOpen)
			} else {
				console.log('未选择文件夹路径')
			}
		} catch (error) {
			console.error('保存路径选择失败:', error)
		}
	}

	// 读取json文件内容
	const saveJsonText = async(cacheJsonText: any) => {
		try {
			// 读取所有图片
			for (const path of Object.keys(cacheJsonText.image_id_cache)) {
				myFiles.addPathtoPathList(path)
			}
			// 更改当前图片
			isSwitch.value = false
			await nextTick()
			imgPath.value = myFiles.getPathfromPathList(cacheJsonText.current_image_id)
			// 读取数据集Classes
			myAllClassList.addClasses(Object.keys(cacheJsonText.image_class_cache), Object.values(cacheJsonText.image_class_cache))
			// 读取每张图片Mask内容并同时更新当前图片Classes
			let index = 0
			for (const image_masks of Object.values(cacheJsonText.image_data_cache)) {
				if (Object.keys((image_masks as any).masks).length > 0) {
					for (const mask of Object.values((image_masks as any).masks)) {
						if (Object.keys(mask as any).length === 0) break
						const CurrentClassNameList = myFiles.getClassItemsFromPath(index)
						const maskId = Object.keys(mask as any)[0]
						const currentClassName = myAllClassList.findClassProperty(maskId.substring(0, maskId.lastIndexOf('_')), 'Id')??''
						const maskName = `${currentClassName}_${maskId.split('_').pop()}`
						const maskMatrix = Object.values(mask as any)[0] as Array<Array<number>>
						console.log(currentClassName)
						const colorNum = CurrentClassNameList.find(tempClass => 
							tempClass.class_name === currentClassName
						) ? 0 : CurrentClassNameList.length
						myFiles.addClasstoPathList(index, currentClassName, ClassColor[colorNum])
						myFiles.addMasktoPathList(index, maskId, maskName, maskMatrix)
					}
				}
				index++
			}
		} finally {
			isLoading.value = false
		}
	}

	const removeAllData = async() => {
		Dots.resetDots()
		Boxes.resetBox()
		tempMaskMatrix.value = []
		if (myFiles.getListLength() !== 0) myFiles.removeAll()
		isSwitch.value = false
		await nextTick()
		imgPath.value = ''
		myAllClassList.removeAll()
		await nextTick()
	}

	function MouseClickBTN(value: string) {
		if (value === 'click') {
			selection.value = 1
		}
		else if (value === 'box') {
			selection.value = 2
		}
	}

	function ChangeMaskBtn(value: string) {
		if (selection.value === 1) {
			if (Dots.isDotted.value) {
				if (value === 'Add') {
					AddClass.value = 'selected-btn'
					AddTextClass.value = 'selected-btn-text'
					RemoveClass.value = 'unselected-btn'
					RemoveTextClass.value = 'unselected-btn-text'
					isDotMasked.value = true
				}
				else if (value === 'Remove') {
					AddClass.value = 'unselected-btn'
					AddTextClass.value = 'unselected-btn-text'
					RemoveClass.value = 'selected-btn'
					RemoveTextClass.value = 'selected-btn-text'
					isDotMasked.value = false
				}
				ResetClass.value = 'abled'
				UndoClass.value = 'abled'
			}
			else if (Boxes.isBoxed.value) {
				if (value === 'Add') {
					AddClass.value = 'selected-btn'
					AddTextClass.value = 'selected-btn-text'
					RemoveClass.value = 'unselected-btn'
					RemoveTextClass.value = 'unselected-btn-text'
					isDotMasked.value = true
				}
				else if (value === 'Remove') {
					AddClass.value = 'unselected-btn'
					AddTextClass.value = 'unselected-btn-text'
					RemoveClass.value = 'selected-btn'
					RemoveTextClass.value = 'selected-btn-text'
					isDotMasked.value = false
				}
				ResetClass.value = 'abled'
				UndoClass.value = 'abled'
			}
			else {
				AddClass.value = 'selected-btn'
				AddTextClass.value = 'selected-btn-text'
				RemoveClass.value = 'prohibit-btn'
				RemoveTextClass.value = 'prohibit-btn-text'
				ResetClass.value = 'disabled'
				UndoClass.value = 'disabled'
			}
		}
		if (selection.value === 2) {
			AddClass.value = 'selected-btn'
			AddTextClass.value = 'selected-btn-text'
			RemoveClass.value = 'prohibit-btn'
			RemoveTextClass.value = 'prohibit-btn-text'
			if (Boxes.isBoxed.value) {
				ResetClass.value = 'abled'
				UndoClass.value = 'abled'
			}
			else {
				ResetClass.value = 'disabled'
				UndoClass.value = 'disabled'
			}
		}
	}

	function Reset() {
		Dots.operation.value = 2
		Boxes.operation.value = 2
	}

	function Undo() {
		if (Dots.isDotted.value) {
			Dots.operation.value = 1
		}
		else if (!Dots.isDotted.value && Boxes.isBoxed.value) {
			Boxes.operation.value = 1
		}
	}

	function Redo() {
		if (Boxes.isBoxed_redo.value) {
			Boxes.operation.value = 3
		}
		else if (!Boxes.isBoxed_redo.value && Dots.isDotted_redo.value) {
			Dots.operation.value = 3
		}
	}

	watch(selection, (newValue) => {
		if (newValue === 1) {
			ChangeMaskBtn('Add')
		}
		else if (newValue === 2) {
			ChangeMaskBtn('Add')
		}
	})

	watch(Dots.isDotted, (newValue, oldValue) => {
		if (newValue === true && oldValue === false) {
			AddClass.value = 'selected-btn'
			AddTextClass.value = 'selected-btn-text'
			RemoveClass.value = 'unselected-btn'
			RemoveTextClass.value = 'unselected-btn-text'
			ResetClass.value = 'abled'
			UndoClass.value = 'abled'
			if (Boxes.isBoxed_redo.value === true) {
				RedoClass.value = 'disabled'
				Boxes.operation.value = 4
			}
		}
		else if (newValue === false && oldValue === true && Boxes.isBoxed.value === false) {
			AddClass.value = 'selected-btn'
			AddTextClass.value = 'selected-btn-text'
			RemoveClass.value = 'prohibit-btn'
			RemoveTextClass.value = 'prohibit-btn-text'
			ResetClass.value = 'disabled'
			UndoClass.value = 'disabled'
		}
		else if (newValue === false && oldValue === true && Boxes.isBoxed.value === true) {
			AddClass.value = 'selected-btn'
			AddTextClass.value = 'selected-btn-text'
			RemoveClass.value = 'unselected-btn'
			RemoveTextClass.value = 'unselected-btn-text'
			ResetClass.value = 'abled'
			UndoClass.value = 'abled'
		}
	})

	watch(Dots.isDotted_redo, (newValue, oldValue) => {
		if (newValue === true && oldValue === false) {
			RedoClass.value = 'abled'
		}
		else if (newValue === false && oldValue === true && Boxes.isBoxed_redo.value === false) {
			RedoClass.value = 'disabled'
		}
	})

	watch(Boxes.isBoxed, (newValue, oldValue) => {
		if (newValue === true && oldValue === false) {
			ResetClass.value = 'abled'
			UndoClass.value = 'abled'
		}
		else if (newValue === false && oldValue === true) {
			RemoveClass.value = 'prohibit-btn'
			RemoveTextClass.value = 'prohibit-btn-text'
			ResetClass.value = 'disabled'
			UndoClass.value = 'disabled'
		}
	})

	watch(Boxes.isBoxed_redo, (newValue, oldValue) => {
		if (newValue === true && oldValue === false) {
			RedoClass.value = 'abled'
		}
		else if (newValue === false && oldValue === true) {
			RedoClass.value = 'disabled'
		}
	})
</script>

<template>
	<ul class="myTools">
		<li class="project-list">
			<button @click="selectDirectoryDialog(false)" class="project-btn">
				<MyNewProjectIcon style="width: 2rem;"></MyNewProjectIcon>&nbsp;&nbsp;<span style="width: 4rem;">New</span>
			</button>
			<button @click="selectDirectoryDialog(true)" class="project-btn">
				<MyOpenProjectIcon style="width: 2rem;"></MyOpenProjectIcon>&nbsp;&nbsp;<span style="width: 4rem;">Open</span>
			</button>
			<button @click="loadFilesDialog" class="project-btn">
				<MyUpLoad style="width: 2rem;"></MyUpLoad>&nbsp;&nbsp;<span style="width: 4rem;">Upload</span>
			</button>
			<Prompt ref="promptRef"/>
		</li>
		<li @click="MouseClickBTN('click')" :class="selection === 1 ? 'selected-tool' : 'unselected-tool'" id="click">
			<div class="tool-btn">&nbsp;&nbsp;<MyClick style="width: 2rem;"></MyClick>&nbsp;&nbsp;<span>Point</span></div>
		</li>
		<li @click="MouseClickBTN('box')" :class="selection === 2 ? 'selected-tool' : 'unselected-tool'" id="box">
			<div class="tool-btn">&nbsp;&nbsp;<MyBox style="width: 2rem;"></MyBox>&nbsp;&nbsp;<span>Box</span></div>
		</li>
		<li class="mask-btns-container">
			<div>
				<div class="mask-btns">
					<div @click="ChangeMaskBtn('Add')">
						<p :class="AddClass">+</p>&nbsp;&nbsp;
						<p :class="AddTextClass">Add</p>
					</div>
					<div @click="ChangeMaskBtn('Remove')">
						<p :class="RemoveClass">-</p>&nbsp;&nbsp;
						<p :class="RemoveTextClass">Remove</p>
					</div>
				</div>
				<div class="operation-btns">
					<button :class="ResetClass" @click="Reset()">Reset</button>
					<button :class="UndoClass" @click="Undo()">Undo</button>
					<button :class="RedoClass" @click="Redo()">Redo</button>
				</div>
			</div>
		</li>
	</ul>
</template>

<style scoped>
	.myTools {
		height: 100%;
		color: #000000;
		font: bold 2.5rem Arial, sans-serif;
		border: 0.1rem solid #D3D3D3;
		padding: 0rem 1.5rem;
		margin: 0rem;
		display: flex;
		list-style-type: none;
		flex-direction: column;
		justify-content: start;
		align-items: center;
		position: relative;
	}

	.myTools .project-list {
		background-color: #FFFFFF;
		color: #000000;
		font: bold 1.6rem Arial, sans-serif;
		border-radius: 1rem;
		border: 0.1rem solid #D3D3D3;
		padding: 0.5rem 1rem;
		width: 85%;
		margin: 2.5rem 1rem 1rem 1rem;
		display: flex;
		flex-direction: column;
		justify-content: start;
		align-items: center;
	}

	.project-list .project-btn {
		width: 100%;
		background: none;
		border: none;
		color: inherit; 
		font: inherit;
		display: flex;
		flex-direction: row;
		justify-content: start;
		align-items: center;
		text-align: left;
		vertical-align: baseline;
		cursor: pointer;
	}

	.myTools .unselected-tool {
		background-color: #FFFFFF;
		color: #000000;
		font: bold 1.6rem Arial, sans-serif;
		border-radius: 1rem;
		border: 0.1em solid #D3D3D3;
		padding: 0.5rem 1rem;
		width: 85%;
		margin: 1rem;
		cursor: pointer;
	}

	.myTools .selected-tool {
		background-color: #FFFFFF;
		color: #409eff;
		font: bold 1.6rem Arial, sans-serif;
		border-radius: 1rem;
		border: 0.1rem solid #409eff;
		padding: 0.5rem 1rem;
		width: 85%;
		margin: 1rem;
		cursor: pointer;
	}

	.tool-btn {
		width: 100%;
		display: flex;
		flex-direction: row;
		justify-content: start;
		align-items: center;
		text-align: left;
		vertical-align: baseline;
		cursor: default;
	}

	.myTools .mask-btns-container {
		border-radius: 1rem;
		border: 0.1rem solid #D3D3D3;
		padding: 0.5rem 1rem;
		width: 85%;
		margin: 1rem;
		cursor: default;
	}
	
	li .mask-btns {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: center;
	}

	.mask-btns div {
		display: flex;
		flex-direction: row;
		width: 90%;
		justify-content: start;
		align-items: center;
	}

	.mask-btns .selected-btn {
		color: #FFFFFF;
		font: bold 2.5rem Arial, sans-serif;
		background-color: #409eff;
		border-radius: 0.5rem;
		padding: 0%;
		margin: 0%;
		width: 3rem;
		height: 3rem;
		cursor: pointer;
	}

	.mask-btns .selected-btn-text {
		color: #409eff;
		font: bold 1.5rem Arial, sans-serif;
		word-break: keep-all;
		cursor: pointer;
	}

	.mask-btns .unselected-btn {
		color: #000000;
		font: bold 2.5rem Arial, sans-serif;
		background-color: #FFFFFF;
		border: 0.1rem solid #000000;
		border-radius: 0.5rem;
		padding: 0%;
		margin: 0%;
		width: 3rem;
		height: 3rem;
		cursor: pointer;
	}

	.mask-btns .unselected-btn-text {
		color: #000000;
		font: bold 1.5rem Arial, sans-serif;
		word-break: keep-all;
		cursor: pointer;
	}

	.mask-btns .prohibit-btn {
		color: #D3D3D3;
		font: bold 2.5rem Arial, sans-serif;
		background-color: #FFFFFF;
		border: 0.1rem solid #D3D3D3;
		border-radius: 0.5rem;
		padding: 0%;
		margin: 0%;
		width: 3rem;
		height: 3rem;
		cursor: default;
	}

	.mask-btns .prohibit-btn-text {
		color: #D3D3D3;
		font: bold 1.5rem Arial, sans-serif;
		word-break: keep-all;
		cursor: default;
	}

	li .operation-btns {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: center;
		background-color: #E8E8E8;
		border: 0.1rem solid #E8E8E8;
		border-radius: 1rem;
		height: 9rem;
	}

	.operation-btns .abled {
		color: #000000;
		font: bold 1.5rem Arial, sans-serif;
		background-color: #E8E8E8;
		border: none;
		width: 40%;
		height: 3rem;
		margin: 0%;
		border-radius: 1rem;
		cursor: pointer;
	}

	.operation-btns .disabled {
		color: #BEBEBE;
		font: bold 1.5rem Arial, sans-serif;
		background-color: #E8E8E8;
		border: none;
		width: 40%;
		height: 3rem;
		margin: 0%;
		border-radius: 1rem;
		cursor: default;
	}
</style>