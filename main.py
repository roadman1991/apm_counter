from pynput.keyboard import Listener as Key_Listener
from pynput.mouse import Listener as Mouse_Listener
from threading import Timer
import logging

# Setup logging
import apm_window

logging.basicConfig(filename="key_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')
minutes_passed = 0
strokes_mouse_and_keyboard = 0
keys = ["minute", "actions"]
list_apm_dict = [dict.fromkeys(keys, None)]


def main():
    with Key_Listener(on_press=on_press) as key_listener:  # Create an instance of Key_Listener
        with Mouse_Listener(on_click=on_click, on_scroll=on_scroll) as mouse_listener:  # Create instance of
            # Mouse_Listener
            apm_window.apm_window()
            start_timer()
            mouse_listener.join()
            key_listener.join()


def on_press(key):  # The function that's called when a key is pressed
    increment_of_key_and_mouse_counter()
    print(key)


def on_click(x, y, button, pressed):
    if pressed:
        increment_of_key_and_mouse_counter()


def on_scroll(x, y, dx, dy):
    increment_of_key_and_mouse_counter()


def timeout():
    increment_minutes_passed()
    logging.info(f"minutes passed: {minutes_passed}, keys_pressed: {strokes_mouse_and_keyboard}")
    values = [minutes_passed, strokes_mouse_and_keyboard]
    new_dict = {keys[0]: values[0], keys[1]: values[1]}
    apm_window.set_apm_text("100")
    list_apm_dict.append(new_dict)
    reset_strokes_mouse_and_keyboard_counter()
    start_timer()


def start_timer():
    t = Timer(1 * 60, timeout)
    t.start()
    t.join()


def increment_of_key_and_mouse_counter():
    global strokes_mouse_and_keyboard
    strokes_mouse_and_keyboard += 1


def increment_minutes_passed():
    global minutes_passed
    minutes_passed += 1


def reset_strokes_mouse_and_keyboard_counter():
    global strokes_mouse_and_keyboard
    strokes_mouse_and_keyboard = 0


if __name__ == '__main__':
    main()
