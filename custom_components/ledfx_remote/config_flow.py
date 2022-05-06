"""Config flow for SolarWattEnergyManager integration."""
from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_PORT,
)

import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT, CONF_SSL
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for SolarWattEnergyManager."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        data_scheme = {
            vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
            vol.Required(CONF_HOST): cv.string,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
            vol.Required(CONF_SSL): cv.boolean,
        }

        errors = {}
        if user_input is not None:
            valid = await self.is_valid(user_input)
            if valid:
                unique_id = f"{user_input[CONF_HOST]}:{CONF_PORT}"
                await self.async_set_unique_id(unique_id)
                return self.async_create_entry(
                    title="LedFx",
                    data=user_input,
                )

            errors["base"] = "API error"

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_scheme), errors=errors
        )

    async def is_valid(self, user_input):
        """Validate input"""
        return True
