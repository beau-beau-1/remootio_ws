import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_API_KEY, CONF_API_SECRET, DEFAULT_PORT

class RemootioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Remootio 3", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_API_SECRET): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema)
