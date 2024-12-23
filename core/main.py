from fastapi import FastAPI, File, UploadFile
from sam_model import SamEncoder, SamDecoder
from routers import prompt, upload_image 
from initialize_model import initialize_models

#     # 涓€涓�鐐�
#     # _, logits = decoder.point(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[1])
#
#     # 涓や釜鐐� 鍚屾椂杈撳叆涓婁竴娆＄殑low-resolution mask
#     # decoder.point(img_embeddings, img_file, point_coords=[[324, 282],[314, 177]], point_labels=[1,0], logits=logits)
#
#     # 杈圭晫妗�
#     decoder.bBox(img_embeddings, img_file, boxes=[225, 153, 308, 240])
#
#     # 杈圭晫妗嗕笌鐐规贩鍚�
#     # decoder.hybrid(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[0], boxes=[225, 153, 308, 240])
app = FastAPI()

initialize_models()



app.include_router(prompt.router, tags=["Prompt"])
app.include_router(upload_image.router, tags=["Upload Image"]) 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8232)



#     # 涓€锟�??锟�??
#     # _, logits = decoder.point(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[1])

#     # 涓や釜锟�?? 鍚屾椂杈撳叆涓婁竴娆＄殑low-resolution mask
#     # decoder.point(img_embeddings, img_file, point_coords=[[324, 282],[314, 177]], point_labels=[1,0], logits=logits)

#     # 杈圭晫锟�??
#     decoder.bBox(img_embeddings, img_file, boxes=[225, 153, 308, 240])

#     # 杈圭晫妗嗕笌鐐规贩锟�??
#     # decoder.hybrid(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[0], boxes=[225, 153, 308, 240])
