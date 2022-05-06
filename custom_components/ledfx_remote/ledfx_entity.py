"""Base Entity for ledfx"""
from .const import DOMAIN

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class LedFxEntity(CoordinatorEntity):
    """Base entity"""

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information about this WLED device."""
        return DeviceInfo(
            connections=None,
            identifiers={(DOMAIN, "MAC")},
            name="LedFx",
            manufacturer=None,
            model=None,
            sw_version=None,
            hw_version=None,
            configuration_url=None,
        )
