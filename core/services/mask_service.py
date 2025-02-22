#mask_service.py
from typing import List
from initialize_model import decoder
def generate_mask(operation, request, current_state, img_embeddings, img_file, logits):
    """Choose whether to generate a mask according to the current operation, and choose the type of function."""
    if decoder is None:
        raise ValueError("Decoder is not initialized")
    masks = None
    #masks_2d = List[List[int]]
    masks_2d = [[]]
    if operation in ['add', 'undo', 'redo', 'remove']:  # These operations need to generate masks
        #101 111 011
        if (current_state["foreground"] or current_state["background"]) and current_state["boxes"]:
            current_lables = [1] * len(current_state["foreground"]) + [0] * len(current_state["background"])
            masks, logits = decoder.hybrid(img_embeddings, img_file, point_coords=current_state["foreground"]+current_state["background"], point_labels=current_lables, boxes=current_state["boxes"], logits=logits)
        #100 110 010    
        elif (current_state["foreground"] or current_state["background"]) and not current_state["boxes"]:
            current_lables = [1] * len(current_state["foreground"]) + [0] * len(current_state["background"])
            masks, logits = decoder.point(img_embeddings, img_file, point_coords=current_state["foreground"]+current_state["background"], point_labels=current_lables, logits=logits)
        #001
        else:
            if not current_state["boxes"]:
                raise ValueError("Boxes is not None")
            masks,_ = decoder.bBox(img_embeddings, img_file, boxes=current_state["boxes"])
            logits = None
        masks_list = masks.tolist()
        masks_2d = [sublist for matrix in masks_list for sublist in matrix]
    return masks_2d, logits
