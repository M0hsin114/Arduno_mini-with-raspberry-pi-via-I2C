#!/usr/bin/env python3
import time
from smbus2 import SMBus
import matplotlib.pyplot as plt
import matplotlib.animation as animation

I2C_BUS    = 1
SLAVE_ADDR = 0x08

NUM_CHANNELS = 8
HISTORY_LEN  = 50

# Channels you want to display (0-indexed)
DISPLAY_CHANNELS = [0, 3, 4, 5, 6, 7]

# ---- Read 8 values (each 2 bytes) ----
def read_touch():
    with SMBus(I2C_BUS) as bus:
        raw = bus.read_i2c_block_data(SLAVE_ADDR, 0, NUM_CHANNELS * 2)

    values = []
    for i in range(NUM_CHANNELS):
        high = raw[i*2]
        low  = raw[i*2 + 1]
        val = (high << 8) | low

        # --- clamp the value between 500 and 1000 ---
        if val < 500:
            val = 500
        elif val > 1000:
            val = 1000

        values.append(val)

    return values

# ---- History for selected channels ----
history = {ch: [500] * HISTORY_LEN for ch in DISPLAY_CHANNELS}

# ---- Matplotlib Setup ----
plt.style.use("ggplot")
fig, ax = plt.subplots()

lines = []
colors = ["b", "g", "r", "c", "m", "y", "k", "orange"]

for idx, ch in enumerate(DISPLAY_CHANNELS):
    line, = ax.plot(history[ch], lw=2, label=f"CH{ch+1}", color=colors[idx % len(colors)])
    lines.append(line)

ax.set_ylim(500, 1000)   # new limits
ax.set_xlim(0, HISTORY_LEN)
ax.set_xlabel("Samples")
ax.set_ylabel("Sensor Value (Clamped 500–1000)")
ax.set_title("Live I2C Multichannel Touch Data (Selected Channels)")
ax.legend(loc="upper left")

# ---- Update Loop ----
def update(frame):
    global history

    try:
        values = read_touch()
    except:
        values = [500] * NUM_CHANNELS  # fail-safe default

    # Update each selected channel
    for i, ch in enumerate(DISPLAY_CHANNELS):
        history[ch].append(values[ch])
        history[ch] = history[ch][-HISTORY_LEN:]

        lines[i].set_ydata(history[ch])

    return lines

ani = animation.FuncAnimation(
    fig, update, interval=5, blit=True
)

plt.show()
