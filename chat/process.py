# your_app/management/commands/process_video.py

import cv2
import asyncio
import websockets
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Process video stream and broadcast to WebSocket'

    async def video_processing(self, websocket):
        # Open the video stream (replace 'your_mpeg_url' with the actual MPEG URL)
        cap = cv2.VideoCapture('196.168.x.x')

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

    def handle(self, *args, **options):
        asyncio.get_event_loop().run_until_complete(
            websockets.serve(self.video_processing, 'ws://127.0.0.1:8000/ws/video/processed/', 8765)
        )
        asyncio.get_event_loop().run_forever()
