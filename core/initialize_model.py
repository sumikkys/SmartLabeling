import cv2
from sam_model import SamEncoder, SamDecoder
import os


encoder = None
decoder = None

def initialize_models():
    global encoder, decoder

    base_path = os.path.dirname(__file__)
    encoder_path = os.path.join(base_path,"models/sam.encoder.onnx")
    decoder_path = os.path.join(base_path,"models/sam.decoder.onnx")

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

initialize_models()