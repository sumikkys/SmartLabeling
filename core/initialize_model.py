import cv2
from sam_model import SamEncoder, SamDecoder
from clip_model import CLIPTextEncoder, CLIPVisionEncoder, CLIPRegionEncoder
import os

encoder = None
decoder = None

clip_text_encoder = None
clip_vision_encoder = None
clip_region_encoder = None

def initialize_models():
    global encoder, decoder, clip_text_encoder, clip_vision_encoder, clip_region_encoder

    base_path = os.path.dirname(__file__)
    encoder_path = os.path.join(base_path,"models/sam.encoder.onnx")
    decoder_path = os.path.join(base_path,"models/sam.decoder.onnx")
    text_encoder_path = os.path.join(base_path,"models/clip_text_encoder.onnx")
    vision_encoder_path = os.path.join(base_path,"models/clip_vision_pre_encoder.onnx")
    region_encoder_path = os.path.join(base_path,"models/clip_region_encoder.onnx")

    # Initialize the SAM-Med2D ONNX model
    encoder = SamEncoder(
        model_path=encoder_path,
        warmup_epoch=3,
        device="cpu"
    )
    decoder = SamDecoder(
        model_path=decoder_path,
        device="cpu",
    )
    
    clip_text_encoder = CLIPTextEncoder(
        model_path=text_encoder_path,
        device="cpu"
    )
    
    clip_region_encoder = CLIPRegionEncoder(
        model_path=region_encoder_path,
        device="cpu"
    )
    
    clip_vision_encoder = CLIPVisionEncoder(
        model_path=vision_encoder_path,
        device="cpu"
    )
    


initialize_models()