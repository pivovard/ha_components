"""Report camera motion without exposing or fetching the associated image."""

from __future__ import annotations

import logging

from tuya_sharing import CustomerDevice

from homeassistant.components.event import EventEntity
from homeassistant.components.tuya import TuyaConfigEntry
from homeassistant.components.tuya.const import DOMAIN as TUYA_DOMAIN
from homeassistant.components.tuya.const import TUYA_HA_SIGNAL_UPDATE_ENTITY
from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import MOTION_DP, torch_devices

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add one motion event entity to each supported Tuya camera."""
    async_add_entities(
        TorchMotionEvent(tuya_entry, device)
        for tuya_entry, device in torch_devices(hass)
    )


class TorchMotionEvent(EventEntity):
    """Publish a motion event when Tuya reports a new motion data point."""

    _attr_has_entity_name = True
    _attr_translation_key = "motion"
    _attr_event_types = ["motion"]

    def __init__(self, tuya_entry: TuyaConfigEntry, device: CustomerDevice) -> None:
        self._tuya_entry = tuya_entry
        self._device_id = device.id
        self._attr_unique_id = f"{device.id}_motion"
        self._attr_device_info = DeviceInfo(identifiers={(TUYA_DOMAIN, device.id)})

    @property
    def _device(self) -> CustomerDevice | None:
        if self._tuya_entry.state != ConfigEntryState.LOADED:
            return None
        return self._tuya_entry.runtime_data.manager.device_map.get(self._device_id)

    @property
    def available(self) -> bool:
        """Reflect availability in the existing Tuya integration."""
        device = self._device
        return device is not None and device.online

    async def async_added_to_hass(self) -> None:
        """Subscribe to live updates and changes to the Tuya entry's availability."""
        await super().async_added_to_hass()
        self.async_on_remove(
            self._tuya_entry.async_on_state_change(self.async_write_ha_state)
        )
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"{TUYA_HA_SIGNAL_UPDATE_ENTITY}_{self._device_id}",
                self._async_update_device,
            )
        )

    @callback
    def _async_update_device(self, updated_properties: list[str] | None) -> None:
        """Ignore cached values and unrelated updates such as motion alarm settings."""
        if updated_properties:
            _LOGGER.debug(
                "%s received Tuya properties: %s", self.entity_id, updated_properties
            )

        device = self._device
        if (
            device is not None
            and device.online
            and updated_properties is not None
            and MOTION_DP in updated_properties
            and device.status.get(MOTION_DP)
        ):
            self._trigger_event("motion")

        self.async_write_ha_state()
