import numpy as np
# import matplotlib.pyplot as plt
import onnxruntime as ort
from onnxruntime import get_available_providers
from tqdm import tqdm
from typing import Any, Union
from copy import deepcopy
from utils import *
from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from routers import polling
from tokenizer import tokenize



class CLIPVisionEncoder:

    def __init__(self,
                 model_path: str,
                 device: str = "cuda",
                 warmup_epoch: int = 3,
                 **kwargs):
        opt = ort.SessionOptions()

        if device == "cuda":
            provider = ['CUDAExecutionProvider']
        elif device == "cpu":
            provider = ['CPUExecutionProvider']
        else:
            raise ValueError("Invalid device, please use 'cuda' or 'cpu' device.")

        print("loading CLIP Vision Encoder model...")
        self.session = ort.InferenceSession(model_path,
                                            opt,
                                            providers=provider,
                                            **kwargs)


        self.input_name = [input.name for input in self.session.get_inputs()]
        self.image_shape = self.session.get_inputs()[0].shape
        self.output_shape = self.session.get_outputs()[0].shape
        
        self.input_size = self.image_shape[-1]
        self.input_shape = (1,3, self.input_size, self.input_size)

        if warmup_epoch:
            self.warmup(warmup_epoch)
            
        

    def warmup(self, epoch: int) -> None:
        """warmup function

        Args:
            epoch (int): warmup epoch.
        """
        # x = np.random.randint(0,256,self.input_shape).astype(np.float32)
        # y = np.random.randint(0,224,(1,1,2)).astype(np.float32)
        # z = np.random.randint(0,4,(1,1)).astype(np.int32)
        x = np.zeros((1,3,224,224)).astype(np.float32)
        print("start warmup!")
        for i in tqdm(range(epoch)):
            self.session.run(None, {self.input_name[0]: x})
        print("warmup finish!")
        polling.initialized = True

    def transform(self, image: np.ndarray) -> np.ndarray:
        """
        Apply preprocessing to an image using OpenCV and NumPy.
        Equivalent to MONAI transforms: Resize, Permute, ToTensor, and Normalize.

        Parameters:
        -----------
        image : np.ndarray
            Input image in HWC format (Height, Width, Channels)
        image_size : int
            Target size for resizing

        Returns:
        --------
        np.ndarray
            Preprocessed image in CHW format (Channels, Height, Width), normalized to [0,1]
        """
        img = image
        # BGR -> RGB
        img = img[..., ::-1]
        # Resize image
        img = cv2.resize(img, (self.input_size, self.input_size), interpolation=cv2.INTER_NEAREST)
        
        # Permute dimensions from HWC to CHW
        img = np.transpose(img, (2, 0, 1))
        
        
        pixel_mean = np.array([123.675, 116.28, 103.53], dtype=np.float32)
        pixel_std = np.array([58.395, 57.12, 57.375], dtype=np.float32)
        
        mean = pixel_mean.reshape(3, 1, 1)
        std = pixel_std.reshape(3, 1, 1)
        
        # Convert to float32 and normalize 
        img = (img.astype(np.float32)-mean) / std
        
        return img

    def _extract_feature(self, image: np.ndarray) -> np.ndarray:
        """extract image feature

        this function can use vit to extract feature from transformed image.

        Args:
            tensor (np.ndarray): input image with BGR format.

        Returns:
            np.ndarray: image`s feature.
        """
        print(image.shape)
        H, W = image.shape[:2]
        if image.ndim == 3:
            input_image = self.transform(image)
            input_image = np.expand_dims(input_image, axis=0)
        else:
            input_image = image
            for i in range(input_image.shape[0]):
                input_image[i] = self.transform(input_image[i])
        feature = self.session.run(None, {self.input_name[0]: input_image})[0]
        shape_dict = {
            'ori': (H, W),
            'post': self.input_size
        }
        return feature, shape_dict

    def __call__(self, img: np.array, *args: Any, **kwds: Any) -> Any:
        return self._extract_feature(img)

    def printsize(self):
        print(self.input_size)

class CLIPRegionEncoder:

    def __init__(self,
                 model_path: str,
                 device: str = "cuda",
                 warmup_epoch: int = 3,
                 **kwargs):
        opt = ort.SessionOptions()

        if device == "cuda":
            provider = ['CUDAExecutionProvider']
        elif device == "cpu":
            provider = ['CPUExecutionProvider']
        else:
            raise ValueError("Invalid device, please use 'cuda' or 'cpu' device.")

        print("loading CLIP Region Encoder model...")
        self.session = ort.InferenceSession(model_path,
                                            opt,
                                            providers=provider,
                                            **kwargs)


        self.input_name = [input.name for input in self.session.get_inputs()]
        

    def _extract_feature(self, image: np.ndarray, points: np.ndarray, labels: np.ndarray, shape_dict: dict) -> np.ndarray:
        """extract image feature

        Args:
            tensor (np.ndarray): input image with BGR format.

        Returns:
            np.ndarray: image`s feature.
        """
        H, W = shape_dict['ori']
        input_size = shape_dict['post']
        points = points/np.array([W, H], dtype=np.float32) * input_size
        feature = self.session.run(None, {self.input_name[0]: image,
                                          self.input_name[1]: points,
                                          self.input_name[2]: labels})[0]
        return feature

    def __call__(self, img: np.array, shape_dict: dict, prompts: dict, *args: Any, **kwds: Any) -> Any:
        return self._extract_feature(img, prompts['points'], prompts['labels'], shape_dict)




class CLIPTextEncoder:

    def __init__(self,
                 model_path: str,
                 device: str = "cuda",
                 **kwargs):
        opt = ort.SessionOptions()

        if device == "cuda":
            provider = ['CUDAExecutionProvider']
        elif device == "cpu":
            provider = ['CPUExecutionProvider']
        else:
            raise ValueError("Invalid device, please use 'cuda' or 'cpu' device.")

        print("loading CLIP Text Encoder model...")
        self.session = ort.InferenceSession(model_path,
                                            opt,
                                            providers=provider,
                                            **kwargs)
        self.input_name = self.session.get_inputs()[0].name

    def _encode(self, texts):
        texts = tokenize(texts)
        return self.session.run(None, {self.input_name: texts})[0]
    
    def __call__(self, texts,*args, **kwds):
        return self._encode(texts) # 输出维度为（num_texts, embedding_dim）因此矩阵乘法时需要.T
    
    def zeroshot_classifier(self, classnames, modality='Xray', device = 'cpu'):
        zeroshot_weights = []
        for classname in classnames:
            texts = []
            for template in tqdm(med_templates):
                # 检查模板中是否包含modality占位符
                if '{modality}' in template:
                    text = template.format(text=classname, modality=modality)
                else:
                    # 如果没有modality占位符，只替换classname
                    text = template.format(text=classname)
                # print(text)
                texts.append(text)  # format with class
            class_embeddings = self._encode(texts)  # embed with text encoder
            class_embeddings = normalize(class_embeddings)  # normalize embeddings
            class_embedding = np.mean(class_embeddings, axis=0)
            # 归一化结果向量 (替代 torch 的 embedding.norm())
            class_embedding_norm = np.sqrt(np.sum(class_embedding * class_embedding))
            class_embedding = class_embedding / (class_embedding_norm + 1e-8)  # 添加小量避免除零
            zeroshot_weights.append(class_embedding)
            
        zeroshot_weights = np.column_stack(zeroshot_weights)
        return zeroshot_weights # 输出维度为（embedding_dim, num_classes）因此矩阵乘法时无需.T

