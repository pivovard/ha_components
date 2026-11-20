"""Expose IP-310 TORCH motion reports from the existing Tuya integration."""

from __future__ import annotations

from collections.abc import Iterator

from tuya_sharing import CustomerDevice

from homeassistant.components.tuya import TuyaConfigEntry
from homeassistant.components.tuya.const import DOMAIN as TUYA_DOMAIN
from homeassistant.components.tuya.const import DPCode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

DOMAIN = "torch_motion"
TORCH_PRODUCT_ID = "4wxl8xpnjstn4jjy"
MOTION_DP = DPCode.MOVEMENT_DETECT_PIC
PLATFORMS = [Platform.EVENT]


def torch_devices(hass: HomeAssistant) -> Iterator[tuple[TuyaConfigEntry, CustomerDevice]]:
    """Find loaded Tuya cameras that advertise the verified motion data point."""
    seen: set[str] = set()
    for entry in hass.config_entries.async_loaded_entries(TUYA_DOMAIN):
        for device in entry.runtime_data.manager.device_map.values():
            if (
                device.product_id == TORCH_PRODUCT_ID
                and MOTION_DP in device.status_range
                and device.id not in seen
            ):
                seen.add(device.id)
                yield entry, device


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the event platform once the Tuya cameras are available."""
    if next(torch_devices(hass), None) is None:
        raise ConfigEntryNotReady("No compatible TORCH cameras are available in Tuya")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the event platform and its subscriptions."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
