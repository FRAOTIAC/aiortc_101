// 配置 WebRTC
const config = {
    sdpSemantics: 'unified-plan',
    iceServers: [{urls: ['stun:stun.l.google.com:19302']}]
};

// 创建 RTCPeerConnection
const pc = new RTCPeerConnection(config);

// 处理远程视频流
pc.ontrack = function(evt) {
    if (evt.track.kind == 'video') {
        document.getElementById('video').srcObject = evt.streams[0];
    }
};

// 创建 offer 并发送到服务器
async function start() {
    try {
        // 创建空的视频轨道接收器
        pc.addTransceiver('video', {direction: 'recvonly'});

        // 创建 offer
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        // 发送 offer 到服务器
        const response = await fetch('/offer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sdp: pc.localDescription.sdp,
                type: pc.localDescription.type,
            }),
        });

        // 处理服务器返回的 answer
        const answer = await response.json();
        await pc.setRemoteDescription(answer);
    } catch (e) {
        console.error('Error:', e);
    }
}

// 页面加载完成后启动连接
document.addEventListener('DOMContentLoaded', start);