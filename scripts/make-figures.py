#!/usr/bin/env python3
"""Generuje wykresy własne kursu (matplotlib) do assets/img/.
Uruchomienie:  uv run --with matplotlib python scripts/make-figures.py
Dane wejściowe pochodzą wyłącznie z scripts/verify-calc.py."""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
CALC = json.load(open("provenance/obliczenia.json"))
OUT = "assets/img"
os.makedirs(OUT, exist_ok=True)

TXT, GRID, ACC, WARN = "#1f2933", "#c7ccd1", "#0b7285", "#b02a37"
plt.rcParams.update({
    "font.size": 15, "axes.titlesize": 18, "axes.labelsize": 16,
    "text.color": TXT, "axes.labelcolor": TXT,
    "xtick.color": TXT, "ytick.color": TXT,
    "axes.edgecolor": "#6b7680", "figure.facecolor": "white",
    "savefig.facecolor": "white", "font.family": "sans-serif",
})

def i_sr(i_act, t, i_sleep, T):
    return (i_act * t + i_sleep * (T - t)) / T

# --- Rys. 1: średni prąd a okres raportowania --------------------------
e = CALC["energia_15min"]
prog = CALC["energia_prog_rok_18650_mA"]
okresy = [1, 2, 5, 10, 15, 30, 60, 120]
vals = [i_sr(e["I_akt_mA"], e["t_akt_s"], e["I_sleep_mA"], m * 60) for m in okresy]

fig, ax = plt.subplots(figsize=(10, 5.6))
ax.plot(okresy, vals, marker="o", lw=3, ms=9, color=ACC, zorder=3,
        label="prąd średni cyklu")
ax.axhline(prog, ls="--", lw=2.5, color=WARN, zorder=2,
           label=f"próg roku pracy z ogniwa 3400 mAh ({prog:.2f} mA)")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xticks(okresy); ax.set_xticklabels([str(m) for m in okresy])
ax.set_xlabel("Okres raportowania [min]")
ax.set_ylabel("Prąd średni [mA]  (skala log.)")
ax.set_title("Okres raportowania jest decyzją energetyczną")
ax.grid(True, which="both", ls=":", color=GRID, zorder=1)
i15 = okresy.index(15)
ax.annotate(f"{vals[i15]:.2f} mA\n(co 15 min)", xy=(15, vals[i15]),
            xytext=(17, vals[i15] * 3.2), color=TXT, fontsize=14,
            arrowprops=dict(arrowstyle="->", color=TXT, lw=1.6))
ax.legend(loc="upper right", frameon=True, fontsize=13)
fig.text(0.01, 0.01,
         f"Założenia: faza aktywna {e['I_akt_mA']:.0f} mA przez {e['t_akt_s']:.0f} s, "
         f"uśpienie {e['I_sleep_mA']} mA. Wartości dydaktyczne, nie pomiar stanowiska.",
         fontsize=10.5, color="#5a646e")
fig.tight_layout(rect=[0, 0.035, 1, 1])
fig.savefig(f"{OUT}/energia-okres.png", dpi=170)
plt.close(fig)
print("OK assets/img/energia-okres.png")

# --- Rys. 3: paliwo a dobowa energia człowieka (wykład 00) -------------
p = CALC["paliwo_czlowiek"]
lo, hi = p["czlowiek_MJ_doba"]
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.barh(["człowiek:\ndoba ciężkiej pracy", "samochód:\n5 km"], [hi, p["auto_5km_MJ"]],
        color=[ACC, WARN], height=0.55, zorder=3)
ax.barh([0], [lo], color="#5fa8b4", height=0.55, zorder=4)
ax.text(hi + 0.2, 0, f"{lo}–{hi} MJ\n(2500–3000 kcal)".replace(".", ","), va="center", fontsize=14)
ax.text(p["auto_5km_MJ"] + 0.2, 1, f"{p['auto_5km_MJ']} MJ".replace(".", ",") + "\n(ok. 0,35 l benzyny)",
        va="center", fontsize=14)
ax.set_xlim(0, 17)
ax.set_xlabel("Energia [MJ]")
ax.set_title("5 km samochodem ≈ dobowa energia człowieka", pad=12)
ax.grid(True, axis="x", ls=":", color=GRID, zorder=1)
fig.text(0.01, 0.01,
         (f"Benzyna E5: 43,2 MJ/kg, 0,80 kg/l → {p['E5_MJ_l']} MJ/l; spalanie 7 l/100 km "
          f"→ {p['auto_kWh_km']} kWh/km").replace(".", ",") + ". Rachunek: scripts/verify-calc.py.",
         fontsize=10.5, color="#5a646e")
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(f"{OUT}/energia-auto-czlowiek.png", dpi=170)
plt.close(fig)
print("OK assets/img/energia-auto-czlowiek.png")

# --- Rys. 4: liczba aktywnych urządzeń IoT (wykład 00) ------------------
# IoT Analytics, State of IoT 2025: 2024 = szacunek, 2025 i 2030 = prognozy.
lata, mld = ["2024", "2025", "2030"], [18.5, 21.1, 39.0]
fig, ax = plt.subplots(figsize=(10, 5.2))
bars = ax.bar(lata, mld, color=[ACC, "white", "white"], edgecolor=ACC,
              hatch=["", "//", "//"], lw=2.5, width=0.55, zorder=3)
for b, v, opis in zip(bars, mld, ["szacunek", "prognoza", "prognoza"]):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.8, f"{v:g} mld\n{opis}".replace(".", ","),
            ha="center", fontsize=15, color=TXT)
ax.set_ylim(0, 48)
ax.set_ylabel("Aktywne urządzenia IoT [mld]")
ax.set_title("Przyszłość jest już infrastrukturą", pad=12)
ax.grid(True, axis="y", ls=":", color=GRID, zorder=1)
fig.text(0.01, 0.01, "Źródło: IoT Analytics, State of IoT 2025 (28.10.2025). "
         "Kreskowanie = prognoza, nie pomiar.", fontsize=10.5, color="#5a646e")
fig.tight_layout(rect=[0, 0.035, 1, 1])
fig.savefig(f"{OUT}/iot-urzadzenia.png", dpi=170)
plt.close(fig)
print("OK assets/img/iot-urzadzenia.png")

# --- Rys. 5: zasięg a przepustowość technologii radiowych (wykład 03) ---
# Orientacyjne zakresy z dokumentów specyfikacji (IEEE 802.11/802.15.4,
# Bluetooth Core, LoRaWAN RP EU868, 3GPP Rel-13/14, Sigfox); zasięg zależy od terenu.
from matplotlib.patches import Rectangle
TECH = [  # nazwa, zasięg min–max [m], przepustowość min–max [b/s], kolor
    ("Wi-Fi", 30, 100, 1e7, 1.5e8, "#0b7285"),
    ("BLE", 10, 100, 1.25e5, 2e6, "#3b8ea5"),
    ("Zigbee / Thread", 10, 100, 1e5, 2.5e5, "#5fa8b4"),
    ("LTE / 5G", 500, 5000, 1e7, 1e9, "#6b7680"),
    ("LTE-M", 1000, 10000, 1e5, 1e6, "#b8860b"),
    ("NB-IoT", 1000, 10000, 2e4, 1.27e5, "#d4a017"),
    ("LoRaWAN", 2000, 15000, 250, 5500, WARN),
    ("Sigfox", 3000, 40000, 100, 600, "#8f2029"),
]
fig, ax = plt.subplots(figsize=(10, 6))
for n, r0, r1, b0, b1, col in TECH:
    ax.add_patch(Rectangle((r0, b0), r1 - r0, b1 - b0, facecolor=col, alpha=0.35,
                           edgecolor=col, lw=2, zorder=3))
    ax.text((r0 * r1) ** 0.5, (b0 * b1) ** 0.5, n, ha="center", va="center",
            fontsize=13.5, fontweight="bold", color=TXT, zorder=4)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(5, 6e4); ax.set_ylim(50, 3e9)
ax.set_xticks([10, 100, 1000, 10000]); ax.set_xticklabels(["10 m", "100 m", "1 km", "10 km"])
ax.set_yticks([1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9])
ax.set_yticklabels(["100 b/s", "1 kb/s", "10 kb/s", "100 kb/s", "1 Mb/s", "10 Mb/s", "100 Mb/s", "1 Gb/s"])
ax.set_xlabel("Typowy zasięg (skala log.)")
ax.set_ylabel("Przepustowość (skala log.)")
ax.set_title("Zasięg kupujemy za przepustowość", pad=12)
ax.grid(True, which="major", ls=":", color=GRID, zorder=1)
fig.text(0.01, 0.01, "Zakresy orientacyjne wg specyfikacji; rzeczywisty zasięg zależy od terenu, anten i mocy.",
         fontsize=10.5, color="#5a646e")
fig.tight_layout(rect=[0, 0.035, 1, 1])
fig.savefig(f"{OUT}/zasieg-przepustowosc.png", dpi=170)
plt.close(fig)
print("OK assets/img/zasieg-przepustowosc.png")
