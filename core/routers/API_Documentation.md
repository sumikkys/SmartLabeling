 # API 接口说明文档
 
 # 声明：此文档为项目开发过程中所记录的接口说明
 # 当前版本：前后端本地运行，涉及数据为本机数据，部分数据（如图片）传输仅传输路径
 # 更新时间：2024.12.23

1. Prompt

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
    
        "position":[[]]     /* array
                            点坐标示例：[[x,y]] 
                            框坐标示例: [x1,y1,x2,y2]
                            */
    }
  ```

 请求示例:
   ```json
    {
        "operation": 0,
        "type": 2,
        "position": [100, 150, 300, 400]
    }
    ```

 响应示例: //以add一个foreground为例
  ```json
  {
    "status": "success",
    "message": "Added successfully",
    "masks": [[]],  //***前端收到的masks为一个二维数组***
    "data": {
        "foreground": [
            [
                220,
                220
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

 2. 上传图像

 URL: `/uploadimage`

 方法: `POST`

 描述: **该接口用于接收用户上传的图像**

 请求格式: `multipart/formdata`

 请求示例:
    POST /uploadimage

    {
        "image_path": "F:/ApiTestImage/test_image_png.png"  //用户上传的图像文件地址，允许格式： `jpeg`、`png`、`bmp`、`jpg` 
    }

  
 响应示例:
  ```json
    {
        "status": "success",
        "message": "Image uploaded successfully",
        "data": {
            "image_path": "upload_images\\test_image_png.png",
        }
    }
  ```

 错误状态码:
    `400`	错误请求：请求参数有误或缺失
    `415`	不支持的媒体类型：上传的图像格式不支持
    `500`	服务器错误：服务器处理请求时出现内部错误

3. Polling 状态

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