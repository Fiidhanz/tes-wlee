import re

# =========================
# TREND GROWTH
# =========================
def trend_growth_from_percentage(value):

    try:

        if value is None:
            return 0.0

        value = str(value).lower().strip()

        # breakout handling
        if "breakout" in value:
            return 1.0

        # ambil angka
        numbers = re.findall(r'\d+', value)

        if not numbers:
            return 0.0

        percent = float(numbers[0])

        # normalisasi skripsi
        growth = min(percent / 10, 100) / 100

        return round(growth, 3)

    except Exception as e:

        print("TREND GROWTH ERROR:", e)

        return 0.0

def classify_trend(growth):
    """
    Klasifikasi tren berdasarkan growth (0–1)
    """
    if growth > 0.3:
        return "Tren Naik"
    elif growth > 0.1:
        return "Tren Stabil"
    else:
        return "Tren Menurun"