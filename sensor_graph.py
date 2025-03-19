import serial
import matplotlib.pyplot as plt
import time

# Serial port setup (change 'COM3' for Windows or '/dev/ttyUSB0' for Linux)
arduino = serial.Serial('COM14', 9600)
time.sleep(2)

# Data lists for plotting
x_data, co2_data, temp_data, hum_data, mq2_data, ozone_data = [], [], [], [], [], []

# Initialize subplots
plt.ion()
fig, axs = plt.subplots(5, 1, figsize=(8, 12))

start_time = time.time()

while True:
    try:
        data = arduino.readline().decode().strip()

        if "CO2:" in data:
            parts = data.split(", ")
            co2_ppm = int(parts[0].split(": ")[1].split(" ")[0])
            temp = float(parts[1].split(": ")[1].split(" ")[0])
            hum = float(parts[2].split(": ")[1].split(" ")[0])
            mq2 = int(parts[3].split(": ")[1])
            ozone = int(parts[4].split(": ")[1])

            # Append data for plotting
            x_data.append(time.time() - start_time)
            co2_data.append(co2_ppm)
            temp_data.append(temp)
            hum_data.append(hum)
            mq2_data.append(mq2)
            ozone_data.append(ozone)

            # Clear and update each subplot
            axs[0].clear()
            axs[0].plot(x_data, co2_data, marker='o', linestyle='-', color='b')
            axs[0].set_ylabel("CO₂ (PPM)")
            axs[0].set_title("CO₂ Concentration Over Time")

            axs[1].clear()
            axs[1].plot(x_data, temp_data, marker='s', linestyle='-', color='r')
            axs[1].set_ylabel("Temperature (°C)")
            axs[1].set_title("Temperature Over Time")

            axs[2].clear()
            axs[2].plot(x_data, hum_data, marker='^', linestyle='-', color='g')
            axs[2].set_ylabel("Humidity (%)")
            axs[2].set_title("Humidity Over Time")

            axs[3].clear()
            axs[3].plot(x_data, mq2_data, marker='d', linestyle='-', color='m')
            axs[3].set_ylabel("MQ-2 Value")
            axs[3].set_title("Gas Concentration (MQ-2) Over Time")

            axs[4].clear()
            axs[4].plot(x_data, ozone_data, marker='*', linestyle='-', color='c')
            axs[4].set_xlabel("Time (seconds)")
            axs[4].set_ylabel("Ozone Sensor Value")
            axs[4].set_title("Ozone Concentration Over Time")

            plt.tight_layout()
            plt.pause(0.1)

    except KeyboardInterrupt:
        print("Graphing stopped.")
        break

arduino.close()
