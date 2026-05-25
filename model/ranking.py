def rank_dataframe(
    df,
    score_column='score',
    top_n=10
):

    return df.sort_values(
        by=score_column,
        ascending=False
    ).head(top_n)