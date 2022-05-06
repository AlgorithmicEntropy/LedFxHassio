"""Support for SolarWatt EnergyManager API."""

from .const import DOMAIN, SERVICE_SET_EFFECT
from .ledfx_entity import LedFxEntity

import logging
import voluptuous as vol

from LedFxAPI import LedFxApi

from homeassistant.helpers import config_validation as cv, entity_platform, service
from homeassistant import config_entries, core
from homeassistant.components.light import (
    COLOR_MODE_BRIGHTNESS,
    LightEntity,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    # update devices
    if config_entry.options:
        config.update(config_entry.options)

    api = config["api"]
    coo = config["coordinator"]

    # custom services
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SET_EFFECT,
        {
            vol.Required("effect_id"): cv.string,
            vol.Required("preset_id", default="reset"): cv.string,
        },
        "set_effect",
    )

    entities = []
    virtuals = await api.helper.get_all_virtuals()
    for virtual_id in virtuals:
        status = await api.api.virtual_get_config(virtual_id)
        status = status[virtual_id]

        virtual = Virtual(coo, virtual_id, status["config"]["name"])
        entities.append(virtual)

    async_add_entities(entities, update_before_add=True)


class Virtual(LedFxEntity, LightEntity):
    "Represents an ledfx virtual"

    def __init__(self, coo, idx, name) -> None:
        super().__init__(coo)
        self.idx = idx
        self._attr_should_poll = True
        self._attr_name = name
        self._attr_unique_id = idx
        self._attr_color_mode = COLOR_MODE_BRIGHTNESS
        self._attr_supported_color_modes = {COLOR_MODE_BRIGHTNESS}

    async def async_turn_on(self, **kwargs) -> None:
        if not self._attr_is_on:
            await self.coordinator.api.api.virtual_set_state(self.idx, True)
        # {"type":"rain","config":{"brightness":0.44}}
        effect = self.coordinator.data[self.idx]["effect"]

        new_brightness = kwargs.get("brightness")
        if new_brightness:
            payload = {
                "type": effect,
                "config": {"brightness": round(new_brightness / 255, 2)},
            }
            await self.coordinator.api.api.virtual_effect_update(self.idx, payload)

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.api.api.virtual_set_state(self.idx, False)

    @core.callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        data = self.coordinator.data[self.idx]
        brightness_float = data["status"]["effect"]["config"]["brightness"]
        self._attr_brightness = 255 * brightness_float
        self._attr_is_on = data["status"]["active"]
        self.async_write_ha_state()

    # async def async_set_effect(self, entity, service_call):
    # await entity.set_effect(service_call.data["effect_id"], "preset_id")

    async def set_effect(self, effect_id: str, preset_id: str) -> None:
        """Set effect service"""
        await self.coordinator.api.helper.set_preset(self.idx, effect_id, preset_id)
