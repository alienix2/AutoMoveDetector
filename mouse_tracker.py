import csv
import time
import math
import argparse
from pynput import mouse
from threading import Timer, Thread

output_file_event = "./dataset/mouse_activity"
output_file_aggregated = "./dataset/mouse_activity_aggregated"

last_move_time = None
last_click_time = None
last_scroll_time = None
last_x, last_y = None, None
previous_velocity = None

buffer = {
    "intervals": [],
    "distances": [],
    "velocities": [],
    "accelerations": [],
    "angles": [],
    "left_clicks": 0,
    "right_clicks": 0,
    "middle_clicks": 0,
    "wheel_scrolls": 0
}

aggregation_interval = 1
aggregation_timer = None

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

def write_to_csv(file, data):
    with open(file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)

def aggregate_stats():
    timestamp = get_timestamp()
    print("Aggregating stats...")

    if not buffer["intervals"]:
        buffer["intervals"].append(0)
        buffer["distances"].append(0)
        buffer["velocities"].append(0)
        buffer["accelerations"].append(0)
        buffer["angles"].append(0)

    # Calculate average stats
    avg_interval = sum(buffer["intervals"]) / len(buffer["intervals"])
    avg_distance = sum(buffer["distances"]) / len(buffer["distances"])
    avg_velocity = sum(buffer["velocities"]) / len(buffer["velocities"])
    avg_acceleration = sum(buffer["accelerations"]) / len(buffer["accelerations"])
    avg_angle = sum(buffer["angles"]) / len(buffer["angles"])

    write_to_csv(output_file_aggregated, [timestamp, avg_distance, avg_velocity, avg_acceleration, avg_angle, buffer["left_clicks"], buffer["right_clicks"], buffer["middle_clicks"], buffer["wheel_scrolls"], label])

    print(f"Aggregated Data: {avg_interval:.6f}s | Avg Distance: {avg_distance:.2f} | Avg Velocity: {avg_velocity:.2f} | Avg Acceleration: {avg_acceleration:.2f} | Avg Angle: {avg_angle:.2f} | Left Clicks: {buffer['left_clicks']} | Right Clicks: {buffer['right_clicks']} | Middle Clicks: {buffer['middle_clicks']} | Wheel Scrolls: {buffer['wheel_scrolls']}")

    buffer["intervals"].clear()
    buffer["distances"].clear()
    buffer["velocities"].clear()
    buffer["accelerations"].clear()
    buffer["angles"].clear()
    buffer["left_clicks"] = 0
    buffer["right_clicks"] = 0
    buffer["middle_clicks"] = 0
    buffer["wheel_scrolls"] = 0

    start_aggregation_timer()

def start_aggregation_timer():
    global aggregation_timer
    aggregation_timer = Timer(aggregation_interval, aggregate_stats)
    aggregation_timer.start()

def start_timer_thread():
    timer_thread = Thread(target=start_aggregation_timer)
    timer_thread.daemon = True
    timer_thread.start()

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

    if interval is not None:
        buffer["intervals"].append(interval)
    buffer["distances"].append(distance)
    buffer["velocities"].append(velocity)
    buffer["accelerations"].append(acceleration)
    buffer["angles"].append(angle)

    write_to_csv(output_file_event, [timestamp, "Move", x, y, None, None, interval, distance, velocity, acceleration, angle, label])

    interval_str = f"{interval:.6f}" if interval is not None else "N/A"
    print(f"[{timestamp}] Mouse moved to ({x}, {y}), interval: {interval_str} s, distance: {distance:.2f}, velocity: {velocity:.2f}, acceleration: {acceleration:.2f}, angle: {angle:.2f}")

def on_click(x, y, button, pressed):
    global last_click_time
    timestamp = get_timestamp()
    action = "Pressed" if pressed else "Released"
    interval = time_diff(last_click_time)
    last_click_time = time.time()

    if pressed:
        if button == mouse.Button.left:
            buffer["left_clicks"] += 1
        elif button == mouse.Button.right:
            buffer["right_clicks"] += 1
        elif button == mouse.Button.middle:
            buffer["middle_clicks"] += 1

    write_to_csv(output_file_event, [timestamp, "Click", x, y, button, action, interval, None, None, None, None, label])

    interval_str = f"{interval:.6f}" if interval is not None else "N/A"
    print(f"[{timestamp}] Mouse {action} at ({x}, {y}) with {button}, interval: {interval_str} s")

def on_scroll(x, y, dx, dy):
    global last_scroll_time
    timestamp = get_timestamp()
    interval = time_diff(last_scroll_time)
    last_scroll_time = time.time()

    buffer["wheel_scrolls"] += 1

    write_to_csv(output_file_event, [timestamp, "Scroll", x, y, None, f"({dx}, {dy})", interval, None, None, None, None, label])

    interval_str = f"{interval:.6f}" if interval is not None else "N/A"
    print(f"[{timestamp}] Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy}), interval: {interval_str} s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track mouse activity and save it to CSV files.")
    parser.add_argument("--label", type=str, required=True, choices=["normal", "anomaly"],
                        help="Set the label for the recorded data (e.g., 'normal' or 'anomaly').")
    args = parser.parse_args()
    label = args.label

    output_file_event += "_" + label + ".csv"
    with open(output_file_event, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Event", "X", "Y", "Button", "Action", "Interval", "Distance", "Velocity", "Acceleration", "Angle", "Label"])

    output_file_aggregated += "_" + label + ".csv"
    with open(output_file_aggregated, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Avg Distance", "Avg Velocity", "Avg Acceleration", "Avg Angle", "Left Clicks", "Right Clicks", "Middle Clicks", "Wheel Scrolls", "Label"])

    start_timer_thread()

    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        print(f"Tracking mouse activity with label '{label}'. Press Ctrl+C to stop.")
        listener.join()
