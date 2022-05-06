"""LedFx Selector Entities"""
from .ledfx_entity import LedFxEntity
from .const import DOMAIN

import logging

from LedFxAPI import LedFxApi

from homeassistant import config_entries, core
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import EntityCategory

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

    entities = []
    virtuals = await api.helper.get_all_virtuals()
    for virtual_id in virtuals:
        status = await api.api.virtual_get_config(virtual_id)
        status = status[virtual_id]

        entities.append(Effects(coo, virtual_id))
        entities.append(Presets(coo, virtual_id))

    async_add_entities(entities, update_before_add=True)


class Presets(LedFxEntity, SelectEntity):
    """preset selector"""

    _attr_icon = "mdi:playlist-play"

    def __init__(self, coo, v_idx: str) -> None:
        super().__init__(coo)
        self.virt_idx = v_idx
        self._attr_options = []
        self._attr_current_option = None
        self._attr_name = f"{v_idx} Preset"
        self._attr_unique_id = f"{v_idx}.preset"
        self.effect_id = None

    @core.callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data
        self.effect_id = data[self.virt_idx]["effect"]
        self._attr_options = data[self.virt_idx]["presets"]
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        if self.effect_id:
            await self.coordinator.api.helper.set_preset(
                self.virt_idx, self.effect_id, option
            )
            await self.coordinator.async_request_refresh()


class Effects(LedFxEntity, SelectEntity):
    """effect selector"""

    _attr_icon = "mdi:playlist-play"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, coo, virtual_id: str) -> None:
        super().__init__(coo)
        self.virt_idx = virtual_id
        self._attr_options = []
        self._attr_current_option = None
        self._attr_name = f"{virtual_id} Effect"
        self._attr_unique_id = f"{virtual_id}.effect"

    @core.callback
    def _handle_coordinator_update(self) -> None:
        data = self.coordinator.data
        self._attr_current_option = data[self.virt_idx]["effect"]
        self._attr_options = data["effects"]
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        await self.coordinator.api.helper.set_preset(self.virt_idx, option, "reset")
        await self.coordinator.async_request_refresh()
