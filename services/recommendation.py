def generate_reason(item):
    return f"Similarity {item['sim']:.2f}, tren {item['growth']*100:.1f}%, density {item['density']}"

CATEGORY_WEIGHTS = {

    "coding & it": 0.95,
    "ai & data": 0.95,
    "tech & gadget": 0.90,
    "edukasi singkat": 0.80,
    "kuliner": 0.75,
    "lifestyle": 0.70,
}

def goal_preference(goal):

    if not goal:
        return 0.5

    goal = str(goal).lower()

    mapping = {

        "python": "coding & it",
        "coding": "coding & it",
        "programming": "coding & it",
        "developer": "coding & it",

        "ai": "ai & data",
        "machine learning": "ai & data",
        "data science": "ai & data",

        "tech": "tech & gadget",
    }

    for key, category in mapping.items():

        if key in goal:

            return CATEGORY_WEIGHTS.get(
                category,
                0.5
            )

    return 0.5