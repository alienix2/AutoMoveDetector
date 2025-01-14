import pyautogui
import time
import random

def move_mouse_randomly():
    screen_width, screen_height = pyautogui.size()
    x = random.randint(0, screen_width - 1)
    y = random.randint(0, screen_height - 1)
    pyautogui.moveTo(x, y, duration=random.uniform(0.0, 2))

def random_click():
    click_type = random.choice(['left', 'middle', 'right'])
    print(f"Performing {click_type} click.")
    if click_type == 'left':
        pyautogui.click()
    elif click_type == 'middle':
        pyautogui.middleClick()
    elif click_type == 'right':
        pyautogui.rightClick()

def random_scroll():
    scroll_amount = random.randint(-50, 50)
    print(f"Performing scroll with amount: {scroll_amount}")
    pyautogui.scroll(scroll_amount)

def perform_random_clicks():
    num_clicks = random.randint(0, 30)
    for _ in range(num_clicks):
        random_click()
        time.sleep(random.uniform(0.0, 0.5))

def perform_random_scrolls():
    num_scrolls = random.randint(0, 3)
    for _ in range(num_scrolls):
        random_scroll()
        time.sleep(random.uniform(0.1, 0.5))

if __name__ == "__main__":
    while True:
        move_mouse_randomly()
        perform_random_clicks()
        perform_random_scrolls()
        time.sleep(random.uniform(0, 5))
