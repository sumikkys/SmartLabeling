 # API 接口说明文档

 # 更新时间：2025.2.16
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

# ***1. Prompt***

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
        "storage_path": "", //改行留空为默认存储路径："F:/SmartLabeling/projects"
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
        "project_path": "D:\\test2"
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
        "annotations": [
            {
                "class_id": 255, //类别id，等同灰度值
                "masks":[[]] //***即API 1生成的masks ***
            },
            {
                "class_id": 150,
                "masks":[[]]
            }//多个标注数据，此处为id： 150和id： 255的标注数据
        ],
        "project_name": "", //用户的项目名称
        "project_path": "", //用户选择的项目地址，留空则为默认存储路径："F:/SmartLabeling/projects"
        "image_width": 350, //所处理图像的宽
        "image_height": 350 //所处理图像的高
    }
  ```

 请求示例:
  ```json
    {
        "annotations": [
            {
                "class_id": 255,
                "masks":[[]] //此处省略
            },
            {
                "class_id": 150,
                "masks":[[]]
            }
        ],
        "project_name": "test1",
        "project_path": "D:/",
        "image_width": 350,
        "image_height": 350
    }
  ```
  
 响应示例:
  ```json
    {
        "status": "success",
        "message": "Export successful",
        "data": {
            "masks_path": "D:\\test1\\masks\\test1_exported_image.png",
            "yaml_path": "D:\\test1\\test1.yaml"
        }
    }
  ```
   错误状态码:

    `404`	找不到资源：请求的资源不存在
    `500`	服务器错误：服务器处理请求时出现内部错误



## ***6. Switch Image***

**URL:** `/annotation-tools/switch_image`

**Method:** `POST`

**Description:** **该接口用于切换当前工作中的图片，切换后图片的标注类别和遮罩将被加载。**

### Request Format: `json`
```json
{
    "image_name": ""  // 图片的唯一标识符
}
```

### Request Example:
```json
{
    "image_name": "test_image_png.png"
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

## ***7. Add Mask***

**URL:** `/annotation-tools/api/add_mask`

**Method:** `POST`

**Description:** **该接口用于为当前选择的图片添加一个标注 Mask。**

### Request Format: `json`
```json
{
    "class_id": 1,  // Mask的类别ID
    "masks": [[0,0], [10,10], [10,0], [0,10]]  // Mask的坐标（多边形的顶点坐标）
}
```

### Request Example:
```json
{
    "class_id": 1,
    "masks": [[0,0], [10,10], [10,0], [0,10]]
}
```

### Response Example:
```json
{
    "message": "Mask added successfully",
    "mask": {
        "mask_id": "1",
        "class_id": 1,
        "masks": [[0,0], [10,10], [10,0], [0,10]]
    }
}
```

### Error Status Codes:

- `400`: No image selected
- `500`: Internal Server Error


---

## ***8. Delete Mask***

**URL:** `/annotation-tools/api/delete_mask/{mask_id}`

**Method:** `DELETE`

**Description:** **该接口用于删除指定的标注 Mask。**

### Request Format: `url`
- `mask_id`: 要删除的标注 Mask 的 ID。

### Request Example:
```json
{
    "mask_id": "1"
}
```

### Response Example:
```json
{
    "message": "Mask deleted successfully"
}
```

### Error Status Codes:

- `404`: Mask not found
- `500`: Internal Server Error


---

## ***9. Update Mask Class***

**URL:** `/annotation-tools/api/update_mask_class/{mask_id}`

**Method:** `PUT`

**Description:** **该接口用于更改已标注 Mask 的类别。**

### Request Format: `json`
```json
{
    "new_class_id": 2  // 新类别ID
}
```

### Request Example:
```json
{
    "new_class_id": 2
}
```

### Response Example:
```json
{
    "message": "Mask class updated",
    "mask": {
        "mask_id": "1",
        "class_id": 2,
        "masks": [[0,0], [10,10], [10,0], [0,10]]
    }
}
```

### Error Status Codes:

- `404`: Mask not found
- `500`: Internal Server Error


---

## ***10. Get Classes***

**URL:** `/annotation-tools/api/classes`

**Method:** `GET`

**Description:** **该接口用于获取当前图片的所有类别。**

### Request Format: `json`
```json
{
    // 无需请求体，默认使用当前选中的图片
}
```

### Request Example:
```json
// 无请求体
```

### Response Example:
```json
{
    "classes": [
        {
            "class_id": 0,
            "class_name": "_background_"
        },
        {
            "class_id": 1,
            "class_name": "class1"
        }
    ]
}
```

### Error Status Codes:

- `400`: No image selected or no classes defined
- `500`: Internal Server Error


---

## ***11. Add Class***

**URL:** `/annotation-tools/api/add_class`

**Method:** `POST`

**Description:** **该接口用于为当前项目添加新的类别。**

### Request Format: `json`
```json
{
    "class_name": "new_class"  // 新类别的名称
}
```

### Request Example:
```json
{
    "class_name": "new_class"
}
```

### Response Example:
```json
{
    "message": "Class added successfully",
    "classes": [
        {
            "class_id": 0,
            "class_name": "_background_"
        },
        {
            "class_id": 1,
            "class_name": "class1"
        },
        {
            "class_id": 2,
            "class_name": "new_class"
        }
    ]
}
```

### Error Status Codes:

- `400`: No image selected
- `500`: Internal Server Error


---

## ***12. Delete Class***

**URL:** `/annotation-tools/api/delete_class/{class_id}`

**Method:** `DELETE`

**Description:** **该接口用于删除类别。删除类别时，若该类别有标注的 Mask，会阻止删除并返回警告信息。**

### Request Format: `json`
- `class_id`: 要删除的类别ID。

### Request Example:
```json
{
    "class_id": 2
}
```

### Response Example:
```json
{
    "message": "Class deleted successfully",
    "classes": [
        {
            "class_id": 0,
            "class_name": "_background_"
        },
        {
            "class_id": 1,
            "class_name": "class1"
        }
    ]
}
```

### Error Status Codes:

- `400`: Cannot delete class, there are masks using it.
- `500`: Internal Server Error


---

## ***13. Add Image***

**URL:** `/annotation-tools/api/add_image`

**Method:** `POST`

**Description:** **该接口用于为当前项目添加一张图片。**

### Request Format: `json`
```json
{
    "image_id": "image2",  // 新图片的ID
    "image_path": "/path/to/image"  // 新图片的路径
}
```

### Request Example:
```json
{
    "image_id": "image2",
    "image_path": "/path/to/image"
}
```

### Response Example:
```json
{
    "message": "Image added successfully"
}
```

### Error Status Codes:

- `400`: Invalid image path
- `500`: Internal Server Error