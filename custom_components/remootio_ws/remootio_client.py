import asyncio
import json
import ssl
import hashlib
import hmac
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import websockets


class RemootioClient:

    def __init__(self, host, port, api_key, api_secret, state_callback):
        self._uri = f"wss://{host}:{port}"
        self._api_key = api_key
        self._api_secret = api_secret.encode()
        self._state_callback = state_callback
        self._ssl = ssl._create_unverified_context()
        self._ws = None
        self._connected = False
        self._state = None

    @property
    def state(self):
        return self._state

    @property
    def connected(self):
        return self._connected

    async def connect(self):
        self._ws = await websockets.connect(
            self._uri,
            ssl=self._ssl,
            ping_interval=20,
        )
        await self._authenticate()
        self._connected = True
        asyncio.create_task(self._listen())

    async def disconnect(self):
        self._connected = False
        if self._ws:
            await self._ws.close()

    async def _authenticate(self):
        raw = await self._ws.recv()
        challenge_msg = json.loads(raw)

        challenge = base64.b64decode(challenge_msg["challenge"])

        key = hashlib.sha256(self._api_secret).digest()

        cipher = AES.new(key, AES.MODE_CBC, iv=challenge[:16])
        encrypted = cipher.encrypt(pad(challenge, AES.block_size))

        signature = hmac.new(key, encrypted, hashlib.sha256).digest()

        payload = {
            "type": "auth",
            "apiKey": self._api_key,
            "response": base64.b64encode(encrypted).decode(),
            "signature": base64.b64encode(signature).decode()
        }

        await self._ws.send(json.dumps(payload))

        result = json.loads(await self._ws.recv())
        if result.get("status") != "ok":
            raise Exception("Remootio authentication failed")

    async def _listen(self):
        while self._connected:
            try:
                msg = await self._ws.recv()
                data = json.loads(msg)

                if "doorState" in data:
                    self._state = data["doorState"]
                    self._state_callback(self._state)

            except Exception:
                self._connected = False
                await asyncio.sleep(5)
                await self.connect()

    async def send_command(self, command):
        await self._ws.send(json.dumps({
            "type": "command",
            "command": command
        }))
