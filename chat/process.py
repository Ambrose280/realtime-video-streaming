import cv2
import asyncio
import websockets
import logging  # Import the logging module
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)  # Create a logger instance

class Command(BaseCommand):
    help = 'Process video stream and broadcast to WebSocket'

    async def video_processing(self, websocket):
        cap = cv2.VideoCapture('196.168.x.x')

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            await websocket.send(gray_frame.tobytes())

            await asyncio.sleep(0.1)

        cap.release()

    def handle(self, *args, **options):
        logger.info("Starting video processing")  # Log a message when the command starts

        try:
            asyncio.get_event_loop().run_until_complete(
                websockets.serve(self.video_processing, 'ws://127.0.0.1:8000/ws/video/processed/', 8765)
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")  # Log an error if an exception occurs

        logger.info("Video processing completed")  # Log a message when the command completes
        asyncio.get_event_loop().run_forever()
