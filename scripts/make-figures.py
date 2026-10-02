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

# --- Rys. 2: limit zapisów Google Sheets ------------------------------
s = CALC["sheets"]
etykiety = ["1 komunikat\nna sekundę", "1 komunikat\nna 10 s",
            "agregat\n1 wiersz/min", "agregat\n1 wiersz/5 min"]
zapisy = [60, 6, 1, 0.2]
fig, ax = plt.subplots(figsize=(10, 5.6))
kolory = [WARN if z >= s["limit_user_min"] else ACC for z in zapisy]
bars = ax.bar(etykiety, zapisy, color=kolory, width=0.58, zorder=3)
ax.axhline(s["limit_user_min"], ls="--", lw=2.5, color=WARN, zorder=4,
           label=f"limit użytkownika: {s['limit_user_min']} zapisów/min")
ax.set_yscale("log")
ax.set_ylim(0.1, 320)
ax.set_ylabel("Zapisy do arkusza na minutę\n(jedno urządzenie, skala log.)")
ax.set_title("Dlaczego brzeg agreguje, zamiast przepisywać każdy komunikat", pad=14)
ax.grid(True, axis="y", which="both", ls=":", color=GRID, zorder=1)
for b, z in zip(bars, zapisy):
    ax.text(b.get_x() + b.get_width() / 2, z * 1.22,
            f"{z:g}", ha="center", fontsize=14, color=TXT, zorder=5)
ax.legend(loc="upper center", frameon=True, fontsize=13, ncol=1)
fig.text(0.01, 0.01,
         "Limity wg dokumentacji Google Sheets API v4: 60 zapisów/min na użytkownika, "
         "300 zapisów/min na projekt. Przekroczenie → HTTP 429.",
         fontsize=10.5, color="#5a646e")
fig.tight_layout(rect=[0, 0.035, 1, 1])
fig.savefig(f"{OUT}/sheets-limit.png", dpi=170)
plt.close(fig)
print("OK assets/img/sheets-limit.png")
