#mask_service.py
from typing import List
from initialize_model import decoder
def generate_mask(operation, request, current_state, img_embeddings, img_file):
    """Choose whether to generate a mask according to the current operation, and choose the type of function."""
    if decoder is None:
        raise ValueError("Decoder is not initialized")
    masks = None
    #masks_2d = List[List[float]]
    masks_2d = [[]]
    if operation in ['add', 'undo', 'redo', 'remove']:  # These operations need to generate masks
        if request.type == 0:  # foreground
            if current_state["foreground"] is None:
                raise ValueError("Foreground is None")
            masks, _ = decoder.point(img_embeddings, img_file, point_coords=current_state["foreground"], point_labels=[1])
        elif request.type == 1:  # background
            if current_state["background"] is None:
                raise ValueError("Background is None")
            masks, _ = decoder.point(img_embeddings, img_file, point_coords=current_state["background"], point_labels=[0])
        elif request.type == 2:  # box
            if current_state["boxes"] is None:
                raise ValueError("Boxes is not None")
            masks, _ = decoder.bBox(img_embeddings, img_file, boxes=current_state["boxes"])
        masks_list = masks.tolist()
        masks_2d = [sublist for matrix in masks_list for sublist in matrix]
    return masks_2d
