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
    """Gerekli veritabanı tablolarını oluşturur."""
    with app.app_context():
        db = get_db()

        # Müşteri talepleri
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

        # Chatbot konuşmaları
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS sohbetler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_mesaji TEXT NOT NULL,
                ai_yaniti TEXT NOT NULL,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        db.commit()

    app.teardown_appcontext(close_db)


def lead_ekle(isim, telefon, mesaj=None):
    """Yeni müşteri talebi kaydeder."""
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
    """Tüm müşteri taleplerini listeler."""
    db = get_db()

    kayitlar = db.execute(
        """
        SELECT id, isim, telefon, mesaj, tarih
        FROM leads
        ORDER BY id DESC
        """
    ).fetchall()

    return [dict(kayit) for kayit in kayitlar]


def sohbet_ekle(kullanici_mesaji, ai_yaniti):
    """Chatbot konuşmasını veritabanına kaydeder."""
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO sohbetler (kullanici_mesaji, ai_yaniti)
        VALUES (?, ?)
        """,
        (kullanici_mesaji, ai_yaniti),
    )

    db.commit()

    return cursor.lastrowid


def tum_sohbetler():
    """Tüm chatbot konuşmalarını en yeniden eskiye listeler."""
    db = get_db()

    kayitlar = db.execute(
        """
        SELECT id, kullanici_mesaji, ai_yaniti, tarih
        FROM sohbetler
        ORDER BY id DESC
        """
    ).fetchall()

    return [dict(kayit) for kayit in kayitlar]


def dashboard_istatistikleri():
    """Yönetim paneli için temel istatistikleri döndürür."""
    db = get_db()

    toplam_sohbet = db.execute(
        "SELECT COUNT(*) AS toplam FROM sohbetler"
    ).fetchone()["toplam"]

    bugunku_sohbet = db.execute(
        """
        SELECT COUNT(*) AS toplam
        FROM sohbetler
        WHERE DATE(tarih) = DATE('now')
        """
    ).fetchone()["toplam"]

    toplam_talep = db.execute(
        "SELECT COUNT(*) AS toplam FROM leads"
    ).fetchone()["toplam"]

    return {
        "toplam_sohbet": toplam_sohbet,
        "bugunku_sohbet": bugunku_sohbet,
        "toplam_talep": toplam_talep,
    }