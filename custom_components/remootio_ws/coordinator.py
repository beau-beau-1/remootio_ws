from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from datetime import timedelta
import logging
from .remootio_client import RemootioClient

_LOGGER = logging.getLogger(__name__)

class RemootioCoordinator(DataUpdateCoordinator):

    def __init__(self, hass: HomeAssistant, entry):
        self._entry = entry
        self.client = RemootioClient(
            entry.data["host"],
            entry.data["port"],
            entry.data["api_key"],
            entry.data["api_secret"],
            self._state_updated,
        )

        super().__init__(
            hass,
            _LOGGER,
            name="Remootio",
            update_interval=timedelta(seconds=30),
        )

    async def async_setup(self):
        await self.client.connect()

    async def async_shutdown(self):
        await self.client.disconnect()

    async def _async_update_data(self):
        return self.client.state

    def _state_updated(self, state):
        self.async_set_updated_data(state)
