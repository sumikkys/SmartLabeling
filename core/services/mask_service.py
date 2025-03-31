#mask_service.py
from typing import List
from initialize_model import decoder

# 一个点
# _, logits = decoder.point(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[1])

# 两个点 同时输入上一次的low-resolution mask
# decoder.point(img_embeddings, img_file, point_coords=[[324, 282],[314, 177]], point_labels=[1,0], logits=logits)

# 边界框
#decoder.bBox(img_embeddings, img_file, boxes=[225, 153, 308, 240])

# 边界框与点混合
# decoder.hybrid(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[0], boxes=[225, 153, 308, 240])

def generate_mask(operation, current_state, img_embeddings, img_file, logits):
    """Choose whether to generate a mask according to the current operation, and choose the type of function."""
    if decoder is None:
        raise ValueError("Decoder is not initialized")
    masks = None
    masks_2d = [[]]
    if operation in ['add', 'undo', 'redo']:  #[, 'remove'] # These operations need to generate masks
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
            masks, logits = decoder.bBox(img_embeddings, img_file, boxes=current_state["boxes"])
        masks_2d = masks.astype(int).squeeze().tolist()
        
    return masks_2d, logits
