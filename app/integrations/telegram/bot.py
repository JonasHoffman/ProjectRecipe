import os

import httpx
from dotenv import load_dotenv


load_dotenv()


class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")

        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not configured.")

        self.base_url = (
            f"https://api.telegram.org/bot{self.token}"
        )

    def get_me(self):
        response = httpx.get(
            f"{self.base_url}/getMe"
        )

        response.raise_for_status()

        return response.json()

    def set_webhook(self, url: str):
        response = httpx.post(
            f"{self.base_url}/setWebhook",
            params={"url": url},
        )

        response.raise_for_status()

        return response.json()
    def get_webhook_info(self):
        response = httpx.get(
            f"{self.base_url}/getWebhookInfo"
        )

        response.raise_for_status()

        return response.json()

    def send_message(
        self,
        chat_id: int,
        text: str,
    ):
        response = httpx.post(
            f"{self.base_url}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=30.0,
        )

        response.raise_for_status()

        return response.json()

    def send_photo(
        self,
        chat_id: int,
        photo: str,
        caption: str | None = None,
    ):
        response = httpx.post(
            f"{self.base_url}/sendPhoto",
            json={
                "chat_id": chat_id,
                "photo": photo,
                "caption": caption,
            },
            timeout=30.0,
        )

        response.raise_for_status()

        return response.json()