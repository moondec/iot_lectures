import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure img dir exists
os.makedirs('img', exist_ok=True)

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6))

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
sizes = [v[2]*15 for v in techs.values()] 

scatter = ax.scatter(x, y, s=sizes, alpha=0.7, c=sizes, cmap='YlOrRd')

for i, txt in enumerate(techs.keys()):
    ax.annotate(txt, (x[i], y[i]), xytext=(10, 0), textcoords='offset points', color='white', fontsize=11, fontweight='bold', va='center')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Zasięg [Metry]', fontsize=12)
ax.set_ylabel('Przepustowość [b/s]', fontsize=12)
ax.set_title('Złoty Trójkąt Łączności IoT: Kompromisy', fontsize=16, fontweight='bold', pad=20)

# Add a colorbar to explain size/color
cbar = plt.colorbar(scatter)
cbar.set_label('Zużycie Energii (szacunkowe)', fontsize=12)

plt.grid(True, which="both", ls="--", alpha=0.2)
plt.tight_layout()
plt.savefig('img/scatter_triangle.png', transparent=True, dpi=300)
print("Saved scatter plot to img/scatter_triangle.png")
