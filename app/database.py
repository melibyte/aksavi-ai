import sqlite3

from flask import current_app, g


def get_db():
    """Mevcut istek için SQLite veritabanı bağlantısını döndürür."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_URL"])
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    """Açık veritabanı bağlantısını kapatır."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    """Leads tablosunu oluşturur ve bağlantı kapatma işlemini kaydeder."""
    with app.app_context():
        db = get_db()

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        db.commit()

    app.teardown_appcontext(close_db)


def lead_ekle(isim, telefon, mesaj=None):
    """Yeni bir potansiyel müşteri kaydı oluşturur."""
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO leads (isim, telefon, mesaj)
        VALUES (?, ?, ?)
        """,
        (isim, telefon, mesaj),
    )

    db.commit()

    return cursor.lastrowid


def tum_leadler():
    """Potansiyel müşteri kayıtlarını en yeniden eskiye listeler."""
    db = get_db()

    kayitlar = db.execute(
        """
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY id DESC
        """
    ).fetchall()

    return [dict(kayit) for kayit in kayitlar]