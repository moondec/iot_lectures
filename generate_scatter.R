library(ggplot2)

# Ensure img directory exists
dir.create("img", showWarnings = FALSE)

# Data definition
techs <- data.frame(
  Name = c('Wi-Fi', 'Bluetooth', 'BLE', 'Zigbee/Z-Wave', 'LoRaWAN', 'NB-IoT', 'Sigfox', '5G (Cellular)'),
  Range = c(50, 10, 30, 100, 15000, 20000, 40000, 5000),
  Bandwidth = c(1e8, 2e6, 1e6, 250000, 5000, 200000, 100, 1e9),
  Power = c(500, 80, 15, 20, 25, 150, 15, 800)
)

# Plotting
p <- ggplot(techs, aes(x = Range, y = Bandwidth)) +
  # Grid lines (major and minor)
  theme_bw() +
  # Bubbles with outline and color scale based on Power consumption
  geom_point(aes(fill = Power, size = Power), shape = 21, color = "#111111", stroke = 1.5, alpha = 0.85) +
  # Custom gradient for hot-to-cold power consumption
  scale_fill_gradientn(
    colors = c("#2ca02c", "#ff7f0e", "#d62728"), # green to orange to red
    name = "Power Consumption /\nPobór prądu [mA]"
  ) +
  # Adjust bubble sizes nicely
  scale_size_continuous(range = c(6, 20), guide = "none") + 
  # Log scale for Range (X axis) with beautiful labels
  scale_x_log10(
    breaks = c(10, 100, 1000, 10000, 100000),
    labels = c("10 m", "100 m", "1 km", "10 km", "100 km")
  ) +
  # Log scale for Bandwidth (Y axis) with beautiful labels
  scale_y_log10(
    breaks = c(100, 1000, 10000, 100000, 1e6, 1e7, 1e8, 1e9),
    labels = c("100 b/s", "1 kb/s", "10 kb/s", "100 kb/s", "1 Mb/s", "10 Mb/s", "100 Mb/s", "1 Gb/s")
  ) +
  # Bold, black labels for each protocol
  geom_text(
    aes(label = Name), 
    fontface = "bold", 
    color = "black", 
    size = 4.2, 
    vjust = -1.5, 
    hjust = 0.5
  ) +
  # Axis labels and Title
  labs(
    title = "IoT Connectivity: Range vs. Bandwidth vs. Power",
    subtitle = "Złoty Trójkąt Łączności IoT: Kompromisy",
    x = "Zasięg / Range [Log]",
    y = "Przepustowość / Bandwidth (Throughput) [Log]"
  ) +
  # Clean high-contrast theme styling
  theme(
    plot.title = element_text(face = "bold", size = 16, color = "black", hjust = 0.5, margin = margin(b = 5)),
    plot.subtitle = element_text(size = 12, color = "#444444", hjust = 0.5, face = "italic", margin = margin(b = 15)),
    axis.title.x = element_text(face = "bold", size = 12, color = "black", margin = margin(t = 10)),
    axis.title.y = element_text(face = "bold", size = 12, color = "black", margin = margin(r = 10)),
    axis.text = element_text(color = "black", size = 10, face = "bold"),
    legend.title = element_text(face = "bold", size = 10, color = "black"),
    legend.text = element_text(color = "black", size = 9, face = "bold"),
    panel.grid.major = element_line(color = "#cccccc", linetype = "dashed"),
    panel.grid.minor = element_line(color = "#e5e5e5", linetype = "dotted"),
    panel.background = element_rect(fill = "#f8f9fa"),
    plot.background = element_rect(fill = "white", color = NA)
  )

# Save plot as high-resolution PNG with solid white background
ggsave("img/scatter_triangle.png", plot = p, width = 10, height = 6.2, dpi = 300, bg = "white")
cat("Successfully generated high-contrast, bilingual scatter plot in img/scatter_triangle.png using R ggplot2!\n")
