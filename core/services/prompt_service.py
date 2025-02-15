# prmpt_service.py
from initialize_model import decoder
from schemas.prompt_schema import PromptRequest, PromptResponse
from typing import List

def generate_mask(operation, request, current_state, img_embeddings, img_file):
    """Choose whether to generate a mask according to the current operation, and choose the type of function."""
    if decoder is None:
        raise ValueError("Decoder is not initialized")
    masks = None
    masks_2d = List[List[float]] 
    if operation in ['add', 'undo', 'redo', 'remove']:  # These operations need to generate masks
        if request.type == 0:  # foreground
            masks, _ = decoder.point(img_embeddings, img_file, point_coords=current_state["foreground"], point_labels=[1])
        elif request.type == 1:  # background
            masks, _ = decoder.point(img_embeddings, img_file, point_coords=current_state["background"], point_labels=[0])
        elif request.type == 2:  # box
            masks, _ = decoder.bBox(img_embeddings, img_file, boxes=current_state["boxes"])
        masks_list = masks.tolist()
        masks_2d = [sublist for matrix in masks_list for sublist in matrix]
    return masks_2d

class OperationManager:
    def __init__(self):
        self.history = []  # record history operations
        self.future = []  # record future operations
        self.current_state = {
            "foreground": [],
            "background": [],
            "boxes": []
        }  # record current state

    def add(self, request, img_embeddings, img_file):
        """Add operation"""
        if request.type == 0:  # foreground
            self.current_state["foreground"].extend(request.position)
        elif request.type == 1:  # background
            self.current_state["background"].extend(request.position)
        elif request.type == 2:  # box
            self.current_state["boxes"].extend(request.position)

        masks = generate_mask('add', request, self.current_state, img_embeddings, img_file)

        self.history.append(('add', request))
        self.future.clear()
        return "Added successfully", masks

    def undo(self, img_embeddings, img_file):
        """Undo operation"""
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
            self.future.append(('undo',request))

            masks = generate_mask('undo', request, self.current_state, img_embeddings, img_file)

            return "Undo operation completed", masks
        return "No operation to undo", None

    def redo(self, img_embeddings, img_file):
        """Redo operation"""
        if self.future:
            operation, request = self.future.pop()
            if operation == 'undo':
                if request.type == 0:  # foreground
                    self.current_state["foreground"].extend(request.position)
                elif request.type == 1:  # background
                    self.current_state["background"].extend(request.position)
                elif request.type == 2:  # box
                    self.current_state["boxes"].extend(request.position)

            masks = generate_mask('redo', request, self.current_state, img_embeddings, img_file)

            self.history.append(('redo', request))
            return "Redo operation completed", masks
        return "No operation to redo", None

    def reset(self):
        """Reset operation"""
        self.history.clear()
        self.future.clear()
        self.current_state = {
            "foreground": [],
            "background": [],
            "boxes": []
        }
        return "All operations cleared", None

    def remove(self, request, img_embeddings, img_file):
        """Remove operation"""
        if request.type == 0:  # foreground
            if request.position in self.current_state["foreground"]:
                self.current_state["foreground"].remove(request.position)
                self.history.append(('remove', request))
                self.future.clear() 
            else:
                return "Foreground point not found", None
        elif request.type == 1:  # background
            if request.position in self.current_state["background"]:
                self.current_state["background"].remove(request.position)
                self.history.append(('remove', request))
                self.future.clear() 
            else:
                return "Background point not found", None
        elif request.type == 2:  # box
            if request.position in self.current_state["boxes"]:
                self.current_state["boxes"].remove(request.position)
                self.history.append(('remove', request))
                self.future.clear() 
            else:
                return "Box not found", None
        else:
            return "Invalid type", None

        masks = generate_mask('remove', request, self.current_state, img_embeddings, img_file)

        return "Operation completed", masks

    def get_current_state(self):
        """Get the current state"""
        return self.current_state

manager = OperationManager()
def process_prompt(request: PromptRequest, img_embeddings, img_file) -> PromptResponse:
    global manager

    if request.operation == 0:  # add
        result, receive_masks = manager.add(request, img_embeddings, img_file)

    elif request.operation == 1:  # undo
        result, receive_masks = manager.undo(img_embeddings, img_file)

    elif request.operation == 2:  # reset
        result, receive_masks = manager.reset()

    elif request.operation == 3:  # redo
        result, receive_masks = manager.redo(img_embeddings, img_file)

    elif request.operation == 4:  # remove
        result, receive_masks = manager.remove(request, img_embeddings, img_file)

    else:
        return PromptResponse(status="error", message="Invalid operation", data=None)

    current_state = manager.get_current_state()
    receive_masks = receive_masks if receive_masks is not None else []
    return PromptResponse(
        status="success",
        message=result,
        masks=receive_masks,
        data={
            "foreground": current_state["foreground"],
            "background": current_state["background"],
            "boxes": current_state["boxes"]
        }
    )
