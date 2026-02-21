from homeassistant.components.cover import CoverEntity
from .const import DOMAIN

class RemootioCover(CoverEntity):
    def __init__(self, coordinator, entry_id):
        self.coordinator = coordinator
        self.entry_id = entry_id
        self._state = None
        self.coordinator.add_listener(self._update_state)

    @property
    def name(self):
        return f"Remootio 3 Door {self.entry_id}"

    @property
    def is_closed(self):
        if self._state is None:
            return None
        return self._state == "closed"

    async def async_open_cover(self, **kwargs):
        await self.coordinator.client.send_command("open")

    async def async_close_cover(self, **kwargs):
        await self.coordinator.client.send_command("close")

    async def async_stop_cover(self, **kwargs):
        await self.coordinator.client.send_command("stop")

    def _update_state(self, state):
        self._state = state
        self.async_write_ha_state()
