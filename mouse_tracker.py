import csv
import time
import math
from pynput import mouse

output_file = "./dataset/mouse_activity.csv"

last_move_time = None
last_click_time = None
last_scroll_time = None
last_x, last_y = None, None
previous_velocity = None

def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def time_diff(last_time):
    if last_time:
        return time.time() - last_time
    return None

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def calculate_velocity(distance, interval):
    if interval and interval > 0:
        return distance / interval
    return 0

def calculate_acceleration(velocity, prev_velocity, interval):
    if interval and interval > 0:
        return (velocity - prev_velocity) / interval
    return 0

def calculate_angle(x1, y1, x2, y2):
    angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
    return angle

def write_to_csv(data):
    with open(output_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def on_move(x, y):
    global last_move_time, last_x, last_y, previous_velocity
    timestamp = get_timestamp()
    interval = time_diff(last_move_time)
    last_move_time = time.time()

    if last_x is not None and last_y is not None:
        distance = calculate_distance(last_x, last_y, x, y)
        velocity = calculate_velocity(distance, interval)
        acceleration = calculate_acceleration(velocity, previous_velocity, interval)
        angle = calculate_angle(last_x, last_y, x, y)
    else:
        distance = 0
        velocity = 0
        acceleration = 0
        angle = 0

    last_x, last_y = x, y
    previous_velocity = velocity

    write_to_csv([timestamp, "Move", x, y, None, None, interval, distance, velocity, acceleration, angle])

    interval_str = f"{interval:.6f}" if interval is not None else "N/A"
    print(f"[{timestamp}] Mouse moved to ({x}, {y}), interval: {interval_str} s, distance: {distance:.2f}, velocity: {velocity:.2f}, acceleration: {acceleration:.2f}, angle: {angle:.2f}")

def on_click(x, y, button, pressed):
    global last_click_time
    timestamp = get_timestamp()
    action = "Pressed" if pressed else "Released"
    interval = time_diff(last_click_time)
    last_click_time = time.time()

    write_to_csv([timestamp, "Click", x, y, button, action, interval, None, None, None, None])

    interval_str = f"{interval:.6f}" if interval is not None else "N/A"
    print(f"[{timestamp}] Mouse {action} at ({x}, {y}) with {button}, interval: {interval_str} s")

def on_scroll(x, y, dx, dy):
    global last_scroll_time
    timestamp = get_timestamp()
    interval = time_diff(last_scroll_time)
    last_scroll_time = time.time()

    write_to_csv([timestamp, "Scroll", x, y, None, f"({dx}, {dy})", interval, None, None, None, None])

    interval_str = f"{interval:.6f}" if interval is not None else "N/A"
    print(f"[{timestamp}] Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy}), interval: {interval_str} s")

if __name__ == "__main__":
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Event", "X", "Y", "Button", "Action", "Interval", "Distance", "Velocity", "Acceleration", "Angle"])

    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        print("Tracking mouse activity. Press Ctrl+C to stop.")
        listener.join()
