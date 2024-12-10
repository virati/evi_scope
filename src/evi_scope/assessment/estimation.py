import asyncio
from hume import AsyncHumeClient
from hume.expression_measurement.stream import Config
from hume.expression_measurement.stream.socket_client import StreamConnectOptions
from dotenv import load_dotenv
import os

async def main():
    load_dotenv(dotenv_path=".env")
    client = AsyncHumeClient(api_key=os.getenv("HUME_API_KEY"))

    model_config = Config(prosody={})

    stream_options = StreamConnectOptions(config=model_config)

    async with client.expression_measurement.stream.connect(options=stream_options) as socket:
        result = await socket.send_file(")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())