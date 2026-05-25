from extensions import db
from datetime import datetime

class SosmedData(db.Model):
    __tablename__ = 'sosmed_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    judul = db.Column(db.Text)
    caption = db.Column(db.Text) 
    hashtag = db.Column(db.Text)
    kategori = db.Column(db.String(100))
    platform = db.Column(db.String(50))
    tanggal = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class TrendsData(db.Model):
    __tablename__ = 'trends_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100))
    trend_query = db.Column(db.String(255))
    increase_percent = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class EmbeddedData(db.Model):
    __tablename__ = 'embedded_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ref_id = db.Column(db.String(50))
    content_preview = db.Column(db.Text)
    platform_origin = db.Column(db.String(20))
    vector_json = db.Column(db.JSON)
    trend_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class User(db.Model):
    __tablename__ = 'users' # Diubah menjadi 'user' agar sinkron dengan FK
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Optional: Tambahkan relationship agar mudah narik data history dari user
    histories = db.relationship('AnalysisHistory', backref='owner', lazy=True)







class AnalysisHistory(db.Model):

    __tablename__ = 'analysis_history'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    generate_id = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

    # =========================
    # INPUT USER
    # =========================
    input_text = db.Column(db.String(255))
    platform = db.Column(db.String(50))
    goal = db.Column(db.String(50))

    # =========================
    # RESULT AI
    # =========================
    trend_query = db.Column(db.Text)

    match_title = db.Column(db.Text)

    category = db.Column(db.String(150))

    content_angle = db.Column(db.Text)

    reasoning = db.Column(db.Text)

    trend_status = db.Column(db.String(100))

    opportunity_label = db.Column(db.String(100))

    # =========================
    # METRICS
    # =========================
    cosine_score = db.Column(db.Float)

    opportunity_index = db.Column(db.Float)

    growth = db.Column(db.Float)

    density = db.Column(db.Float)

    preference_score = db.Column(db.Float)

    final_score = db.Column(db.Float)

    # =========================
    # GENERATED CONTENT
    # =========================
    caption = db.Column(db.Text)

    strategy = db.Column(db.Text)

    hashtags = db.Column(db.Text)

    # STORYBOARD DISIMPAN JSON
    storyboard = db.Column(db.JSON)



class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100))
    action = db.Column(db.String(100))
    status = db.Column(db.String(50))
    description = db.Column(db.Text)
    execution_time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class PreprocessingData(db.Model):
    __tablename__ = 'preprocessing_data'

    id = db.Column(db.Integer, primary_key=True)

    source_type = db.Column(db.String(20))  # sosmed / trend

    source_id = db.Column(db.Integer)

    raw_text = db.Column(db.Text)
    case_folding = db.Column(db.Text)
    cleaned = db.Column(db.Text)
    tokens = db.Column(db.Text)
    stopwords = db.Column(db.Text)
    final_text = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=db.func.now())




