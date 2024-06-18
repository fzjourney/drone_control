# media_manager.py

import pygame.camera
import os
import time
from .error_logger_manager import log_error

# Directory paths for media
VIDEO_DIR = "drone_capture/video"
IMAGE_DIR = "drone_capture/img"

def capture_image(camera):
    """Capture an image from the camera and save it."""
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        img_filename = os.path.join(IMAGE_DIR, f"image_{timestamp}.jpg")
        img = camera.get_image()
        pygame.image.save(img, img_filename)
        print(f"Image captured and saved: {img_filename}")
    except Exception as e:
        log_error(f"Error capturing image: {str(e)}")

def record_video(camera):
    """Record a video from the camera and save it."""
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        video_filename = os.path.join(VIDEO_DIR, f"video_{timestamp}.avi")
        camera.start_recording(video_filename)
        print(f"Recording video: {video_filename}")
        # Let it record for 5 seconds
        time.sleep(5)
        camera.stop_recording()
        print(f"Video saved: {video_filename}")
    except Exception as e:
        log_error(f"Error recording video: {str(e)}")