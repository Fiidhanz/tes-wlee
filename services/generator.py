# services/generator.py

import random
import re
# =========================================================
# CATEGORY DETECTOR (SUPER FLEXIBLE)
# =========================================================
def detect_category(topic):

    topic = str(topic).lower().strip()

    keyword_map = {

        "Teknologi & Gadget": [

            # AI & DATA
            "ai", "artificial intelligence", "chatgpt",
            "machine learning", "deep learning", "data science",
            "big data", "neural network", "automation",
            "prompt", "openai", "gemini", "claude",

            # TECH
            "teknologi", "teknologi terbaru", "digital",
            "startup", "software", "hardware",
            "internet", "website", "aplikasi",
            "system", "sistem", "database",
            "cloud", "server", "hosting",

            # PROGRAMMING
            "coding", "programming", "developer",
            "python", "javascript", "java",
            "php", "laravel", "flask",
            "react", "nodejs", "frontend",
            "backend", "fullstack", "ui ux",
            "algoritma", "debugging",

            # DEVICE
            "gadget", "smartphone", "iphone",
            "android", "laptop", "pc",
            "komputer", "kamera", "monitor",
            "gpu", "processor", "robot",
            "cyber", "cybersecurity",
            "smartwatch", "tablet"
        ],

        "Hiburan & Komedi": [

            "meme", "komedi", "lucu", "humor",
            "viral", "prank", "hiburan",
            "funny", "ngakak", "challenge",
            "drama", "parodi", "sketsa",

            # ENTERTAINMENT
            "film", "movie", "anime",
            "series", "netflix", "bioskop",
            "music", "musik", "concert",
            "lagu", "dj", "cover lagu",

            # SOCIAL
            "fyp", "trend", "tiktok viral",
            "reaction", "roasting",
            "story lucu", "random",
            "shitpost", "gaming funny"
        ],

        "Edukasi & Tutorial": [

            "tutorial", "belajar", "tips",
            "edukasi", "how to", "cara",
            "panduan", "kelas", "skill",
            "produktif", "mindset",

            # EDUCATION
            "matematika", "fisika", "kimia",
            "biologi", "sejarah", "kampus",
            "kuliah", "mahasiswa", "skripsi",
            "belajar cepat", "belajar coding",

            # FINANCE
            "investasi", "saham", "crypto",
            "keuangan", "financial",
            "money management",

            # SELF LEARNING
            "self improvement",
            "public speaking",
            "time management",
            "belajar online",
            "produktifitas",
            "career tips"
        ],

        "Fashion & Beauty": [

            "fashion", "outfit", "ootd",
            "style", "aesthetic",
            "beauty", "makeup",
            "skincare", "glow up",

            # BEAUTY
            "lipstick", "serum", "parfum",
            "haircare", "nail art",
            "make over", "bodycare",

            # FASHION
            "streetwear", "thrift",
            "sepatu", "tas", "hoodie",
            "wear", "lookbook",
            "fashion wanita",
            "fashion pria"
        ],

        "Kuliner / Food & Beverage": [

            "makanan", "kuliner", "food",
            "minuman", "drink", "cafe",
            "coffee", "kopi", "dessert",

            # COOKING
            "masak", "resep", "baking",
            "jajanan", "restaurant",
            "warung", "street food",

            # FOODS
            "burger", "pizza", "ayam",
            "bakso", "mie", "seblak",
            "matcha", "boba", "sushi",
            "ramen", "seafood",

            # CONTENT
            "mukbang", "food review",
            "review makanan"
        ],

        "Travel & Lifestyle": [

            "travel", "liburan", "healing",
            "wisata", "pantai", "gunung",
            "hotel", "villa", "staycation",

            # DAILY LIFE
            "daily life", "daily vlog",
            "vlog", "morning routine",
            "daily routine",
            "kehidupan", "sehari hari",

            # SELF IMPROVEMENT
            "self improvement",
            "productive", "produktif",
            "mindset", "wellness",
            "slow living",

            # HEALTH
            "gym", "workout", "fitness",
            "healthy life", "diet",
            "olahraga", "yoga",

            # LIFESTYLE
            "aesthetic room",
            "minimalist",
            "cleaning", "journaling"
        ],

        "Bisnis & Marketing": [

            "bisnis", "marketing",
            "jualan", "jualan online",
            "affiliate", "seller",
            "marketplace",

            # BUSINESS
            "branding", "startup bisnis",
            "usaha", "umkm",
            "digital marketing",
            "content marketing",

            # SOCIAL MEDIA
            "instagram ads",
            "facebook ads",
            "tiktok ads",
            "seo", "copywriting",

            # ECOMMERCE
            "shopee", "tokopedia",
            "ecommerce", "dropship",
            "reseller", "promo",
            "diskon", "closing"
        ],

        "Gaming & Esports": [

            "game", "gaming", "esports",
            "mlbb", "mobile legends",
            "pubg", "valorant", "genshin",
            "minecraft", "free fire",
            "steam", "console",

            # GAMING CONTENT
            "rank", "push rank",
            "gameplay", "streamer",
            "live gaming", "pro player",
            "build hero", "combo hero"
        ],

        "Kesehatan & Mental Health": [

            "kesehatan", "mental health",
            "burnout", "stress",
            "anxiety", "overthinking",

            "healthy", "mental",
            "psikologi", "healing",
            "self care", "meditasi",
            "kesehatan mental",
            "kebiasaan sehat"
        ]
    }

    # =========================
    # SCORE CATEGORY
    # =========================
    scores = {
        cat: 0
        for cat in keyword_map
    }

    for cat, keywords in keyword_map.items():

        for kw in keywords:

            if kw in topic:

                # keyword panjang lebih kuat
                if len(kw.split()) >= 2:
                    scores[cat] += 2
                else:
                    scores[cat] += 1

    # =========================
    # BEST CATEGORY
    # =========================
    best = max(
        scores,
        key=scores.get
    )

    # =========================
    # FALLBACK
    # =========================
    if scores[best] <= 0:
        return "General Content"

    return best

# =========================================================
# GOAL STYLE ENGINE (ADAPTIVE VERSION)
# =========================================================
def goal_style(goal):

    goal = str(goal).lower().strip()

    styles = {

        "Teknologi & Gadget": {
            "tone": "informatif, modern, dan futuristik",
            "cta": "Ajak audience mencoba tools, berdiskusi, atau eksplor teknologi baru.",
            "focus": "AI, coding, gadget, inovasi digital, dan perkembangan teknologi"
        },

        "Hiburan & Komedi": {
            "tone": "fun, chaos, dan menghibur",
            "cta": "Dorong audience share, comment, atau tag teman.",
            "focus": "humor, emosi, relatable moment, dan viral content"
        },

        "Edukasi & Tutorial": {
            "tone": "edukatif, ringan, dan mudah dipahami",
            "cta": "Ajak audience save konten, belajar, atau mencoba tips yang dibahas.",
            "focus": "knowledge, tutorial, insight, dan problem solving"
        },

        "Fashion & Beauty": {
            "tone": "stylish, aesthetic, dan trendy",
            "cta": "Dorong audience mencoba style, outfit, atau beauty routine tertentu.",
            "focus": "visual, outfit, skincare, beauty trend, dan lifestyle"
        },

        "Kuliner / Food & Beverage": {
            "tone": "lezat, menggoda, dan hangat",
            "cta": "Ajak audience mencoba makanan, share rekomendasi, atau review tempat.",
            "focus": "visual makanan, experience, rasa, dan suasana kuliner"
        },

        "Travel & Lifestyle": {
            "tone": "relax, inspiratif, dan personal",
            "cta": "Bangun interaksi tentang pengalaman, rutinitas, atau aktivitas sehari-hari.",
            "focus": "daily life, healing, productivity, wellness, dan self improvement"
        },

        "Bisnis & Marketing": {
            "tone": "persuasif, strategis, dan insightfull",
            "cta": "Ajak audience mencoba strategi bisnis atau membangun brand mereka.",
            "focus": "marketing, branding, jualan online, dan growth bisnis"
        },

        "Gaming & Esports": {
            "tone": "kompetitif, hype, dan energik",
            "cta": "Ajak audience share rank, pengalaman bermain, atau mabar.",
            "focus": "gameplay, skill, esports, update game, dan entertainment gaming"
        },

        "Kesehatan & Mental Health": {
            "tone": "supportive, tenang, dan positif",
            "cta": "Ajak audience menjaga kesehatan fisik dan mental secara perlahan.",
            "focus": "mental health, healthy lifestyle, healing, dan self care"
        }
    }

    return styles.get(goal, {

        "tone": "natural dan fleksibel",

        "cta": "Ajak audience berinteraksi secara natural.",

        "focus": "engagement, insight, dan relevansi topik"
    })


# =========================================================
# HOOK GENERATOR (SUPER ADAPTIVE)
# =========================================================
def generate_hooks(topic, category, goal):

    import random

    topic = str(topic).strip()

    category = str(category).strip()

    hooks_map = {

        "Teknologi & Gadget": [

            f"Awali video dengan screen recording, setup laptop, atau visual modern yang berhubungan dengan {topic} supaya audience langsung penasaran sejak detik pertama.",

            f"Buka video dengan kalimat seperti 'aku baru sadar ternyata {topic} sekarang mulai dipakai banyak orang' sambil memperlihatkan contoh visual nyata.",

            f"Mulai dengan before-after, tools AI, atau hasil teknologi yang berkaitan dengan {topic} supaya audience langsung mikir 'ini kok bisa?'.",

            f"Awali dengan suasana kerja, coding, atau editing sambil masuk perlahan ke pembahasan {topic} dengan tone santai.",

            f"Gunakan hook berupa fakta mengejutkan atau perubahan teknologi yang berkaitan dengan {topic} agar audience langsung berhenti scrolling."
        ],

        "Hiburan & Komedi": [

            f"Mulai video dengan ekspresi overreact atau situasi random yang relate dengan {topic} supaya audience langsung tertarik.",

            f"Awali dengan POV lucu atau dialog singkat yang berhubungan dengan {topic} agar video terasa lebih hidup dan relatable.",

            f"Buka video dengan trend sound atau scene chaos yang bikin audience penasaran sama arah kontennya.",

            f"Gunakan opening berupa momen absurd, awkward, atau kejadian lucu tentang {topic} supaya engagement naik.",

            f"Awali dengan kalimat pendek yang relatable banget lalu langsung masuk ke situasi yang berhubungan dengan {topic}."
        ],

        "Edukasi & Tutorial": [

            f"Mulai video dengan fakta menarik atau hasil akhir dari {topic}, lalu perlahan jelaskan cara kerjanya dengan sederhana.",

            f"Awali dengan kesalahan umum tentang {topic} lalu langsung kasih solusi praktis yang mudah dipahami audience.",

            f"Gunakan opening seperti 'cuma butuh 1 menit buat ngerti ini' sambil memperlihatkan visual yang berkaitan dengan {topic}.",

            f"Buka video dengan pertanyaan sederhana yang sering dipikirkan audience tentang {topic} agar mereka merasa relate.",

            f"Mulai dengan simulasi atau contoh nyata tentang {topic} supaya audience lebih gampang memahami isi konten."
        ],

        "Fashion & Beauty": [

            f"Awali video dengan transisi outfit, mirror selfie, atau detail aesthetic yang terinspirasi dari {topic}.",

            f"Buka video menggunakan close-up fashion, makeup, atau detail visual yang bikin audience langsung tertarik.",

            f"Mulai dengan before-after styling atau beauty routine yang berkaitan dengan {topic}.",

            f"Gunakan cinematic shot dan transisi smooth supaya visual dari {topic} terasa lebih premium.",

            f"Awali dengan vibe clean girl, streetwear, atau aesthetic setup yang cocok dengan tema {topic}."
        ],

        "Kuliner / Food & Beverage": [

            f"Awali video dengan close-up makanan, suara crunchy, atau visual lelehan yang berkaitan dengan {topic}.",

            f"Mulai dengan reaksi pertama saat nyobain sesuatu tentang {topic} supaya audience ikut penasaran.",

            f"Buka video menggunakan cinematic food shot dan ambience hangat agar visual terasa lebih menggoda.",

            f"Awali dengan proses masak, plating, atau potongan visual satisfying yang berhubungan dengan {topic}.",

            f"Mulai dengan kalimat seperti 'aku nemu sesuatu yang bikin nagih banget' sambil memperlihatkan visual utama dari {topic}."
        ],

        "Travel & Lifestyle": [

            f"Awali video dengan potongan rutinitas harian, journaling, workout, atau suasana aesthetic yang berkaitan dengan {topic}.",

            f"Mulai dengan suasana pagi, healing, atau aktivitas santai sebelum perlahan masuk ke pembahasan {topic}.",

            f"Buka video dengan cinematic vlog style supaya audience langsung merasa nyaman dengan vibe kontennya.",

            f"Awali dengan pengalaman personal atau refleksi singkat tentang {topic} agar video terasa lebih authentic.",

            f"Gunakan montage daily activity yang simple tapi relatable supaya audience lebih connect dengan kontennya."
        ],

        "Bisnis & Marketing": [

            f"Awali video dengan hasil penjualan, insight bisnis, atau dashboard analytics yang berkaitan dengan {topic}.",

            f"Mulai dengan pertanyaan seperti 'kenapa sekarang banyak brand mulai fokus ke {topic}?' supaya audience penasaran.",

            f"Buka video dengan studi kasus sederhana tentang strategi marketing yang berhubungan dengan {topic}.",

            f"Awali dengan before-after bisnis atau perubahan engagement setelah menerapkan strategi {topic}.",

            f"Gunakan hook berupa fakta bisnis atau kesalahan marketing yang sering dilakukan audience."
        ],

        "Gaming & Esports": [

            f"Awali video dengan gameplay epic, momen clutch, atau highlight yang berhubungan dengan {topic}.",

            f"Mulai dengan scene kalah lucu, comeback, atau reaction gaming supaya audience langsung tertarik.",

            f"Buka video menggunakan sound effect game dan montage cepat yang berkaitan dengan {topic}.",

            f"Awali dengan build hero, tips rank, atau gameplay unik tentang {topic}.",

            f"Gunakan opening berupa momen emosional atau lucu saat bermain game yang relate dengan audience."
        ],

        "Kesehatan & Mental Health": [

            f"Awali video dengan suasana tenang, self care routine, atau aktivitas kecil yang berkaitan dengan {topic}.",

            f"Mulai dengan kalimat reflektif tentang burnout, stress, atau kehidupan sehari-hari yang relate dengan audience.",

            f"Buka video menggunakan visual calming dan tone lembut supaya audience merasa nyaman menonton.",

            f"Awali dengan pengalaman personal atau reminder sederhana tentang pentingnya menjaga kesehatan mental.",

            f"Gunakan hook berupa kebiasaan kecil yang ternyata berpengaruh besar terhadap kesehatan fisik dan mental."
        ]
    }

    # =========================
    # FALLBACK
    # =========================
    default_hooks = [

        f"Awali video dengan visual yang langsung menarik perhatian audience sebelum masuk ke pembahasan {topic}.",

        f"Mulai dengan pertanyaan sederhana yang relate dengan audience tentang {topic}.",

        f"Buka video dengan suasana natural dan storytelling ringan agar audience merasa lebih connect.",

        f"Gunakan opening yang bikin audience penasaran supaya mereka tertarik menonton sampai akhir."
    ]

    hooks = hooks_map.get(
        category,
        default_hooks
    )

    return random.choice(hooks)

# =========================================================
# PLATFORM STRATEGY (ADAPTIF & CONTEXT-AWARE)
# =========================================================
def platform_strategy(platform, category=None, goal=None):

    platform = str(platform).lower().strip()
    category = str(category or "").lower()
    goal = str(goal or "").lower()

    # =====================================================
    # BASE PLATFORM CHARACTER
    # =====================================================
    base_mapping = {

        "tiktok": {

            "style": "fast paced, emotional, dan highly engaging",

            "base_tip":
            "Audience TikTok memiliki attention span yang sangat cepat sehingga 1-3 detik pertama harus langsung menarik perhatian. "
            "Gunakan hook kuat, subtitle besar, visual aktif, dan perpindahan scene cepat agar retention tetap tinggi. "
            "Konten dengan pacing dinamis, ekspresi natural, serta elemen relatable biasanya lebih mudah masuk FYP dan meningkatkan engagement."
        },

        "instagram": {

            "style": "visual aesthetic, clean, dan branding focused",

            "base_tip":
            "Audience Instagram lebih sensitif terhadap kualitas visual, estetika feed, dan konsistensi branding. "
            "Gunakan komposisi visual yang rapi, pencahayaan bagus, warna konsisten, serta transisi yang smooth agar konten terasa lebih premium dan profesional."
        },

        "youtube": {

            "style": "storytelling, informative, dan retention focused",

            "base_tip":
            "Audience YouTube Shorts cenderung lebih menikmati alur konten yang jelas dan memiliki storytelling bertahap. "
            "Bangun rasa penasaran sejak awal lalu berikan payoff di akhir video agar watch duration dan retention meningkat."
        }
    }

    # =====================================================
    # CATEGORY STRATEGY
    # =====================================================
    category_tips = {

        "teknologi & gadget":
            "Fokus pada demo nyata, before-after, tools, AI, atau hasil teknologi yang langsung terlihat impact-nya supaya audience cepat tertarik.",

        "hiburan & komedi":
            "Gunakan ekspresi kuat, timing cepat, dialog relatable, punchline ringan, dan situasi yang dekat dengan kehidupan sehari-hari agar audience lebih mudah connect.",

        "edukasi & tutorial":
            "Pecah informasi menjadi bagian kecil yang mudah dipahami. Hindari penjelasan terlalu panjang di awal dan gunakan contoh nyata supaya audience tidak cepat bosan.",

        "fashion & beauty":
            "Utamakan visual, detail outfit, warna, transisi clean, dan cinematic shot agar audience lebih fokus pada estetika konten.",

        "kuliner / food & beverage":
            "Gunakan close-up makanan, ambience tempat makan, tekstur visual, dan reaksi natural agar audience ikut merasakan experience dari kontennya.",

        "travel & lifestyle":
            "Bangun suasana yang nyaman, relatable, dan immersive menggunakan cinematic vlog style, daily activity, atau storytelling personal.",

        "bisnis & marketing":
            "Gunakan pendekatan problem solving, insight praktis, studi kasus, atau strategi yang langsung relevan dengan kebutuhan audience.",

        "gaming & esports":
            "Gunakan highlight gameplay, reaction moment, editing cepat, serta momen intense atau lucu agar audience tetap engaged.",

        "kesehatan & fitness":
            "Gunakan visual progress, aktivitas workout, tips sederhana, atau edukasi ringan yang terasa realistis dan achievable.",

        "otomotif":
            "Tonjolkan detail kendaraan, suara mesin, cinematic rolling shot, atau pengalaman berkendara agar visual lebih menarik.",

        "keuangan & investasi":
            "Gunakan penyampaian sederhana dan relatable supaya topik finansial terasa lebih mudah dipahami audience awam.",

        "musik & audio":
            "Bangun vibe emosional melalui audio, beat, ambience, atau transisi yang sinkron dengan musik.",

        "general content":
            "Gunakan pendekatan storytelling ringan, visual menarik, dan format yang mudah dipahami audience umum."
    }

    # =====================================================
    # GOAL / INTENT BOOSTER
    # =====================================================
    goal_tips = {

        "edukasi":
            "Prioritaskan value, insight praktis, dan penyampaian sederhana agar audience merasa mendapatkan manfaat nyata.",

        "hiburan":
            "Bangun emosi, humor, atau momen relatable supaya audience terdorong untuk share dan comment.",

        "branding":
            "Pastikan identitas visual dan tone konten konsisten agar audience lebih mudah mengenali brand atau persona creator.",

        "jualan":
            "Fokus pada pain point audience, solusi nyata, dan manfaat produk tanpa terasa terlalu hard selling.",

        "engagement":
            "Gunakan pertanyaan, opini, atau situasi relatable agar audience terdorong untuk ikut berinteraksi.",

        "viral":
            "Gunakan format yang cepat, emosional, mudah dipahami, dan memiliki elemen surprise atau curiosity tinggi."
    }

    # =====================================================
    # GET BASE
    # =====================================================
    base = base_mapping.get(platform, {

        "style": "adaptive social media strategy",

        "base_tip":
        "Gunakan hook yang jelas, visual menarik, dan alur yang mudah dipahami supaya audience nyaman mengikuti isi konten."
    })

    # =====================================================
    # CATEGORY MATCHING
    # =====================================================
    category_tip = category_tips.get(
        category,
        category_tips["general content"]
    )

    # =====================================================
    # GOAL MATCHING
    # =====================================================
    goal_tip = goal_tips.get(goal, "")

    # =====================================================
    # FINAL STRATEGY
    # =====================================================
    final_tip = (
        f"{base['base_tip']} "
        f"{category_tip} "
        f"{goal_tip}"
    ).strip()

    return {
        "style": base["style"],
        "tip": final_tip
    }

   # =========================================================
# STORYBOARD AI STYLE (ADAPTIF KEYMAP)
# =========================================================
def generate_storyboard(trend, goal, platform, real_caption=None):

    import random

    topic = str(trend.get("query", "konten")).strip()

    category = detect_category(topic)

    category_lower = category.lower()

    style = goal_style(goal)

    pstyle = platform_strategy(
        platform,
        category,
        goal
    )

    opening = generate_hooks(
        topic,
        category,
        goal
    )

    # =====================================================
    # CATEGORY-BASED STORY ENGINE
    # =====================================================
    category_story = {

        "teknologi & gadget": [

            f"Tunjukkan bagaimana {topic} mulai mempengaruhi kebiasaan digital, pekerjaan, atau aktivitas sehari-hari audience sekarang. Gunakan visual modern, screen recording, AI tools, atau before-after supaya audience langsung merasa topiknya relevan.",

            f"Jelaskan insight menarik tentang {topic} menggunakan contoh tools, aplikasi, gadget, atau simulasi sederhana supaya audience lebih cepat memahami manfaat dan impact teknologinya.",

            f"Bangun rasa penasaran audience dengan menunjukkan fitur, hasil, atau kemampuan unik dari {topic} secara bertahap agar retention tetap tinggi sampai akhir video."
        ],

        "hiburan & komedi": [

            f"Bangun suasana fun dan relatable menggunakan situasi sehari-hari yang berhubungan dengan {topic}. Gunakan ekspresi, timing cepat, dan punchline ringan agar audience lebih mudah connect.",

            f"Gunakan format storytelling atau POV yang menggambarkan situasi absurd, lucu, atau viral terkait {topic} supaya audience terdorong untuk share dan mention teman.",

            f"Tampilkan reaksi berlebihan, dialog ringan, atau momen random yang berkaitan dengan {topic} agar vibe kontennya terasa lebih hidup dan menghibur."
        ],

        "edukasi & tutorial": [

            f"Jelaskan inti pembahasan {topic} menggunakan bahasa sederhana dan contoh nyata supaya audience merasa belajar tanpa tekanan. Pecah penjelasan menjadi bagian kecil agar mudah dipahami.",

            f"Tampilkan kesalahan umum atau miskonsepsi tentang {topic}, lalu perlahan berikan solusi atau penjelasan yang benar agar audience merasa mendapatkan insight baru.",

            f"Gunakan simulasi sederhana, analogi ringan, atau studi kasus nyata terkait {topic} supaya audience lebih cepat memahami isi konten."
        ],

        "fashion & beauty": [

            f"Fokus pada visual aesthetic, detail outfit, styling, atau transformasi yang terinspirasi dari {topic} agar audience menikmati visual sejak awal video.",

            f"Tampilkan proses mix and match, skincare routine, atau detail beauty look yang berkaitan dengan {topic} menggunakan transisi clean dan cinematic shot.",

            f"Bangun vibe classy, modern, dan relatable supaya audience merasa kontennya inspiratif sekaligus nyaman ditonton."
        ],

        "kuliner / food & beverage": [

            f"Tampilkan visual close-up makanan, tekstur, proses masak, atau ambience tempat makan yang berkaitan dengan {topic} supaya audience ikut merasakan experience-nya.",

            f"Gunakan reaksi natural saat mencoba sesuatu terkait {topic} agar audience lebih penasaran dan terdorong untuk mencoba juga.",

            f"Bangun suasana hangat dan menggoda menggunakan cinematic food shot, suara crunchy, atau detail visual yang satisfying."
        ],

        "travel & lifestyle": [

            f"Bangun storytelling santai menggunakan rutinitas harian, vlog cinematic, atau pengalaman pribadi yang berkaitan dengan {topic} supaya audience merasa lebih dekat secara emosional.",

            f"Tampilkan suasana tempat, aktivitas sehari-hari, atau self improvement journey yang berhubungan dengan {topic} agar video terasa lebih authentic.",

            f"Gunakan visual calming, natural lighting, dan pacing nyaman supaya audience menikmati vibe konten sampai akhir."
        ],

        "bisnis & marketing": [

            f"Jelaskan bagaimana {topic} bisa membantu audience meningkatkan branding, penjualan, atau strategi marketing menggunakan contoh sederhana dan realistis.",

            f"Tampilkan problem yang sering dialami audience terkait bisnis atau content marketing lalu berikan solusi praktis menggunakan pendekatan yang mudah dipahami.",

            f"Bangun rasa penasaran dengan insight, strategi, atau pola viral yang berkaitan dengan {topic} agar audience merasa mendapatkan value baru."
        ],

        "gaming & esports": [

            f"Gunakan gameplay cepat, highlight moment, reaction lucu, atau momen clutch yang berkaitan dengan {topic} agar audience tetap engaged.",

            f"Tampilkan scene intense, strategi unik, atau momen chaos dari {topic} supaya audience penasaran menonton sampai akhir.",

            f"Bangun vibe kompetitif dan fun menggunakan editing cepat, subtitle besar, dan reaction natural."
        ],

        "kesehatan & fitness": [

            f"Tampilkan aktivitas workout, progress kecil, atau kebiasaan sehat yang berkaitan dengan {topic} supaya audience merasa termotivasi.",

            f"Gunakan penjelasan sederhana dan realistis agar audience merasa tips terkait {topic} bisa langsung diterapkan dalam kehidupan sehari-hari.",

            f"Bangun vibe positif dan produktif menggunakan visual clean, gerakan aktif, dan storytelling ringan."
        ],

        "otomotif": [

            f"Tampilkan detail kendaraan, suara mesin, rolling shot, atau pengalaman berkendara yang berkaitan dengan {topic} agar visual terasa lebih cinematic.",

            f"Gunakan angle close-up dan transisi cepat untuk memperlihatkan bagian menarik dari {topic} supaya audience otomotif lebih engaged.",

            f"Bangun suasana modern dan energetic menggunakan visual kendaraan, modifikasi, atau aktivitas riding."
        ],

        "keuangan & investasi": [

            f"Jelaskan insight finansial terkait {topic} menggunakan bahasa sederhana supaya audience awam tetap mudah memahami isi konten.",

            f"Gunakan contoh realistis, simulasi sederhana, atau problem sehari-hari agar topik {topic} terasa lebih relate dan aplikatif.",

            f"Bangun rasa penasaran dengan fakta atau kesalahan umum terkait keuangan dan investasi supaya audience terdorong menonton sampai akhir."
        ],

        "musik & audio": [

            f"Bangun vibe emosional menggunakan beat, ambience, audio trend, atau visual yang sinkron dengan suasana {topic}.",

            f"Gunakan transisi mengikuti ritme musik supaya audience lebih menikmati flow video dan merasa lebih immersed dengan isi konten.",

            f"Tampilkan potongan proses kreatif, reaction audio, atau suasana yang memperkuat emosi dari {topic}."
        ],

        "general content": [

            f"Gunakan storytelling ringan dan natural tentang {topic} supaya audience merasa lebih relate dengan isi konten.",

            f"Bangun rasa penasaran secara bertahap menggunakan visual aktif, subtitle besar, dan alur yang mudah dipahami audience umum.",

            f"Masukkan opini, pengalaman, atau sudut pandang unik terkait {topic} agar konten terasa lebih personal dan tidak generic."
        ]
    }

    # =====================================================
    # RETENTION ENGINE
    # =====================================================
    retention_options = [

        f"{pstyle['tip']} Pastikan setiap beberapa detik ada perubahan visual, subtitle, zoom, atau transisi agar audience tetap fokus.",

        f"Bangun rasa penasaran audience secara bertahap dan hindari menjelaskan semuanya di awal supaya retention tetap stabil sampai akhir video.",

        f"Gunakan kombinasi visual aktif, subtitle dinamis, voice over, dan perubahan angle supaya konten terasa lebih engaging.",

        f"Masukkan elemen relatable atau pengalaman yang dekat dengan kehidupan audience supaya interaksi seperti komentar dan share meningkat.",

        f"Buat audience merasa ada payoff menarik di akhir video sehingga mereka terdorong menonton sampai selesai."
    ]

    # =====================================================
    # CTA ENGINE
    # =====================================================
    ending_options = [

        style['cta'],

        f"Akhiri video dengan pertanyaan ringan tentang {topic} supaya audience terdorong ikut berdiskusi di kolom komentar.",

        f"Buat ending yang memancing rasa penasaran audience agar mereka menunggu part berikutnya tentang {topic}.",

        f"Gunakan CTA natural seperti save, share, atau tag teman agar engagement meningkat tanpa terasa hard selling.",

        f"Tutup video menggunakan opini menarik atau fakta mengejutkan terkait {topic} supaya audience terus kepikiran setelah selesai menonton.",

        f"Arahkan audience untuk mencoba, mencari tahu, atau ikut tren {topic} agar mereka merasa lebih terlibat dengan isi konten."
    ]

    # =====================================================
    # PICK CATEGORY STORY
    # =====================================================
    middle_options = category_story.get(
        category_lower,
        category_story["general content"]
    )

    # =====================================================
    # FINAL STORYBOARD
    # =====================================================
    storyboard = [

        {
            "scene": "Kilas Balik Konten Singkat (0-5s)",
            "text": opening
        },

        {
            "scene": "Inti Konten (5-30s)",
            "text": random.choice(middle_options)
        },

        {
            "scene": "Ngobrol dengan Audience (30-45s)",
            "text": random.choice(retention_options)
        },

        {
            "scene": "Penutup Konten (CTA)",
            "text": random.choice(ending_options)
        }
    ]

    return storyboard
# =========================================================
# TITLE GENERATOR (ADAPTIF KEYMAP + FLEXIBLE)
# =========================================================
def generate_title(topic, goal, category=None):

    import random

    topic = str(topic).title().strip()

    goal = str(goal).lower().strip()

    # =====================================================
    # AUTO CATEGORY DETECTION
    # =====================================================
    if not category:
        category = detect_category(topic)

    category = str(category).lower()

    # =====================================================
    # TITLE MAP
    # =====================================================
    title_map = {

        # =================================================
        # TEKNOLOGI & GADGET
        # =================================================
        "teknologi & gadget": [

            f"Nyobain Tren {topic} yang Lagi Ramai Dipakai Banyak Orang",
            f"Upgrade Aktivitas Digital Pakai Konsep {topic}",
            f"Setup Simpel Bertema {topic} yang Bikin Kerja Lebih Praktis",
            f"Eksplor Hal Menarik dari Dunia {topic}",
            f"Rutinitas Digital Modern yang Lagi Identik dengan {topic}",
            f"Cara Orang-Orang Memanfaatkan {topic} di Aktivitas Harian",
            f"Hal Kecil dari {topic} yang Ternyata Bikin Produktif",
            f"Trend {topic} yang Lagi Sering Berseliweran di FYP",
            f"Ngulik {topic} dengan Cara yang Lebih Santai",
            f"Transformasi Aktivitas Harian Gara-Gara {topic}",
            f"Hal Menarik yang Lagi Ramai di Dunia {topic}",
            f"Gaya Baru Anak Digital yang Lagi Dekat dengan {topic}",
            f"Exploring {topic} yang Lagi Hype Banget Sekarang",
            f"Pengalaman Seru Saat Mulai Nyoba {topic}",
            f"Hal Simpel dari {topic} yang Ternyata Berguna Banget",
            f"AI dan {topic} Ternyata Mulai Mengubah Cara Orang Kerja",
            f"Kenapa {topic} Mulai Banyak Dipakai Creator dan Anak Digital",
            f"Trik Simpel Memanfaatkan {topic} Biar Aktivitas Lebih Cepat",
            f"Tool Bertema {topic} yang Lagi Banyak Dibahas Netizen",
            f"Hal Futuristik dari {topic} yang Ternyata Udah Dekat Sama Kita"
        ],

        # =================================================
        # HIBURAN & KOMEDI
        # =================================================
        "hiburan & komedi": [

            f"POV Pas Lagi Ngadepin Situasi {topic} 😂",
            f"Kelakuan Orang-Orang Kalau Udah Bahas {topic}",
            f"Momen Random Gara-Gara {topic} yang Relate Banget",
            f"Drama Receh Tentang {topic} yang Sering Kejadiannya",
            f"Timeline Sekarang Rasanya Isinya {topic} Semua 😭",
            f"Versi Realita dari Tren {topic} di Kehidupan Sehari-Hari",
            f"Chaos Kecil yang Selalu Muncul Gara-Gara {topic}",
            f"Relate Banget Sama Situasi {topic} Akhir-Akhir Ini",
            f"Orang-Orang Sekarang Kalau Ketemu {topic}:",
            f"Hal Absurd dari {topic} Tapi Malah Bikin Ketagihan",
            f"Gak Ada yang Siap Sama Randomness dari {topic}",
            f"Kelakuan Netizen Pas {topic} Lagi Viral",
            f"Trend {topic} yang Bikin Scroll Jadi Gak Berhenti",
            f"Situasi {topic} yang Auto Bikin Ketawa Sendiri",
            f"Realita Lucu di Balik Tren {topic}",
            f"Netizen Lagi Heboh Gara-Gara {topic}",
            f"Mood Hari Ini: {topic}",
            f"Kenapa {topic} Selalu Bikin Timeline Chaos 😭",
            f"Ketika Hidup Mulai Terlalu Dekat Sama {topic}",
            f"Plot Twist dari {topic} yang Gak Kepikiran"
        ],

        # =================================================
        # EDUKASI & TUTORIAL
        # =================================================
        "edukasi & tutorial": [

            f"Memahami {topic} dengan Cara yang Lebih Simpel",
            f"Mulai Kenal {topic} Tanpa Harus Bingung",
            f"Penjelasan Santai Tentang {topic} Buat Pemula",
            f"Step-by-Step Memahami {topic} dengan Mudah",
            f"Hal Dasar Tentang {topic} yang Wajib Dipahami",
            f"Cara Cepat Adaptasi dengan {topic}",
            f"Belajar {topic} dengan Penjelasan yang Lebih Relatable",
            f"Dasar-Dasar {topic} yang Sering Dilewatkan",
            f"Rahasia Memahami {topic} Tanpa Ribet",
            f"Hal Penting Tentang {topic} yang Jarang Dijelaskan",
            f"Awal Mula Memahami Dunia {topic}",
            f"Mindset Penting Sebelum Mulai Belajar {topic}",
            f"Hal Simpel dari {topic} yang Ternyata Penting",
            f"Penjelasan {topic} dengan Bahasa yang Lebih Santai",
            f"Belajar {topic} Biar Gak Kerasa Ribet",
            f"Kenapa Banyak Orang Mulai Belajar {topic}",
            f"Kesalahan Umum Saat Mulai Memahami {topic}",
            f"Cuma Butuh Beberapa Menit Buat Paham {topic}",
            f"Belajar {topic} Tanpa Harus Terlalu Teori",
            f"Tutorial Simpel Tentang {topic} Buat Daily Activity"
        ],

        # =================================================
        # FASHION & BEAUTY
        # =================================================
        "fashion & beauty": [

            f"Mix and Match Ala {topic} yang Lagi Hype",
            f"Look Simpel Tapi Tetap Standout Ala {topic}",
            f"Inspirasi Outfit Bertema {topic} Buat Daily Activity",
            f"Style {topic} yang Lagi Dipakai Banyak Anak Gen Z",
            f"Transisi Outfit Ala {topic} yang Clean Banget",
            f"Daily Look Bertema {topic} yang Lagi Viral",
            f"Gaya Simpel Ala {topic} Tapi Tetap Aesthetic",
            f"Referensi Style {topic} Buat Nongkrong Sampai Ngampus",
            f"Vibes Fashion {topic} yang Lagi Ramai di TikTok",
            f"Style Harian Bertema {topic} yang Nyaman Dipakai",
            f"Look {topic} yang Cocok Buat Aktivitas Seharian",
            f"Upgrade Penampilan Pakai Inspirasi {topic}",
            f"Gaya Outfit {topic} yang Lagi Masuk FYP",
            f"Simple Styling Ala {topic} yang Gampang Ditiru",
            f"Fashion Vibes Bertema {topic} yang Lagi Naik",
            f"Outfit Bertema {topic} yang Lagi Banyak Dipakai Creator",
            f"Clean Girl / Soft Boy Vibes Ala {topic}",
            f"Style Minimalis Bertema {topic} yang Lagi Trending",
            f"Look Simpel Ala {topic} Tapi Tetap Kelihatan Mahal",
            f"Transformasi Visual Ala {topic} yang Lagi Viral"
        ],

        # =================================================
        # KULINER
        # =================================================
        "kuliner / food & beverage": [

            f"Nyobain {topic} yang Lagi Ramai Dicari Orang",
            f"First Impression Pas Nyicipin {topic}",
            f"Jajanan {topic} yang Lagi Berseliweran di FYP",
            f"Rasa dari {topic} yang Ternyata Bikin Nagih",
            f"Eksplor Menu {topic} yang Lagi Viral",
            f"Hal Menarik dari Dunia {topic} yang Lagi Hype",
            f"Ngiler Gara-Gara Lihat {topic} 😭",
            f"Pengalaman Pertama Kali Coba {topic}",
            f"Street Food {topic} yang Lagi Banyak Diburu",
            f"Visual {topic} yang Bahaya Buat Malam Hari",
            f"Menu {topic} yang Lagi Jadi Obrolan Banyak Orang",
            f"Hal Simpel dari {topic} yang Bikin Penasaran",
            f"Trend Kuliner {topic} yang Lagi Naik Banget",
            f"Momen Paling Memuaskan Pas Lagi Makan {topic}",
            f"Keseruan Nyari {topic} yang Lagi Viral",
            f"Hidden Gem Bertema {topic} yang Jarang Orang Tahu",
            f"Kenapa {topic} Mulai Banyak Masuk FYP Kuliner",
            f"Makanan Bertema {topic} yang Visualnya Gak Aman 😭",
            f"Comfort Food Ala {topic} yang Lagi Dicari Banyak Orang",
            f"Hal Random dari {topic} Tapi Malah Bikin Ketagihan"
        ],

        # =================================================
        # TRAVEL & LIFESTYLE
        # =================================================
        "travel & lifestyle": [

            f"Morning Routine Ala {topic} yang Lagi Disukai Banyak Orang",
            f"Rutinitas Santai Bertema {topic} Biar Hari Lebih Enjoy",
            f"Slow Living Vibes Ala {topic} yang Lagi Hype",
            f"Daily Habit Simpel yang Terinspirasi dari {topic}",
            f"Weekend Ala {topic} yang Bikin Pikiran Lebih Tenang",
            f"Rutinitas Produktif Tapi Tetap Santai Ala {topic}",
            f"Hal-Hal Kecil dari {topic} yang Bikin Mood Naik",
            f"Daily Life Vibes yang Lagi Identik dengan {topic}",
            f"Menikmati Hari dengan Cara Ala {topic}",
            f"Rutinitas Seharian dengan Vibes {topic}",
            f"Self Improvement Ala {topic} yang Lagi Banyak Dicoba",
            f"Recharge Energy Lewat Aktivitas Ala {topic}",
            f"Vibes Nyaman dari Rutinitas Bertema {topic}",
            f"Kebiasaan Simpel Ala {topic} yang Bikin Hari Lebih Balance",
            f"Healing Tipis-Tipis Ala {topic}",
            f"Produktif Tapi Tetap Slow Living Ala {topic}",
            f"Daily Reset Routine Bertema {topic}",
            f"Life Update dengan Vibes {topic}",
            f"Cara Simpel Menikmati Hari Ala {topic}",
            f"Rutinitas Ringan yang Lagi Identik dengan {topic}"
        ],

        # =================================================
        # BISNIS & MARKETING
        # =================================================
        "bisnis & marketing": [

            f"Strategi {topic} yang Lagi Banyak Dipakai Brand",
            f"Kenapa Bisnis Mulai Fokus ke {topic}",
            f"Cara Simpel Memanfaatkan {topic} Buat Branding",
            f"Insight Marketing Tentang {topic} yang Lagi Viral",
            f"Rahasia Konten {topic} yang Bikin Engagement Naik",
            f"Mindset Penting Sebelum Mulai {topic}",
            f"Hal Kecil dari {topic} yang Ternyata Pengaruh Besar",
            f"Kenapa Audience Sekarang Lebih Suka Konten {topic}",
            f"Strategi Digital Ala {topic} yang Lagi Naik",
            f"Belajar Branding Lewat Tren {topic}",
            f"Pattern Viral dari Dunia {topic}",
            f"Tips Marketing Bertema {topic} Buat Pemula",
            f"Konten {topic} yang Lagi Banyak Dipakai Seller",
            f"Ngulik Strategi {topic} yang Lagi Ramai di Sosmed",
            f"Hal Menarik dari Dunia Bisnis {topic}"
        ]
    }

    # =====================================================
    # FALLBACK
    # =====================================================
    default_titles = [

        f"Hal Menarik dari {topic} yang Lagi Ramai Sekarang",
        f"Tren {topic} yang Lagi Berseliweran di FYP",
        f"Keseruan di Balik Ramainya {topic}",
        f"Hal Simpel Tentang {topic} yang Lagi Banyak Dibahas",
        f"Vibes dari {topic} yang Lagi Disukai Banyak Orang",
        f"Kenapa {topic} Mulai Sering Muncul di Timeline",
        f"Hal Random dari {topic} Tapi Bikin Penasaran",
        f"Ngobrol Santai Tentang {topic}",
        f"Hal Menarik yang Lagi Naik dari Dunia {topic}",
        f"Cerita Menarik di Balik Tren {topic}"
    ]

    # =====================================================
    # PRIORITY CATEGORY
    # =====================================================
    titles = title_map.get(category)

    # =====================================================
    # FALLBACK GOAL
    # =====================================================
    if not titles:

        goal_mapping = {
            "teknologi": "teknologi & gadget",
            "hiburan": "hiburan & komedi",
            "edukasi": "edukasi & tutorial",
            "fashion": "fashion & beauty",
            "kuliner": "kuliner / food & beverage",
            "lifestyle": "travel & lifestyle",
            "bisnis": "bisnis & marketing"
        }

        mapped = goal_mapping.get(goal)

        if mapped:
            titles = title_map.get(mapped)

    # =====================================================
    # FINAL FALLBACK
    # =====================================================
    if not titles:
        titles = default_titles

    return random.choice(titles)


# =========================================================
# CAPTION GENERATOR AI STYLE (ADAPTIF KEYMAP)
# =========================================================
def generate_caption(topic, goal, category, platform, real_caption=None):

    import random

    topic = str(topic).strip()
    goal = str(goal).lower().strip()
    category = str(category).strip()
    platform = str(platform).lower().strip()

    # =========================================================
    # PLATFORM STYLE
    # =========================================================
    platform_opening = {

        "tiktok": [
            "jujur akhir-akhir ini",
            "fix sekarang",
            "gak heran kalau",
            "entah kenapa sekarang",
            "random banget tapi",
            "baru sadar ternyata",
            "serius deh",
            "aneh tapi nyata 😭",
            "akhirnya ngerti kenapa",
            "sekarang makin banyak orang"
        ],

        "instagram": [
            "lagi suka vibes",
            "akhir-akhir ini tertarik sama",
            "pelan-pelan mulai suka",
            "ternyata aesthetic dari",
            "suka banget sama nuansa",
            "beberapa hari ini lagi menikmati",
            "rasanya nyaman banget lihat",
            "vibes kayak gini tuh",
            "kadang hal sederhana kayak",
            "gak nyangka ternyata"
        ],

        "youtube": [
            "kalau diperhatiin",
            "menariknya dari",
            "hal yang bikin banyak orang tertarik sama",
            "aku coba lebih ngulik tentang",
            "setelah dipelajari ternyata",
            "yang jarang dibahas dari",
            "ternyata ada alasan kenapa",
            "semakin dicari karena",
            "yang bikin topik ini menarik adalah",
            "beberapa waktu terakhir"
        ]
    }

    openings = platform_opening.get(platform, [
        "akhir-akhir ini",
        "sekarang makin banyak orang",
        "ternyata"
    ])

    opener = random.choice(openings)

    # =========================================================
    # REAL CAPTION SUPPORT
    # =========================================================
    if real_caption and len(real_caption.strip()) > 40:

        templates = [

            f"{opener} {topic} mulai sering lewat di timeline 😭\n\n"
            f"{real_caption[:260]}\n\n"
            f"dan ternyata audience sekarang lebih suka konten yang delivery-nya natural, relate, dan gak terlalu dibuat formal.",

            f"{opener} banyak creator mulai bahas {topic} karena engagement-nya lumayan naik.\n\n"
            f"{real_caption[:260]}\n\n"
            f"apalagi kalau visual dan storytelling-nya enak ditonton, audience biasanya lebih betah stay sampai akhir.",

            f"{opener} vibes {topic} makin sering muncul di FYP dan honestly emang menarik buat dibahas.\n\n"
            f"{real_caption[:260]}\n\n"
            f"konten model kayak gini biasanya lebih gampang connect karena audience merasa relate sama situasinya."
        ]

        return random.choice(templates)

    # =========================================================
    # CATEGORY CONTEXT
    # =========================================================
    category_context = {

        "Teknologi & Gadget": [

            f"{opener} {topic} mulai sering dipakai banyak orang buat aktivitas digital sehari-hari.",

            f"perkembangan {topic} sekarang makin menarik karena mulai dipakai bukan cuma creator, tapi juga pelajar sampai pekerja.",

            f"kadang teknologi kayak {topic} tuh awalnya keliatan ribet, tapi ternyata sekarang makin gampang dipahami 😭",

            f"algoritma sekarang juga lagi sering naikin konten bertema {topic} karena audience penasaran sama perkembangan digital terbaru.",

            f"yang bikin {topic} menarik tuh bukan cuma teknologinya, tapi gimana orang-orang mulai adaptasi di kehidupan sehari-hari."
        ],

        "Hiburan & Komedi": [

            f"{opener} timeline rasanya penuh sama {topic} 😭",

            f"konten random tentang {topic} tuh anehnya malah bikin susah berhenti scrolling.",

            f"kadang hal paling receh dari {topic} justru yang paling relate buat audience sekarang 😂",

            f"vibes chaotic dari {topic} ternyata malah bikin engagement naik terus.",

            f"jujur format konten kayak {topic} tuh gampang banget connect ke audience karena terasa natural."
        ],

        "Edukasi & Tutorial": [

            f"ternyata sekarang makin banyak orang pengen ngerti soal {topic} tapi bingung mulai dari mana 😭",

            f"belajar tentang {topic} ternyata lebih gampang kalau dijelasin santai dan pake contoh nyata.",

            f"konten edukasi tentang {topic} sekarang lebih disukai karena audience suka pembahasan cepat dan praktis.",

            f"yang bikin audience betah nonton konten {topic} biasanya karena penyampaiannya ringan dan gak terlalu formal.",

            f"format belajar singkat tentang {topic} sekarang lebih gampang masuk FYP dibanding penjelasan terlalu panjang."
        ],

        "Fashion & Beauty": [

            f"vibes {topic} akhir-akhir ini lagi sering banget muncul di FYP fashion 😭",

            f"simple tapi aesthetic, itu yang bikin style {topic} sekarang banyak disukai.",

            f"kadang yang bikin look keliatan mahal tuh bukan outfit-nya, tapi vibe dari styling {topic}.",

            f"transisi, tone warna, dan visual bertema {topic} sekarang lagi cocok banget buat short content.",

            f"style kayak {topic} tuh keliatan effortless tapi tetap standout kalau visualnya clean."
        ],

        "Kuliner / Food & Beverage": [

            f"jujur visual {topic} tuh tipe yang sekali lewat langsung bikin lapar 😭",

            f"konten makanan tentang {topic} sekarang gampang banget dapet engagement karena visualnya satisfying.",

            f"apalagi kalau ada close-up, crispy sound, atau reaction pertama pas nyobain {topic} 😭",

            f"kadang audience gak butuh review panjang, cukup lihat visual {topic} beberapa detik langsung penasaran.",

            f"vibes kuliner {topic} sekarang lagi sering banget muncul di konten FYP."
        ],

        "Travel & Lifestyle": [

            f"akhir-akhir ini lagi suka vibes yang berhubungan sama {topic} karena terasa lebih calming 😭",

            f"konten lifestyle tentang {topic} sekarang lebih gampang connect karena relate sama kehidupan sehari-hari.",

            f"kadang hal sederhana dari {topic} justru bikin mood jadi lebih enak.",

            f"vibes slow living dan aktivitas bertema {topic} sekarang lagi banyak disukai audience.",

            f"audience sekarang lebih suka konten yang terasa authentic dan natural kayak {topic}."
        ],

        "Bisnis & Marketing": [

            f"sekarang makin banyak orang mulai bahas {topic} karena potensinya lumayan menarik buat bisnis digital.",

            f"strategi tentang {topic} makin sering muncul karena audience sekarang lebih aware soal branding dan marketing.",

            f"konten bisnis bertema {topic} biasanya lebih gampang dapet attention kalau pembahasannya langsung to the point.",

            f"yang bikin {topic} menarik adalah bagaimana orang mulai memanfaatkannya buat jualan dan personal branding.",

            f"format konten tentang {topic} sekarang lebih efektif kalau dikemas singkat tapi tetap insightful."
        ]
    }

    # =========================================================
    # PLATFORM ENDING
    # =========================================================
    platform_ending = {

        "tiktok": [

            "apalagi kalau editannya cepat, subtitle jelas, dan hook-nya langsung kena di awal video.",

            "konten model kayak gini biasanya lebih gampang bikin audience stay sampai akhir.",

            "format short video yang pacing-nya cepat sekarang emang lagi disukai algoritma.",

            "audience TikTok biasanya lebih suka konten yang langsung relate dan gak muter-muter.",

            "visual dinamis + storytelling singkat biasanya bikin retention lebih stabil."
        ],

        "instagram": [

            "apalagi kalau visual, tone warna, dan transisinya dibuat lebih clean dan aesthetic.",

            "konten dengan vibe visual yang nyaman biasanya lebih gampang disimpan dan dishare audience.",

            "storytelling ringan dan visual cinematic sekarang lebih sering perform di Instagram.",

            "audience Instagram biasanya lebih menikmati konten yang terasa premium tapi tetap relatable.",

            "kombinasi visual clean dan caption personal biasanya bikin audience lebih connect."
        ],

        "youtube": [

            "apalagi kalau penyampaiannya runtut dan bikin audience penasaran sampai akhir video.",

            "format storytelling yang perlahan build curiosity biasanya lebih efektif buat retention.",

            "audience YouTube Shorts biasanya lebih suka konten yang punya alur jelas.",

            "video dengan payoff di akhir biasanya lebih kuat mempertahankan watch duration.",

            "penjelasan yang detail tapi santai biasanya lebih nyaman ditonton audience YouTube."
        ]
    }

    # =========================================================
    # FALLBACK
    # =========================================================
    generic_context = [

        f"{opener} {topic} makin sering muncul di timeline dan ternyata audience cukup tertarik sama topik beginian.",

        f"konten tentang {topic} sekarang lebih gampang masuk FYP kalau delivery-nya natural dan relate.",

        f"vibes {topic} sekarang cocok banget dipakai buat format konten short video.",

        f"makin banyak creator mulai eksplor {topic} karena engagement-nya cukup menarik.",

        f"kadang hal sederhana tentang {topic} justru bikin audience penasaran buat nonton sampai habis."
    ]

    intro_pool = category_context.get(category, generic_context)
    ending_pool = platform_ending.get(platform, [
        "konten yang natural biasanya lebih gampang connect sama audience sekarang."
    ])

    intro = random.choice(intro_pool)
    ending = random.choice(ending_pool)

    # =========================================================
    # FINAL COMBINE
    # =========================================================
    return f"{intro}\n\n{ending}"
# =========================================================
# HASHTAG GENERATOR (SUPER ADAPTIF KEYMAP + PLATFORM)
# =========================================================
def generate_hashtags(topic, goal, platform):

    import random
    import re

    topic = str(topic).lower().strip()
    goal = str(goal).lower().strip()
    platform = str(platform).lower().strip()

    # =========================================================
    # CLEAN TOPIC
    # =========================================================
    clean_topic = re.sub(r'[^a-zA-Z0-9\s]', '', topic)

    words = clean_topic.split()

    base = "".join(words[:3]) if words else "viralcontent"

    hashtags = []

    # =========================================================
    # UNIVERSAL TAGS
    # =========================================================
    universal_tags = [

        "#fyp",
        "#viral",
        "#trending",
        "#trend",
        "#foryou",
        "#foryoupage",
        "#viralindonesia",
        "#kontenviral",
        "#contentcreator",
        "#creatorindonesia",
        "#explorepage",
        "#socialmedia",
        "#trendindonesia",
        "#viralcontent",
        "#kontenkreator",
        "#digitalcreator",
        "#kontenkreatif",
        "#viralvideo",
        "#indonesiacreator",
        "#videoviral",
        "#kontenharian",
        "#trendingnow",
        "#creativecontent",
        "#explore",
        "#dailycontent",
        "#influencerindonesia",
        "#shortcontent",
        "#creatorlife"
    ]

    # =========================================================
    # PLATFORM SPECIFIC
    # =========================================================
    platform_tags = {

        "tiktok": [

            "#fypシ",
            "#tiktokviral",
            "#tiktokindonesia",
            "#tiktokcreator",
            "#trendtiktok",
            "#masukfyp",
            "#tiktokfyp",
            "#kontentiktok",
            "#tiktokindo",
            "#videotiktok",
            "#tiktoktrend",
            "#fypindonesia",
            "#viraltiktok",
            "#creatorindo",
            "#tiktokcontent",
            "#fypviral",
            "#trendviral",
            "#shortvideo",
            "#tiktokdaily",
            "#tiktokvideo"
        ],

        "instagram": [

            "#instagramreels",
            "#reelsinstagram",
            "#igreels",
            "#reelsviral",
            "#reelsvideo",
            "#instacreator",
            "#exploreindonesia",
            "#konteninstagram",
            "#viralreels",
            "#reelitfeelit",
            "#reelsindo",
            "#instadaily",
            "#igviral",
            "#instagramcontent",
            "#instareels",
            "#reelscreator",
            "#exploreviral",
            "#aestheticfeed",
            "#instacontent",
            "#reelsdaily"
        ],

        "youtube": [

            "#youtubeshorts",
            "#shorts",
            "#shortsvideo",
            "#viralshorts",
            "#shortsviral",
            "#youtubecreator",
            "#shortsfeed",
            "#trendingshorts",
            "#kontenyoutube",
            "#shortsindonesia",
            "#youtubeviral",
            "#ytshorts",
            "#shortcontent",
            "#creatoryoutube",
            "#videoyoutube",
            "#youtubevideo",
            "#shortvideo",
            "#youtubeindo",
            "#youtubefyp",
            "#shortsyoutube"
        ]
    }

    # =========================================================
    # CATEGORY TAGS
    # =========================================================
    category_tags = {

        # =====================================================
        # TEKNOLOGI
        # =====================================================
        "teknologi": [

            "#teknologi",
            "#teknologiterbaru",
            "#technology",
            "#digitaltrend",
            "#digital",
            "#techtok",
            "#tekgadget",
            "#ai",
            "#artificialintelligence",
            "#machinelearning",
            "#chatgpt",
            "#coding",
            "#programming",
            "#developer",
            "#codinglife",
            "#software",
            "#startup",
            "#cybersecurity",
            "#webdeveloper",
            "#technews",
            "#teknologiindonesia",
            "#robotics",
            "#futuretech",
            "#smarttechnology",
            "#innovation",
            "#programmer",
            "#codingindonesia",
            "#computer",
            "#gadget",
            "#techviral"
        ],

        # =====================================================
        # HIBURAN
        # =====================================================
        "hiburan": [

            "#hiburan",
            "#funny",
            "#komedi",
            "#videolucu",
            "#ngakak",
            "#meme",
            "#memeindonesia",
            "#storytime",
            "#relatable",
            "#receh",
            "#humor",
            "#prank",
            "#challenge",
            "#viralhumor",
            "#kontenhiburan",
            "#funnyvideo",
            "#randomvideo",
            "#chaotic",
            "#funnymoments",
            "#komediindonesia",
            "#lawak",
            "#parodi",
            "#trendhiburan",
            "#lucu",
            "#viralfunny",
            "#comedytiktok",
            "#dailyfun",
            "#moodbooster"
        ],

        # =====================================================
        # EDUKASI
        # =====================================================
        "edukasi": [

            "#edukasi",
            "#tutorial",
            "#belajar",
            "#belajarbareng",
            "#kontenedukasi",
            "#edukasiviral",
            "#faktamenarik",
            "#ilmupengetahuan",
            "#tips",
            "#tipsandtricks",
            "#howto",
            "#pengetahuan",
            "#tutorialindonesia",
            "#informasi",
            "#belajaronline",
            "#produktif",
            "#mindset",
            "#selfimprovement",
            "#belajarmudah",
            "#edukatif",
            "#informasimenarik",
            "#quicklearning",
            "#smartcontent",
            "#study",
            "#learning",
            "#belajartiktok",
            "#studygram",
            "#studytips"
        ],

        # =====================================================
        # FASHION
        # =====================================================
        "fashion": [

            "#fashion",
            "#ootd",
            "#fashionstyle",
            "#outfitideas",
            "#style",
            "#styleinspo",
            "#aesthetic",
            "#fashionviral",
            "#beauty",
            "#makeup",
            "#skincare",
            "#outfitinspo",
            "#fashionindonesia",
            "#streetstyle",
            "#fashiontrend",
            "#dailylook",
            "#styleviral",
            "#fashioncreator",
            "#beautytips",
            "#glowup",
            "#fashiondaily",
            "#lookbook",
            "#ootdinspiration",
            "#styleideas",
            "#beautycontent",
            "#outfitcheck",
            "#fashiontok",
            "#minimalstyle"
        ],

        # =====================================================
        # KULINER
        # =====================================================
        "kuliner": [

            "#kuliner",
            "#foodie",
            "#foodcontent",
            "#foodviral",
            "#makananenak",
            "#kulinerindonesia",
            "#jajananviral",
            "#makananviral",
            "#foodreview",
            "#foodlover",
            "#streetfood",
            "#kulinerviral",
            "#resep",
            "#masakan",
            "#masakanrumahan",
            "#kulinerhits",
            "#foodphotography",
            "#foodvideo",
            "#dessert",
            "#cafehits",
            "#kopi",
            "#foodtiktok",
            "#mukbang",
            "#viralfood",
            "#rekomendasimakanan",
            "#foodblogger",
            "#jajananhits",
            "#makanankekinian"
        ],

        # =====================================================
        # LIFESTYLE
        # =====================================================
        "lifestyle": [

            "#lifestyle",
            "#dailyvlog",
            "#selfimprovement",
            "#productive",
            "#produktif",
            "#healing",
            "#wellness",
            "#dailylife",
            "#dailyroutine",
            "#slowliving",
            "#mindset",
            "#motivation",
            "#travel",
            "#traveling",
            "#morningroutine",
            "#aestheticlife",
            "#lifestyletips",
            "#workout",
            "#gym",
            "#healthy",
            "#balance",
            "#routine",
            "#vlog",
            "#selfcare",
            "#positivevibes",
            "#inspirasi",
            "#lifecontent",
            "#lifestylecreator"
        ],

        # =====================================================
        # BISNIS
        # =====================================================
        "bisnis": [

            "#bisnis",
            "#marketing",
            "#digitalmarketing",
            "#branding",
            "#jualanonline",
            "#entrepreneur",
            "#business",
            "#bisnisonline",
            "#affiliate",
            "#contentmarketing",
            "#socialmediamarketing",
            "#jualan",
            "#businessowner",
            "#startup",
            "#brandstrategy",
            "#marketingdigital",
            "#smallbusiness",
            "#creativebusiness",
            "#onlineshop",
            "#marketplace",
            "#businessideas",
            "#bisnisanakmuda",
            "#personalbranding",
            "#viralmarketing",
            "#entrepreneurship",
            "#digitalbusiness",
            "#bisnisviral"
        ]
    }

    # =========================================================
    # DETECT CATEGORY FROM GOAL
    # =========================================================
    selected_tags = []

    if any(x in goal for x in [
        "teknologi", "gadget", "ai", "coding",
        "programming", "software", "digital"
    ]):
        selected_tags = category_tags["teknologi"]

    elif any(x in goal for x in [
        "hiburan", "komedi", "meme", "funny"
    ]):
        selected_tags = category_tags["hiburan"]

    elif any(x in goal for x in [
        "edukasi", "tutorial", "belajar", "tips"
    ]):
        selected_tags = category_tags["edukasi"]

    elif any(x in goal for x in [
        "fashion", "beauty", "ootd", "style"
    ]):
        selected_tags = category_tags["fashion"]

    elif any(x in goal for x in [
        "kuliner", "food", "makanan", "minuman"
    ]):
        selected_tags = category_tags["kuliner"]

    elif any(x in goal for x in [
        "lifestyle", "travel", "daily", "wellness"
    ]):
        selected_tags = category_tags["lifestyle"]

    elif any(x in goal for x in [
        "bisnis", "marketing", "branding", "jualan"
    ]):
        selected_tags = category_tags["bisnis"]

    # =========================================================
    # TOPIC TAGS
    # =========================================================
    topic_tags = [

        f"#{base}",
        f"#{base}viral",
        f"#{base}trend",
        f"#{base}trending",
        f"#{base}indonesia",
        f"#{base}tips",
        f"#{base}content",
        f"#{base}creator",
        f"#{base}daily",
        f"#{base}video"
    ]

    # =========================================================
    # WORD BASED TAGS
    # =========================================================
    word_tags = []

    for word in words[:5]:

        if len(word) > 2:

            word_tags.extend([

                f"#{word}",
                f"#{word}viral",
                f"#{word}trend",
                f"#{word}indonesia",
                f"#{word}content"
            ])

    # =========================================================
    # COMBINE
    # =========================================================
    hashtags.extend(universal_tags)
    hashtags.extend(platform_tags.get(platform, []))
    hashtags.extend(selected_tags)
    hashtags.extend(topic_tags)
    hashtags.extend(word_tags)

    # =========================================================
    # REMOVE DUPLICATE
    # =========================================================
    hashtags = list(dict.fromkeys(hashtags))

    # =========================================================
    # SHUFFLE
    # =========================================================
    random.shuffle(hashtags)

    # =========================================================
    # FINAL
    # =========================================================
    return " ".join(hashtags[:18])
# =========================================================
# STRATEGY GENERATOR (ADAPTIVE & FLEXIBLE)
# =========================================================
def generate_strategy(category, goal, platform="tiktok"):

    import random

    category = str(category).strip()
    goal = str(goal).lower().strip()
    platform = str(platform).lower().strip()

    # =========================================================
    # PLATFORM BOOST
    # =========================================================
    platform_boost = {

        "tiktok": [

            "Pastikan 1-3 detik pertama langsung memancing rasa penasaran audience karena behavior TikTok sangat cepat dalam scrolling content.",

            "Gunakan subtitle besar, cut cepat, zoom dinamis, dan visual yang terus bergerak supaya retention audience tetap stabil sampai akhir video.",

            "Konten TikTok biasanya lebih efektif jika terasa spontan, natural, dan tidak terlalu formal. Gunakan gaya komunikasi yang santai dan relatable.",

            "Gunakan format storytelling pendek, hook agresif, dan payoff di akhir video agar peluang masuk FYP lebih tinggi.",

            "Tambahkan elemen yang sedang ramai seperti sound viral, meme ringan, atau komentar audience agar engagement meningkat."
        ],

        "instagram": [

            "Fokus pada kualitas visual, tone warna yang konsisten, dan framing yang clean agar konten terasa lebih premium dan aesthetic.",

            "Audience Instagram cenderung lebih memperhatikan branding visual sehingga thumbnail, cover, dan transisi perlu dibuat lebih rapi.",

            "Gunakan visual cinematic, lighting yang nyaman dilihat, dan storytelling ringan supaya audience lebih betah menikmati isi konten.",

            "Konten Instagram biasanya perform lebih baik jika terlihat aesthetic namun tetap terasa personal dan relatable.",

            "Bangun identitas visual yang konsisten agar audience lebih mudah mengenali style konten yang dibuat."
        ],

        "youtube": [

            "Bangun storytelling yang jelas dari awal sampai akhir supaya audience memiliki alasan untuk terus menonton video.",

            "Audience YouTube Shorts biasanya lebih nyaman dengan penjelasan yang sedikit lebih detail dibanding TikTok.",

            "Gunakan build-up informasi secara bertahap dan jangan langsung reveal semua poin utama di awal video.",

            "Tambahkan kombinasi voice over, visual pendukung, dan transisi natural agar video terasa lebih profesional.",

            "Pastikan ada curiosity loop di beberapa bagian video supaya retention tetap tinggi hingga akhir."
        ]
    }

    # =========================================================
    # CATEGORY STRATEGY
    # =========================================================
    strategies = {

        # =====================================================
        # TEKNOLOGI & GADGET
        # =====================================================
        "Teknologi & Gadget": [

            "Gunakan visual modern, screen recording, close-up device, atau simulasi AI supaya audience langsung memahami konteks teknologi yang dibahas. Konten teknologi lebih menarik jika penyampaiannya cepat, visualnya clean, dan langsung menunjukkan manfaat nyata dari topik tersebut.",

            "Fokus pada insight yang relevan dengan kehidupan digital audience seperti AI tools, gadget terbaru, automation, coding, aplikasi viral, atau tren teknologi yang sedang ramai dibahas di media sosial.",

            "Bangun rasa penasaran dengan menunjukkan hasil akhir terlebih dahulu sebelum menjelaskan prosesnya. Strategi ini efektif meningkatkan watch duration pada konten teknologi.",

            "Gunakan pendekatan problem solving dengan menjelaskan bagaimana topik tersebut dapat membantu produktivitas, pekerjaan, belajar, atau aktivitas sehari-hari audience.",

            "Konten teknologi biasanya lebih perform jika dikemas menggunakan bahasa sederhana dan tidak terlalu teknis supaya tetap mudah dipahami audience umum."
        ],

        # =====================================================
        # HIBURAN & KOMEDI
        # =====================================================
        "Hiburan & Komedi": [

            "Gunakan ekspresi yang lebih hidup, pacing cepat, dan situasi yang relatable agar audience merasa dekat dengan isi konten sejak awal video.",

            "Bangun humor dari situasi sehari-hari, POV, dialog random, atau reaction yang sering dialami audience media sosial sekarang.",

            "Tambahkan punchline ringan, subtitle ekspresif, dan editing cepat supaya energi konten tetap terasa hidup sampai akhir video.",

            "Konten hiburan biasanya lebih mudah viral jika terasa spontan, chaotic, dan tidak terlalu terlihat scripted.",

            "Fokus pada emosi audience seperti lucu, kaget, relate, atau absurd supaya peluang share dan komentar meningkat."
        ],

        # =====================================================
        # EDUKASI & TUTORIAL
        # =====================================================
        "Edukasi & Tutorial": [

            "Gunakan format step-by-step, penjelasan sederhana, dan contoh nyata supaya audience lebih cepat memahami isi konten tanpa merasa bosan.",

            "Konten edukasi akan terasa lebih engaging jika dikemas seperti ngobrol santai dibanding presentasi formal.",

            "Gunakan analogi sederhana, visual pendukung, dan subtitle jelas agar informasi terasa lebih ringan dipahami audience media sosial.",

            "Awali video dengan kesalahan umum, fakta unik, atau pertanyaan sederhana agar audience penasaran untuk terus menonton.",

            "Fokus pada penyampaian insight yang praktis dan langsung bisa dipahami hanya dalam waktu singkat."
        ],

        # =====================================================
        # FASHION & BEAUTY
        # =====================================================
        "Fashion & Beauty": [

            "Tonjolkan visual outfit, makeup, skincare, atau styling menggunakan angle clean dan lighting yang aesthetic agar audience langsung tertarik sejak awal.",

            "Gunakan transisi smooth, detail visual close-up, dan tone warna yang konsisten supaya konten terasa lebih premium.",

            "Konten fashion dan beauty biasanya lebih engaging jika dikombinasikan dengan vibe lifestyle, GRWM, atau daily activity yang relatable.",

            "Bangun visual branding yang kuat menggunakan style editing, outfit palette, dan ambience yang sesuai target audience.",

            "Gunakan before-after, tutorial singkat, atau styling tips agar audience merasa mendapatkan inspirasi langsung dari konten."
        ],

        # =====================================================
        # KULINER
        # =====================================================
        "Kuliner / Food & Beverage": [

            "Fokus pada visual makanan yang menggoda seperti close-up texture, pouring sauce, crispy sound, atau first bite reaction agar audience langsung lapar secara visual.",

            "Gunakan angle kamera yang memperlihatkan detail makanan secara jelas supaya audience merasa lebih immersive saat menonton.",

            "Konten kuliner lebih menarik jika dikemas menggunakan reaction natural, storytelling pengalaman makan, atau hidden gem recommendation.",

            "Tambahkan ambience tempat makan, suasana cafe, atau proses memasak agar video terasa lebih hidup dan tidak monoton.",

            "Gunakan deskripsi rasa yang relatable dan emosional supaya audience ikut membayangkan pengalaman makan tersebut."
        ],

        # =====================================================
        # LIFESTYLE
        # =====================================================
        "Travel & Lifestyle": [

            "Bangun suasana video yang calming, natural, dan relatable supaya audience merasa nyaman mengikuti alur konten.",

            "Gunakan cinematic vlog-style shot, montage rutinitas, dan storytelling personal agar audience merasa lebih dekat secara emosional.",

            "Konten lifestyle biasanya lebih efektif jika fokus pada pengalaman kecil sehari-hari yang terasa authentic dan tidak dibuat berlebihan.",

            "Tambahkan aktivitas seperti journaling, working setup, gym, healing, traveling, atau productive routine supaya konten terasa lebih hidup.",

            "Gunakan pacing yang lebih smooth dan visual yang aesthetic agar vibe konten tetap nyaman ditonton."
        ],

        # =====================================================
        # BISNIS & MARKETING
        # =====================================================
        "Bisnis & Marketing": [

            "Fokus pada insight yang langsung relevan dengan kebutuhan audience seperti strategi jualan, branding, affiliate, atau marketing media sosial.",

            "Gunakan studi kasus nyata, before-after strategy, atau contoh brand yang sedang viral agar audience lebih mudah memahami isi konten.",

            "Konten bisnis biasanya lebih efektif jika dikemas singkat, actionable, dan tidak terlalu teoritis.",

            "Bangun hook menggunakan kesalahan umum, fakta mengejutkan, atau peluang yang sedang ramai dibahas di dunia digital.",

            "Gunakan bahasa sederhana dan relatable supaya topik bisnis terasa lebih ringan dipahami audience umum."
        ],

        # =====================================================
        # GENERAL
        # =====================================================
        "General Content": [

            "Gunakan storytelling ringan, visual dinamis, dan gaya komunikasi natural agar audience merasa lebih nyaman mengikuti isi konten.",

            "Bangun engagement menggunakan opini relatable, pengalaman sehari-hari, atau insight sederhana yang dekat dengan kehidupan audience.",

            "Fokus pada alur video yang tidak terlalu kaku supaya audience merasa sedang menikmati konten, bukan menonton presentasi formal.",

            "Gunakan kombinasi visual cepat, subtitle jelas, dan hook ringan agar audience tidak cepat skip video.",

            "Konten general biasanya lebih perform jika terasa authentic, mudah dipahami, dan punya emotional connection dengan audience."
        ]
    }

    # =========================================================
    # PICK MAIN STRATEGY
    # =========================================================
    selected = random.choice(
        strategies.get(category, strategies["General Content"])
    )

    # =========================================================
    # PLATFORM INJECTION
    # =========================================================
    selected += " " + random.choice(
        platform_boost.get(platform, platform_boost["tiktok"])
    )

    # =========================================================
    # GOAL BOOSTER
    # =========================================================
    goal_boost = {

        "branding": [
            "Fokus pada konsistensi tone visual, karakter komunikasi, dan identitas konten agar audience lebih mudah mengenali branding yang dibangun.",
            "Bangun image yang konsisten melalui gaya editing, pilihan visual, dan cara penyampaian supaya personal branding terasa lebih kuat."
        ],

        "promosi": [
            "Masukkan CTA yang natural namun tetap jelas agar audience terdorong mencoba atau mencari tahu lebih lanjut.",
            "Fokus pada value utama dan alasan kenapa audience perlu tertarik dengan topik tersebut sekarang juga."
        ],

        "hard selling": [
            "Gunakan urgency ringan, benefit yang jelas, dan problem solving supaya audience merasa topik tersebut benar-benar relevan dengan kebutuhan mereka.",
            "Pastikan promosi terasa natural dan tetap menyatu dengan storytelling agar audience tidak merasa sedang ditawari secara berlebihan."
        ],

        "hiburan": [
            "Pastikan energi video tetap stabil dan jangan terlalu banyak jeda kosong supaya audience terus engaged.",
            "Gunakan momen relatable dan ekspresi yang lebih natural agar audience lebih mudah connect dengan isi konten."
        ],

        "edukasi": [
            "Gunakan penjelasan singkat namun tetap padat insight agar audience mendapatkan value tanpa merasa overwhelmed.",
            "Fokus pada contoh nyata dan bahasa sederhana supaya informasi lebih cepat dipahami audience."
        ],

        "engagement": [
            "Tambahkan pertanyaan, opini ringan, atau ajakan diskusi supaya audience lebih terdorong untuk komentar dan share.",
            "Bangun interaksi dengan format yang terasa dekat dan relatable bagi audience media sosial."
        ]
    }

    # =========================================================
    # APPLY GOAL BOOST
    # =========================================================
    if goal in goal_boost:
        selected += " " + random.choice(goal_boost[goal])

    # =========================================================
    # FINAL
    # =========================================================
    return selected

# =========================================================
# REASONING GENERATOR (ADAPTIVE & CONTEXT AWARE)
# =========================================================
def generate_reasoning(topic, category, goal, platform):

    import random

    topic = str(topic).strip()
    category = str(category).strip()
    goal = str(goal).lower().strip()
    platform = str(platform).lower().strip()

    style = goal_style(goal)

    # =========================================================
    # PLATFORM CHARACTER
    # =========================================================
    platform_desc = {

        "tiktok": [

            "Audience TikTok cenderung lebih tertarik pada konten dengan hook cepat, visual dinamis, subtitle besar, dan penyampaian yang langsung masuk ke inti pembahasan dalam beberapa detik pertama.",

            "Behavior audience TikTok yang cepat scrolling membuat konten perlu memiliki pacing yang agresif, visual yang terus bergerak, dan elemen yang memancing rasa penasaran sejak awal video.",

            "Konten TikTok biasanya lebih mudah perform jika terasa spontan, relatable, dan tidak terlalu formal sehingga audience merasa lebih dekat dengan isi konten.",

            "Format short video di TikTok lebih efektif jika dikombinasikan dengan storytelling singkat, visual aktif, dan punchline yang menjaga retention audience.",

            "Audience TikTok cenderung lebih menyukai konten yang terasa natural namun tetap memiliki value atau hiburan yang langsung bisa dipahami dalam waktu singkat."
        ],

        "instagram": [

            "Audience Instagram biasanya lebih memperhatikan kualitas visual, tone warna, estetika feed, dan konsistensi branding dalam sebuah konten.",

            "Konten Instagram lebih efektif jika memiliki visual clean, cinematic, dan tetap terasa ringan untuk dinikmati audience sehari-hari.",

            "Karakter audience Instagram cenderung menyukai konten yang aesthetic namun tetap relatable sehingga visual dan storytelling perlu berjalan seimbang.",

            "Konten Instagram biasanya lebih mudah menarik perhatian jika memiliki framing rapi, transisi smooth, dan visual yang nyaman dilihat sejak awal.",

            "Audience Instagram cenderung menikmati konten yang terasa personal, inspiring, dan memiliki vibe visual yang konsisten."
        ],

        "youtube": [

            "Audience YouTube Shorts biasanya memiliki retention lebih baik pada konten yang memiliki storytelling jelas, build-up informasi, dan alur pembahasan yang lebih terstruktur.",

            "Konten YouTube lebih efektif jika audience dibuat penasaran secara bertahap melalui storytelling dan payoff di akhir video.",

            "Audience YouTube Shorts cenderung lebih nyaman dengan penjelasan yang sedikit lebih detail dibanding platform short video lainnya.",

            "Format YouTube biasanya lebih cocok untuk konten yang memiliki narasi kuat, insight yang lebih dalam, dan penyampaian yang terasa lebih profesional.",

            "Konten YouTube Shorts dengan kombinasi visual pendukung, voice over, dan storytelling natural biasanya lebih mampu mempertahankan watch duration audience."
        ]
    }

    # =========================================================
    # CATEGORY REASONING
    # =========================================================
    category_reason = {

        # =====================================================
        # TEKNOLOGI
        # =====================================================
        "Teknologi & Gadget": [

            f"Topik '{topic}' memiliki potensi engagement yang cukup tinggi karena audience digital saat ini cenderung tertarik pada AI, teknologi baru, gadget, automation, maupun tren internet yang sedang berkembang.",

            f"Konten bertema '{topic}' relevan dengan pola konsumsi audience modern yang menyukai informasi cepat, insight praktis, dan update teknologi dengan gaya penyampaian yang lebih ringan.",

            f"Pembahasan tentang '{topic}' memiliki peluang perform yang baik karena audience media sosial saat ini cenderung penasaran dengan perkembangan teknologi yang berdampak langsung pada aktivitas sehari-hari.",

            f"Konten teknologi seperti '{topic}' biasanya lebih mudah menarik perhatian karena audience menyukai topik yang terasa futuristik, inovatif, dan relevan dengan kehidupan digital mereka.",

            f"Topik '{topic}' cocok dikembangkan menjadi konten informatif karena audience teknologi biasanya aktif mencari insight baru, tools digital, maupun tren online yang sedang ramai dibahas."
        ],

        # =====================================================
        # HIBURAN
        # =====================================================
        "Hiburan & Komedi": [

            f"Topik '{topic}' memiliki potensi viral yang cukup tinggi karena konten hiburan yang relatable dan emosional biasanya lebih mudah mendapatkan komentar maupun share audience.",

            f"Konten dengan pendekatan ringan seperti '{topic}' biasanya lebih mudah membangun engagement karena audience merasa dekat dengan situasi yang dibahas.",

            f"Topik '{topic}' cocok dikembangkan menjadi konten hiburan karena memiliki unsur relatability, humor, dan emosi yang mudah connect dengan audience media sosial.",

            f"Konten hiburan bertema '{topic}' berpotensi mendapatkan retention yang baik apabila dikemas menggunakan ekspresi natural, storytelling ringan, dan situasi yang familiar bagi audience.",

            f"Pembahasan '{topic}' cukup relevan dengan pola konsumsi audience yang saat ini lebih menyukai konten ringan, spontan, dan mudah dibagikan ke teman."
        ],

        # =====================================================
        # EDUKASI
        # =====================================================
        "Edukasi & Tutorial": [

            f"Topik '{topic}' memiliki potensi yang baik untuk dikembangkan menjadi konten edukasi karena audience media sosial saat ini cenderung menyukai pembelajaran singkat yang praktis dan mudah dipahami.",

            f"Konten edukatif tentang '{topic}' berpeluang mendapatkan retention yang baik jika dikemas menggunakan bahasa sederhana, visual cepat, dan contoh yang relatable.",

            f"Pembahasan '{topic}' cukup relevan dengan kebutuhan audience yang sedang mencari informasi praktis dan mudah dipahami tanpa harus membaca penjelasan panjang.",

            f"Topik '{topic}' cocok dikembangkan menjadi konten tutorial karena audience saat ini lebih tertarik pada format belajar cepat yang langsung bisa diterapkan.",

            f"Konten edukasi dengan pembahasan '{topic}' biasanya lebih efektif jika disampaikan menggunakan gaya santai dan tidak terlalu formal agar audience merasa lebih nyaman mengikuti isi konten."
        ],

        # =====================================================
        # FASHION
        # =====================================================
        "Fashion & Beauty": [

            f"Topik '{topic}' cukup relevan dengan tren visual media sosial karena audience fashion dan beauty biasanya tertarik pada konten aesthetic, styling, dan visual transformation.",

            f"Konten fashion bertema '{topic}' memiliki potensi engagement yang baik karena audience cenderung menyukai inspirasi visual yang relatable dan mudah diterapkan.",

            f"Pembahasan '{topic}' cocok dikembangkan menggunakan pendekatan visual yang clean dan aesthetic karena karakter audience fashion lebih sensitif terhadap tampilan visual konten.",

            f"Konten fashion dan beauty seperti '{topic}' biasanya lebih mudah menarik perhatian jika dikombinasikan dengan visual detail, vibe aesthetic, dan storytelling ringan.",

            f"Topik '{topic}' cukup potensial untuk dikembangkan menjadi konten trend-aware karena audience fashion cenderung aktif mengikuti style dan visual yang sedang viral."
        ],

        # =====================================================
        # KULINER
        # =====================================================
        "Kuliner / Food & Beverage": [

            f"Topik '{topic}' memiliki peluang engagement yang tinggi karena konten kuliner cenderung mudah memancing rasa penasaran audience melalui visual dan emotional response.",

            f"Konten bertema '{topic}' cocok dikembangkan menggunakan pendekatan visual close-up, reaction natural, dan storytelling pengalaman makan agar audience lebih tertarik menonton sampai akhir.",

            f"Pembahasan '{topic}' cukup potensial karena audience media sosial biasanya mudah tertarik pada visual makanan, minuman, atau pengalaman kuliner yang terlihat menggoda.",

            f"Konten kuliner seperti '{topic}' biasanya lebih mudah mendapatkan interaksi karena audience cenderung suka membagikan rekomendasi makanan yang terlihat menarik.",

            f"Topik '{topic}' relevan dengan tren food content saat ini yang lebih menonjolkan visual satisfying, first impression, dan pengalaman mencoba sesuatu yang viral."
        ],

        # =====================================================
        # LIFESTYLE
        # =====================================================
        "Travel & Lifestyle": [

            f"Topik '{topic}' cocok dikembangkan menjadi konten lifestyle karena audience biasanya tertarik pada pengalaman personal, rutinitas harian, dan suasana yang terasa authentic.",

            f"Konten lifestyle bertema '{topic}' memiliki potensi membangun emotional connection yang cukup kuat karena terasa dekat dengan kehidupan sehari-hari audience.",

            f"Pembahasan '{topic}' relevan dengan karakter audience media sosial yang saat ini lebih menyukai konten calming, relatable, dan inspiring.",

            f"Konten lifestyle seperti '{topic}' biasanya lebih efektif jika dikemas menggunakan storytelling natural dan visual yang nyaman ditonton.",

            f"Topik '{topic}' cukup potensial karena audience cenderung menyukai konten yang memberikan vibe santai, personal, dan terasa realistis."
        ],

        # =====================================================
        # BISNIS
        # =====================================================
        "Bisnis & Marketing": [

            f"Topik '{topic}' relevan dengan kebutuhan audience yang sedang mencari insight bisnis, strategi marketing, maupun peluang digital yang sedang berkembang.",

            f"Konten bisnis bertema '{topic}' memiliki potensi engagement yang baik apabila dikemas menggunakan studi kasus nyata dan bahasa yang lebih ringan.",

            f"Pembahasan '{topic}' cocok dikembangkan menjadi konten edukatif karena audience media sosial saat ini lebih tertarik pada insight yang langsung bisa diterapkan.",

            f"Topik '{topic}' cukup potensial karena audience bisnis biasanya aktif mencari strategi praktis yang relevan dengan tren digital saat ini.",

            f"Konten bisnis dengan pendekatan sederhana seperti '{topic}' biasanya lebih mudah dipahami audience dibanding penjelasan yang terlalu teoritis."
        ],

        # =====================================================
        # GENERAL
        # =====================================================
        "General Content": [

            f"Topik '{topic}' memiliki potensi cukup baik untuk dikembangkan menjadi konten media sosial karena masih relevan dengan pola konsumsi audience saat ini.",

            f"Konten bertema '{topic}' cukup fleksibel untuk dikembangkan menjadi berbagai format konten yang lebih ringan, relatable, dan mudah dinikmati audience.",

            f"Pembahasan '{topic}' memiliki peluang engagement yang cukup baik apabila dikemas menggunakan storytelling dan visual yang sesuai karakter platform.",

            f"Topik '{topic}' cukup potensial karena audience media sosial biasanya tertarik pada konten yang terasa dekat dengan aktivitas dan pengalaman sehari-hari.",

            f"Konten dengan pembahasan '{topic}' masih relevan untuk dikembangkan karena audience cenderung menyukai topik yang ringan namun tetap menarik untuk diikuti."
        ]
    }

    # =========================================================
    # GOAL REASONING
    # =========================================================
    goal_reason = {

        "teknologi": [
            "Pendekatan konten difokuskan pada insight digital, tren internet, dan pembahasan yang terasa modern agar audience merasa topik tersebut relevan dengan perkembangan saat ini.",
            "Strategi penyampaian dibuat lebih modern dan informatif supaya audience merasa mendapatkan insight baru tanpa harus mengikuti penjelasan yang terlalu teknis."
        ],

        "hiburan": [
            "Strategi konten dibuat lebih ringan, ekspresif, dan relatable agar audience lebih mudah terhibur serta terdorong untuk berinteraksi.",
            "Pendekatan hiburan difokuskan pada emosi, humor, dan situasi yang mudah connect dengan audience media sosial."
        ],

        "edukasi": [
            "Penyampaian konten difokuskan pada penjelasan sederhana dan visual yang mudah dipahami agar audience tetap nyaman mengikuti isi konten.",
            "Strategi edukasi dibuat lebih santai dan tidak terlalu formal supaya audience tetap mendapatkan value tanpa merasa sedang belajar serius."
        ],

        "fashion": [
            "Strategi visual dibuat lebih aesthetic dan trend-aware karena audience fashion biasanya lebih memperhatikan detail visual dan vibe keseluruhan konten.",
            "Pendekatan fashion difokuskan pada visual styling, aesthetic branding, dan suasana konten yang terasa lebih modern."
        ],

        "kuliner": [
            "Konten difokuskan pada pengalaman visual dan emotional response audience karena konten makanan biasanya lebih efektif jika mampu membangun craving.",
            "Pendekatan kuliner dibuat lebih immersive melalui visual close-up, ambience, dan storytelling pengalaman mencoba makanan."
        ],

        "lifestyle": [
            "Strategi dibuat lebih personal dan natural agar audience merasa lebih dekat dengan creator serta menikmati storytelling yang dibangun.",
            "Pendekatan lifestyle diarahkan pada pengalaman sehari-hari, emotional connection, dan suasana yang terasa authentic."
        ],

        "branding": [
            "Pendekatan konten diarahkan untuk membangun identitas visual dan positioning agar audience lebih mudah mengenali karakter brand maupun creator.",
            "Strategi branding dibuat lebih konsisten dari sisi visual, tone komunikasi, dan gaya penyampaian agar lebih mudah diingat audience."
        ],

        "promosi": [
            "Strategi konten difokuskan pada penyampaian benefit dan alasan kenapa audience perlu tertarik pada topik tersebut saat ini juga.",
            "Pendekatan promosi dibuat lebih persuasive namun tetap natural agar audience tetap nyaman menikmati isi konten."
        ],

        "hard selling": [
            "Konten dibuat lebih persuasive dengan CTA yang jelas agar audience terdorong melakukan tindakan secara langsung setelah menonton.",
            "Strategi hard selling difokuskan pada urgency, problem solving, dan value utama yang ingin ditawarkan kepada audience."
        ],

        "soft selling": [
            "Pendekatan dibuat lebih natural dan tidak terlalu terasa menjual supaya audience tetap nyaman mengikuti isi konten.",
            "Strategi soft selling diarahkan melalui storytelling dan emotional connection sebelum audience diarahkan pada produk atau layanan tertentu."
        ]
    }

    # =========================================================
    # RANDOMIZE
    # =========================================================
    category_text = random.choice(
        category_reason.get(
            category,
            [f"Topik '{topic}' memiliki potensi cukup baik untuk dikembangkan menjadi konten media sosial."]
        )
    )

    platform_text = random.choice(
        platform_desc.get(
            platform,
            ["Strategi konten disesuaikan dengan karakter audience platform agar performa konten lebih optimal."]
        )
    )

    goal_text = random.choice(
        goal_reason.get(
            goal,
            [f"Pendekatan konten disesuaikan dengan gaya {style['tone']} agar audience lebih nyaman menikmati isi konten."]
        )
    )

    # =========================================================
    # FINAL
    # =========================================================
    return (

        f"{category_text}\n\n"

        f"{platform_text}\n\n"

        f"{goal_text}\n\n"

        f"Strategi rekomendasi ini dibuat agar konten tidak hanya mengikuti tren, tetapi juga tetap relevan dengan karakter audience, gaya konsumsi platform, serta tujuan utama konten yang ingin dicapai."
    )

# =========================================================
# CONTENT ANGLE GENERATOR (ADAPTIVE + KEYMAP BASED)
# =========================================================
def generate_content_angle(goal, topic=None, category=None):

    import random
    import re

    goal = str(goal).lower() if goal else ""
    topic = str(topic).lower() if topic else ""
    category = str(category).lower() if category else ""

    merged = f"{goal} {topic} {category}"

    # normalisasi
    merged = re.sub(r'[^a-z0-9\s]', ' ', merged)
    merged = " ".join(merged.split())

    # =====================================================
    # TEKNOLOGI & DIGITAL
    # =====================================================
    teknologi_keywords = [

        "ai", "artificial intelligence", "chatgpt", "teknologi",
        "gadget", "laptop", "smartphone", "iphone", "android",
        "coding", "programming", "software", "startup",
        "cyber", "kamera", "gpu", "pc", "robot",
        "machine learning", "website", "app", "digital"
    ]

    # =====================================================
    # HIBURAN
    # =====================================================
    hiburan_keywords = [

        "meme", "komedi", "lucu", "viral", "prank",
        "hiburan", "parodi", "funny", "ngakak",
        "challenge", "drama", "anime", "film",
        "music", "musik", "concert", "reaction"
    ]

    # =====================================================
    # EDUKASI
    # =====================================================
    edukasi_keywords = [

        "tutorial", "belajar", "tips", "edukasi",
        "how to", "cara", "panduan", "kelas",
        "skill", "produktif", "matematika",
        "coding", "investasi", "belajar cepat"
    ]

    # =====================================================
    # FASHION & BEAUTY
    # =====================================================
    fashion_keywords = [

        "fashion", "outfit", "skincare", "makeup",
        "beauty", "style", "ootd", "parfum",
        "lipstick", "glow up", "haircare",
        "aesthetic", "clean girl"
    ]

    # =====================================================
    # KULINER
    # =====================================================
    kuliner_keywords = [

        "makanan", "kuliner", "cafe", "kopi",
        "masak", "resep", "minuman", "food",
        "restaurant", "jajanan", "dessert",
        "matcha", "bakso", "mie", "ayam",
        "burger", "street food"
    ]

    # =====================================================
    # LIFESTYLE & TRAVEL
    # =====================================================
    lifestyle_keywords = [

        "travel", "liburan", "hotel", "healing",
        "lifestyle", "morning routine", "gym",
        "workout", "daily", "routine",
        "daily life", "vlog", "wisata",
        "pantai", "self improvement",
        "wellness", "mindset",
        "slow living", "productive"
    ]

    # =====================================================
    # BISNIS & MARKETING
    # =====================================================
    bisnis_keywords = [

        "jualan", "marketing", "bisnis",
        "branding", "produk", "affiliate",
        "promo", "diskon", "seller",
        "marketplace", "content marketing",
        "personal branding", "jualan online"
    ]

    # =====================================================
    # DETECT CATEGORY
    # =====================================================
    detected = "general"

    if any(k in merged for k in teknologi_keywords):
        detected = "teknologi"

    elif any(k in merged for k in hiburan_keywords):
        detected = "hiburan"

    elif any(k in merged for k in edukasi_keywords):
        detected = "edukasi"

    elif any(k in merged for k in fashion_keywords):
        detected = "fashion"

    elif any(k in merged for k in kuliner_keywords):
        detected = "kuliner"

    elif any(k in merged for k in lifestyle_keywords):
        detected = "lifestyle"

    elif any(k in merged for k in bisnis_keywords):
        detected = "bisnis"

    # =====================================================
    # ANGLE MAPPING
    # =====================================================
    angle_map = {

        # =================================================
        # TEKNOLOGI
        # =================================================
        "teknologi": [

            "Tutorial AI sederhana",
            "Review teknologi viral",
            "Eksperimen tools AI",
            "Perbandingan aplikasi",
            "Tips produktivitas digital",
            "Hidden feature gadget",
            "AI workflow sehari-hari",
            "Tools gratis yang underrated",
            "Teknologi yang lagi hype",
            "Eksperimen ChatGPT",
            "Setup meja produktif",
            "Aplikasi yang bikin kerja cepat",
            "Transformasi digital",
            "Review gadget viral",
            "Cara kerja teknologi modern",
            "Website keren yang jarang diketahui",
            "Life hack digital",
            "Teknologi masa depan",
            "Insight dunia startup",
            "Coding untuk pemula",
            "Kesalahan umum pengguna AI",
            "Tools AI buat content creator",
            "AI vs manusia",
            "Eksplor fitur terbaru",
            "Tech facts yang bikin kaget"
        ],

        # =================================================
        # HIBURAN
        # =================================================
        "hiburan": [

            "POV relatable",
            "Storytelling lucu",
            "Drama ringan sehari-hari",
            "Reaction content",
            "Meme format viral",
            "Trend challenge",
            "Situasi random",
            "Kelakuan netizen",
            "Sketsa komedi pendek",
            "Relatable Gen Z moment",
            "Humor kehidupan sehari-hari",
            "POV absurd",
            "Expectation vs reality",
            "Reaction tren viral",
            "Challenge kocak",
            "Storytime chaos",
            "Momen memalukan",
            "Kelakuan orang zaman sekarang",
            "Konten random tapi relate",
            "Parodi internet culture",
            "Trend TikTok lucu",
            "Drama tongkrongan",
            "Ekspresi overthinking",
            "Sound viral adaptation"
        ],

        # =================================================
        # EDUKASI
        # =================================================
        "edukasi": [

            "Tutorial singkat",
            "Penjelasan sederhana",
            "Step-by-step",
            "Tips cepat dipahami",
            "Kesalahan umum pemula",
            "Fakta mengejutkan",
            "Belajar cepat ala Gen Z",
            "Cara kerja sesuatu",
            "Mindset penting",
            "Tips produktif",
            "Hack belajar",
            "Penjelasan pakai analogi",
            "Tutorial praktis",
            "Life hack edukatif",
            "Problem solving sederhana",
            "Quick tips harian",
            "Insight yang jarang dijelaskan",
            "Kesalahan yang sering dilakukan",
            "Cara mulai dari nol",
            "Tutorial tanpa ribet",
            "Visual learning",
            "Belajar 1 menit",
            "Tips anti bingung",
            "Rahasia produktivitas"
        ],

        # =================================================
        # FASHION
        # =================================================
        "fashion": [

            "OOTD aesthetic",
            "Fashion hacks",
            "Makeup transformation",
            "Styling tips",
            "Before-after look",
            "Trend outfit viral",
            "Outfit kampus",
            "Outfit nongkrong",
            "Clean girl aesthetic",
            "Get ready with me",
            "Daily outfit inspo",
            "Glow up transformation",
            "Mix and match outfit",
            "Skincare routine",
            "Style ala Pinterest",
            "Fashion Gen Z",
            "Simple classy look",
            "Outfit budget friendly",
            "Tutorial makeup natural",
            "Daily makeup look",
            "Streetwear vibes",
            "Aesthetic transition",
            "Haircare routine",
            "Fashion trend analysis"
        ],

        # =================================================
        # KULINER
        # =================================================
        "kuliner": [

            "Review makanan viral",
            "Street food hunting",
            "Mukbang aesthetic",
            "Resep sederhana",
            "Food recommendation",
            "Makanan underrated",
            "Cafe hopping",
            "First bite reaction",
            "Kuliner malam",
            "Hidden gem kuliner",
            "Menu viral TikTok",
            "Dessert aesthetic",
            "Minuman viral",
            "Masak cepat ala anak kos",
            "Battle makanan viral",
            "Review jujur makanan",
            "Kuliner budget friendly",
            "Menu unik dan aneh",
            "Comfort food vibes",
            "Kuliner nostalgia",
            "Jajanan trending",
            "ASMR makanan",
            "Behind the kitchen",
            "Taste test challenge"
        ],

        # =================================================
        # LIFESTYLE
        # =================================================
        "lifestyle": [

            "Daily lifestyle vlog",
            "Healing aesthetic",
            "Morning routine",
            "Produktivitas harian",
            "Weekend activity idea",
            "Self improvement",
            "Slow living vibes",
            "Study vlog",
            "Travel diary",
            "Night routine",
            "Reset day routine",
            "Cafe productivity",
            "Healthy lifestyle",
            "Gym motivation",
            "Mindset positif",
            "Rutinitas realistis",
            "Me time activity",
            "Daily habits",
            "Journaling routine",
            "Work-life balance",
            "Travel hidden gem",
            "Lifestyle ala Gen Z",
            "Kebiasaan kecil produktif",
            "Digital detox"
        ],

        # =================================================
        # BISNIS
        # =================================================
        "bisnis": [

            "Strategi marketing viral",
            "Tips jualan online",
            "Personal branding",
            "Cara bikin audience tertarik",
            "Konten soft selling",
            "Analisis bisnis viral",
            "Studi kasus brand",
            "Kesalahan branding",
            "Cara naikkan engagement",
            "Content marketing strategy",
            "Bisnis modal kecil",
            "Affiliate marketing",
            "Strategi closing",
            "Cara bikin produk viral",
            "Mindset entrepreneur",
            "Tips UMKM digital",
            "Growth strategy",
            "Cara bangun komunitas",
            "Brand storytelling",
            "Psikologi marketing",
            "Strategi FYP untuk bisnis",
            "Digital selling hacks",
            "Tren bisnis online",
            "Customer psychology"
        ],

        # =================================================
        # GENERAL
        # =================================================
        "general": [

            "Trend storytelling",
            "Insight viral",
            "Pendapat kontroversial",
            "Analisis tren",
            "Konten relatable",
            "Storytime personal",
            "Fakta menarik",
            "Opini ringan",
            "Sudut pandang unik",
            "Random thoughts",
            "Eksperimen sosial",
            "Observasi internet",
            "Fenomena media sosial",
            "Bahasan yang lagi rame",
            "Vibes kehidupan sekarang"
        ]
    }

    return random.choice(angle_map.get(detected, angle_map["general"]))

# =========================================================
# MAIN GENERATOR
# =========================================================
def generate_content_idea(
    trend,
    goal,
    platform,
    category,
    real_caption="",
    context_signal=None
):

    topic = str(trend.get('query', '')).strip()

    # ambil fallback dari trend + context content kalau ada
    if not topic:
        topic = (
            trend.get("query")
            or trend.get("keyword")
            or "topik viral"
        )

    # 🔥 TAMBAHAN: paksa topic lebih “context-aware”
    if isinstance(trend, dict):
        topic = (
            trend.get("main_topic")
            or trend.get("user_keyword")
            or trend.get("trend_query")
            or trend.get("clean")
            or "konten"
        )

        topic = str(topic).strip()
    # =========================
    # DETECT CATEGORY
    # =========================
    if not category:
        category = detect_category(topic)

    # 🔥 override kecil biar tidak melenceng
    trend_category = detect_category(trend.get("query", ""))
    if trend_category != "General Content":
        category = trend_category

    # =========================
    # GOAL STYLE
    # =========================
    style = goal_style(goal)

    # =========================
    # TITLE
    # =========================
    title = generate_title(
        topic,
        goal
    )

    # =========================
    # CAPTION
    # =========================
    caption = generate_caption(
        topic=trend.get("query", topic),
        goal=goal,
        category=category,
        platform=platform,
        real_caption=real_caption
    )

    # =========================
    # HASHTAGS
    # =========================
    hashtags = generate_hashtags(
        trend.get("query", topic),  # 🔥 pakai trend utama
        goal,
        platform
    )

    # =========================
    # STRATEGY
    # =========================
    strategy = generate_strategy(
        category,
        goal
    )

    # 🔥 tambahkan konteks trend biar tidak generic
    strategy += f"\nKonten ini diarahkan berdasarkan tren utama: {trend.get('query', topic)}."

    # =========================
    # REASONING
    # =========================
    reasoning = generate_reasoning(
        topic,
        category,
        goal,
        platform
    )

    # 🔥 inject trend context (ini penting untuk skripsi)
    reasoning += f"\n\nTren utama yang digunakan sebagai referensi: '{trend.get('query', topic)}'."

    # =========================
    # CONTENT ANGLE
    # =========================
    content_angle = generate_content_angle(
        goal
    )

    # =========================
    # STORYBOARD
    # =========================
    storyboard = generate_storyboard(
        {
            "query": trend.get("query", topic),
            "category": category
        },
        goal,
        platform,
        real_caption
    )

    # =========================
    # RETURN
    # =========================
    return {
        "category": category,
        "title": title,
        "caption": caption,
        "hashtags": hashtags,
        "strategy": strategy,
        "reasoning": reasoning,
        "content_angle": content_angle,
        "storyboard": storyboard,

        # 🔥 TAMBAHAN KONTROL SKRIPSI
        "trend_source": trend.get("query"),
        "used_as_core_topic": True,

        # style metadata
        "tone": style["tone"],
        "focus": style["focus"],
        "cta": style["cta"]
    }