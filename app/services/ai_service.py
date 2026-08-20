import requests

from config import Config


class AIServiceError(Exception):
    """Yapay zekâ servisiyle ilgili hataları temsil eder."""
    pass


class AIService:
    """Yapay zekâ sağlayıcısıyla iletişimi yöneten servis."""

    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "openai/gpt-oss-20b"

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.business_context = Config.BUSINESS_CONTEXT

    def _sistem_talimati(self):
        """Yapay zekânın davranışını belirleyen sistem mesajını döndürür."""
        return self.business_context

    def _mesajlari_hazirla(self, mesaj, gecmis=None):
        """Groq API'ye gönderilecek mesaj dizisini hazırlar."""
        messages = [
            {
                "role": "system",
                "content": self._sistem_talimati()
            }
        ]

        if gecmis:
            messages.extend(gecmis)

        messages.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        return messages

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajını Groq'a gönderir ve AI yanıtını döndürür."""

        if not self.api_key:
            return (
                "AI servisi şu anda demo modunda çalışıyor. "
                "Lütfen daha sonra tekrar deneyin."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.MODEL,
            "messages": self._mesajlari_hazirla(mesaj, gecmis),
        }

        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            return data["choices"][0]["message"]["content"]

        except (requests.RequestException, KeyError, IndexError, ValueError) as error:
            raise AIServiceError(
                "Yapay zekâ servisinden yanıt alınamadı."
            ) from error


ai_service = AIService()