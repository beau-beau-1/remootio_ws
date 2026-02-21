import asyncio
    @property
    def state(self):
        return self._state

    async def connect(self):
        try:
            print(f"[Remootio] Connecting to {self._uri}")
            self._ws = await websockets.connect(
                self._uri,
                ping_interval=20,
                close_timeout=10,
            )
            await self._authenticate()
            self._connected = True
            print("[Remootio] Authentication successful, starting listener")
            asyncio.create_task(self._listen())
        except Exception as e:
            print(f"[Remootio] Connect error: {e}")
            self._connected = False
            await asyncio.sleep(5)
            await self.connect()

    async def disconnect(self):
        self._connected = False
        if self._ws:
            await self._ws.close()
            self._ws = None
            print("[Remootio] Disconnected")

    async def _authenticate(self):
        raw = await self._ws.recv()
        challenge_msg = json.loads(raw)
        challenge_b64 = challenge_msg.get("challenge")
        if not challenge_b64:
            raise Exception("No challenge received from Remootio")

        challenge = base64.b64decode(challenge_b64)
        print(f"[Remootio] Challenge received (len={len(challenge)}): {challenge.hex()}")

        iv = challenge[:16].ljust(16, b'\0')
        key = hashlib.sha256(self._api_secret).digest()
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        encrypted = cipher.encrypt(pad(challenge, AES.block_size))
        signature = hmac.new(key, encrypted, hashlib.sha256).digest()

        payload = {
            "type": "auth",
            "apiKey": self._api_key,
            "response": base64.b64encode(encrypted).decode(),
            "signature": base64.b64encode(signature).decode()
        }

        await self._ws.send(json.dumps(payload))

        response = json.loads(await self._ws.recv())
        print(f"[Remootio] Authentication response: {response}")
        if response.get("status") != "ok":
            raise Exception("Remootio authentication failed")

    async def _listen(self):
        while self._connected:
            try:
                msg = await self._ws.recv()
                data = json.loads(msg)
                door_state = data.get("doorState")
                if door_state:
                    self._state = door_state
                    if self._state_callback:
                        self._state_callback(self._state)
            except Exception as e:
                print(f"[Remootio] Listen loop error: {e}")
                self._connected = False
                await asyncio.sleep(5)
                await self.connect()

    async def send_command(self, command):
        if not self._connected or not self._ws:
            raise Exception("Not connected to Remootio")
        payload = {"type": "command", "command": command}
        await self._ws.send(json.dumps(payload))
        print(f"[Remootio] Command sent: {command}")
