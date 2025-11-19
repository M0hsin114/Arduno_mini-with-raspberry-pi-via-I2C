#!/usr/bin/env python3
import time
from smbus2 import SMBus
import matplotlib.pyplot as plt
import matplotlib.animation as animation

I2C_BUS    = 1
SLAVE_ADDR = 0x08

def read_touch():
    with SMBus(I2C_BUS) as bus:
        data = bus.read_i2c_block_data(SLAVE_ADDR, 0, 2)
    return (data[0] << 8) | data[1]

# Keep last 50 values
history = [0] * 50

# Matplotlib setup
plt.style.use("ggplot")
fig, ax = plt.subplots()
line, = ax.plot(history, lw=2)

ax.set_ylim(0, 1023)     # adjust to your sensor range
ax.set_xlim(0, 50)
ax.set_xlabel("Samples")
ax.set_ylabel("Touch Value")
ax.set_title("Live I2C Touch Data (Last 50 Samples)")

# --- VERY FAST UPDATE FUNCTION ---
def update(frame):
    global history

    try:
        value = read_touch()
    except:
        value = 0

    history.append(value)
    history = history[-50:]

    line.set_ydata(history)
    return line,

# Use blitting for speed
ani = animation.FuncAnimation(
    fig, update, interval=5, blit=True
)

plt.show()
