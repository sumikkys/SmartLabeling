from schemas.prompt_schema import PromptRequest, PromptResponse

data_store = {
    "foreground": [],
    "background": [],
    "boxes": [],
    "history": []
}

def process_prompt(request: PromptRequest, decoder, img_embeddings, img_file) -> PromptResponse:
    # 记录操作
    data_store["history"].append(request)
    
    if request.operation == 0:  # add
        
        if request.type == 0:  # foreground
            data_store["foreground"].extend(request.position)
            decoder.point(img_embeddings, img_file, point_coords=request.position, point_labels=[1])

        elif request.type == 1:  # background   
            data_store["background"].extend(request.position)
            decoder.point(img_embeddings, img_file, point_coords=request.position, point_labels=[0])

        elif request.type == 2:  # box
            data_store["boxes"].append(request.position)
            decoder.bBox(img_embeddings, img_file, boxes=request.position)
        
        result = "Added successfully"

    elif request.operation == 1:  # undo
        if not data_store["history"]:
            return PromptResponse(status="error", message="No operation to undo", data=None)
        last_operation = data_store["history"].pop()  # 移除最后一个操作
        # 根据类型执行相应的撤销逻辑
        if last_operation.type == 0:  # foreground
            data_store["foreground"].pop()
        elif last_operation.type == 1:  # background
            data_store["background"].pop()
        elif last_operation.type == 2:  # box
            data_store["boxes"].pop()
        
        result = "Undo operation completed"

    elif request.operation == 2:  # reset
        data_store["foreground"].clear()
        data_store["background"].clear()
        data_store["boxes"].clear()
        data_store["history"].clear()  # 清空历史
        result = "All operations cleared"

    elif request.operation == 3:  # redo
        if len(data_store["history"]) == 0:
            return PromptResponse(status="error", message="No operation to redo", data=None)
        last_operation = data_store["history"][-1]  # 获取最后一个操作
        # 再次执行最后一个操作
        if last_operation.operation == 0:  # 如果是添加操作
            data_store["history"].append(last_operation)
            if last_operation.type == 0:  # foreground
                data_store["foreground"].extend(last_operation.position)
            elif last_operation.type == 1:  # background
                data_store["background"].extend(last_operation.position)
            elif last_operation.type == 2:  # box
                data_store["boxes"].append(last_operation.position)
            result = "Redo operation completed"

    elif request.operation == 4:  # remove
        if request.type == 0:  # foreground
            if request.position in data_store["foreground"]:
                data_store["foreground"].remove(request.position)
                result = "Foreground point removed"
            else:
                return PromptResponse(status="error", message="Foreground point not found", data=None)
        elif request.type == 1:  # background
            if request.position in data_store["background"]:
                data_store["background"].remove(request.position)
                result = "Background point removed"
            else:
                return PromptResponse(status="error", message="Background point not found", data=None)
        elif request.type == 2:  # box
            if request.position in data_store["boxes"]:
                data_store["boxes"].remove(request.position)
                result = "Box removed"
            else:
                return PromptResponse(status="error", message="Box not found", data=None)

    else:
        return PromptResponse(status="error", message="Invalid operation", data=None)

    return PromptResponse(status="success", message=result, data={
        "foreground": data_store["foreground"],
        "background": data_store["background"],
        "boxes": data_store["boxes"]
    })
