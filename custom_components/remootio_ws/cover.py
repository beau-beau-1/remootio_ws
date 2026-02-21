from homeassistant.components.cover import (
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RemootioCover(coordinator)])

class RemootioCover(CoordinatorEntity, CoverEntity):

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Garage Door"
        self._attr_supported_features = (
            CoverEntityFeature.OPEN |
            CoverEntityFeature.CLOSE |
            CoverEntityFeature.STOP
        )

    @property
    def is_closed(self):
        return self.coordinator.data == "closed"

    @property
    def available(self):
        return self.coordinator.client.connected

    async def async_open_cover(self, **kwargs):
        await self.coordinator.client.send_command("open")

    async def async_close_cover(self, **kwargs):
        await self.coordinator.client.send_command("close")

    async def async_stop_cover(self, **kwargs):
        await self.coordinator.client.send_command("stop")
