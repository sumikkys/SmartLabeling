from fastapi import FastAPI
from initialize_model import encoder, decoder
from routers import readProject,prompt, upload_image, polling, export, newProject, annotation_tools, switch_image
import argparse

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
app.include_router(readProject.router, tags=["Read Project"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='params')
    parser.add_argument('--host', type=str, default='localhost', help='host')
    parser.add_argument('--port', type=int, default=8000, help='port')
    
    import uvicorn
    uvicorn.run(app, host=parser.parse_args().host, port=parser.parse_args().port)