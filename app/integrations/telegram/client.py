import os

import httpx
from dotenv import load_dotenv


load_dotenv()


class TelegramClient:

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")

        if not self.token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured.")

        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.file_url = f"https://api.telegram.org/file/bot{self.token}"

    async def get_file(self, file_id: str) -> dict:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.api_url}/getFile",
                params={"file_id": file_id},
            )

            response.raise_for_status()

            data = response.json()

            if not data["ok"]:
                raise RuntimeError("Failed to get Telegram file.")

            return data["result"]

    async def download_file(
        self,
        file_path: str,
        destination: str,
    ) -> None:
        url = f"{self.file_url}/{file_path}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)

            response.raise_for_status()

            with open(destination, "wb") as file:
                file.write(response.content)