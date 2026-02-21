import asyncio
from homeassistant.core import HomeAssistant
from .remootio_client import RemootioClient

class RemootioCoordinator:
    def __init__(self, hass: HomeAssistant, entry):
        self.hass = hass
        self.entry = entry
        self.client = RemootioClient(
            host=entry.data["host"],
            port=entry.data["port"],
            api_key=entry.data["api_key"],
            api_secret=entry.data["api_secret"],
            state_callback=self._state_update,
        )
        self._listeners = []

    async def async_setup(self):
        await self.client.connect()

    async def async_shutdown(self):
        await self.client.disconnect()

    def _state_update(self, state):
        for listener in self._listeners:
            listener(state)

    def add_listener(self, callback):
        self._listeners.append(callback)
