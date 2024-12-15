from fastapi import FastAPI, File, UploadFile
from sam_model import SamEncoder, SamDecoder
from routers import prompt, upload_image, get_result
from initialize_models import initialize_models

initialize_models()

app = FastAPI()

app.include_router(prompt.router, tags=["Prompt"])
app.include_router(upload_image.router, tags=["Upload Image"])
app.include_router(get_result.router, tags=["Result"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8232)



#     # 一�??�??
#     # _, logits = decoder.point(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[1])

#     # 两个�?? 同时输入上一次的low-resolution mask
#     # decoder.point(img_embeddings, img_file, point_coords=[[324, 282],[314, 177]], point_labels=[1,0], logits=logits)

#     # 边界�??
#     decoder.bBox(img_embeddings, img_file, boxes=[225, 153, 308, 240])

#     # 边界框与点混�??
#     # decoder.hybrid(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[0], boxes=[225, 153, 308, 240])
