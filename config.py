# import os
# from dotenv import load_dotenv

# load_dotenv()


# class Config:
#     """Uygulamanın ortak yapılandırma ayarları."""

#     SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
#     ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")
#     ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
#     DATABASE_URL = os.environ.get("DATABASE_URL", "aksavi.db")
#     GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
#     AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

#     BUSINESS_CONTEXT = os.environ.get(
#         "BUSINESS_CONTEXT",
#         (
#             "Sen AKSAVİ'nin yapay zekâ destekli Cloud & DevOps asistanısın. "
#             "Kullanıcılara AKSAVİ hizmetleri hakkında temel bilgi ver ve "
#             "ihtiyaçlarını anlamaya çalış."
#         ),
#     )

#     CORS_ORIGINS = [
#         origin.strip()
#         for origin in os.environ.get(
#             "CORS_ORIGINS",
#             "http://localhost:5000"
#         ).split(",")
#         if origin.strip()
#     ]


# class DevelopmentConfig(Config):
#     """Yerel geliştirme ortamı."""

#     DEBUG = True


# class ProductionConfig(Config):
#     """Canlı ortam."""

#     DEBUG = False


# config_by_name = {
#     "development": DevelopmentConfig,
#     "production": ProductionConfig,
#     "default": DevelopmentConfig,
# }


import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    """Uygulamanın ortak yapılandırma ayarları."""

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-change-me"
    )

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "aksavi.db"
    )

    GROQ_API_KEY = os.environ.get(
        "GROQ_API_KEY",
        ""
    )

    AI_PROVIDER = os.environ.get(
        "AI_PROVIDER",
        "groq"
    )

    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        (
            "Sen AKSAVİ'nin yapay zekâ destekli Cloud & DevOps asistanısın. "
            "Kullanıcılara AKSAVİ hizmetleri hakkında temel bilgi ver ve "
            "ihtiyaçlarını anlamaya çalış."
        ),
    )

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.environ.get(
            "CORS_ORIGINS",
            "http://localhost:5000"
        ).split(",")
        if origin.strip()
    ]


class DevelopmentConfig(Config):
    """Yerel geliştirme ortamı."""

    DEBUG = True


class ProductionConfig(Config):
    """Canlı ortam."""

    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}