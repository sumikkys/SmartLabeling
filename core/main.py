from fastapi import FastAPI, File, UploadFile
from sam_model import SamEncoder, SamDecoder
from initialize_model import encoder, decoder
from routers import prompt, upload_image 
from initialize_model import initialize_models

#     # 娑撯偓娑擄拷閻愶拷
#     # _, logits = decoder.point(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[1])
#
#     # 娑撱倓閲滈悙锟� 閸氬本妞傛潏鎾冲弳娑撳﹣绔村▎锛勬畱low-resolution mask
#     # decoder.point(img_embeddings, img_file, point_coords=[[324, 282],[314, 177]], point_labels=[1,0], logits=logits)
#
#     # 鏉堝湱鏅�濡楋拷
#     decoder.bBox(img_embeddings, img_file, boxes=[225, 153, 308, 240])
#
#     # 鏉堝湱鏅�濡楀棔绗岄悙瑙勮穿閸氾拷
#     # decoder.hybrid(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[0], boxes=[225, 153, 308, 240])
app = FastAPI()

print(encoder is not None)
print(decoder is not None)



app.include_router(prompt.router, tags=["Prompt"])
app.include_router(upload_image.router, tags=["Upload Image"]) 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8232)



#     # 娑撯偓閿燂拷??閿燂拷??
#     # _, logits = decoder.point(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[1])

#     # 娑撱倓閲滈敓锟�?? 閸氬本妞傛潏鎾冲弳娑撳﹣绔村▎锛勬畱low-resolution mask
#     # decoder.point(img_embeddings, img_file, point_coords=[[324, 282],[314, 177]], point_labels=[1,0], logits=logits)

#     # 鏉堝湱鏅�閿燂拷??
#     decoder.bBox(img_embeddings, img_file, boxes=[225, 153, 308, 240])

#     # 鏉堝湱鏅�濡楀棔绗岄悙瑙勮穿閿燂拷??
#     # decoder.hybrid(img_embeddings, img_file, point_coords=[[324, 282]], point_labels=[0], boxes=[225, 153, 308, 240])
