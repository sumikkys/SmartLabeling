from fastapi import FastAPI
from initialize_model import encoder, decoder
from routers import prompt, upload_image

# 一个点
# _, logits = decoder.point(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[1])

# 两个点 同时输入上一次的low-resolution mask
# decoder.point(img_embeddings, img_file, point_coords=[[324, 282],[314, 177]], point_labels=[1,0], logits=logits)

# 边界框
#decoder.bBox(img_embeddings, img_file, boxes=[225, 153, 308, 240])

# 边界框与点混合
# decoder.hybrid(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[0], boxes=[225, 153, 308, 240])
app = FastAPI()

print(f"Encoder initialized: {encoder is not None}")
print(f"Decoder initialized: {decoder is not None}")

app.include_router(prompt.router, tags=["Prompt"])
app.include_router(upload_image.router, tags=["Upload Image"]) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8232)