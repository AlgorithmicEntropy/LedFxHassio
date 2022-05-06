"""Ledfx integration"""
from .const import DOMAIN
from .coordinator import EffectCoordinator

import asyncio

from LedFxAPI import LedFxApi

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant import config_entries, core

from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
)


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    hass_data = dict(entry.data)
    # Registers update listener to update config entry when options are updated.
    unsub_options_update_listener = entry.add_update_listener(options_update_listener)
    # Store a reference to the unsubscribe function to cleanup if an entry is unloaded.
    hass_data["unsub_options_update_listener"] = unsub_options_update_listener
    # api and coo
    api = LedFxApi(hass_data[CONF_HOST], hass_data[CONF_PORT], hass_data[CONF_SSL])
    await api.helper.load_helpers()
    coo = EffectCoordinator(hass, api)
    await coo.async_config_entry_first_refresh()
    hass_data["coordinator"] = coo
    hass_data["api"] = api

    hass.data[DOMAIN][entry.entry_id] = hass_data

    # Forward the setup to the select platform.
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "light")
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "select")
    )
    return True


async def options_update_listener(
    hass: core.HomeAssistant, config_entry: config_entries.ConfigEntry
):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)


async def async_unload_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        [
            await asyncio.gather(
                *[hass.config_entries.async_forward_entry_unload(entry, "light")]
            ),
            await asyncio.gather(
                *[hass.config_entries.async_forward_entry_unload(entry, "select")]
            ),
        ]
    )
    # Remove options_update_listener.
    hass.data[DOMAIN][entry.entry_id]["unsub_options_update_listener"]()

    # Remove config entry from domain.
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
