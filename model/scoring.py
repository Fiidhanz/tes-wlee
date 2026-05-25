def final_score(
    similarity,
    keyword_score,
    preference,
    growth,
    opportunity
):

    return (

        (similarity * 0.30)

        +

        (keyword_score * 0.35)

        +

        (preference * 0.15)

        +

        (growth * 0.10)

        +

        (opportunity * 0.10)

    )