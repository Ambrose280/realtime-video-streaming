# consumers.py
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
        # You may process the received text_data if needed
        pass

    async def video_processing(self):
        cap = cv2.VideoCapture('http://192.168.0.2:8080/video')

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Send the grayscale frame to the WebSocket
            await self.send(text_data=gray_frame.tobytes())

            await asyncio.sleep(0.1)

        cap.release()
