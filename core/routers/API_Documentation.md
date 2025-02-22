 # API 接口说明文档

 # 更新时间：2025.2.19
 # 关于项目结构：
- storage_path/project_name/
  - images/
    - image1.png
    - image2.png
  - masks/
    - mask1.png
    - mask2.png
  - project_name.yaml

  API涉及storage_path时留空则默认为 "F:/SmartLabeling/projects"，用户可自行修改

# ***1. Mask Prompt***

 URL: `/prompt`

 方法: `POST`

 描述: **上传用户指令的prompt返回相应的响应**

 请求格式: `json`:
  ```json:
    {
        "operation": 0,     /* int
                            0:add 
                            1:undo  撤销
                            2:reset 清空当前操作
                            3:redo  反撤销
                            4:remove
                            */

        "type": 0,          /* int 
                            0:前景点  
                            1:背景点
                            2：框
                            */
    
        "position":[[]],     /* array
                            点坐标示例：[[x,y]] 
                            框坐标示例: [x1,y1,x2,y2]
                            */

        "project_name": "",
        "storage_path": "", //该行留空为默认存储路径："F:/SmartLabeling/projects"
        "image_name": ""
    }
  ```

 请求示例:
   ```json
    {
        "operation": 0,
        "type": 0,
        "position":[[120,120]],
        "project_name": "test1",
        "storage_path": "D:/",
        "image_name": "test_image_png.png"
    }
    ```

 响应示例: //以上述请求为例
  ```json
  {
        "status": "success",
        "message": "Added successfully",
        "masks": [[]],  //***前端收到的masks为一个二维数组,此处省略***
        "data": {
            "foreground": [
                [
                    120,
                    120
                ]
            ],
            "background": [],
            "boxes": []
    }
}
  ```

 错误状态码:

    `400`	错误请求：请求参数有误或缺失
    `404`	找不到资源：请求的资源不存在
    `500`	服务器错误：服务器处理请求时出现内部错误

# ***2. uploadImage***

 URL: `/uploadimage`

 方法: `POST`

 描述: **该接口用于接收用户上传的图像**

 请求格式: `json`
   ```json
    {
        "image_path": "",  //用户上传的图像文件地址，允许格式： `jpeg`、`png`、`bmp`、`jpg` 
        "project_name": "",
        "storage_path": ""  //改行留空为默认存储路径："F:/SmartLabeling/projects"
    }
  ```

 请求示例:
  ```json
    {
        "image_path": "F:/ApiTestImage/test_image_jpg.jpg",
        "project_name": "test1",
        "storage_path": "D:/"
    }
  ```
  
 响应示例:
  ```json
    {
        "status": "success",
        "message": "Image uploaded successfully",
        "data": {
            "image_path": "D:\\test1\\images\\test_image_jpg.jpg",
            "storage_path": "D:\\test1\\images"
        }
    }
  ```

 错误状态码:

    `400`	错误请求：请求参数有误或缺失
    `415`	不支持的媒体类型：上传的图像格式不支持
    `500`	服务器错误：服务器处理请求时出现内部错误

# ***3. Polling status***

 URL: `/status`

 方法: `GET`

 描述: **获取系统初始化状态**

 请求示例:
    GET /status

 响应示例:
  ```json
    {
        "initialized": true
    }
  ```

 错误状态码:

    `404`	找不到资源：请求的资源不存在
    `500`	服务器错误：服务器处理请求时出现内部错误

# ***4. Create project***

 URL: `/create-project`

 方法: `POST`

 描述: **该接口用于用户新建项目**

 请求格式: `json`
  ```json
    {
        "project_name": "", //用户新建的项目名称
        "storage_path": ""  //用户选择的项目地址，留空则为默认存储路径："F:/SmartLabeling/projects"
    }
  ```

 请求示例:
  ```json
    {
        "project_name": "test2",
        "storage_path": "D:/"
    }
  ```
  
 响应示例:
  ```json
    {
        "message": "Project created successfully",
        "project_path": "D:\\test2" //若同名项目存在则返回"Project test1 already exists."
    }
  ```
   错误状态码:

    `404`	找不到资源：请求的资源不存在
    `500`	服务器错误：服务器处理请求时出现内部错误

# ***5. Export label data***

 URL: `/export`

 方法: `POST`

 描述: **该接口用于用户导出标注数据**

 请求格式: `json`
  ```json
    {
        "image_id": [], // 用户需要导出的图片id列表，***留空则导出所有图片***
        "project_name": "", //用户的项目名称
        "project_path": "" //用户选择的项目地址，留空则为默认存储路径："F:/SmartLabeling/projects"
    }
  ```

 请求示例:
  ```json
    {
        "image_id": [1],
        "project_name": "test1",
        "project_path": "D:/"
    }
  ```
  
 响应示例:
  ```json
    {
        "status": "success",
        "message": "Export successful",
        "data": {
            "masks_path": "D:\\test1\\masks",
            "yaml_path": "D:\\test1\\test1.yaml"
        }
    }
  ```
   错误状态码:

    `404`	找不到资源：请求的资源不存在
    `500`	服务器错误：服务器处理请求时出现内部错误



## ***6. Switch Image***

**URL:** `/switch_image`

**Method:** `POST`

**Description:** **该接口用于切换当前工作中的图片，切换后新图片的遮罩将被加载。**

### Request Format: `json`
```json
{
    "image_id": 1,  // int 图片的唯一标识符
    "project_name": "", //用户的项目名称
    "project_path": "" //用户选择的项目地址，留空则为默认存储路径："F:/SmartLabeling/projects"
}
```

### Request Example:
```json
{
    "image_id": 1,
    "project_name": "test1",
    "project_path": "D:/"
}
```

### Response Example:
```json
{
    "message": "Switched to image: test_image_png.png"
}
```

### Error Status Codes:

- `400`: No image selected or image not found
- `500`: Internal Server Error


---


# ***7. Annotation Prompt***

**URL**: `/annotation-tools/prompt`  
**方法**: `POST`  
**描述**: **处理来自前端的标注请求，支持添加、删除、更新标注 Mask，获取当前类别及添加、删除类别操作**  

### 请求格式: `json`  
```json
{
    "operation": 0,      /* int 必要
                          0:单个Mask添加标注
                          1:删除单个已标注Mask
                          2:更新类别
                          3:获取类别
                          4:添加类别
                          5:删除类别(会导致该类别下已标注的masks也一并删除)
                          */
  
    "mask_data": {        /* object 可选(仅在operation为0时使用)
                          {
                            "class_id": int,
                            "masks": [[x1, y1], [x2, y2], ...]
                          }
                          */
    },
    
    "mask_id": "string",  /* string 可选(仅在operation为1时使用)
                          标识需要操作的Mask的ID
                          */
    
    "class_id_change": 0, /* int 可选(仅在operation为2和5时使用)
                          用于更新或删除类别时，指定新的类别ID
                          */
    
    "class_name": "string" /* string 可选(仅在operation为2和4时使用)
                            类别名称，用于更新或添加类别
                            */
}
```
### 关于mask_id(str):
**mask_id为字符串，表示一个唯一的标注ID，用于标识一个标注。**
`mask_id = "class_id"+ "_" + "mask_id2"`

`mask_id = "2_9"` // 类别ID为2，标注ID为9

### 请求示例:
1. **添加标注 Mask** (`operation: 0`):
```json
{
    "operation": 0,
    "mask_data": {
        "class_id": 1,
        "masks": [[120, 120], [130, 130]]
    }
}
```

2. **删除标注 Mask** (`operation: 1`):
```json
{
    "operation": 1,
    "mask_id": "1_0"
}
```

3. **更新类别** (`operation: 2`):
```json
{
    "operation": 2,
    "class_id_change": 2,
    "class_name": "tree" //表示对于id为2的class新的name是tree
}
```

4. **获取类别** (`operation: 3`):
```json
{
    "operation": 3
}
```

5. **添加类别** (`operation: 4`):
```json
{
    "operation": 4,
    "class_name": "NewClass"
}
```

6. **删除类别** (`operation: 5`):
```json
{
    "operation": 5,
    "class_id_change": 3
}
```

### 响应格式:
```json
{
    "status": "success",   /* 操作状态：success | error */
    "message": "操作的反馈消息",  /* 反馈的具体消息 */
    "mask_id": "string",   /* 如果操作涉及Mask，返回新增/删除的Mask的ID */
    "class_id": 0,         /* 如果操作涉及类别，返回操作后类别的ID */
    "masks": [[x1, y1], [x2, y2], ...], /* 操作后的标注坐标数据 */
    "classes": [           /* 操作为3、4时返回所有类别的信息 */
        {
            "class_id": 1,
            "class_name": "Foreground"
        },
        {
            "class_id": 2,
            "class_name": "Background"
        }
    ],
    "data": null           /* 附加数据，如果没有返回null */
}
```

### 错误状态码:
- **400**: 错误请求：请求参数有误或缺失。
- **404**: 找不到资源：指定的资源或标注不存在。
- **500**: 服务器错误：处理请求时出现内部错误。


### 操作说明:

- **operation: 0 (单个Mask添加标注)**  
  - 请求中必须包含 `mask_data`，包括 `class_id` 和 `masks`（标注坐标数据）。成功后返回新增的 `mask_id` 

- **operation: 1 (删除单个已标注Mask)**  
  - 需要提供 `mask_id`，指定要删除的标注 Mask。成功时返回删除操作的结果。

- **operation: 2 (更新类别)**  
  - 需要提供 `class_name` 和 `class_id_change`，用于更新指定class类别名称。如果更新成功，返回更新后的类别 ID 和 类别名称。

- **operation: 3 (获取类别)**  
  - 获取与当前图像相关的所有类别信息，返回类别列表。

- **operation: 4 (添加类别)**  
  - 提供 `class_name`，添加新类别。返回操作结果消息。

- **operation: 5 (删除类别)**  
  - 提供 `class_id_change`，删除指定类别。返回操作结果消息。

---