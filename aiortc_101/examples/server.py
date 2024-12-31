import os
import json
import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaPlayer, MediaRelay
from PIL import Image
import argparse
from loguru import logger
from image_stream import OptimizedImageTrack

# 获取当前文件所在目录
ROOT = os.path.dirname(__file__)

async def index(request):
    """提供网页"""
    content = open(os.path.join(ROOT, "static/index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)

async def javascript(request):
    """提供JavaScript文件"""
    content = open(os.path.join(ROOT, "static/client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)

async def offer(request):
    """处理WebRTC offer"""
    params = await request.json()
    offer = RTCSessionDescription(
        sdp=params["sdp"],
        type=params["type"]
    )
    
    pc = RTCPeerConnection()
    
    # # 加载并更新图片
    # image = args.play_from
    # logger.info(f"Loading image from {image}")
    # if not os.path.exists(image):
    #     logger.error(f"Image file not found: {image}")
    #     return
    # player = MediaPlayer(image)
    # # 添加轨道到peer connection
    # pc.addTrack(player.video)
    logger.info(f"Loading image from {args.play_from}")
    video_track = OptimizedImageTrack()
    video_track.get_image(args.play_from)
    pc.addTrack(video_track)
    logger.info(f"Added video track to peer connection")

    

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    
    return web.Response(
        content_type="application/json",
        text=json.dumps({
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        })
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebRTC webcam demo")
    # make args play_from required
    parser.add_argument("--play-from", required=True, help="Read the media from a file and play it")

    args = parser.parse_args()

    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)
    
    web.run_app(app, host="0.0.0.0", port=8080)