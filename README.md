# Introduction

This is a simple example of how to use aiortc to create a WebRTC server and play a video file in the browser.

# Server

The server is a simple HTTP server that serves the client.js file and handles the WebRTC signaling.

# Installation

```bash
pip install aiortc aiohttp opencv-python
```

# Run

```bash
python -m aiortc_101.examples.server --play-from <path_to_video_file>
```

View the video in the browser at http://localhost:8080/

