def opportunity_index(
    growth,
    density
):

    return growth * (1 - density)

def normalize_oi(value):

    return max(
        0.0,
        min(float(value), 1.0)
    )

def interpret_opportunity(
    growth,
    density
):

    oi = opportunity_index(
        growth,
        density
    )

    if oi >= 0.7:
        return "Peluang Tinggi"

    elif oi >= 0.4:
        return "Peluang Sedang"

    return "Peluang Rendah"