from fastapi import FastAPI
from initialize_model import encoder, decoder
from routers import prompt, upload_image, polling, export, newProject, annotation_tools, switch_image
import argparse

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
app.include_router(polling.router, tags=["Polling"])
app.include_router(export.router, tags=["Export"])
app.include_router(newProject.router, tags=["New Project"])
app.include_router(switch_image.router, tags=["Switch Image"])
app.include_router(annotation_tools.router, prefix="/annotation-tools", tags=["Annotations Tools"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='params')
    parser.add_argument('--host', type=str, default='localhost', help='host')
    parser.add_argument('--port', type=int, default=8000, help='port')
    
    import uvicorn
    uvicorn.run(app, host=parser.parse_args().host, port=parser.parse_args().port)