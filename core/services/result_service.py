def get_segmentation_result(result_id: str) -> dict:
    # ģ������ݿ��ȡ���
    segmentation_results = {
        "123456": {
            "mask_path": "/path/to/segmentation_mask.png",
            "original_image_path": "/path/to/original_image.jpg"
        }
    }
    return segmentation_results.get(result_id)
