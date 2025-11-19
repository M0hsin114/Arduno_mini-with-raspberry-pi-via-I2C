#!/usr/bin/env python3
import time
from smbus2 import SMBus
import matplotlib.pyplot as plt
import matplotlib.animation as animation

I2C_BUS    = 1
SLAVE_ADDR = 0x08

# --- Your read function ---
def read_touch():
    with SMBus(I2C_BUS) as bus:
        data = bus.read_i2c_block_data(SLAVE_ADDR, 0, 2)
    return (data[0] << 8) | data[1]

# --- Data buffer for last 100 values ---
history = [0] * 100

# --- Matplotlib setup ---
fig, ax = plt.subplots()
line, = ax.plot(history)
ax.set_ylim(0, 1023)  # adjust based on your sensor range
ax.set_xlim(0, 100)
ax.set_xlabel("Sample index")
ax.set_ylabel("Touch value")
ax.set_title("Live I2C Touch Sensor Graph (Scrolling)")

# --- Animation update function ---
def update(frame):
    global history

    try:
        value = read_touch()
    except Exception as e:
        print("I2C error:", e)
        value = 0

    # Add new value, keep last 100 samples
    history.append(value)
    history = history[-100:]

    line.set_ydata(history)
    return line,

# --- Start animation ---
ani = animation.FuncAnimation(fig, update, interval=10)  # ~100 Hz
plt.show()
