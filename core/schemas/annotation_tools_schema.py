# annotation_tools_schema.py
from pydantic import BaseModel
from typing import List, Dict, Optional

class MaskData(BaseModel):#(仅用于添加操作)
    class_id: int             # Mask的classID
    masks: List[List[int]]    # Mask的坐标数据

class PromptRequest(BaseModel):
    operation: int            # 操作类型: 0 - 单个mask添加标注，1 - 删除单个已标注mask，2 - 更新类别，3 - 获取类别，4 - 添加类别，5 - 删除类别
    mask_data: Optional[MaskData] = None  # 标注的Mask数据 (0)
    mask_id: Optional[str] = None         # 需要操作的Mask ID (1)
    class_id_change: Optional[int] = None    # 新的类别ID (2、5)
    class_name: Optional[str] = None      # 类别名称 (2、4)


class ClassResponse(BaseModel):
    class_id: int           # 类别ID
    class_name: str         # 类别名称

class MaskResponse(BaseModel):
    mask_id: str             # Mask的ID
    class_id: int            # Mask属于的classID


class PromptResponse(BaseModel):
    status: str              # 请求状态: success | error
    message: str             # 操作的反馈消息
    mask_id: Optional[str] = None   # 如果操作涉及Mask，返回新增/删除的Mask的ID
    class_id: Optional[int] = None  # 如果操作涉及类别，返回操作后类别的ID
    masks: Optional[List[List[int]]] = None  # 如果操作涉及Mask，返回更新后的Mask坐标
    classes: Optional[List[ClassResponse]] = None  # 如果操作涉及类别，返回所有类别的信息
    data: Optional[dict] = None  # 操作后其他的附加数据