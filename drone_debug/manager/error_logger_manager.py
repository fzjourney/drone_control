import os
import time

# Directory path for log
LOG_DIR = "drone_capture/log"

def log_error(error_message):
    """Log an error message with current date and time."""
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        log_filename = os.path.join(LOG_DIR, "error_log.txt")
        with open(log_filename, "a") as f:
            f.write(f"{timestamp}: {error_message}\n")
        print(f"Error logged: {error_message}")
    except Exception as e:
        print(f"Error logging error: {str(e)}")
