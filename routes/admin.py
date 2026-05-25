import os
import pandas as pd
import time
from datetime import datetime
from flask import json, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from sqlalchemy import text, func
from extensions import db, cache # Pastikan extensions.py sudah ada cache
from models import SosmedData, TrendsData, EmbeddedData, User, PreprocessingData
from model.similarity import compute_all
from model.embedding import embed
from model.opportunity import opportunity_index
from model.density import content_density 
from utils.preprocessing import full_preprocess
from decorators import admin_required
from sqlalchemy import select

# --- FUNGSI HELPER LOG ACTIVITY ---

def log_activity(action, status, description, execution_time=None):
    """Mencatat aktivitas ke tabel activity_logs secara otomatis"""
    try:
        # Mengambil email dari session sebagai identifier user
        u_id = session.get('email', 'SYSTEM')
        
        query = text("""
            INSERT INTO activity_logs (user_id, action, status, description, execution_time, created_at)
            VALUES (:u_id, :action, :status, :description, :exec_time, :ts)
        """)
        
        db.session.execute(query, {
            'u_id': u_id,
            'action': action,
            'status': status,
            'description': description,
            'exec_time': execution_time,
            'ts': datetime.now()
        })
        db.session.commit()
    except Exception as e:
        print(f"Gagal mencatat log: {e}")
        db.session.rollback()

# --- FUNGSI CACHE UNTUK PROSES BERAT ---

from sklearn.metrics.pairwise import cosine_similarity

@cache.memoize(timeout=3600)
def get_cached_similarity_results():

    trends = db.session.execute(db.select(TrendsData)).scalars().all()
    sosmed = db.session.execute(db.select(SosmedData)).scalars().all()

    if not trends or not sosmed:
        return []

    trend_texts = [str(t.trend_query or "") for t in trends]
    sosmed_texts = [f"{s.judul or ''} {s.caption or ''}" for s in sosmed]

    # EMBEDDING SEKALI
    trend_vecs = embed(trend_texts)
    sosmed_vecs = embed(sosmed_texts)

    # 🔥 FIX BESAR: MATRIX (bukan loop manual)
    sim_matrix = cosine_similarity(trend_vecs, sosmed_vecs)

    results = []

    for i, row in enumerate(sim_matrix):

        best_idx = row.argmax()
        max_score = row[best_idx]

        matched = sosmed[best_idx]

        results.append({
            "trend_query": trends[i].trend_query,
            "best_match_title": matched.judul or "Untitled",
            "best_match_caption": (matched.caption or "")[:120],
            "platform": matched.platform,
            "score": round(float(max_score), 4),
            "percentage": int(max_score * 100)
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)

@cache.memoize(timeout=3600)
def get_cached_opportunity_results():

    trends = db.session.execute(db.select(TrendsData)).scalars().all()
    sosmed = db.session.execute(db.select(SosmedData)).scalars().all()

    if not trends or not sosmed:
        return []

    trend_texts = [str(t.trend_query or "") for t in trends]
    sosmed_texts = [f"{s.judul or ''} {s.caption or ''}" for s in sosmed]

    trend_vecs = embed(trend_texts)
    sosmed_vecs = embed(sosmed_texts)

    sim_matrix = cosine_similarity(trend_vecs, sosmed_vecs)

    results = []

    for i, row in enumerate(sim_matrix):

        density_val = float(row.mean()) if len(row) > 0 else 0.0
        max_sim = float(row.max()) if len(row) > 0 else 0.0

        growth_val = str(trends[i].increase_percent or "0").lower()
        growth_val = growth_val.replace("%", "").replace("+", "")

        if "breakout" in growth_val:
            growth_val = 5.0
        else:
            try:
                growth_val = float(growth_val) / 100
            except:
                growth_val = 0.1

        oi_score = opportunity_index(growth_val, density_val)

        results.append({
            "query": trends[i].trend_query,
            "category": trends[i].category,
            "growth": trends[i].increase_percent,
            "oi": round(oi_score, 2),
            "density": round(density_val, 4),
            "max_sim_percent": int(max_sim * 100)
        })

    return sorted(results, key=lambda x: x["oi"], reverse=True)

# --- INIT ROUTES ---

def init_admin_routes(app):
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            if email == "admin@trendreco.com" and password == "admin_secret_2026":
                session.clear()
                session['user_logged_in'] = True
                session['user_role'] = 'admin'
                session['email'] = email
                flash("Akses Admin Diberikan.", "success")
                
                # LOG ACTIVITY
                log_activity("Login", "Success", f"Admin {email} berhasil login.")
                
                return redirect(url_for('admin_dashboard'))
            else:
                # LOG ACTIVITY FAILED
                log_activity("Login Attempt", "Warning", f"Gagal login admin dengan email: {email}")
                flash("Kredensial Admin Tidak Valid!", "danger")
        return render_template('admin/login.html')

    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        # 1. Total Dataset (Semua baris di tabel sosmed_data)
        total_dataset = db.session.execute(text("SELECT COUNT(*) FROM sosmed_data")).scalar() or 0
        
        # 2. Vectorized Data (Data yang sudah punya embedding/vector)
        total_vectorized = db.session.execute(text("SELECT COUNT(*) FROM sosmed_data WHERE caption IS NOT NULL")).scalar() or 0
        
        # 3. Total Users
        total_users = db.session.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        
        # 4. Distribusi Platform (Hitung persentase)
        def get_platform_pct(platform_name):
            count = db.session.execute(text(
                "SELECT COUNT(*) FROM sosmed_data WHERE platform = :p"), {'p': platform_name}
            ).scalar() or 0
            return round((count / total_dataset * 100), 1) if total_dataset > 0 else 0

        platform_stats = {
            'ig': get_platform_pct('Instagram'),
            'tiktok': get_platform_pct('TikTok'),
            'youtube': get_platform_pct('YouTube')
        }

        # 5. Activity Logs (Ambil 3 aktivitas terbaru dari tabel activity_logs)
        recent_activities = db.session.execute(text(
            "SELECT action, created_at FROM activity_logs ORDER BY created_at DESC LIMIT 3"
        )).fetchall()

        return render_template('admin/dashboard.html', 
                            total_dataset=total_dataset,
                            total_vectorized=total_vectorized,
                            total_users=total_users,
                            platform_stats=platform_stats,
                            recent_activities=recent_activities)

    @app.route('/admin/upload', methods=['GET'])
    @admin_required
    def admin_upload():
        recent_data = []
        try:
            sosmed_summary = db.session.execute(text(
                "SELECT platform as name, COUNT(*) as count, MAX(created_at) as date, 'Sosmed' as type "
                "FROM sosmed_data GROUP BY platform"
            )).fetchall()

            trends_summary = db.session.execute(text(
                "SELECT category as name, COUNT(*) as count, MAX(created_at) as date, 'Trend' as type "
                "FROM trends_data GROUP BY category"
            )).fetchall()

            combined = list(sosmed_summary) + list(trends_summary)
            combined.sort(key=lambda x: x.date if x.date else "", reverse=True)

            for row in combined:
                recent_data.append({
                    'name': row.name, 'count': row.count,
                    'date': row.date.strftime('%d %b %Y, %H:%M') if row.date else "-",
                    'type': row.type
                })
        except Exception as e:
            print(f"Error fetching summary: {e}")
        return render_template('admin/upload.html', recent_data=recent_data)

    @app.route('/admin/embedding')
    @admin_required
    def admin_embedding():
        try:
            stmt = select(EmbeddedData).order_by(EmbeddedData.created_at.desc())
            embedded_list = db.session.execute(stmt).scalars().all()
        except Exception as e:
            print("ERROR admin_embedding:", e)
            embedded_list = []

        return render_template('admin/embedding.html', embedded_list=embedded_list)


    
    @app.route('/admin/execute-embedding', methods=['POST'])
    @admin_required
    def execute_embedding():
        start_time = time.time()

        try:
            import json
            from sqlalchemy import select

            raw_sosmed = db.session.execute(select(SosmedData)).scalars().all()
            raw_trends = db.session.execute(select(TrendsData)).scalars().all()

            count_sosmed = 0
            count_trend = 0

            # ==================================================
            # SOSMED BATCH EMBEDDING
            # ==================================================
            sosmed_texts = []
            sosmed_items = []

            for item in raw_sosmed:
                ref = f"SOS-{item.id}"

                exists = db.session.execute(
                    select(EmbeddedData).where(EmbeddedData.ref_id == ref)
                ).scalar_one_or_none()

                if exists:
                    continue

                text_content = f"{item.judul or ''} {item.caption or ''} {item.hashtag or ''}".strip()

                if not text_content:
                    continue

                sosmed_texts.append(text_content)
                sosmed_items.append((item, ref))

            # EMBEDDING SEKALI (FAST)
            if sosmed_texts:
                sosmed_vectors = embed(sosmed_texts)

                for i, (item, ref) in enumerate(sosmed_items):
                    vector = sosmed_vectors[i]

                    vec_list = vector.tolist() if hasattr(vector, "tolist") else list(vector)

                    db.session.add(EmbeddedData(
                        ref_id=ref,
                        content_preview=sosmed_texts[i][:150],
                        platform_origin=item.platform,
                        vector_json=json.dumps(vec_list),
                        trend_score=0.0
                    ))

                    count_sosmed += 1

            # ==================================================
            # TRENDS BATCH EMBEDDING
            # ==================================================
            trend_texts = []
            trend_items = []

            for t in raw_trends:
                ref = f"TRD-{t.id}"

                exists = db.session.execute(
                    select(EmbeddedData).where(EmbeddedData.ref_id == ref)
                ).scalar_one_or_none()

                if exists:
                    continue

                text_content = f"{t.trend_query or ''} {t.category or ''}".strip()

                if not text_content:
                    continue

                trend_texts.append(text_content)
                trend_items.append((t, ref))

            # EMBEDDING SEKALI
            if trend_texts:
                trend_vectors = embed(trend_texts)

                for i, (t, ref) in enumerate(trend_items):
                    vector = trend_vectors[i]

                    vec_list = vector.tolist() if hasattr(vector, "tolist") else list(vector)

                    db.session.add(EmbeddedData(
                        ref_id=ref,
                        content_preview=trend_texts[i][:150],
                        platform_origin="Google Trends",
                        vector_json=json.dumps(vec_list),
                        trend_score=0.0
                    ))

                    count_trend += 1

            # ==================================================
            # COMMIT SEKALI (WAJIB UNTUK SPEED)
            # ==================================================
            db.session.commit()

            exec_time = round((time.time() - start_time) * 1000)

            log_activity(
                "Embedding Execution",
                "Success",
                f"Sosmed: {count_sosmed}, Trend: {count_trend}",
                exec_time
            )

            return jsonify({
                "status": "success",
                "message": f"Embedding selesai | Sosmed: {count_sosmed}, Trend: {count_trend}",
                "time_ms": exec_time
            })

        except Exception as e:
            db.session.rollback()

            return jsonify({
                "status": "error",
                "message": str(e)
            })
        



    @app.route('/admin/upload/sosmed', methods=['POST'])
    @admin_required
    def upload_sosmed():
        start_time = time.time()
        platform = request.form.get('platform')
        files = request.files.getlist('file_dataset[]')

        if not files or files[0].filename == '':
            flash("Pilih file CSV dulu!", "danger")
            return redirect(url_for('admin_upload'))

        # 🔥 FUNCTION HARUS DI LUAR LOOP & RAPI
        def auto_map_columns(df):
            column_mapping = {}

            for col in df.columns:
                c = col.lower().strip()

                if any(x in c for x in ['title', 'judul', 'headline']):
                    column_mapping[col] = 'judul'

                elif any(x in c for x in ['caption', 'content', 'text', 'deskripsi']):
                    column_mapping[col] = 'caption'

                elif any(x in c for x in ['hashtag', 'tag', 'tags']):
                    column_mapping[col] = 'hashtag'

                elif any(x in c for x in ['kategori', 'category']):
                    column_mapping[col] = 'kategori'

                elif any(x in c for x in ['date', 'tanggal', 'time']):
                    column_mapping[col] = 'tanggal'

            return df.rename(columns=column_mapping)

        try:
            file_names = []

            for file in files:
                if file and file.filename.endswith('.csv'):

                    filename = secure_filename(f"{platform}_{file.filename}")
                    file_names.append(filename)

                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sosmed', filename)

                    # 🔥 pastikan folder ada
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                    file.save(file_path)

                    # 🔥 baca CSV aman
                    try:
                        df_raw = pd.read_csv(file_path, encoding='utf-8')
                    except:
                        df_raw = pd.read_csv(file_path, encoding='latin1')

                    df_raw.columns = df_raw.columns.str.strip()

                    # 🔥 AUTO MAPPING
                    df_mapped = auto_map_columns(df_raw)

                    # 🔥 AMBIL KOLOM SESUAI DB
                    df_fixed = df_mapped.reindex(columns=[
                        'judul', 'caption', 'hashtag', 'kategori', 'tanggal'
                    ])

                    # 🔥 TAMBAHKAN PLATFORM
                    df_fixed['platform'] = platform

                    # 🔥 HANDLE NULL
                    df_fixed = df_fixed.where(pd.notnull(df_fixed), None)

                    # 🔥 DEBUG (WAJIB SAAT TESTING)
                    print(df_fixed.head())

                    # 🔥 INSERT KE DB
                    with db.engine.begin() as connection:
                        df_fixed.to_sql('sosmed_data', con=connection, if_exists='append', index=False)

            exec_duration = round((time.time() - start_time) * 1000)

            log_activity(
                "Upload Sosmed",
                "Success",
                f"Upload dataset {platform}: {', '.join(file_names)}",
                exec_duration
            )

            cache.delete_memoized(get_cached_similarity_results)
            cache.delete_memoized(get_cached_opportunity_results)

            flash(f"Berhasil upload dataset {platform}!", "success")

        except Exception as e:
            import traceback
            traceback.print_exc()

            log_activity("Upload Sosmed", "Error", f"Gagal upload {platform}: {str(e)}")
            flash(f"Gagal simpan: {str(e)}", "danger")

        return redirect(url_for('admin_upload'))

    @app.route('/admin/upload/gtrends', methods=['POST'])
    @admin_required
    def upload_gtrends():

        start_time = time.time()

        category = request.form.get('category')
        files = request.files.getlist('file_dataset[]')

        if not files or files[0].filename == '':
            flash("Pilih file CSV!", "danger")
            return redirect(url_for('admin_upload'))

        try:

            total_inserted = 0
            file_names = []

            for file in files:

                if file and file.filename.endswith('.csv'):

                    # =========================
                    # SAVE FILE
                    # =========================
                    filename = secure_filename(
                        f"gtrends_{file.filename}"
                    )

                    file_names.append(filename)

                    file_path = os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        'gtrends',
                        filename
                    )

                    os.makedirs(
                        os.path.dirname(file_path),
                        exist_ok=True
                    )

                    file.save(file_path)

                    # =========================
                    # READ CSV
                    # =========================
                    try:

                        df = pd.read_csv(
                            file_path,
                            encoding='utf-8'
                        )

                    except:

                        df = pd.read_csv(
                            file_path,
                            encoding='latin1'
                        )

                    # =========================
                    # CLEAN HEADER
                    # =========================
                    df.columns = (
                        df.columns
                        .str.strip()
                        .str.lower()
                    )

                    print("=== CSV COLUMNS ===")
                    print(df.columns.tolist())

                    # =========================
                    # AUTO DETECT COLUMN
                    # =========================
                    query_col = None
                    growth_col = None

                    for col in df.columns:

                        c = col.lower().strip()

                        # QUERY
                        if c in [
                            'query',
                            'top queries',
                            'rising queries'
                        ]:
                            query_col = col

                        # GROWTH
                        elif c in [
                            'search interest',
                            'increase percent',
                            'increase_percent',
                            'value'
                        ]:
                            growth_col = col

                    print("QUERY COL:", query_col)
                    print("GROWTH COL:", growth_col)

                    # =========================
                    # VALIDASI
                    # =========================
                    if not query_col:

                        flash(
                            f"Kolom query tidak ditemukan di {filename}",
                            "danger"
                        )

                        continue

                    # =========================
                    # INSERT MANUAL
                    # =========================
                    inserted = 0

                    for _, row in df.iterrows():

                        trend_query = str(
                            row.get(query_col, '')
                        ).strip()

                        if not trend_query:
                            continue

                        increase_percent = None

                        if growth_col:

                            increase_percent = str(
                                row.get(growth_col, '')
                            ).strip()

                            increase_percent = (
                                increase_percent
                                .replace('%', '')
                                .replace('+', '')
                            )

                        new_trend = TrendsData(
                            category=category,
                            trend_query=trend_query,
                            increase_percent=increase_percent
                        )

                        db.session.add(new_trend)

                        inserted += 1

                    db.session.commit()

                    total_inserted += inserted

                    print(f"INSERTED: {inserted}")

            # =========================
            # EXEC TIME
            # =========================
            exec_duration = round(
                (time.time() - start_time) * 1000
            )

            # =========================
            # LOG
            # =========================
            log_activity(
                "Upload G-Trends",
                "Success",
                f"Upload tren kategori {category}: {total_inserted} data",
                exec_duration
            )

            # =========================
            # CLEAR CACHE
            # =========================
            cache.delete_memoized(
                get_cached_similarity_results
            )

            cache.delete_memoized(
                get_cached_opportunity_results
            )

            flash(
                f"Berhasil upload {total_inserted} data Google Trends!",
                "success"
            )

        except Exception as e:

            import traceback
            traceback.print_exc()

            db.session.rollback()

            print("ERROR:", str(e))

            log_activity(
                "Upload G-Trends",
                "Error",
                str(e)
            )

            flash(
                f"Gagal upload: {str(e)}",
                "danger"
            )

        return redirect(url_for('admin_upload'))
    
    @app.route('/admin/users')
    @admin_required
    def admin_users():
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template('admin/users.html', users_list=users)


    @app.route('/admin/users/create', methods=['POST'])
    @admin_required
    def create_user():
        try:
            fullname = request.form.get('fullname')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role', 'user')

            if not fullname or not email or not password:
                return jsonify({"status": "error", "message": "Field tidak boleh kosong"})

            exists = User.query.filter_by(email=email).first()
            if exists:
                return jsonify({"status": "error", "message": "Email sudah terdaftar"})

            new_user = User(
                fullname=fullname,
                email=email,
                password=password,
                role=role
            )

            db.session.add(new_user)
            db.session.commit()

            return jsonify({"status": "success", "message": "User berhasil ditambahkan"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)})


    @app.route('/admin/users/update/<int:user_id>', methods=['POST'])
    @admin_required
    def update_user(user_id):
        try:
            user = User.query.get_or_404(user_id)

            user.fullname = request.form.get('fullname')
            user.email = request.form.get('email')
            user.role = request.form.get('role')

            if request.form.get('password'):
                user.password = request.form.get('password')

            db.session.commit()

            return jsonify({"status": "success", "message": "User berhasil diupdate"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)})


    @app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
    @admin_required
    def delete_user(user_id):
        try:
            user = User.query.get_or_404(user_id)

            db.session.delete(user)
            db.session.commit()

            return jsonify({"status": "success", "message": "User berhasil dihapus"})

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)})


    @app.route('/admin/pre-processing')
    @admin_required
    def pre_processing():

        page = request.args.get('page', 1, type=int)
        per_page = 50
        dataset = request.args.get('dataset', 'all')  # all | sosmed | trend

        query = PreprocessingData.query

        # FILTER DATASET
        if dataset != 'all':
            query = query.filter(PreprocessingData.source_type == dataset)

        data = query.order_by(
            PreprocessingData.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        preview_data = []
        for row in data.items:
            preview_data.append({
                'raw': row.raw_text,
                'case_folding': row.case_folding,
                'cleaning': row.cleaned,
                'tokenization': row.tokens,
                'stopword': row.stopwords,
                'final': row.final_text,
                'source_type': row.source_type
            })

        return render_template(
            'admin/pre_processing.html',
            preview_data=preview_data,
            pagination=data,
            dataset=dataset
        )
    

    @app.route('/admin/run-preprocessing', methods=['POST'])
    @admin_required
    def run_preprocessing():

        try:

            # =========================
            # AMBIL DATA
            # =========================
            from sqlalchemy import select
            sosmed_data = db.session.execute(
                select(SosmedData)
            ).scalars().all()

            trend_data = db.session.execute(
                select(TrendsData)
            ).scalars().all()

            if not sosmed_data and not trend_data:

                return jsonify({
                    "status": "error",
                    "msg": "Dataset kosong"
                })

            # =========================
            # KOSONGKAN TABLE
            # =========================
            db.session.query(PreprocessingData).delete()

            count = 0

            # ==================================================
            # PREPROCESSING SOSMED
            # ==================================================
            for item in sosmed_data:

                raw = f"""
                {item.judul or ''}
                {item.caption or ''}
                {item.hashtag or ''}
                """

                result = full_preprocess(raw)

                new_row = PreprocessingData(

                    source_type='sosmed',

                    source_id=item.id,

                    raw_text=raw,

                    case_folding=result["case_folding"],

                    cleaned=result["cleaning"],

                    tokens=" ".join(result["tokens"]),

                    stopwords=" ".join(result["final_tokens"]),

                    final_text=result["final_text"]
                )

                db.session.add(new_row)

                count += 1

            # ==================================================
            # PREPROCESSING GOOGLE TRENDS
            # ==================================================
            for trend in trend_data:

                raw = f"""
                {trend.trend_query or ''}
                {trend.category or ''}
                """

                result = full_preprocess(raw)

                new_row = PreprocessingData(

                    source_type='trend',

                    source_id=trend.id,

                    raw_text=raw,

                    case_folding=result["case_folding"],

                    cleaned=result["cleaning"],

                    tokens=" ".join(result["tokens"]),

                    stopwords=" ".join(result["final_tokens"]),

                    final_text=result["final_text"]
                )

                db.session.add(new_row)

                count += 1

            db.session.commit()

            return jsonify({
                "status": "success",
                "msg": f"{count} data berhasil dipreprocess"
            })

        except Exception as e:

            db.session.rollback()

            return jsonify({
                "status": "error",
                "msg": str(e)
            })
    
    @app.route('/admin/similarity')
    @admin_required
    def similarity_page():
        results = get_cached_similarity_results()
        log_activity("Similarity View", "Success", "Melihat hasil analisis Cosine Similarity.")
        return render_template('admin/similarity.html', results=results)

    @app.route('/admin/trend-growth')
    @admin_required
    def trend_growth_page():

        trends = db.session.execute(
            db.select(TrendsData)
        ).scalars().all()

        total_trends = len(trends)

        # =========================
        # NORMALIZE PERCENT
        # =========================
        def normalize_growth(val):

            try:
                if not val:
                    return 0.0

                val = str(val).lower().replace('%', '').replace('+', '').strip()

                # breakout dari Google Trends
                if 'breakout' in val:
                    return 1.0

                numeric = float(val)

                # =========================
                # RUMUS SKRIPSI
                # =========================
                normalized = min(numeric / 10, 100) / 100

                return round(normalized, 3)

            except Exception as e:
                print("NORMALIZE ERROR:", e)
                return 0.0

        # =========================
        # ATTACH NORMALIZED VALUE
        # =========================
        for t in trends:

            raw = getattr(t, 'increase_percent', 0)

            t.normalized_growth = normalize_growth(raw)

        # =========================
        # AVG
        # =========================
        if trends:

            avg_growth = (
                sum(t.normalized_growth for t in trends)
                / total_trends
            )

            avg_growth_display = f"{round(avg_growth, 2)}"

        else:
            avg_growth_display = "0.0"

        log_activity(
            "Trend Growth View",
            "Success",
            "Melihat grafik pertumbuhan tren."
        )

        return render_template(
            'admin/trend_growth.html',
            trends=trends,
            avg_growth=avg_growth_display,
            total_data=total_trends
        )

    @app.route('/admin/content-density')
    @admin_required
    def content_density():

        sosmed_data = db.session.execute(
            text("SELECT platform, judul, caption FROM sosmed_data")
        ).fetchall()

        trends = db.session.execute(
            text("SELECT trend_query FROM trends_data")
        ).fetchall()

        if not sosmed_data or not trends:
            return render_template("admin/content_density.html",
                                results=[], total_sosmed=0, total_trends=0)

        sosmed_texts = [f"{s.judul or ''} {s.caption or ''}" for s in sosmed_data]
        trend_texts = [t.trend_query for t in trends]

        sosmed_vecs = embed(sosmed_texts)
        trend_vecs = embed(trend_texts)

        sim_matrix = cosine_similarity(trend_vecs, sosmed_vecs)

        platforms = list(set([s.platform for s in sosmed_data]))

        results = []

        # 🔥 PRE-GROUP INDEX (FIX BESAR)
        platform_map = {}
        for idx, s in enumerate(sosmed_data):
            platform_map.setdefault(s.platform, []).append(idx)

        for i, row in enumerate(sim_matrix):

            for p in platforms:

                idx_list = platform_map.get(p, [])

                if not idx_list:
                    continue

                filtered = [row[j] for j in idx_list]

                density = sum(filtered) / len(filtered)
                max_sim = max(filtered)

                if density <= 0.3:
                    status = "High Potential"
                elif density >= 0.7:
                    status = "Oversaturated"
                else:
                    status = "Balanced"

                results.append({
                    "trend": trend_texts[i],
                    "platform": p,
                    "density": round(density, 4),
                    "max_similarity": round(max_sim, 4),
                    "total_content": len(filtered),
                    "status": status
                })

        results = sorted(results, key=lambda x: x["density"], reverse=True)

        return render_template(
            "admin/content_density.html",
            results=results,
            total_sosmed=len(sosmed_data),
            total_trends=len(trends)
        )

    @app.route('/admin/opportunity')
    @admin_required
    def opportunity_page():
        results = get_cached_opportunity_results()
        top_trend = results[0] if results else None
        log_activity("Opportunity View", "Success", "Melihat analisis Opportunity Index.")
        return render_template('admin/opportunity.html', results=results, top_trend=top_trend)
    
    @app.route('/admin/logs')
    @admin_required
    def system_logs():
        try:
            logs_data = db.session.execute(text("""
                SELECT action, status, description, execution_time, created_at, user_id 
                FROM activity_logs 
                ORDER BY created_at DESC
            """)).fetchall()

            total_events = len(logs_data)

            # Hitung success rate REAL
            success_count = db.session.execute(text("""
                SELECT COUNT(*) FROM activity_logs WHERE status = 'Success'
            """)).scalar() or 0

            success_rate = round((success_count / total_events * 100), 1) if total_events > 0 else 0

            # Alerts (Warning)
            alerts = db.session.execute(text("""
                SELECT COUNT(*) FROM activity_logs WHERE status = 'Warning'
            """)).scalar() or 0

        except:
            logs_data = []
            total_events = 0
            success_rate = 0
            alerts = 0

        return render_template(
            'admin/logs.html',
            logs=logs_data,
            total_events=total_events,
            success_rate=success_rate,
            alerts=alerts
        )