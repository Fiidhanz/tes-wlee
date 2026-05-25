from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
# Inisialisasi tanpa app dulu
db = SQLAlchemy()
cache = Cache()