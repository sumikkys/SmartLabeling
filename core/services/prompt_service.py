from schemas.prompt_schema import PromptRequest, PromptResponse

Current_prompt = {
    "foreground": [],
    "background": [],
    "boxes": []
}

Undo_prompt = []

History_prompt = []

def process_prompt(request: PromptRequest, decoder, img_embeddings, img_file) -> PromptResponse:

    History_prompt.append(request)
    
    if request.operation == 0:  # add

        if request.type == 0:  # foreground
            Current_prompt["foreground"].extend(request.position)
            decoder.point(img_embeddings, img_file, point_coords=Current_prompt["foreground"], point_labels=[1])

        elif request.type == 1:  # background   
            Current_prompt["background"].extend(request.position)
            decoder.point(img_embeddings, img_file, point_coords=Current_prompt["background"], point_labels=[0])

        elif request.type == 2:  # box
            Current_prompt["boxes"].extend(request.position)
            decoder.bBox(img_embeddings, img_file, boxes=Current_prompt["boxes"])
        
        result = "Added successfully"

    elif request.operation == 1:  # undo 
        if not History_prompt:
            return PromptResponse(status="error", message="No operation to undo", data=None)
        last_operation = History_prompt.pop()  # 移除最后一个操作
        Undo_prompt.append(last_operation) # 将操作添加到撤销列表
        result = "Undo operation completed"

    elif request.operation == 2:  # reset 无法被redo和undo，待优化
        Current_prompt["foreground"].clear()
        Current_prompt["background"].clear()
        Current_prompt["boxes"].clear()
        Current_prompt["history"].clear()
        History_prompt.clear()
        Undo_prompt.clear()
        result = "All operations cleared"

    elif request.operation == 3:  # redo 需要模型重新计算上一步而非返回上一个mask，待优化
        if len(Current_prompt["history"]) == 0:
            return PromptResponse(status="error", message="No operation to redo", data=None)
        last_operation = Undo_prompt[-1]  # 获取最后一个操作

        # 再次执行最后一个操作
        if last_operation.operation == 0:  # 如果是添加操作
            if last_operation.type == 0:  # foreground
                Current_prompt["foreground"].extend(last_operation.position)
                decoder.point(img_embeddings, img_file, point_coords=Current_prompt["foreground"], point_labels=[1])
            elif last_operation.type == 1:  # background
                Current_prompt["background"].extend(last_operation.position)
                decoder.point(img_embeddings, img_file, point_coords=Current_prompt["foreground"], point_labels=[0])
            elif last_operation.type == 2:  # box
                Current_prompt["boxes"].extend(last_operation.position)
                decoder.bBox(img_embeddings, img_file, boxes=Current_prompt["boxes"])
                
            result = "Redo operation completed"

    elif request.operation == 4:  # remove
        if request.type == 0:  # foreground
            if request.position in Current_prompt["foreground"]:
                Current_prompt["foreground"].remove(request.position)
                result = "Foreground point removed"
            else:
                return PromptResponse(status="error", message="Foreground point not found", data=None)
        elif request.type == 1:  # background
            if request.position in Current_prompt["background"]:
                Current_prompt["background"].remove(request.position)
                result = "Background point removed"
            else:
                return PromptResponse(status="error", message="Background point not found", data=None)
        elif request.type == 2:  # box
            if request.position in Current_prompt["boxes"]:
                Current_prompt["boxes"].remove(request.position)
                result = "Box removed"
            else:
                return PromptResponse(status="error", message="Box not found", data=None)

    else:
        return PromptResponse(status="error", message="Invalid operation", data=None)

    return PromptResponse(status="success", message=result, data={
        "foreground": Current_prompt["foreground"],
        "background": Current_prompt["background"],
        "boxes": Current_prompt["boxes"]
    })
