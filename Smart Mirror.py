import tkinter as tk
from datetime import datetime
import time
import threading

try:
    import Adafruit_DHT
    DHT_AVAILABLE = True
except ImportError:
    DHT_AVAILABLE = False

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False


# -----------------------------
# Configuration
# -----------------------------

DHT_SENSOR = Adafruit_DHT.DHT11 if DHT_AVAILABLE else None
DHT_PIN = 4
PIR_PIN = 17

UPDATE_INTERVAL = 2000


# -----------------------------
# GPIO Setup
# -----------------------------

if GPIO_AVAILABLE:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()
root.title("Smart Mirror")
root.configure(bg="black")
root.attributes("-fullscreen", True)


# -----------------------------
# UI Variables
# -----------------------------

time_var = tk.StringVar()
date_var = tk.StringVar()
temperature_var = tk.StringVar(value="Temperature: -- °C")
humidity_var = tk.StringVar(value="Humidity: -- %")
motion_var = tk.StringVar(value="Motion: --")


# -----------------------------
# UI
# -----------------------------

time_label = tk.Label(
    root,
    textvariable=time_var,
    font=("Helvetica", 72),
    fg="white",
    bg="black"
)

time_label.pack(pady=(60, 10))


date_label = tk.Label(
    root,
    textvariable=date_var,
    font=("Helvetica", 28),
    fg="white",
    bg="black"
)

date_label.pack(pady=10)


info_frame = tk.Frame(root, bg="black")
info_frame.pack(pady=40)


temperature_label = tk.Label(
    info_frame,
    textvariable=temperature_var,
    font=("Helvetica", 28),
    fg="cyan",
    bg="black"
)

temperature_label.pack(pady=10)


humidity_label = tk.Label(
    info_frame,
    textvariable=humidity_var,
    font=("Helvetica", 28),
    fg="cyan",
    bg="black"
)

humidity_label.pack(pady=10)


motion_label = tk.Label(
    root,
    textvariable=motion_var,
    font=("Helvetica", 24),
    fg="gray",
    bg="black"
)

motion_label.pack(pady=20)


# -----------------------------
# Clock
# -----------------------------

def update_clock():
    now = datetime.now()

    time_var.set(now.strftime("%I:%M:%S %p"))
    date_var.set(now.strftime("%A, %d %B %Y"))

    root.after(1000, update_clock)


# -----------------------------
# Sensor Update
# -----------------------------

def update_sensors():
    temperature = None
    humidity = None

    if DHT_AVAILABLE:
        try:
            humidity, temperature = Adafruit_DHT.read_retry(
                DHT_SENSOR,
                DHT_PIN
            )
        except Exception:
            temperature = None
            humidity = None

    if temperature is not None:
        temperature_var.set(
            f"Temperature: {temperature:.1f} °C"
        )

    if humidity is not None:
        humidity_var.set(
            f"Humidity: {humidity:.1f} %"
        )

    if GPIO_AVAILABLE:
        try:
            motion = GPIO.input(PIR_PIN)

            if motion:
                motion_var.set("Motion: Detected")
            else:
                motion_var.set("Motion: None")
        except Exception:
            motion_var.set("Motion: --")

    root.after(UPDATE_INTERVAL, update_sensors)


# -----------------------------
# Exit
# -----------------------------

def close_application(event=None):
    if GPIO_AVAILABLE:
        GPIO.cleanup()

    root.destroy()


root.bind("<Escape>", close_application)


# -----------------------------
# Start
# -----------------------------

update_clock()
update_sensors()

root.mainloop()
