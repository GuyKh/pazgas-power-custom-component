"""Custom types for PazGas Power."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from pazgas_power import PazGasPowerApi

    from .coordinator import PazGasPowerDataUpdateCoordinator


type PazGasPowerConfigEntry = ConfigEntry[PazGasPowerData]


@dataclass
class PazGasPowerDeviceInfo:
    """Class describing PazGas Power device info."""

    is_smart_meter: bool
    customer_id: str


@dataclass
class PazGasPowerData:
    """Data for the PazGas Power integration."""

    client: PazGasPowerApi
    coordinator: PazGasPowerDataUpdateCoordinator
    integration: Integration
    device_info: PazGasPowerDeviceInfo
