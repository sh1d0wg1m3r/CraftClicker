import time
import random
import threading
from pynput import mouse, keyboard

# Configuration section
config = {
    'toggle_key': '\\',  # Key to toggle the auto-clicker on/off
    'click_button': mouse.Button.left,  # Button to simulate click
    'min_clicks': 8,  # Minimum number of clicks per activation
    'max_clicks': 9,  # Maximum number of clicks per activation
    'min_delay': 0.038,  # Minimum delay between clicks in seconds
    'max_delay': 0.047,  # Maximum delay between clicks in seconds
    'verbose': True,  # Control print statements for performance
}

class AutoClicker:
    def __init__(self, config):
        self.toggle_key = keyboard.KeyCode(char=config['toggle_key'])
        self.click_button = config['click_button']
        self.min_clicks = config['min_clicks']
        self.max_clicks = config['max_clicks']
        self.min_delay = config['min_delay']
        self.max_delay = config['max_delay']
        self.verbose = config['verbose']
        
        self.clicks_activated = False
        self.listening_for_click = False
        self.mouse_controller = mouse.Controller()
        self.running = True  # This now only controls the main loop, not tied directly to activation status

        # Setup listeners
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)

    def on_press(self, key):
        if key == self.toggle_key:
            self.toggle_clicker()

    def toggle_clicker(self):
        self.clicks_activated = not self.clicks_activated
        self.listening_for_click = self.clicks_activated
        if self.verbose: print(f"AutoClicker {'activated' if self.clicks_activated else 'in standby mode'}")
        # No longer setting self.running to False here

    def on_click(self, x, y, button, pressed):
        if self.clicks_activated and self.listening_for_click and button == self.click_button and pressed:
            self.listening_for_click = False
            threading.Thread(target=self.perform_clicks, daemon=True).start()

    def perform_clicks(self):
        num_clicks = random.randint(self.min_clicks, self.max_clicks)
        for _ in range(num_clicks):
            time.sleep(random.uniform(self.min_delay, self.max_delay))
            self.mouse_controller.click(self.click_button)
            if self.verbose: print("Click!")
        self.listening_for_click = True  # Ready to listen for the next click

    def start(self):
        self.keyboard_listener.start()
        self.mouse_listener.start()
        try:
            while self.running:  # This loop now keeps running regardless of clicks_activated status
                time.sleep(0.1)  # Keep the main thread alive
        except KeyboardInterrupt:
            print("AutoClicker shutting down.")
        finally:
            self.cleanup()

    def cleanup(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

if __name__ == "__main__":
    auto_clicker = AutoClicker(config)
    auto_clicker.start()