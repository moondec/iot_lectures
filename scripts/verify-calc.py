#!/usr/bin/env python3
"""Weryfikacja liczbowa wszystkich obliczeń użytych na slajdach.
Uruchomienie:  python3 scripts/verify-calc.py
Każda liczba pokazana na slajdzie musi wynikać z tego pliku."""
import json, sys

out = {}

# --- 1. Budżet energii węzła bateryjnego (wykład 02) ---------------------
def i_sr(i_act_ma, t_s, i_sleep_ma, T_s):
    """Średni prąd cyklu pracy [mA]."""
    return (i_act_ma * t_s + i_sleep_ma * (T_s - t_s)) / T_s

I_ACT, T_ACT, I_SLEEP = 120.0, 3.0, 0.05      # mA, s, mA
T_CYCLE = 15 * 60                              # s  (raport co 15 min)
isr = i_sr(I_ACT, T_ACT, I_SLEEP, T_CYCLE)
q_rok = isr * 24 * 365                         # mAh/rok
out["energia_15min"] = {
    "I_akt_mA": I_ACT, "t_akt_s": T_ACT, "I_sleep_mA": I_SLEEP, "T_s": T_CYCLE,
    "I_sr_mA": round(isr, 4), "Q_rok_mAh": round(q_rok, 1),
}
# ogniwa (dane katalogowe typowe)
CR2032, LI18650 = 220.0, 3400.0                # mAh
out["energia_15min"]["CR2032_h"] = round(CR2032 / isr, 1)
out["energia_15min"]["CR2032_dni"] = round(CR2032 / isr / 24, 1)
out["energia_15min"]["18650_h"] = round(LI18650 / isr, 1)
out["energia_15min"]["18650_miesiecy"] = round(LI18650 / isr / 24 / 30.44, 1)

# wpływ okresu raportowania oraz wynikający czas pracy ogniwa 3400 mAh
okresy_min = (1, 5, 15, 30, 60)
prady_okres = {m: i_sr(I_ACT, T_ACT, I_SLEEP, m * 60) for m in okresy_min}
out["energia_okres"] = {f"{m}min": round(prady_okres[m], 4) for m in okresy_min}
out["energia_okres_czas_3400mAh"] = {
    f"{m}min": {
        "dni": round(LI18650 / prady_okres[m] / 24, 1),
        "miesiace_30_44d": round(LI18650 / prady_okres[m] / 24 / 30.44, 1),
        "lata_365d": round(LI18650 / prady_okres[m] / 24 / 365, 2),
    }
    for m in okresy_min
}
# ile trzeba, by jedno 18650 dało rok pracy
out["energia_prog_rok_18650_mA"] = round(LI18650 / (24 * 365), 4)
assert out["energia_15min"]["I_sr_mA"] == 0.4498
assert out["energia_15min"]["Q_rok_mAh"] == 3940.5
assert out["energia_15min"]["CR2032_dni"] == 20.4
assert out["energia_15min"]["18650_miesiecy"] == 10.3
assert out["energia_okres"]["5min"] == 1.2495
assert out["energia_okres_czas_3400mAh"]["5min"]["miesiace_30_44d"] == 3.7
assert out["energia_okres_czas_3400mAh"]["30min"]["lata_365d"] == 1.55

# --- 2. Sprostowanie: liczba 0,19 mA z materiałów kursu ------------------
out["sprostowanie_019"] = {
    "wartosc_w_materiale_mA": 0.19,
    "wartosc_wyliczona_mA": round(isr, 4),
    "zgodna": abs(0.19 - isr) < 0.01,
    "komentarz": "0,19 mA nie wynika z podanych danych wejsciowych; poprawna wartosc ~0,45 mA",
}

# --- 4. Tempo wydania OTA w ThingsBoard (wykład 03) ---------------------
PACK, INTERVAL_MS = 100, 60_000
def czas_wydania_gorny(n_dev):
    """Konserwatywne górne ograniczenie: liczba pełnych okien wysyłki."""
    import math
    return math.ceil(n_dev / PACK) * INTERVAL_MS / 1000.0

def czas_wydania_sredni(n_dev):
    """Model średniego tempa używany w dokumentacji ThingsBoard."""
    return n_dev / PACK * INTERVAL_MS / 1000.0

out["ota_tempo"] = {
    "pack_size": PACK, "interval_ms": INTERVAL_MS,
    "gorne_s_dla_1": czas_wydania_gorny(1),
    "gorne_s_dla_100": czas_wydania_gorny(100),
    "gorne_s_dla_240": czas_wydania_gorny(240),
    "gorne_s_dla_250": czas_wydania_gorny(250),
    "gorne_min_dla_1000": czas_wydania_gorny(1000) / 60,
    "srednie_s_dla_240": czas_wydania_sredni(240),
}
assert out["ota_tempo"]["gorne_s_dla_250"] == 180.0
assert out["ota_tempo"]["gorne_min_dla_1000"] == 10.0
assert out["ota_tempo"]["srednie_s_dla_240"] == 144.0

# --- 5. Próg nieaktywności vs okres raportowania (wykład 06) ------------
REPORT_TIMEOUT_MS = 3000     # TB_TRANSPORT_SESSIONS_REPORT_TIMEOUT
SESSION_INACTIVITY_TIMEOUT_MS = 300_000
out["nieaktywnosc"] = {
    "report_timeout_ms": REPORT_TIMEOUT_MS,
    "min_prog_s": REPORT_TIMEOUT_MS / 1000,
    "domyslny_prog_s": 600, "interwal_sprawdzania_s": 60,
    "prog_laboratoryjny_ms": 60_000,
    "prog_laboratoryjny_s": 60,
    "session_inactivity_timeout_ms": SESSION_INACTIVITY_TIMEOUT_MS,
    "zapas_krotnosc": round(60 / (REPORT_TIMEOUT_MS / 1000), 1),
}
assert out["nieaktywnosc"]["min_prog_s"] == 3.0
assert out["nieaktywnosc"]["zapas_krotnosc"] == 20.0
assert out["nieaktywnosc"]["session_inactivity_timeout_ms"] == 300_000

# --- 6. Koszt energii: człowiek vs samochód (wykład 06) ----------------
KCAL = 3000.0
J_PER_KCAL = 4184.0
mj_czlowiek = KCAL * J_PER_KCAL / 1e6
AUTO_MJ_KM = 2.5
out["energia_rama"] = {
    "kcal_dzien": KCAL, "MJ_dzien": round(mj_czlowiek, 2),
    "kWh_dzien": round(mj_czlowiek / 3.6, 2),
    "auto_MJ_na_km": AUTO_MJ_KM,
    "km_rownowazne_dobie": round(mj_czlowiek / AUTO_MJ_KM, 1),
    "mozg_W": 20,
}
assert out["energia_rama"]["MJ_dzien"] == 12.55
assert out["energia_rama"]["kWh_dzien"] == 3.49
assert out["energia_rama"]["km_rownowazne_dobie"] == 5.0

# --- 7. Narzut nagłówka MQTT (wykład 04) -------------------------------
def publish_bytes(topic, payload_len, qos):
    fixed = 1                                   # typ pakietu + flagi
    remaining = 2 + len(topic.encode()) + (2 if qos > 0 else 0) + payload_len
    rl_bytes = 1
    r = remaining
    while r > 127:
        rl_bytes += 1
        r //= 128
    return fixed + rl_bytes + remaining
# ThingsBoard device API telemetry topic: short form (since 3.5) vs standard form.
t_krotki, t_dlugi = "v2/t", "v1/devices/me/telemetry"
out["mqtt_naglowek"] = {
    "min_fixed_header_B": 2,
    "krotki_temat": t_krotki, "krotki_temat_len": len(t_krotki),
    "dlugi_temat": t_dlugi, "dlugi_temat_len": len(t_dlugi),
    "publish_krotki_qos1_pusty_B": publish_bytes(t_krotki, 0, 1),
    "publish_dlugi_qos1_pusty_B": publish_bytes(t_dlugi, 0, 1),
    "roznica_B": publish_bytes(t_dlugi, 0, 1) - publish_bytes(t_krotki, 0, 1),
}

# Roczny narzut dla przykładu MQTT 3.1.1, bez ACK/TCP/IP/TLS.
# Nie przeliczamy bajtów wprost na czas pracy radia ani energię.
messages_year = 365 * 24 * 60 * 60 // 10
annual_bytes = out["mqtt_naglowek"]["roznica_B"] * messages_year
out["mqtt_naglowek"].update({
    "okres_publikacji_s": 10,
    "dni_roku": 365,
    "komunikaty_rocznie": messages_year,
    "roczny_dodatkowy_publish_B": annual_bytes,
    "roczny_dodatkowy_publish_MB": round(annual_bytes / 1_000_000, 1),
    "roczny_dodatkowy_publish_MiB": round(annual_bytes / 2**20, 1),
})
assert messages_year == 3_153_600
assert out["mqtt_naglowek"]["publish_krotki_qos1_pusty_B"] == 10
assert out["mqtt_naglowek"]["publish_dlugi_qos1_pusty_B"] == 29
assert out["mqtt_naglowek"]["roznica_B"] == 19
assert annual_bytes == 59_918_400
assert out["mqtt_naglowek"]["roczny_dodatkowy_publish_MB"] == 59.9
assert out["mqtt_naglowek"]["roczny_dodatkowy_publish_MiB"] == 57.1

# --- 8. Rozdzielczość ADC ≠ dokładność (wykład 02) ---------------------
out["adc"] = {
    "bity": 12, "kroki": 2 ** 12,
    "LSB_mV_dla_3V3": round(3300 / 2 ** 12, 3),
}
assert out["adc"]["kroki"] == 4096
assert out["adc"]["LSB_mV_dla_3V3"] == 0.806

# --- 8b. Seryjna płytka w uśpieniu i próg roku pracy (wykład 02) -------
# Seryjna Nano ESP32 w deep sleep: ok. 2 mA (dioda zasilania, przetwornica,
# PSRAM); pomiary użytkowników, nie dane producenta.
I_SLEEP_PLYTKA = 2.0                           # mA
isr_plytka = i_sr(I_ACT, T_ACT, I_SLEEP_PLYTKA, T_CYCLE)
prog_rok = LI18650 / (24 * 365)                # mA dla roku z 3400 mAh
T_rok = (I_ACT * T_ACT - I_SLEEP * T_ACT) / (prog_rok - I_SLEEP)
out["energia_plytka_seryjna"] = {
    "I_sleep_mA": I_SLEEP_PLYTKA,
    "I_sr_15min_mA": round(isr_plytka, 3),
    "18650_dni": round(LI18650 / isr_plytka / 24, 1),
    "okres_dla_roku_18650_min": round(T_rok / 60, 1),
}
assert out["energia_plytka_seryjna"]["I_sr_15min_mA"] == 2.393
assert out["energia_plytka_seryjna"]["okres_dla_roku_18650_min"] == 17.7

# --- 9. Paliwo a dobowa energia człowieka (wykład 00) ------------------
# Rachunek z prezentacji źródłowej „Internet przyszłości” (2022).
E5_MJ_KG, E5_KG_L = 43.2, 0.80                 # wartość opałowa, gęstość benzyny
SPALANIE_L_100KM = 7.0
KCAL_MJ = 4.184e-3                              # 1 kcal = 4,184 kJ
e5_mj_l = E5_MJ_KG * E5_KG_L
mj_km = e5_mj_l * SPALANIE_L_100KM / 100
dieta_mj = [k * KCAL_MJ for k in (2500, 3000)]
out["paliwo_czlowiek"] = {
    "E5_MJ_l": round(e5_mj_l, 2),
    "auto_MJ_km": round(mj_km, 3), "auto_kWh_km": round(mj_km / 3.6, 3),
    "czlowiek_MJ_doba": [round(x, 1) for x in dieta_mj],
    "czlowiek_kWh_doba": [round(x / 3.6, 2) for x in dieta_mj],
    "auto_5km_MJ": round(5 * mj_km, 1),
    "km_na_dobe_czlowieka": [round(x / mj_km, 1) for x in dieta_mj],
}
assert out["paliwo_czlowiek"]["E5_MJ_l"] == 34.56
assert out["paliwo_czlowiek"]["auto_kWh_km"] == 0.672
assert out["paliwo_czlowiek"]["czlowiek_MJ_doba"] == [10.5, 12.6]
assert out["paliwo_czlowiek"]["auto_5km_MJ"] == 12.1

json.dump(out, open("provenance/obliczenia.json", "w"), ensure_ascii=False, indent=1)
for k, v in out.items():
    if isinstance(v, dict):
        print(f"[{k}]")
        for kk, vv in v.items():
            print(f"   {kk} = {vv}")
    else:
        print(f"[{k}] = {v}")
print("\nZapisano: provenance/obliczenia.json")
