"""Set up TORCH Motion without asking for new Tuya credentials."""

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from . import DOMAIN, torch_devices


class TorchMotionConfigFlow(ConfigFlow, domain=DOMAIN):
    """Add the event platform for compatible cameras on existing Tuya accounts."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Create a single configuration entry if a camera is available."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if next(torch_devices(self.hass), None) is None:
            return self.async_abort(reason="no_cameras")

        return self.async_create_entry(title="TORCH Motion", data={})
