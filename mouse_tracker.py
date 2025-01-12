import csv
from pynput import mouse

output_file = "./dataset/mouse_activity.csv"

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Event", "X", "Y", "Button", "Action"])


def on_move(x, y):
    with open(output_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Move", x, y, None, None])
    print(f"Mouse moved to ({x}, {y})")


def on_click(x, y, button, pressed):
    action = "Pressed" if pressed else "Released"
    with open(output_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Click", x, y, button, action])
    print(f"Mouse {action} at ({x}, {y}) with {button}")


def on_scroll(x, y, dx, dy):
    with open(output_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Scroll", x, y, None, f"({dx}, {dy})"])
    print(f"Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})")


if __name__ == "__main__":
    with mouse.Listener(
        on_move=on_move, on_click=on_click, on_scroll=on_scroll
    ) as listener:
        print("Tracking mouse activity. Press Ctrl+C to stop.")
        listener.join()
