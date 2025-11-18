"# Arduno_mini-with-raspberry-pi-via-I2C" 
#!/usr/bin/env python3
from smbus2 import SMBus
import time

I2C_BUS    = 1      # /dev/i2c-1
SLAVE_ADDR = 0x08

def read_touch():
    with SMBus(I2C_BUS) as bus:
        # read 2 bytes starting at register 0
        data = bus.read_i2c_block_data(SLAVE_ADDR, 0, 2)
    # data[0] = MSB, data[1] = LSB
    return (data[0] << 8) | data[1]

if __name__ == "__main__":
    while True:
        try:
            val = read_touch()
            print(f"Smoothed touch = {val}")
        except Exception as e:
            print("I2C error:", e)
        time.sleep(0.01)
