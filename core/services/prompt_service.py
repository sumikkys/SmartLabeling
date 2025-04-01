# prmpt_service.py
from schemas.prompt_schema import PromptRequest, PromptResponse
from services.mask_service import generate_mask
from services.clip_service import clip_class
from cache.image_cache import cache_manager
import asyncio

class OperationManager:
    def __init__(self):
        self.history = []  # record history operations
        self.future = []  # record future operations
        self.current_state = {
            "foreground": [],
            "background": [],
            "boxes": []
        }  # record current state

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
    async def add(self, request, img_embeddings, img_file, image_id, classes_features):
        """Add operation"""
        clip_result = None
        if request.type == 0:  # foreground
            self.current_state["foreground"].extend(request.position)
            logits = self.history[-1][2] if self.history else None
        elif request.type == 1:  # background
            self.current_state["background"].extend(request.position)
            logits = self.history[-1][2] if self.history else None
        elif request.type == 2:  # box
            self.history.clear()
            self.future.clear()
            self.current_state = {
                "foreground": [],
                "background": [],
                "boxes": []
            }
            self.current_state["boxes"].append(request.position)
            logits = None
        
        # #print(self.current_state)
        # masks, logits= generate_mask('add', self.current_state, img_embeddings, img_file, logits)
        # clip_result = clip_class('add', self.current_state, image_id)

        # masks_task = asyncio.to_thread(generate_mask, 'add', self.current_state, img_embeddings, img_file, logits)
        # clip_task = asyncio.to_thread(clip_class, 'add', self.current_state, image_id, classes_features)

        # masks, logits = await masks_task
        # clip_result = await clip_task

        results = await asyncio.gather(
            asyncio.to_thread(generate_mask, 'add', self.current_state, img_embeddings, img_file, logits),
            asyncio.to_thread(clip_class, 'add', self.current_state, image_id, classes_features)
        )
        masks, logits = results[0]  
        clip_result = results[1]   

        self.history.append(['add', request, logits])
        self.future.clear()
        #return "Added successfully", None , clip_result #测试版本保留
        return "Added successfully", masks, clip_result

    async def undo(self, img_embeddings, img_file, image_id, classes_features):
        """Undo operation"""
        if not hasattr(self, 'history') or not isinstance(self.history, list):
            raise AttributeError("self.history is not initialized or not a list")
        if not hasattr(self, 'future') or not isinstance(self.future, list):
            raise AttributeError("self.future is not initialized or not a list")

        if self.history:
            try:
                operation, request, logits = self.history.pop()
            except IndexError:
                return "No operation to undo", None

            self.future.append([operation, request, logits])

            if operation == 'add':
                if request.type == 0:  # foreground
                    for pos in request.position:
                        if pos in self.current_state["foreground"]:
                            self.current_state["foreground"].remove(pos)
                elif request.type == 1:  # background
                    for pos in request.position:
                        if pos in self.current_state["background"]:
                            self.current_state["background"].remove(pos)
                elif request.type == 2:  # box
                    pos = request.position
                    if pos in self.current_state["boxes"]:
                        self.current_state["boxes"].remove(pos)

            elif operation == 'remove':
                if request.type == 0:  # foreground
                    self.current_state["foreground"].extend(request.position)
                elif request.type == 1:  # background
                    self.current_state["background"].extend(request.position)
                elif request.type == 2:  # box
                    self.current_state["boxes"].append(request.position)

            if not self.history:
                return "back to original", None

            logits = self.history[-2][2] if len(self.history)>=2 else None

            try:
                results = await asyncio.gather(
                    asyncio.to_thread(generate_mask, 'add', self.current_state, img_embeddings, img_file, logits),
                    asyncio.to_thread(clip_class, 'add', self.current_state, image_id, classes_features)
                )
                masks, logits = results[0]  
                clip_result = results[1]  

                self.history[-1][2] = logits
            except Exception as e:
                return f"Error generating mask: {str(e)}", None

            return "Undo operation completed", masks, clip_result
            # return "Undo operation completed", None, clip_result #测试版本保留

        return "No operation to undo", None, None

    async def redo(self, img_embeddings, img_file, image_id, classes_features):
        """Redo operation"""
        if self.future:
            operation, request, logits = self.future.pop()
            self.history.append([operation, request, logits])
            if operation == 'add':
                if request.type == 0:  # foreground
                    self.current_state["foreground"].extend(request.position)
                elif request.type == 1:  # background
                    self.current_state["background"].extend(request.position)
                elif request.type == 2:  # box
                    self.current_state["boxes"].append(request.position)

            elif operation == 'remove':
                if request.type == 0:  # foreground
                    for pos in request.position:
                        if pos in self.current_state["foreground"]:
                            self.current_state["foreground"].remove(pos)
                elif request.type == 1:  # background
                    for pos in request.position:
                        if pos in self.current_state["background"]:
                            self.current_state["background"].remove(pos)
                elif request.type == 2:  # box
                    pos = request.position
                    if pos in self.current_state["boxes"]:
                        self.current_state["boxes"].remove(pos)
            logits = self.history[-2][2] if len(self.history)>=2 else None
            results = await asyncio.gather(
                asyncio.to_thread(generate_mask, 'add', self.current_state, img_embeddings, img_file, logits),
                asyncio.to_thread(clip_class, 'add', self.current_state, image_id, classes_features)
            )
            masks, logits = results[0]  
            clip_result = results[1]  
            
            self.history[-1][2] = logits
            
            if not self.future:
                # return "come to latest", None, None
                return "come to latest", masks, clip_result

            return "Redo operation completed", masks, clip_result
            # return "Redo operation completed", None, clip_result #测试版本保留
        return "No operation to redo", None, None
    def get_current_state(self):
        """Get the current state"""
        return self.current_state
    
    ###当前版本弃用###
    # def remove(self, request, img_embeddings, img_file):
    #     """Remove operation"""
    #     if request.type == 0:  # foreground
    #         for pos in request.position:
        #         if pos in self.current_state["foreground"]:
        #             self.current_state["foreground"].remove(pos)
        #             self.history.append(['remove', request, None])
        #             self.future.clear() 
        #         else:
        #             return "Foreground point not found", None
        # elif request.type == 1:  # background
        #     for pos in request.position:
        #         if pos in self.current_state["background"]:
        #             self.current_state["background"].remove(pos)
        #             self.history.append(['remove', request, None])
        #             self.future.clear()
        #         else:
        #             return "Background point not found", None
        # elif request.type == 2:  # box
        #     pos = request.position
        #     if pos in self.current_state["boxes"]:
        #         self.current_state["boxes"].remove(pos)
        #         self.history.append(['remove', request, None])
        #         self.future.clear() 
        #     else:
        #         return "Box not found", None
        # else:
        #     return "Invalid type", None
        
        # if (not self.current_state["foreground"]) or (not self.current_state["background"]) or (not self.current_state["boxes"]):
        #     return "back to original", None

        # masks, _ = generate_mask('remove',self.current_state, img_embeddings, img_file)

        # # return "Operation completed", None #测试版本保留
        # return "Operation completed", masks


manager = OperationManager()
async def process_prompt(request: PromptRequest, img_embeddings, img_file, classes_features) -> PromptResponse:
    global manager
    clip_result = None
    image_id = cache_manager.find_key_by_value(cache_manager.image_id_cache, request.image_name)

    if request.operation == 0:  # add
        result, receive_masks, clip_result = await manager.add(request, img_embeddings, img_file, image_id,classes_features)

    elif request.operation == 1:  # undo
        result, receive_masks, clip_result = await manager.undo(img_embeddings, img_file, image_id,classes_features)

    elif request.operation == 2:  # reset
        result, receive_masks = manager.reset()

    elif request.operation == 3:  # redo
        result, receive_masks, clip_result = await manager.redo(img_embeddings, img_file, image_id,classes_features)

    # elif request.operation == 4:  # remove
    #     result, receive_masks = manager.remove(request, img_embeddings, img_file)

    else:
        return PromptResponse(status="error", message="Invalid operation", data=None)

    current_state = manager.get_current_state()
    receive_masks = receive_masks if receive_masks is not None else []
    
    return PromptResponse(
        status="success",
        message=result,
        masks=receive_masks,
        clip_result = clip_result,
        data={
            "foreground": current_state["foreground"],
            "background": current_state["background"],
            "boxes": current_state["boxes"]
        }
    )
