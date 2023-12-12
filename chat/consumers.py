# your_app/consumers.py

import cv2
import asyncio
import websockets
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def video_processing(self, websocket):
        # Open the video stream (replace 'your_mpeg_url' with the actual MPEG URL)
        cap = cv2.VideoCapture('http://192.168.0.2:8080/')

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Convert the frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Send the grayscale frame to the WebSocket
            await websocket.send(gray_frame.tobytes())

            # Adjust the delay based on your video frame rate
            await asyncio.sleep(0.1)

        cap.release()

    async def receive(self, text_data):
        websocket_url = 'ws://127.0.0.1:8000/ws/video/processed/'
        
        # Start the video processing within the consumer
        await self.video_processing(self.channel_layer.get('websocket.receive'))
