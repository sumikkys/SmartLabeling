from pydantic import BaseModel
from typing import List, Optional
import numpy as np

#����������ģ��
class PromptRequest(BaseModel):
    operation: int  # 0:add, 1:undo, 2:reset, 3:redo, 4:remove
    type: int       # 0:foreground, 1:background, 2:box
    position: List[List[int]]  # List of positions

#��Ӧ������ģ��
class PromptResponse(BaseModel):
    status: str
    message: str
    masks: np.ndarray = None
    data: Optional[dict]
