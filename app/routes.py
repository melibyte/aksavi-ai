from flask import Blueprint, jsonify, render_template, request

from app.database import (
    lead_ekle,
    tum_leadler,
    sohbet_ekle,
    tum_sohbetler,
    dashboard_istatistikleri,
)

from app.services.ai_service import AIServiceError, ai_service


main_bp = Blueprint("main", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")


# ---------------------------------------------------
# ANA SAYFA
# ---------------------------------------------------

@main_bp.route("/", methods=["GET"])
def ana_sayfa():
    return render_template("index.html")


# ---------------------------------------------------
# YÖNETİM PANELİ
# ---------------------------------------------------

@main_bp.route("/dashboard", methods=["GET"])
def dashboard():

    sohbetler = tum_sohbetler()
    leads = tum_leadler()
    istatistikler = dashboard_istatistikleri()

    return render_template(
        "dashboard.html",
        sohbetler=sohbetler,
        leads=leads,
        istatistikler=istatistikler,
    )


# ---------------------------------------------------
# CHATBOT
# ---------------------------------------------------

@api_bp.route("/sohbet", methods=["POST"])
def sohbet():

    data = request.get_json(silent=True) or {}

    mesaj = str(data.get("mesaj", "")).strip()
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basarili": False,
            "hata": "Mesaj alanı zorunludur."
        }), 400

    try:

        # Yapay zekâdan cevap al
        yanit = ai_service.yanit_uret(
            mesaj,
            gecmis
        )

        # Konuşmayı veritabanına kaydet
        sohbet_ekle(
            kullanici_mesaji=mesaj,
            ai_yaniti=yanit
        )

        return jsonify({
            "basarili": True,
            "yanit": yanit
        }), 200

    except AIServiceError:

        return jsonify({
            "basarili": False,
            "hata": "Yapay zekâ servisine şu anda ulaşılamıyor."
        }), 503


# ---------------------------------------------------
# MÜŞTERİ TALEBİ EKLE
# ---------------------------------------------------

@api_bp.route("/leads", methods=["POST"])
def lead_olustur():

    data = request.get_json(silent=True) or {}

    isim = str(data.get("isim", "")).strip()
    telefon = str(data.get("telefon", "")).strip()
    mesaj = str(data.get("mesaj", "")).strip()

    if not isim or not telefon:

        return jsonify({
            "basarili": False,
            "hata": "İsim ve telefon alanları zorunludur."
        }), 400

    lead_id = lead_ekle(
        isim=isim,
        telefon=telefon,
        mesaj=mesaj or None
    )

    return jsonify({
        "basarili": True,
        "mesaj": "Talebiniz başarıyla kaydedildi.",
        "id": lead_id
    }), 201


# ---------------------------------------------------
# MÜŞTERİ TALEPLERİNİ LİSTELE
# ---------------------------------------------------

@api_bp.route("/leads", methods=["GET"])
def leadleri_listele():

    return jsonify({
        "basarili": True,
        "leads": tum_leadler()
    }), 200


# ---------------------------------------------------
# CHATBOT KONUŞMALARINI LİSTELE
# ---------------------------------------------------

@api_bp.route("/sohbetler", methods=["GET"])
def sohbetleri_listele():

    return jsonify({
        "basarili": True,
        "sohbetler": tum_sohbetler()
    }), 200