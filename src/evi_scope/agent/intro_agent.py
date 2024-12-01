import asyncio
import base64
import datetime
import os
from dotenv import load_dotenv
from hume.client import AsyncHumeClient
from hume.empathic_voice.chat.socket_client import ChatConnectOptions, ChatWebsocketConnection
from hume.empathic_voice.chat.types import SubscribeEvent
from hume.empathic_voice.types import UserInput
from hume.core.api_error import ApiError
from hume import MicrophoneInterface, Stream

class WebSocketHandler:
  """Interface for containing the EVI WebSocket and associated socket handling behavior."""

  def __init__(self):
    """Construct the WebSocketHandler, initially assigning the socket to None and the byte stream to a new Stream object."""
    self.socket = None
    self.byte_strs = Stream.new()

  def set_socket(self, socket: ChatWebsocketConnection):
    """Set the socket."""
    self.socket = socket

  async def on_open(self):
    """Logic invoked when the WebSocket connection is opened."""
    print("WebSocket connection opened.")

  async def on_message(self, message: SubscribeEvent):
    """Callback function to handle a WebSocket message event.
    
    This asynchronous method decodes the message, determines its type, and 
    handles it accordingly. Depending on the type of message, it 
    might log metadata, handle user or assistant messages, process
    audio data, raise an error if the message type is "error", and more.

    See the full list of "Receive" messages in the API Reference.
    """

    if message.type == "chat_metadata":
      chat_id = message.chat_id
      chat_group_id = message.chat_group_id
      # ...
    elif message.type in ["user_message", "assistant_message"]:
      role = message.message.role.upper()
      message_text = message.message.content
      # ...
    elif message.type == "audio_output":
      message_str: str = message.data
      message_bytes = base64.b64decode(message_str.encode("utf-8"))
      await self.byte_strs.put(message_bytes)
      return
    elif message.type == "error":
      error_message = message.message
      error_code = message.code
      raise ApiError(f"Error ({error_code}): {error_message}")
    
    # Print timestamp and message
    # ...
      
  async def on_close(self):
    """Logic invoked when the WebSocket connection is closed."""
    print("WebSocket connection closed.")

  async def on_error(self, error):
    """Logic invoked when an error occurs in the WebSocket connection."""
    print(f"Error: {error}")


async def main() -> None:
    # Retrieve any environment variables stored in the .env file
    load_dotenv()

    # Retrieve the API key, Secret key, and EVI config id from the environment variables
    HUME_API_KEY = os.getenv("HUME_API_KEY")
    HUME_SECRET_KEY = os.getenv("HUME_SECRET_KEY")
    HUME_CONFIG_ID = os.getenv("HUME_CONFIG_ID")

    # Initialize the asynchronous client, authenticating with your API key
    client = AsyncHumeClient(api_key=HUME_API_KEY)

    # Define options for the WebSocket connection, such as an EVI config id and a secret key for token authentication
    options = ChatConnectOptions(config_id=HUME_CONFIG_ID, secret_key=HUME_SECRET_KEY)
    
    # ...
        # Instantiate the WebSocketHandler
    websocket_handler = WebSocketHandler()
    # Open the WebSocket connection with the configuration options and the handler's functions
    async with client.empathic_voice.chat.connect_with_callbacks(
      options=options,
      on_open=websocket_handler.on_open,
      on_message=websocket_handler.on_message,
      on_close=websocket_handler.on_close,
      on_error=websocket_handler.on_error
    ) as socket:
    
      # Set the socket instance in the handler
        websocket_handler.set_socket(socket)
        # Create an asynchronous task to continuously detect and process input from the microphone, as well as play audio
        microphone_task = asyncio.create_task(
        MicrophoneInterface.start(
            socket,
            byte_stream=websocket_handler.byte_strs
        )
        )
    
        # Await the microphone task
        await microphone_task
