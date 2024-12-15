from schemas.prompt_schema import PromptRequest, PromptResponse
from initialize_models import decoder
from routers.prompt import img_embeddings, img_file

class OperationManager:
    def __init__(self):
        self.history = []  # ���ڼ�¼��ʷ����
        self.future = []  # ���ڼ�¼δ������
        self.current_state = {
            "foreground": [],
            "background": [],
            "boxes": []
        }  # ���ڴ洢��ǰ״̬

    def add(self, request):
        """��Ӳ���"""
        if request.type == 0:  # foreground
            self.current_state["foreground"].extend(request.position)
            masks, _ = decoder.point(img_embeddings, img_file, point_coords=self.current_state["foreground"], point_labels=[1])
        elif request.type == 1:  # background
            self.current_state["background"].extend(request.position)
            masks, _ = decoder.point(img_embeddings, img_file, point_coords=self.current_state["background"], point_labels=[0])
        elif request.type == 2:  # box
            self.current_state["boxes"].extend(request.position)
            masks, _ = decoder.bBox(img_embeddings, img_file, boxes=self.current_state["boxes"])

        self.history.append(('add', request))
        self.future.clear()  # ���δ������ջ
        return "Added successfully"

    def undo(self):
        """��������"""
        if self.history:
            operation, request = self.history.pop()
            if operation == 'add':
                if request.type == 0:  # foreground
                    for pos in request.position:
                        self.current_state["foreground"].remove(pos)
                elif request.type == 1:  # background
                    for pos in request.position:
                        self.current_state["background"].remove(pos)
                elif request.type == 2:  # box
                    for pos in request.position:
                        self.current_state["boxes"].remove(pos)
            self.future.append(('undo', operation, request))
            return "Undo operation completed"
        return "No operation to undo"

    def redo(self):
        """����������"""
        if self.future:
            operation, request = self.future.pop()
            if operation == 'undo':
                if request.type == 0:  # foreground
                    self.current_state["foreground"].extend(request.position)
                    masks, _ = decoder.point(img_embeddings, img_file, point_coords=self.current_state["foreground"], point_labels=[1])
                elif request.type == 1:  # background
                    self.current_state["background"].extend(request.position)
                    masks, _ = decoder.point(img_embeddings, img_file, point_coords=self.current_state["background"], point_labels=[0])
                elif request.type == 2:  # box
                    self.current_state["boxes"].extend(request.position)
                    masks, _ = decoder.bBox(img_embeddings, img_file, boxes=self.current_state["boxes"])
            self.history.append(('redo', operation, request))
            return "Redo operation completed"
        return "No operation to redo"

    def reset(self):
        """���ò���"""
        self.history.clear()
        self.future.clear()
        self.current_state = {
            "foreground": [],
            "background": [],
            "boxes": []
        }
        return "All operations cleared"

    def remove(self, request):
        """�Ƴ�����"""
        if request.type == 0:  # foreground
            if request.position in self.current_state["foreground"]:
                self.current_state["foreground"].remove(request.position)
                self.history.append(('remove', request))
                self.future.clear()  # ���δ������ջ
                return "Foreground point removed"
            else:
                return "Foreground point not found"
            
        elif request.type == 1:  # background
            if request.position in self.current_state["background"]:
                self.current_state["background"].remove(request.position)
                self.history.append(('remove', request))
                self.future.clear()  # ���δ������ջ
                return "Background point removed"
            else:
                return "Background point not found"
            
        elif request.type == 2:  # box
            if request.position in self.current_state["boxes"]:
                self.current_state["boxes"].remove(request.position)
                self.history.append(('remove', request))
                self.future.clear()  # ���δ������ջ
                return "Box removed"
            else:
                return "Box not found"
            
        return "Invalid type"

    def get_current_state(self):
        """��ȡ��ǰ״̬"""
        return self.current_state

def process_prompt(request: PromptRequest, img_embeddings, img_file) -> PromptResponse:
    manager = OperationManager()

    if request.operation == 0:  # add
        result = manager.add(request, img_embeddings, img_file)

    elif request.operation == 1:  # undo
        result = manager.undo()

    elif request.operation == 2:  # reset
        result = manager.reset()

    elif request.operation == 3:  # redo
        result = manager.redo()

    elif request.operation == 4:  # remove
        result = manager.remove(request)

    else:
        return PromptResponse(status="error", message="Invalid operation", data=None)

    current_state = manager.get_current_state()
    return PromptResponse(
        status="success",
        message=result,
        data={
            "foreground": current_state["foreground"],
            "background": current_state["background"],
            "boxes": current_state["boxes"]
        }
    )