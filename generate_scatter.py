import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure img dir exists
os.makedirs('img', exist_ok=True)

# Use clean default style
plt.style.use('default')
fig, ax = plt.subplots(figsize=(10, 6.2), facecolor='white')
ax.set_facecolor('#f8f9fa')

# Data: [Range (m), Bandwidth (bps), Power (mA scale)]
techs = {
    'Wi-Fi': [50, 1e8, 500],
    'Bluetooth': [10, 2e6, 80],
    'BLE': [30, 1e6, 15],
    'Zigbee/Z-Wave': [100, 250000, 20],
    'LoRaWAN': [15000, 5000, 25],
    'NB-IoT': [20000, 200000, 150],
    'Sigfox': [40000, 100, 15],
    '5G (Cellular)': [5000, 1e9, 800]
}

x = [v[0] for v in techs.values()]
y = [v[1] for v in techs.values()]
sizes = [v[2]*1.5 for v in techs.values()] # scale for bubble sizes

# Create scatter plot
scatter = ax.scatter(x, y, s=sizes, alpha=0.85, c=[v[2] for v in techs.values()], cmap='YlOrRd', edgecolors='#111111', linewidths=1.5)

# Annotate each technology label in bold black
for i, txt in enumerate(techs.keys()):
    ax.annotate(txt, (x[i], y[i]), xytext=(12, 0), textcoords='offset points', color='black', fontsize=11, fontweight='bold', va='center')

# Log scales as required by the logarithmic nature of range/bandwidth
ax.set_xscale('log')
ax.set_yscale('log')

# Axis labels and titles in bold black (bilingual)
ax.set_xlabel('Zasięg / Range [m]', fontsize=13, fontweight='bold', color='black', labelpad=10)
ax.set_ylabel('Przepustowość / Bandwidth [b/s]', fontsize=13, fontweight='bold', color='black', labelpad=10)
ax.set_title('IoT Connectivity: Range vs. Bandwidth vs. Power', fontsize=16, fontweight='bold', pad=20, color='black')

# Style ticks
ax.tick_params(colors='black', which='both', labelsize=10)

# Add a colorbar to explain size/color with bold black labels
cbar = plt.colorbar(scatter)
cbar.set_label('Power Consumption / Pobór prądu [mA]', fontsize=11, fontweight='bold', color='black', labelpad=10)
cbar.ax.tick_params(colors='black')

# Grid setup
plt.grid(True, which="both", ls="--", alpha=0.5, color='#cccccc')
plt.tight_layout()

# Save with a solid white background (not transparent) so it is universally high contrast
plt.savefig('img/scatter_triangle.png', transparent=False, dpi=300, facecolor='white')
print("Saved light-themed scatter plot to img/scatter_triangle.png")
