from homeassistant import config_entries
from .const import DOMAIN, CONF_API_KEY, CONF_API_SECRET

class RemootioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validate input here if needed
            return self.async_create_entry(title="Remootio 3", data=user_input)

        data_schema = {
            CONF_API_KEY: str,
            CONF_API_SECRET: str,
            "host": str,
            "port": int,
        }
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
