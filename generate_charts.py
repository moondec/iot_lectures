import matplotlib.pyplot as plt
import numpy as np

# 1. Line chart for IoT devices (1990-2025)
years = np.array([1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025])
# Estimated data in billions
devices = np.array([0.003, 0.05, 0.2, 0.5, 2, 15, 30, 75])

plt.figure(figsize=(10, 6))
plt.style.use('ggplot')
plt.plot(years, devices, marker='o', linestyle='-', color='#007acc', linewidth=3, markersize=8)
plt.title('Wzrost liczby urządzeń IoT na świecie (1990-2025)', fontsize=16)
plt.xlabel('Rok', fontsize=14)
plt.ylabel('Liczba urządzeń (w miliardach)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
for i, txt in enumerate(devices):
    if i in [0, 4, 7]: # Annotate a few key points
        plt.annotate(f"{txt} mld", (years[i], devices[i] + 2), ha='center')
plt.tight_layout()
plt.savefig('iot_growth_chart.png', dpi=300)
plt.close()

# 2. Bubble chart for protocols
# Data: [Protocol, Range (m, log scale roughly), Bandwidth (kbps, log scale roughly), Power consumption (relative bubble size)]
protocols = ['Wi-Fi', 'Bluetooth (BLE)', 'Zigbee', 'LoRaWAN', 'NB-IoT', '5G']
ranges = [100, 10, 50, 15000, 20000, 1000] # Approximate range in meters
bandwidths = [54000, 1000, 250, 50, 200, 1000000] # Approximate max bandwidth in kbps
power = [800, 50, 100, 20, 150, 1000] # Relative power consumption index

# Use log scale for both axes due to huge differences
fig, ax = plt.subplots(figsize=(12, 8))
plt.style.use('ggplot')

# Use scatter plot with sizes proportional to power consumption
scatter = ax.scatter(ranges, bandwidths, s=[p*3 for p in power], alpha=0.6, 
            c=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#34495e'],
            edgecolors='white', linewidth=2)

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_title('Protokoły IoT: Zasięg vs Przepustowość vs Zużycie Energii (wielkość bąbelka)', fontsize=16)
ax.set_xlabel('Zasięg [metry, skala logarytmiczna]', fontsize=14)
ax.set_ylabel('Przepustowość [kbps, skala logarytmiczna]', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.7)

# Annotate points
for i, txt in enumerate(protocols):
    ax.annotate(txt, (ranges[i], bandwidths[i]), xytext=(0, 10), textcoords='offset points', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('protocols_bubble_chart.png', dpi=300)
plt.close()
