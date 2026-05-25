from model.similarity import compute_all

DENSITY_THRESHOLD = 0.6

def content_density(
    trend_vectors,
    content_vectors,
    threshold=DENSITY_THRESHOLD
):

    results = []

    for trend_vec in trend_vectors:

        sims = compute_all(
            trend_vec,
            content_vectors
        )

        density = (
            (sims >= threshold).sum()
            / len(content_vectors)
        )

        results.append(
            round(float(density), 3)
        )

    return results