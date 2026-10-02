import asyncio

from app.integrations.telegram.client import TelegramClient


async def main():
    client = TelegramClient()

    file_info = await client.get_file(
        "AwACAgEAAxkBAAM-ar8JBFQNlCX9qab5K6cbUggdpm8AAksJAAKT2vhFcxW34P2OGxA9BA"
    )

    print("FILE INFO:")
    print(file_info)

    file_path = file_info["file_path"]

    await client.download_file(
        file_path,
        "voice_test.oga",
    )

    print("FILE DOWNLOADED")


if __name__ == "__main__":
    asyncio.run(main())