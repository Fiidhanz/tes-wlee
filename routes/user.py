import random
import re
import uuid
from flask import app, render_template, request, redirect, url_for, session, flash
from sqlalchemy import or_, func
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from extensions import db
from models import SosmedData, TrendsData, User, AnalysisHistory, EmbeddedData
from datetime import datetime
from services.pipeline import run_pipeline
from services.generator import (
    generate_content_idea,
    detect_category
)

# Decorator sederhana untuk login_required jika belum ada
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_logged_in' not in session:
            flash("Silahkan login terlebih dahulu.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def init_user_routes(app):
    
    # --- ROUTE LOGIN ---
    @app.route('/user/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                session.clear()
                
                # Ambil data dari database ke variabel lokal dulu
                db_fullname = user.fullname
                db_role = user.role
                db_email = user.email
                
                # Debug di Terminal: Cek apakah data ini muncul di terminal paman?
                print(f"DEBUG LOGIN: {db_fullname}, {db_role}, {db_email}")

                session['user_logged_in'] = True
                session['user_id'] = user.id
                session['user_name'] = str(db_fullname).strip() if db_fullname else "User"
                session['user_role'] = str(db_role).strip() if db_role else "user"
                session['email'] = db_email
                
                # Paksa session tersimpan
                session.modified = True
                
                nama_depan = session['user_name'].split()[0]
                flash(f"Selamat datang kembali, {nama_depan}!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Email atau Password salah!", "danger")
        
        return render_template('user/login.html')

    # --- ROUTE REGISTER ---
    @app.route('/user/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            fullname = request.form.get('fullname')
            email = request.form.get('email')
            password = request.form.get('password')

            user_exists = User.query.filter_by(email=email).first()
            if user_exists:
                flash("Email sudah terdaftar!", "danger")
                return redirect(url_for('register'))

            hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')

            try:
                new_user = User(fullname=fullname, email=email, password=hashed_pw)
                db.session.add(new_user)
                db.session.commit()
                flash("Akun berhasil dibuat! Silahkan login.", "success")
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f"Terjadi kesalahan: {str(e)}", "danger")

        return render_template('user/register.html')

    # --- ROUTE DASHBOARD ---
    @app.route('/user/dashboard')
    @login_required
    def dashboard():

        from sqlalchemy.sql.expression import func

        # =========================
        # COUNT DATA
        # =========================
        google_total = db.session.query(TrendsData).count()

        tiktok_total = db.session.query(SosmedData)\
            .filter(SosmedData.platform.ilike('tiktok'))\
            .count()

        ig_total = db.session.query(SosmedData)\
            .filter(SosmedData.platform.ilike('instagram'))\
            .count()

        yt_total = db.session.query(SosmedData)\
            .filter(SosmedData.platform.ilike('youtube'))\
            .count()

        # =========================
        # LATEST TREND
        # =========================
        google_trend = db.session.query(TrendsData)\
            .order_by(TrendsData.created_at.desc())\
            .first()

        # =========================
        # QUICK INSIGHT
        # =========================
        counts = {
            "TikTok": tiktok_total,
            "Instagram": ig_total,
            "YouTube": yt_total
        }

        top_platform = max(counts, key=counts.get)
        top_value = counts[top_platform]

        # =========================
        # GRAND TOTAL
        # =========================
        grand_total = (
            google_total +
            tiktok_total +
            ig_total +
            yt_total
        )

        # =========================
        # RANDOM RECOMMENDATION
        # =========================
        recommendations = db.session.query(EmbeddedData)\
            .order_by(func.random())\
            .limit(5)\
            .all()

        return render_template(
            'user/dashboard.html',

            google_total=google_total,
            google_trend=google_trend,

            tiktok_total=tiktok_total,
            ig_total=ig_total,
            yt_total=yt_total,

            top_platform=top_platform,
            top_value=top_value,

            grand_total=grand_total,

            recommendations=recommendations,

            now=datetime.now()
        )

    # --- ROUTE GENERATE (ALGORITMA & AUTO-SAVE HISTORY) ---
    def parse_prompt(text):

        text_lower = text.lower()

        # =========================
        # PLATFORM DETECTION
        # =========================
        platform = "tiktok"

        platform_patterns = {
            "instagram": ["instagram", "ig", "reels"],
            "youtube": ["youtube", "yt", "shorts"],
            "tiktok": ["tiktok", "tik tok"]
        }

        for p, keywords in platform_patterns.items():
            if any(k in text_lower for k in keywords):
                platform = p
                break

        # =========================
        # GOAL DETECTION
        # =========================
        goal = "edukasi"

        goal_patterns = {
            "hiburan": [
                "hiburan", "funny", "viral",
                "lucu", "meme", "relate", "komedi"
            ],

            "promosi": [
                "jualan", "promosi", "marketing",
                "bisnis", "produk", "brand"
            ],

            "edukasi": [
                "belajar", "tutorial",
                "edukasi", "tips", "cara"
            ]
        }

        for g, keywords in goal_patterns.items():
            if any(k in text_lower for k in keywords):
                goal = g
                break

        # =========================
        # CATEGORY DETECTION
        # =========================
        category = "Edukasi & Tutorial"

        category_patterns = {

            "Teknologi & Gadget": [
                "ai", "teknologi", "coding", "programming",
                "laptop", "smartphone", "iphone",
                "android", "gadget", "aplikasi"
            ],

            "Hiburan & Komedi": [
                "hiburan", "komedi", "meme",
                "lucu", "viral", "parodi", "ngakak"
            ],

            "Edukasi & Tutorial": [
                "tutorial", "belajar", "tips",
                "cara", "edukasi", "kelas"
            ],

            "Fashion & Beauty": [
                "fashion", "outfit", "skincare",
                "makeup", "beauty", "style"
            ],

            "Kuliner / Food & Beverage": [
                "makanan", "kuliner", "resep",
                "minuman", "coffee", "cafe",
                "food", "masak"
            ],

            "Travel & Lifestyle": [
                "travel", "liburan", "healing",
                "lifestyle", "hotel", "wisata",
                "trip"
            ]
        }

        for cat, keywords in category_patterns.items():
            if any(k in text_lower for k in keywords):
                category = cat
                break

        # =========================
        # CLEANING
        # =========================
        filler = [
            "saya", "ingin", "mau",
            "buat", "membuat",
            "konten", "tentang",
            "untuk", "yang",
            "agar", "supaya",
            "di", "ke", "dari",
            "bantu", "tolong"
        ]

        cleaned = text_lower

        for f in filler:
            cleaned = re.sub(rf'\b{f}\b', ' ', cleaned)

        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        # =========================
        # SMART KEYWORD EXTRACTION
        # =========================
        important_phrases = []

        patterns = [
            r"tentang (.+)",
            r"mengenai (.+)",
            r"bahas (.+)",
            r"topik (.+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text_lower)

            if match:
                important_phrases.append(match.group(1))

        if important_phrases:
            keyword = important_phrases[0]
        else:
            keyword = cleaned

        keyword = " ".join(keyword.split()[:12])

        return keyword, platform, goal, category


    # --- ROUTE GENERATE ---
    @app.route('/user/generate', methods=['GET', 'POST'])
    @login_required
    def generate():

        # =========================
        # GET -> FORM PAGE
        # =========================
        if request.method == 'GET':

            return render_template(
                'user/generate_form.html',
                is_prompt=False,
                detected_category="General"
            )

        # =========================
        # DEFAULT
        # =========================
        result = []
        trend_keywords = []
        content_ranking = []
        trend_graph = []
        opportunity_distribution = []

        category = "General"
        is_prompt = False

        # =========================
        # SMART PROMPT MODE
        # =========================
        prompt = request.form.get('user_prompt')

        if prompt and prompt.strip():

            keyword, platform_target, goal, category = parse_prompt(prompt)
            is_prompt = True

        # =========================
        # FORM MODE
        # =========================
        else:

            keyword = request.form.get('keyword')
            platform_target = request.form.get('platform')
            goal = request.form.get('goal')

            goal = str(goal).lower().strip() if goal else ""
            goal = goal.replace("&", " ").replace("/", " ")
            goal = " ".join(goal.split())

            goal_map = {
                "promotion": "promosi",
                "promosi": "promosi",
                "hard selling": "promosi",
                "soft selling": "promosi",

                "entertainment": "hiburan",
                "hiburan": "hiburan",

                "education": "edukasi",
                "edukasi": "edukasi"
            }

            category = detect_category(keyword)

            print("DEBUG CATEGORY INPUT:", category)

            is_prompt = False

        # =========================
        # DEBUG
        # =========================
        print("========== DEBUG GENERATE ==========")
        print("Keyword :", keyword)
        print("Platform:", platform_target)
        print("Goal    :", goal)
        print("Category:", category)
        print("====================================")

        # =========================
        # VALIDASI
        # =========================
        if not keyword or keyword.strip() == "":

            flash("Keyword tidak boleh kosong!", "warning")

            return redirect('/user/generate')

        # =========================
        # THRESHOLD
        # =========================
        threshold = 0.45 if is_prompt else 0.30

        # =========================
        # PIPELINE
        # =========================
        data = run_pipeline(
            keyword,
            platform_target,
            goal,
            threshold=threshold
        )

        # =========================
        # HASIL
        # =========================
        trend_keywords = data.get("trend_keywords", [])
        content_ranking = data.get("content_ranking", [])
        trend_graph = data.get("trend_graph", [])
        opportunity_distribution = data.get("opportunity_distribution", [])

        result = trend_keywords

        # =========================
        # FALLBACK AI
        # =========================
        if len(result) == 0:

            fake_trend = {
                "query": keyword,
                "sim": 0.55,
                "growth_val": 0.35,
                "density": 0.25,
                "oi": 0.70,
                "score": 0.62
            }

            from services.generator import generate_content_idea

            ai_result = generate_content_idea(
                fake_trend,
                goal,
                platform_target,
                category=category,
                real_caption=None
            )

            result = [{
                "query": keyword,

                "sim": 0.55,
                "growth_val": 0.35,
                "density": 0.25,
                "oi": 0.70,
                "score": 0.62,

                "trend_status": "AI Generated Trend",
                "opportunity_label": "Potential Topic",

                "title": ai_result.get("title"),
                "caption": ai_result.get("caption"),
                "hashtags": ai_result.get("hashtags"),
                "strategy": ai_result.get("strategy"),
                "storyboard": ai_result.get("storyboard"),

                "category": ai_result.get("category"),
                "content_angle": ai_result.get("content_angle"),
                "reasoning": ai_result.get("reasoning"),

                "platform": platform_target
            }]

        # =========================
        # SAVE ALL HISTORY
        # =========================
        if len(result) > 0:

            try:

                # 🔥 1 generate = 1 ID
                generate_id = str(uuid.uuid4())

                history_entries = []

                for r in result:

                    history_entry = AnalysisHistory(

                        # =========================
                        # GROUP GENERATE
                        # =========================
                        generate_id=generate_id,

                        # =========================
                        # USER INPUT
                        # =========================
                        user_id=session['user_id'],

                        input_text=keyword,
                        platform=platform_target,
                        goal=goal,

                        # =========================
                        # AI RESULT
                        # =========================
                        trend_query=r.get('query'),

                        match_title=r.get('title'),

                        category=r.get('category'),

                        content_angle=r.get('content_angle'),

                        reasoning=r.get('reasoning'),

                        trend_status=r.get('trend_status'),

                        opportunity_label=r.get('opportunity_label'),

                        # =========================
                        # METRICS
                        # =========================
                        cosine_score=float(r.get('sim', 0) or 0),

                        opportunity_index=float(r.get('oi', 0) or 0),

                        growth=float(r.get('growth_val', 0) or 0),

                        density=float(r.get('density', 0) or 0),

                        preference_score=float(
                            r.get('preference_score', 0) or 0
                        ),

                        final_score=float(r.get('score', 0) or 0),

                        # =========================
                        # GENERATED CONTENT
                        # =========================
                        caption=r.get('caption'),

                        strategy=r.get('strategy'),

                        hashtags=r.get('hashtags'),

                        storyboard=r.get('storyboard', [])
                    )

                    history_entries.append(history_entry)

                db.session.add_all(history_entries)

                db.session.commit()

                print(f"SUCCESS SAVE {len(history_entries)} HISTORY")

            except Exception as e:

                db.session.rollback()

                print("ERROR SAVE HISTORY:", str(e))

        # =========================
        # RESULT PAGE
        # =========================
        return render_template(
            'user/generate_result.html',
            result=result,
            trend_keywords=trend_keywords,
            content_ranking=content_ranking,
            trend_graph=trend_graph,
            opportunity_distribution=opportunity_distribution,
            is_prompt=is_prompt,
            detected_category=category
        )

    # --- ROUTE HISTORY ---
    @app.route('/user/history')
    @login_required
    def history():

        selected_platform = request.args.get('platform', 'all')

        query = db.session.query(

            AnalysisHistory.generate_id,

            func.max(AnalysisHistory.timestamp).label('timestamp'),

            func.max(AnalysisHistory.input_text).label('input_text'),

            func.max(AnalysisHistory.platform).label('platform'),

            func.max(AnalysisHistory.goal).label('goal'),

            func.count(AnalysisHistory.id).label('total_result')

        ).filter(

            AnalysisHistory.user_id == session['user_id']

        )

        # FILTER PLATFORM
        if selected_platform != 'all':

            query = query.filter(
                AnalysisHistory.platform.ilike(selected_platform)
            )

        history_data = query.group_by(

            AnalysisHistory.generate_id

        ).order_by(

            func.max(AnalysisHistory.timestamp).desc()

        ).all()

        return render_template(
            'user/history.html',
            history_data=history_data,
            selected_platform=selected_platform
        )


    # --- DETAIL HISTORY ---
    @app.route('/user/history/<generate_id>')
    @login_required
    def history_detail(generate_id):

        history_detail = AnalysisHistory.query.filter_by(
            generate_id=generate_id,
            user_id=session['user_id']
        ).order_by(
            AnalysisHistory.final_score.desc()
        ).all()

        if not history_detail:
            flash("History tidak ditemukan", "danger")
            return redirect('/user/history')

        return render_template(
            'user/history_detail.html',
            history_detail=history_detail
        )


    # --- ROUTE LOGOUT ---
    @app.route('/user/logout')
    def logout():
        session.clear()
        flash("Anda telah logout.", "info")
        return redirect(url_for('common.landing'))