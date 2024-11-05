"""
Custom integration to integrate PazGas Power with Home Assistant.

For more details about this integration, please refer to
https://github.com/GuyKh/pazgas-power-custom-component
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from pazgas_power import (
    PazGasPowerApi,
)

from .const import (
    CONF_CUSTOMER_ID,
    CONF_IS_SMART_METER,
    CONF_PHONE,
    CONF_USER_ID,
    DOMAIN,
    LOGGER,
)
from .coordinator import PazGasPowerDataUpdateCoordinator
from .data import PazGasPowerData, PazGasPowerDeviceInfo

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import PazGasPowerConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: PazGasPowerConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = PazGasPowerDataUpdateCoordinator(
        hass=hass,
    )
    entry.runtime_data = PazGasPowerData(
        client=PazGasPowerApi(
            user_id=entry.data[CONF_USER_ID],
            phone=entry.data[CONF_PHONE],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
        device_info=PazGasPowerDeviceInfo(
            is_smart_meter=entry.data.get(CONF_IS_SMART_METER, False),
            customer_id=entry.data.get[CONF_CUSTOMER_ID],
        ),
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    # Register the debug service
    async def handle_debug_get_coordinator_data(call) -> None:  # noqa: ANN001 ARG001
        # Log or return coordinator data
        data = coordinator.data
        LOGGER.info("Coordinator data: %s", data)
        hass.bus.async_fire("custom_component_debug_event", {"data": data})

    hass.services.async_register(
        DOMAIN, "debug_get_coordinator_data", handle_debug_get_coordinator_data
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: PazGasPowerConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: PazGasPowerConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
