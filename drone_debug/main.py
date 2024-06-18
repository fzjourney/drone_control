# main.py

import sys
import pygame
import time
from manager.joystick_manager import JoystickManager
from manager.display_manager import DisplayManager
from manager.media_manager import capture_image, record_video

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

BUTTON_CAPTURE_IMAGE = 2  
BUTTON_RECORD_VIDEO = 3  

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

def main():
    try:
        pygame.init()
        pygame.camera.init()

        joystick_manager = JoystickManager()
        display_manager = DisplayManager()

        # Initialize Camera
        camera = pygame.camera.Camera(pygame.camera.list_cameras()[0])  # Assuming only one camera connected
        camera.start()

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

            # Handle media capture based on joystick button presses
            if buttons_state[BUTTON_CAPTURE_IMAGE]:
                img_filename = capture_image(camera)
                if img_filename:
                    print(f"Captured image: {img_filename}")

            if buttons_state[BUTTON_RECORD_VIDEO]:
                video_filename = record_video(camera)
                if video_filename:
                    print(f"Recording video: {video_filename}")

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Clean up
        camera.stop()
        pygame.quit()

if __name__ == "__main__":
    main()
