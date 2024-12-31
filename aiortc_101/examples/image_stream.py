import av
import asyncio
import fractions
import numpy as np
from av import VideoFrame
from PIL import Image
from aiortc.mediastreams import MediaStreamTrack
from loguru import logger

class OptimizedImageTrack(MediaStreamTrack):
    kind = "video"
    
    def __init__(self, fps=30):
        super().__init__()
        self.fps = fps
        self._timestamp = 0
        
    async def recv(self):
        # 简单高效的实现
        logger.info(f"Received frame")
        pil_image = Image.open(self.image_path)
        # 转换为 RGB（如果需要）
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        frame = av.VideoFrame.from_image(pil_image)
        logger.info(f"Frame received")
        
        # 设置时间戳
        frame.pts = self._timestamp
        frame.time_base = fractions.Fraction(1, self.fps)
        self._timestamp += 1
        logger.info(f"Frame set")

        await asyncio.sleep(1/self.fps)  # 控制帧率
        logger.info(f"Frame sent")
        return frame

    def get_image(self, image_path):
        self.image_path = image_path
        logger.info(f"Loaded image from {image_path}")