"""LedFx Update Coordinator"""
from datetime import timedelta
import logging

from LedFxAPI import LedFxApi

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)

_LOGGER = logging.getLogger(__name__)


class EffectCoordinator(DataUpdateCoordinator):
    """Custom update coordinator"""

    def __init__(self, hass, api: LedFxApi):
        super().__init__(
            hass,
            _LOGGER,
            name="LedFx",
            update_interval=timedelta(seconds=15),
        )
        self.api = api

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        data = {}
        effects = await self.api.helper.get_all_effect_ids()
        virtuals = await self.api.helper.get_all_virtuals()
        for idx in virtuals:
            status = await self.api.api.virtual_get_config(idx)
            status = status[idx]
            effect_idx = status["effect"]["type"]
            presets = await self.api.helper.get_all_presets_for_effect(effect_idx)
            data["effects"] = effects
            data[idx] = {"effect": effect_idx, "presets": presets, "status": status}

        return data
