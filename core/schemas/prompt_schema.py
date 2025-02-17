# prompt_schema.py
from pydantic import BaseModel
from typing import List, Optional, Union
import numpy as np

#Request body data model
class PromptRequest(BaseModel):
    operation: int  # 0:add, 1:undo, 2:reset, 3:redo, 4:remove
    type: int       # 0:foreground, 1:background, 2:box
    position: Union[List[int], List[List[int]]]  # List of positions
    project_name: str
    storage_path: Optional[str] = "F:/SmartLabeling/projects"  # 默认路径
    image_name: str

#Response body data model
class PromptResponse(BaseModel):
    status: str
    message: str
    masks: List[List[int]] 
    data: Optional[dict]
