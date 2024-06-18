import pygame.camera
import cv2
import os
import time
from .error_logger_manager import log_error

VIDEO_DIR = "drone_capture/video"
IMAGE_DIR = "drone_capture/img"
LOG_DIR = "drone_capture/log"

os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

record_video_flag = False

def capture_image(camera):
    """Capture an image from the camera and save it as a JPEG file."""
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        img_filename = os.path.join(IMAGE_DIR, f"image_{timestamp}.jpg")
        img = camera.get_image()
        pygame.image.save(img, img_filename)
        print(f"Image captured and saved: {img_filename}")
        return img_filename 
    except Exception as e:
        log_error(f"Error capturing image: {str(e)}")
        return None

def record_video(camera):
    """Record a video from the camera and save it as an AVI file with MJPG codec."""
    global record_video_flag
    
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        video_filename = os.path.join(VIDEO_DIR, f"video_{timestamp}.avi")
        
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  
        fps = 30.0  # Adjust FPS as needed
        frame_size = (camera.get_size()[0], camera.get_size()[1])
        video_out = cv2.VideoWriter(video_filename, fourcc, fps, frame_size)
        
        print(f"Recording video: {video_filename}")
        record_video_flag = True
        
        while record_video_flag:
            img = camera.get_image()
            img_rgb = pygame.surfarray.pixels3d(img)
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            video_out.write(img_bgr)
            
            cv2.imshow('Recording', img_bgr)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        video_out.release()
        cv2.destroyAllWindows()
        
        print(f"Video saved: {video_filename}")
        
        if os.path.exists(video_filename) and os.path.getsize(video_filename) > 0:
            return video_filename
        else:
            log_error(f"Error: Recorded video file '{video_filename}' is empty or missing.")
            return None
    
    except Exception as e:
        log_error(f"Error recording video: {str(e)}")
        return None


def stop_video_recording():
    global record_video_flag
    record_video_flag = False
