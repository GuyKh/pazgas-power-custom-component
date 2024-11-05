"""PazGasPoweryEntity class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import PazGasPowerDataUpdateCoordinator

if TYPE_CHECKING:
    from collections.abc import Callable

    from .data import PazGasPowerDeviceInfo


@dataclass(frozen=True, kw_only=True)
class PazGasPowerEntityDescriptionMixin:
    """Mixin values for required keys."""

    value_fn: Callable[dict, str | float] | None = None
    custom_attrs_fn: Callable[dict, dict[str, str | int | float]] | None = None


class PazGasPowerEntity(CoordinatorEntity[PazGasPowerDataUpdateCoordinator]):
    """PazGasPowerEntity class."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PazGasPowerDataUpdateCoordinator,
        device_info: PazGasPowerDeviceInfo,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    coordinator.config_entry.entry_id,
                ),
            },
            name=f"PazGas Power {device_info.customer_id}",
            manufacturer="PazGas",
        )
