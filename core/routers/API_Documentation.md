 # API �ӿ�˵���ĵ�
 
 # ���������ĵ�Ϊ��Ŀ��������������¼�Ľӿ�˵��
 # ��ǰ�汾��ǰ��˱������У��漰����Ϊ�������ݣ��������ݣ���ͼƬ�����������·��
 # ����ʱ�䣺2024.12.23

1. Prompt

 URL: `/prompt`

 ����: `POST`

 ����: **�ϴ��û�ָ���prompt������Ӧ����Ӧ**

 �����ʽ: `json`:
  ```json:
    {
        "operation": 0,     /* int
                            0:add 
                            1:undo  ����
                            2:reset ��յ�ǰ����
                            3:redo  ������
                            4:remove
                            */

        "type": 0,          /* int 
                            0:ǰ����  
                            1:������
                            2����
                            */
    
        "position":[[]]     /* array
                            ������ʾ����[[x,y]] 
                            ������ʾ��: [x1,y1,x2,y2]
                            */
    }
  ```

 ����ʾ��:
   ```json
    {
        "operation": 0,
        "type": 2,
        "position": [100, 150, 300, 400]
    }
    ```

 ��Ӧʾ��: //��addһ��foregroundΪ��
  ```json
  {
    "status": "success",
    "message": "Added successfully",
    "masks": [[]],  //***ǰ���յ���masksΪһ����ά����***
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

 ����״̬��:
    `400`	��������������������ȱʧ
    `404`	�Ҳ�����Դ���������Դ������
    `500`	���������󣺷�������������ʱ�����ڲ�����

 2. �ϴ�ͼ��

 URL: `/uploadimage`

 ����: `POST`

 ����: **�ýӿ����ڽ����û��ϴ���ͼ��**

 �����ʽ: `multipart/formdata`

 ����ʾ��:
    POST /uploadimage

    {
        "image_path": "F:/ApiTestImage/test_image_png.png"  //�û��ϴ���ͼ���ļ���ַ�������ʽ�� `jpeg`��`png`��`bmp`��`jpg` 
    }

  
 ��Ӧʾ��:
  ```json
    {
        "status": "success",
        "message": "Image uploaded successfully",
        "data": {
            "image_path": "upload_images\\test_image_png.png",
        }
    }
  ```

 ����״̬��:
    `400`	��������������������ȱʧ
    `415`	��֧�ֵ�ý�����ͣ��ϴ���ͼ���ʽ��֧��
    `500`	���������󣺷�������������ʱ�����ڲ�����

3. Polling ״̬

 URL: `/status`

 ����: `GET`

 ����: **��ȡϵͳ��ʼ��״̬**

 ����ʾ��:
    GET /status

 ��Ӧʾ��:
  ```json
    {
        "initialized": true
    }
  ```

 ����״̬��:
    `404`	�Ҳ�����Դ���������Դ������
    `500`	���������󣺷�������������ʱ�����ڲ�����