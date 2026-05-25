import pandas as pd

from extensions import db

from utils.preprocessing import full_preprocess

from model.embedding import embed

from model.similarity import compute_all

from model.density import content_density

from model.opportunity import (
    opportunity_index,
    normalize_oi,
    interpret_opportunity
)

from model.trend import (
    trend_growth_from_percentage,
    classify_trend
)

from model.scoring import final_score

from model.ranking import rank_dataframe

from services.generator import (
    generate_content_idea,
    detect_category
)

# =========================
# CATEGORY WEIGHTS
# =========================
CATEGORY_WEIGHTS = {

    "meme & humor": 1.0,
    "hiburan viral": 0.91,
    "tech & gadget": 0.90,
    "kuliner": 0.84,
    "lifestyle": 0.82,
    "daily vlog": 0.79,
    "game": 0.69,
    "health & fitness": 0.66,
    "fashion / ootd": 0.61,
    "travel": 0.61,
    "self improvement": 0.59,
    "edukasi singkat": 0.58,
    "beauty & skincare": 0.57,
    "bisnis online": 0.56,
    "edukasi kampus": 0.49,
    "coding & it": 0.88,
    "motivasi & quotes": 0.35,
    "ai & data": 0.95,
}

# =========================
# GENERIC WORDS
# =========================
GENERIC_WORDS = {

    "tutorial",
    "edukasi",
    "belajar",
    "online",
    "tips",
    "cara",
    "panduan",
    "konten",
    "menarik",
    "viral",
    "trend",
    "video",
    "shorts",
    "fyp",
    "tiktok",
    "youtube",
    "instagram",
    "pemula",
    "dasar",
    "mudah",
    "simple",
    "cepat",
    "lengkap",
    "step",
    "step-by-step",

}

# =========================
# BAD PATTERNS
# =========================
BAD_PATTERNS = [

    r'png',
    r'logo',
    r'wallpaper',
    r'vector',
    r'apartments',
    r'travel lifestyle',
    r'http',
    r'www',
    r'\.com',
    r'\d{4,}',
    r'xlme',
    r'cyou',
    r'slot',
    r'casino',
    r'judi',
    r'bet',
    r'gacor',
]

# =========================
# GOAL PREFERENCE
# =========================
def goal_preference(goal):

    if not goal:
        return 0.5

    goal = str(goal).lower().strip()

    keyword_map = {

        "ai": "ai & data",
        "artificial intelligence": "ai & data",
        "machine learning": "ai & data",
        "chatgpt": "ai & data",
        "data science": "ai & data",

        "coding": "coding & it",
        "programming": "coding & it",
        "python": "coding & it",
        "developer": "coding & it",

        "tech": "tech & gadget",
        "gadget": "tech & gadget",
        "smartphone": "tech & gadget",

        "food": "kuliner",
        "makanan": "kuliner",

        "fashion": "fashion / ootd",
        "ootd": "fashion / ootd",

        "fitness": "health & fitness",
        "gym": "health & fitness",

        "travel": "travel",

        "motivasi": "motivasi & quotes",

        "game": "game",

        "humor": "meme & humor",
        "meme": "meme & humor",
    }

    for keyword, category in keyword_map.items():

        if keyword in goal:
            return CATEGORY_WEIGHTS.get(category, 0.5)

    return 0.5


# =========================
# KEYWORD BOOST
# =========================
def keyword_boost(user_query, trend_text):

    user_words = set(
        str(user_query).lower().split()
    )

    trend_words = set(
        str(trend_text).lower().split()
    )

    user_words = user_words - GENERIC_WORDS

    if not user_words:
        return 0.0

    overlap = user_words.intersection(
        trend_words
    )

    return len(overlap) / len(user_words)


# =========================
# STRICT FILTER
# =========================
def strict_keyword_match(user_query, text):

    user_words = set(
        str(user_query).lower().split()
    )

    text_words = set(
        str(text).lower().split()
    )

    user_words = user_words - GENERIC_WORDS

    if len(user_words) == 0:
        return False

    overlap = user_words.intersection(
        text_words
    )

    ratio = (
        len(overlap)
        / len(user_words)
    )

    return ratio >= 0.5


# =========================
# VALID TOPIC
# =========================
def is_valid_topic(text):

    text = str(text).lower().strip()

    if len(text.split()) < 2:
        return False

    generic = {
        "viral",
        "fyp",
        "trend",
        "konten",
        "video",
        "random"
    }

    words = set(text.split())

    if len(words.intersection(generic)) >= 2:
        return False

    pattern = '|'.join(BAD_PATTERNS)

    if pd.Series([text]).str.contains(
        pattern,
        case=False,
        regex=True
    ).iloc[0]:

        return False

    return True


# =========================
# MAIN PIPELINE
# =========================
def run_pipeline(
    keyword,
    platform,
    goal,
    threshold=0.35,
    # =========================
    # CONCEPTUAL PARAMETERS
    # =========================
    intent_strength=0.7,
    trend_bias=0.6,
    novelty_weight=0.5,
    platform_bias=1.0,
    risk_filter=0.5
):

    try:

        # =========================
        # GET TRENDS
        # =========================
        trends = pd.read_sql("""

            SELECT *
            FROM trends_data
            ORDER BY id DESC
            LIMIT 500

        """, db.engine).copy()

        # =========================
        # GET CONTENTS
        # =========================
        contents = pd.read_sql(f"""

            SELECT *
            FROM sosmed_data
            WHERE LOWER(platform)
            LIKE '%%{platform.lower()}%%'

        """, db.engine).copy()

        # =========================
        # GET PREPROCESS
        # =========================
        preprocessed = pd.read_sql("""

            SELECT
                source_id,
                source_type,
                final_text
            FROM preprocessing_data

        """, db.engine)

    except Exception as e:

        print("DB ERROR:", e)

        return {
            "trend_keywords": [],
            "content_ranking": []
        }

    # =========================
    # EMPTY CHECK
    # =========================
    if trends.empty or contents.empty:

        return {
            "trend_keywords": [],
            "content_ranking": []
        }

    # =========================
    # NORMALIZE COLUMN
    # =========================
    trends.columns = trends.columns.str.strip().str.lower()

    contents.columns = (
        contents.columns
        .str.strip()
        .str.lower()
    )

    preprocessed.columns = (
        preprocessed.columns
        .str.strip()
        .str.lower()
    )

    # =========================
    # PREPROCESS TREND
    # =========================
    trend_pre = preprocessed[
        preprocessed['source_type'] == 'trend'
    ]

    trends = trends.merge(

        trend_pre[
            ['source_id', 'final_text']
        ],

        left_on='id',
        right_on='source_id',
        how='left'
    )

    # =========================
    # PREPROCESS CONTENT
    # =========================
    content_pre = preprocessed[
        preprocessed['source_type'] == 'sosmed'
    ]

    contents = contents.merge(

        content_pre[
            ['source_id', 'final_text']
        ],

        left_on='id',
        right_on='source_id',
        how='left'
    )

    # =========================
    # CLEAN TEXT
    # =========================
    trends['final_text'] = (
        trends['final_text']
        .replace('', pd.NA)
    )

    contents['final_text'] = (
        contents['final_text']
        .replace('', pd.NA)
    )

    trends['clean'] = (
        trends['final_text']
        .fillna(trends['trend_query'])
        .fillna('')
        .astype(str)
        .str.lower()
        .str.strip()
    )

    contents['clean'] = (
        contents['final_text']
        .fillna(contents['judul'])
        .fillna('')
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # =========================
    # REMOVE BAD PATTERN
    # =========================
    pattern = '|'.join(BAD_PATTERNS)

    trends = trends[
        ~trends['clean'].str.contains(
            pattern,
            case=False,
            regex=True,
            na=False
        )
    ]

    # =========================
    # VALID TOPIC
    # =========================
    trends = trends[
        trends['clean'].apply(
            is_valid_topic
        )
    ]

    # =========================
    # USER QUERY
    # =========================
    keyword_clean = full_preprocess(
        keyword
    )["final_text"]

    keyword_clean = (
        str(keyword_clean)
        .lower()
        .strip()
    )

    # =========================
    # STRICT FILTER
    # =========================
    filtered_trends = trends[
        trends['clean'].apply(
            lambda x: strict_keyword_match(
                keyword_clean,
                x
            )
        )
    ]

    if len(filtered_trends) >= 3:

        trends = filtered_trends.copy()

    else:

        trends = trends[
            trends['clean'].apply(
                lambda x: keyword_boost(
                    keyword_clean,
                    x
                ) >= 0.1
            )
        ]

    # fallback safety
    if len(trends) == 0:

        trends = filtered_trends.copy()

    # =========================
    # EMBEDDING
    # =========================
    user_vec = embed([
        f"{keyword_clean} | intent:{intent_strength} | trend:{trend_bias} | platform:{platform}"
    ])[0]

    trend_texts = trends[
        'clean'
    ].tolist()

    content_texts = contents[
        'clean'
    ].tolist()

    trend_vecs = embed(
        trend_texts
    )

    content_vecs = embed(
        content_texts
    )

    # =========================
    # SIMILARITY
    # =========================
    trend_sims = compute_all(
        user_vec,
        trend_vecs
    )

    content_sims = compute_all(
        user_vec,
        content_vecs
    )

    trends['sim'] = trend_sims
    contents['sim'] = content_sims

    # =========================
    # CLIP NEGATIVE
    # =========================
    trends['sim'] = trends[
        'sim'
    ].clip(lower=0)

    contents['sim'] = contents[
        'sim'
    ].clip(lower=0)

    # =========================
    # KEYWORD BOOST
    # =========================
    trends['keyword_boost'] = (
        trends['clean']
        .apply(
            lambda x: keyword_boost(
                keyword_clean,
                x
            )
        )
    )

    # =========================
    # TREND FILTER
    # =========================
    trend_mask = trends['sim'] >= threshold

    if trend_mask.sum() < 5:

        soft_threshold = max(
            0.20,
            threshold - 0.10
        )

        trend_mask = (
            trends['sim'] >= soft_threshold
        )

    trends = trends[
        trend_mask
    ].copy()

    if len(trends) < 5:

        trends = trends.sort_values(
            by=['sim', 'keyword_boost'],
            ascending=False
        ).head(10)


    # =========================
    # CONTENT FILTER
    # =========================
    content_mask = (
        contents['sim'] >= threshold
    )

    if content_mask.sum() < 10:

        soft_threshold = max(
            0.20,
            threshold - 0.15
        )

        content_mask = (
            contents['sim'] >= soft_threshold
        )

    contents = contents[
        content_mask
    ].copy()

    if len(contents) < 10:

        contents = contents.sort_values(
            by='sim',
            ascending=False
        ).head(20)

    # =========================
    # TREND GROWTH
    # =========================
    if 'increase_percent' in trends.columns:

        trends['growth_val'] = (
            trends['increase_percent']
            .apply(
                trend_growth_from_percentage
            )
        )

    else:

        trends['growth_val'] = 0.0

    # =========================
    # DENSITY
    # =========================
    filtered_content_vecs = embed(
        contents['clean'].tolist()
    )
    filtered_trend_vecs = embed(
        trends['clean'].tolist()
    )

    densities = content_density(
        filtered_trend_vecs,
        filtered_content_vecs,
        threshold=0.5
    )

    trends['density'] = densities

    # =========================
    # PREFERENCE
    # =========================
    pref = goal_preference(goal)
    # =========================
    # CONCEPTUAL NORMALIZATION
    # =========================
    intent_strength = float(intent_strength)
    trend_bias = float(trend_bias)
    novelty_weight = float(novelty_weight)
    platform_bias = float(platform_bias)
    risk_filter = float(risk_filter)
    # =========================
    # OPPORTUNITY
    # =========================
    trends['oi_raw'] = trends.apply(

        lambda x: opportunity_index(
            x['growth_val'],
            x['density']
        ),

        axis=1
    )

    trends['oi'] = trends[
        'oi_raw'
    ].apply(
        normalize_oi
    )

    # =========================
    # FINAL SCORE
    # =========================
    trends['score'] = trends.apply(

        lambda x: final_score(

            similarity=x['sim'],

            keyword_score=(
                x['keyword_boost']
                * novelty_weight
            ),

            preference=(
                pref
                * platform_bias
            ),

            growth=(
                x['growth_val']
                * trend_bias
            ),

            opportunity=(
                x['oi']
                * (1 - risk_filter)
            )
        ),

        axis=1
    )

    # =========================
    # RANKING
    # =========================
    trends = rank_dataframe(
        trends,
        score_column='score',
        top_n=10
    )

    # =========================
    # FINAL RESULT
    # =========================
    final_results = []

    for _, r in trends.iterrows():

        category = detect_category(
            r.get('clean', '')
        )

        idea = generate_content_idea(
            trend={
                **r.to_dict(),
                "user_keyword": keyword,
                "main_topic": keyword,
                "meta_score": r['score'],
                "meta_score": r['score'],
                "trend_strength": r['growth_val'],
                "trend_density": r['density'],
                "trend_opportunity": r['oi'],
                "trend_similarity": r['sim']
            },
            goal=goal,
            platform=platform,
            category=category,
            real_caption="",
            context_signal={
                "intent_strength": intent_strength,
                "trend_bias": trend_bias,
                "novelty_weight": novelty_weight,
                "platform_bias": platform_bias
            }
        )

        final_results.append({

            "platform": platform,

            "category": category,

            "query": r.get(
                'trend_query',
                r.get('clean', '')
            ),

            "similarity": round(
                float(r['sim']),
                3
            ),

            "keyword_boost": round(
                float(r['keyword_boost']),
                3
            ),

            "growth_val": round(
                float(r['growth_val']),
                3
            ),

            "density": round(
                float(r['density']),
                3
            ),

            "oi": round(
                float(r['oi']),
                3
            ),

            "score": round(
                float(r['score']),
                3
            ),

            "preference_score": round(
                float(pref),
                3
            ),

            "trend_status": classify_trend(
                r['growth_val']
            ),

            "opportunity_label": (
                interpret_opportunity(
                    r['growth_val'],
                    r['density']
                )
            ),

            "title": idea.get(
                "title"
            ),

            "caption": idea.get(
                "caption"
            ),

            "hashtags": idea.get(
                "hashtags"
            ),

            "strategy": idea.get(
                "strategy"
            ),

            "storyboard": idea.get(
                "storyboard"
            ),

            "reasoning": idea.get(
                "reasoning"
            ),

            "content_angle": idea.get(
                "content_angle"
            )
        })

    # =========================
    # CONTENT SCORE
    # =========================
    contents['final_score'] = (

        (contents['sim'] * 0.7)

        +

        (pref * 0.3)
    )

    # =========================
    # CONTENT RANKING
    # =========================
    contents = contents[
        contents['sim'] >= 0.30
    ]
    contents_sorted = rank_dataframe(
        contents,
        score_column='final_score',
        top_n=10
    )

    content_ranking = [

        {

            "title": c.get(
                "judul",
                ""
            ),

            "similarity": round(
                float(
                    c.get("sim", 0)
                ),
                3
            ),

            "final_score": round(
                float(
                    c.get("final_score", 0)
                ),
                3
            )
        }

        for _, c in contents_sorted.iterrows()
    ]

    # =========================
    # RETURN
    # =========================
    return {

        "trend_keywords": final_results,

        "content_ranking": content_ranking
    }