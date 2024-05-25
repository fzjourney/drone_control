import sys
import pygame
import time

# Initialize Pygame and Joystick
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick found")
    sys.exit("No joystick found")

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick name: {joystick.get_name()}")

# Previous axis states to detect changes
prev_axes = [0.0] * joystick.get_numaxes()

# Mapping joystick buttons and axes
def handle_joystick_input():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
                if event.button == 0:  # Example button 0
                    print("Example action for button 0 (Takeoff)")
                elif event.button == 1:  # Example button 1
                    print("Example action for button 1 (Land)")
                # Add more button mappings as needed

            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released")

        # Read joystick axes
        for i in range(joystick.get_numaxes()):
            axis_value = joystick.get_axis(i)
            if abs(axis_value - prev_axes[i]) > 0.01:  # Threshold to avoid noise
                print(f"Axis {i} value: {axis_value:.2f}")
                prev_axes[i] = axis_value

        time.sleep(0.1)

# Run the joystick input handler
try:
    handle_joystick_input()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    pygame.quit()
