from flask import Blueprint, jsonify, render_template, request

from app.database import (
    dashboard_istatistikleri,
    lead_ekle,
    sohbet_ekle,
    tum_leadler,
    tum_sohbetler,
)

from app.services.ai_service import AIServiceError, ai_service


main_bp = Blueprint("main", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")


# =========================================================
# YARDIMCI FONKSIYONLAR
# =========================================================

def boolean_degeri(deger):
    """
    Wix'ten gelen KVKK degerini boolean'a cevirir.
    """

    if isinstance(deger, bool):
        return deger

    if isinstance(deger, (int, float)):
        return bool(deger)

    if isinstance(deger, str):
        return deger.strip().lower() in (
            "true",
            "1",
            "yes",
            "evet",
            "on"
        )

    return False


def talep_json_hazirla(lead):
    """
    Veritabani kaydini Wix yonetim panelinin
    bekledigi formata cevirir.
    """

    return {

        "id":
            lead.get("id"),

        "ad_soyad":
            lead.get("isim") or "",

        "eposta":
            lead.get("eposta") or "",

        "telefon":
            lead.get("telefon") or "",

        "firma":
            lead.get("firma") or "",

        "talep_konusu":
            lead.get("talep_konusu") or "",

        "mesaj":
            lead.get("mesaj") or "",

        "kvkk":
            bool(lead.get("kvkk_onay")),

        "tarih":
            lead.get("tarih") or ""
    }


# =========================================================
# ANA SAYFA
# =========================================================

@main_bp.route("/", methods=["GET"])
def ana_sayfa():

    return render_template(
        "index.html"
    )


# =========================================================
# FLASK YONETIM PANELI
# =========================================================

@main_bp.route("/dashboard", methods=["GET"])
def dashboard():

    sohbetler = tum_sohbetler()

    leads = tum_leadler()

    istatistikler = (
        dashboard_istatistikleri()
    )

    return render_template(
        "dashboard.html",
        sohbetler=sohbetler,
        leads=leads,
        istatistikler=istatistikler
    )


# =========================================================
# CHATBOT
# =========================================================

@api_bp.route(
    "/sohbet",
    methods=["POST"]
)
def sohbet():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    mesaj = str(
        data.get(
            "mesaj",
            ""
        )
    ).strip()

    gecmis = data.get(
        "gecmis",
        []
    )

    if not mesaj:

        return jsonify({

            "basarili":
                False,

            "hata":
                "Mesaj alani zorunludur."

        }), 400


    try:

        # Groq / AI cevabi
        yanit = ai_service.yanit_uret(
            mesaj,
            gecmis
        )

        # Konusmayi veritabanina kaydet
        sohbet_ekle(
            kullanici_mesaji=mesaj,
            ai_yaniti=yanit
        )

        return jsonify({

            "basarili":
                True,

            "yanit":
                yanit

        }), 200


    except AIServiceError:

        return jsonify({

            "basarili":
                False,

            "hata":
                (
                    "Yapay zeka servisine "
                    "su anda ulasilamiyor."
                )

        }), 503


# =========================================================
# ESKI LEADS ENDPOINT'I
# CHATBOT / ESKI SISTEM BOZULMASIN DIYE KALIYOR
# =========================================================

@api_bp.route(
    "/leads",
    methods=["POST"]
)
def lead_olustur():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    isim = str(
        data.get(
            "isim",
            ""
        )
    ).strip()

    eposta = str(
        data.get(
            "eposta",
            ""
        )
    ).strip()

    telefon = str(
        data.get(
            "telefon",
            ""
        )
    ).strip()

    firma = str(
        data.get(
            "firma",
            ""
        )
    ).strip()

    talep_konusu = str(
        data.get(
            "talep_konusu",
            ""
        )
    ).strip()

    mesaj = str(
        data.get(
            "mesaj",
            ""
        )
    ).strip()

    kvkk_onay = boolean_degeri(
        data.get(
            "kvkk_onay",
            False
        )
    )


    if not isim:

        return jsonify({

            "basarili":
                False,

            "hata":
                "Ad Soyad alani zorunludur."

        }), 400


    if not eposta:

        return jsonify({

            "basarili":
                False,

            "hata":
                "E-posta alani zorunludur."

        }), 400


    if not telefon:

        return jsonify({

            "basarili":
                False,

            "hata":
                "Telefon alani zorunludur."

        }), 400


    if not kvkk_onay:

        return jsonify({

            "basarili":
                False,

            "hata":
                (
                    "KVKK Aydinlatma Metni'ni "
                    "kabul etmeniz gerekmektedir."
                )

        }), 400


    lead_id = lead_ekle(

        isim=isim,

        eposta=eposta,

        telefon=telefon,

        firma=(
            firma
            or None
        ),

        talep_konusu=(
            talep_konusu
            or None
        ),

        mesaj=(
            mesaj
            or None
        ),

        kvkk_onay=kvkk_onay
    )


    return jsonify({

        "basarili":
            True,

        "mesaj":
            "Talebiniz basariyla alinmistir.",

        "id":
            lead_id

    }), 201


# =========================================================
# ESKI LEADS LISTESI
# =========================================================

@api_bp.route(
    "/leads",
    methods=["GET"]
)
def leadleri_listele():

    return jsonify({

        "basarili":
            True,

        "leads":
            tum_leadler()

    }), 200


# =========================================================
# YENI WIX ILETISIM FORMU
# POST /api/talepler
# =========================================================

@api_bp.route(
    "/talepler",
    methods=["POST"]
)
def talep_olustur():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    ad_soyad = str(
        data.get(
            "ad_soyad",
            ""
        )
    ).strip()


    eposta = str(
        data.get(
            "eposta",
            ""
        )
    ).strip()


    telefon = str(
        data.get(
            "telefon",
            ""
        )
    ).strip()


    firma = str(
        data.get(
            "firma",
            ""
        )
    ).strip()


    talep_konusu = str(
        data.get(
            "talep_konusu",
            ""
        )
    ).strip()


    mesaj = str(
        data.get(
            "mesaj",
            ""
        )
    ).strip()


    kvkk = boolean_degeri(
        data.get(
            "kvkk",
            False
        )
    )


    # ------------------------------------------------
    # ZORUNLU ALANLAR
    # ------------------------------------------------

    if not ad_soyad:

        return jsonify({

            "basarili":
                False,

            "hata":
                "Ad Soyad alani zorunludur."

        }), 400


    if not eposta:

        return jsonify({

            "basarili":
                False,

            "hata":
                "E-posta alani zorunludur."

        }), 400


    if not talep_konusu:

        return jsonify({

            "basarili":
                False,

            "hata":
                "Talep Konusu alani zorunludur."

        }), 400


    if not mesaj:

        return jsonify({

            "basarili":
                False,

            "hata":
                "Mesaj alani zorunludur."

        }), 400


    if not kvkk:

        return jsonify({

            "basarili":
                False,

            "hata":
                (
                    "KVKK Aydinlatma Metni'ni "
                    "kabul etmeniz gerekmektedir."
                )

        }), 400


    # ------------------------------------------------
    # VERITABANINA KAYDET
    # ------------------------------------------------

    lead_id = lead_ekle(

        isim=ad_soyad,

        eposta=eposta,

        telefon=telefon,

        firma=(
            firma
            or None
        ),

        talep_konusu=talep_konusu,

        mesaj=mesaj,

        kvkk_onay=kvkk
    )


    return jsonify({

        "basarili":
            True,

        "mesaj":
            "Talebiniz basariyla alinmistir.",

        "id":
            lead_id

    }), 201


# =========================================================
# WIX YONETIM PANELI
# GET /api/talepler
# =========================================================

@api_bp.route(
    "/talepler",
    methods=["GET"]
)
def talepleri_listele():

    leads = tum_leadler()

    talepler = [

        talep_json_hazirla(
            lead
        )

        for lead in leads
    ]


    return jsonify({

        "basarili":
            True,

        "talepler":
            talepler

    }), 200


# =========================================================
# CHATBOT KONUŞMALARINI LISTELE
# =========================================================

@api_bp.route(
    "/sohbetler",
    methods=["GET"]
)
def sohbetleri_listele():

    return jsonify({

        "basarili":
            True,

        "sohbetler":
            tum_sohbetler()

    }), 200