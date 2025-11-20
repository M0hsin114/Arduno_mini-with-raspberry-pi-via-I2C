#!/usr/bin/env python3
import time
from smbus2 import SMBus
import matplotlib.pyplot as plt
import matplotlib.animation as animation

I2C_BUS    = 1
SLAVE_ADDR = 0x08

NUM_CHANNELS = 8
HISTORY_LEN  = 50

# ---- Read 8 values (each 2 bytes) ----
def read_touch():
    with SMBus(I2C_BUS) as bus:
        raw = bus.read_i2c_block_data(SLAVE_ADDR, 0, NUM_CHANNELS * 2)

    values = []
    for i in range(NUM_CHANNELS):
        high = raw[i*2]
        low  = raw[i*2 + 1]
        values.append((high << 8) | low)

    return values

# ---- History for each channel ----
history = [[0] * HISTORY_LEN for _ in range(NUM_CHANNELS)]

# ---- Matplotlib Setup ----
plt.style.use("ggplot")
fig, ax = plt.subplots()

lines = []
colors = ["b", "g", "r", "c", "m", "y", "k", "orange"]

for i in range(NUM_CHANNELS):
    line, = ax.plot(history[i], lw=2, label=f"CH{i+1}", color=colors[i % len(colors)])
    lines.append(line)

ax.set_ylim(0, 20000)      # YOU MUST ADJUST THIS TO YOUR SENSOR RANGE
ax.set_xlim(0, HISTORY_LEN)
ax.set_xlabel("Samples")
ax.set_ylabel("Sensor Value")
ax.set_title("Live I2C Multichannel Touch Data")
ax.legend(loc="upper left")

# ---- Update Loop ----
def update(frame):
    global history

    try:
        values = read_touch()   # read 8 channels
    except:
        values = [0] * NUM_CHANNELS

    # Update each history buffer
    for ch in range(NUM_CHANNELS):
        history[ch].append(values[ch])
        history[ch] = history[ch][-HISTORY_LEN:]  # keep last 50

        lines[ch].set_ydata(history[ch])

    return lines

ani = animation.FuncAnimation(
    fig, update, interval=5, blit=True
)

plt.show()
