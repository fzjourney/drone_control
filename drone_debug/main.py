import sys
import pygame
import time
import threading
from manager.joystick_manager import JoystickManager
from manager.display_manager import DisplayManager
from manager.media_manager import capture_image, record_video, stop_video_recording

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

BUTTON_CAPTURE_IMAGE = 2  
BUTTON_RECORD_VIDEO = 3  
BUTTON_STOP_VIDEO = 5

BUTTON_NAMES = {
    0: "middle button (1)",
    1: "button 2",
    2: "button 3",
    3: "button 4",
    4: "button 5",
    5: "button 6",
    6: "button 7",
    7: "button 8",
    8: "button 9",
    9: "button 10",
    10: "button 11",
    11: "button 12"
}

AXIS_NAMES = {
    0: "X Axis",
    1: "Y Axis",
    2: "Diagonal Axis",
    3: "Zoom in/out"
}

def record_video_task(camera):
    record_video(camera)

def main():
    try:
        pygame.init()
        pygame.camera.init()

        joystick_manager = JoystickManager()
        display_manager = DisplayManager()

        camera = pygame.camera.Camera(pygame.camera.list_cameras()[0]) 
        camera.start()

        record_thread = None

        while True:
            display_manager.clear_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            axes_values = joystick_manager.get_axes()
            buttons_state = joystick_manager.get_buttons()

            for i in range(joystick_manager.get_axis_count()):
                axis_value = axes_values[i]
                display_manager.draw_text(f"{AXIS_NAMES.get(i, f'Axis {i}')} value: {axis_value:.2f}", (20, 20 + i * 30))

            for i in range(joystick_manager.get_button_count()):
                button_state = buttons_state[i]
                display_manager.draw_text(f"{BUTTON_NAMES.get(i, f'Button {i}')} : {button_state}", (20, 140 + i * 30))

            display_manager.draw_axes(axes_values)
            display_manager.update_display()

            if buttons_state[BUTTON_CAPTURE_IMAGE]:
                img_filename = capture_image(camera)
                if img_filename:
                    print(f"Captured image: {img_filename}")

            if buttons_state[BUTTON_RECORD_VIDEO] and record_thread is None:
                record_thread = threading.Thread(target=record_video_task, args=(camera,))
                record_thread.start()

            if buttons_state[BUTTON_STOP_VIDEO] and record_thread is not None:
                stop_video_recording()
                record_thread.join() 
                record_thread = None
                print("Video recording stopped")

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        camera.stop()
        pygame.quit()

if __name__ == "__main__":
    main()
