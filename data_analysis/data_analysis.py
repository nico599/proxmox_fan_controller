import matplotlib.pyplot as plt

"""
2025-02-03_22-55-45: CPU Temp: 28.000, Fan Speed: 0x0A
2025-02-03_23-11-29: CPU Temp: 27.000, Fan Speed: 0x09
2025-02-03_23-13-45: CPU Temp: 28.000, Fan Speed: 0x0A
2025-02-03_23-18-35: CPU Temp: 27.000, Fan Speed: 0x09
2025-02-03_23-20-45: CPU Temp: 28.000, Fan Speed: 0x0A
"""

hex_to_rpm_mapping = {hex(i): (2400 + ((i - 8) / (32 - 8)) * (5400 - 2400)) for i in range(8, 33)}

timestamps = []
cpu_temperatures = []
fan_speeds_rpm = []

with open ('data.txt', 'r') as file:
    data = file.read()

    data = data.split('\n')

    for entry in data:  
            timestamp = entry.split(': ')[0]
            print(f"timestamp: {timestamp}")
            cpu_temp = float(entry.split(' ')[3][:-1])
            print(f"cpu_temp: {cpu_temp}")
            fan_speed_hex = int(entry.split(' ')[6], 16)
            print(f"fan_speed_hex: {fan_speed_hex}")
            fan_speed_rpm = hex_to_rpm_mapping[hex(fan_speed_hex)]

            timestamps.append(timestamp)
            cpu_temperatures.append(cpu_temp)
            fan_speeds_rpm.append(fan_speed_rpm)

# Plotting the data
fig, ax1 = plt.subplots(figsize=(10, 6))

offset = 2400  # Add this to fan speed to shift it up

# Plotting the data
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot CPU temperature
ax1.set_xlabel('Time')
ax1.set_ylabel('CPU Temperature (°C)', color='tab:red')
ax1.plot(timestamps, cpu_temperatures, color='tab:red', label='CPU Temp', linestyle='-', marker='o')
ax1.tick_params(axis='y', labelcolor='tab:red')

ax1.set_ylim(min(cpu_temperatures) - 0, max(cpu_temperatures) + 10)

# Create a second y-axis to plot Fan Speed (RPM)
ax2 = ax1.twinx()
ax2.set_ylabel('Fan Speed (RPM)', color='tab:blue')
ax2.plot(timestamps, fan_speeds_rpm, color='tab:blue', label='Fan Speed', linestyle='-', marker='x')
ax2.tick_params(axis='y', labelcolor='tab:blue')


ax2.set_ylim(min(fan_speeds_rpm) - 2000, max(fan_speeds_rpm) + 1000)  # Add buffer space

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Title and layout adjustments
plt.title('CPU Temperature and Fan Speed Over Time')
fig.tight_layout()

# Show the plot
plt.show()

# Save the plot

# Save the plot with higher resolution
fig.savefig('plot.png', dpi=72)
