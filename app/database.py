import sqlite3

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE_URL"])
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def kolon_var_mi(db, tablo, kolon):
    kolonlar = db.execute(
        f"PRAGMA table_info({tablo})"
    ).fetchall()

    return kolon in [kayit["name"] for kayit in kolonlar]


def init_db(app):
    with app.app_context():
        db = get_db()

        # ---------------------------------------------------
        # MÜŞTERİ TALEPLERİ
        # ---------------------------------------------------

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                eposta TEXT,
                telefon TEXT NOT NULL,
                firma TEXT,
                talep_konusu TEXT,
                mesaj TEXT,
                kvkk_onay INTEGER DEFAULT 0,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Eski leads tablosunu SİLMEDEN yeni kolonları ekle

        if not kolon_var_mi(db, "leads", "eposta"):
            db.execute(
                "ALTER TABLE leads ADD COLUMN eposta TEXT"
            )

        if not kolon_var_mi(db, "leads", "firma"):
            db.execute(
                "ALTER TABLE leads ADD COLUMN firma TEXT"
            )

        if not kolon_var_mi(db, "leads", "talep_konusu"):
            db.execute(
                "ALTER TABLE leads ADD COLUMN talep_konusu TEXT"
            )

        if not kolon_var_mi(db, "leads", "kvkk_onay"):
            db.execute(
                """
                ALTER TABLE leads
                ADD COLUMN kvkk_onay INTEGER DEFAULT 0
                """
            )

        # ---------------------------------------------------
        # CHATBOT KONUŞMALARI
        # ---------------------------------------------------

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


# ---------------------------------------------------
# MÜŞTERİ TALEBİ EKLE
# ---------------------------------------------------

def lead_ekle(
    isim,
    telefon,
    mesaj=None,
    eposta=None,
    firma=None,
    talep_konusu=None,
    kvkk_onay=False
):
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO leads (
            isim,
            eposta,
            telefon,
            firma,
            talep_konusu,
            mesaj,
            kvkk_onay
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            isim,
            eposta,
            telefon,
            firma,
            talep_konusu,
            mesaj,
            1 if kvkk_onay else 0
        )
    )

    db.commit()

    return cursor.lastrowid


# ---------------------------------------------------
# MÜŞTERİ TALEPLERİNİ GETİR
# ---------------------------------------------------

def tum_leadler():
    db = get_db()

    kayitlar = db.execute(
        """
        SELECT
            id,
            isim,
            eposta,
            telefon,
            firma,
            talep_konusu,
            mesaj,
            kvkk_onay,
            tarih
        FROM leads
        ORDER BY id DESC
        """
    ).fetchall()

    return [dict(kayit) for kayit in kayitlar]


# ---------------------------------------------------
# CHATBOT KONUŞMASI EKLE
# ---------------------------------------------------

def sohbet_ekle(kullanici_mesaji, ai_yaniti):
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO sohbetler (
            kullanici_mesaji,
            ai_yaniti
        )
        VALUES (?, ?)
        """,
        (
            kullanici_mesaji,
            ai_yaniti
        )
    )

    db.commit()

    return cursor.lastrowid


# ---------------------------------------------------
# CHATBOT KONUŞMALARINI GETİR
# ---------------------------------------------------

def tum_sohbetler():
    db = get_db()

    kayitlar = db.execute(
        """
        SELECT
            id,
            kullanici_mesaji,
            ai_yaniti,
            tarih
        FROM sohbetler
        ORDER BY id DESC
        """
    ).fetchall()

    return [dict(kayit) for kayit in kayitlar]


# ---------------------------------------------------
# DASHBOARD İSTATİSTİKLERİ
# ---------------------------------------------------

def dashboard_istatistikleri():
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