import RPi.GPIO as GPIO
import tkinter as tk

GPIO.setmode(GPIO.BOARD)
relay_pins = [16, 11, 12, 7, 10, 5, 8, 3, 26, 21, 24, 19, 22, 15, 18, 13]

def toggle_relay(relay_pin, status_label):
    GPIO.output(relay_pin, not GPIO.input(relay_pin))
    update_status(relay_pin, status_label)

def setup_gpio():
    for pin in relay_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

def create_button(relay_pin, root, status_label):
    button = tk.Button(root, text=f"Relay {relay_pin + 1}", command=lambda p=relay_pin: toggle_relay(relay_pins[p], status_label))
    button.grid(row=relay_pin // 4, column=relay_pin % 4, padx=10, pady=10)

def update_status(relay_pin, status_label):
    status = "ON" if GPIO.input(relay_pin) == GPIO.LOW else "OFF"
    status_label.config(text=f"Relay {relay_pin + 1}: {status}")

def on_closing():
    GPIO.cleanup()
    root.destroy()

def main():
    try:
        global root
        root = tk.Tk()
        root.title("Relay Control")
        root.attributes('-fullscreen', True)
        root.protocol("WM_DELETE_WINDOW", on_closing)

        setup_gpio()

        status_label = tk.Label(root, text="", font=("Helvetica", 12))
        status_label.grid(row=len(relay_pins) // 4, columnspan=4)

        for i in range(len(relay_pins)):
            create_button(i, root, status_label)
            update_status(relay_pins[i], status_label)

        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
