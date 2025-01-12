"""Sensor platform for PazGas Power."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)

from .commons import get_invoice_month
from .const import (
    LAST_MONTH_INVOICE_KEY,
    MY_PACKAGE_KEY,
    UNIT_ILS,
)
from .entity import PazGasPowerEntity, PazGasPowerEntityDescriptionMixin

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from pazgas_power import Package

    from .coordinator import PazGasPowerDataUpdateCoordinator
    from .data import PazGasPowerConfigEntry, PazGasPowerEnergyDeviceInfo


@dataclass(frozen=True, kw_only=True)
class PazGasPowerSensorEntityDescription(
    SensorEntityDescription, PazGasPowerEntityDescriptionMixin
):
    """Class describing PazGas Power Energy sensors entities."""


def _generate_discount_text(package: Package) -> str:
    txt = ""
    txt += f"{package.discount_text}" if package.discount_text else ""
    txt += f" {package.discount_value}" if package.discount_value else ""
    txt += f"{package.currency}" if package.currency else ""
    return txt


ENTITY_DESCRIPTIONS = [
    PazGasPowerSensorEntityDescription(
        key="last_month_cost",
        device_class=SensorDeviceClass.MONETARY,
        native_unit_of_measurement=UNIT_ILS,
        suggested_display_precision=3,
        value_fn=lambda data: data[LAST_MONTH_INVOICE_KEY].invoice_total_price
        if data[LAST_MONTH_INVOICE_KEY]
        else None,
        custom_attrs_fn=lambda data: {
            "month": get_invoice_month(data[LAST_MONTH_INVOICE_KEY])
            if data[LAST_MONTH_INVOICE_KEY]
            else None,
            "invoice_number": data[LAST_MONTH_INVOICE_KEY].invoice_number
            if data[LAST_MONTH_INVOICE_KEY]
            else None,
        },
    ),
    PazGasPowerSensorEntityDescription(
        key="package",
        value_fn=lambda data: data[MY_PACKAGE_KEY].name
        if data[MY_PACKAGE_KEY]
        else None,
        custom_attrs_fn=lambda data: {
            "description": data[MY_PACKAGE_KEY].description
            if data[MY_PACKAGE_KEY]
            else None,
            "discount": _generate_discount_text(data[MY_PACKAGE_KEY])
            if data[MY_PACKAGE_KEY]
            else None,
        },
    ),
]

SMART_METER_ENTITY_DESCRIPTIONS = []


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 function argument: `hass`
    entry: PazGasPowerConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    entity_descriptions = ENTITY_DESCRIPTIONS
    if entry.runtime_data.device_info.is_smart_meter:
        entity_descriptions += SMART_METER_ENTITY_DESCRIPTIONS

    async_add_entities(
        PazGasPowerSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
            device_info=entry.runtime_data.device_info,
        )
        for entity_description in entity_descriptions
    )


class PazGasPowerSensor(PazGasPowerEntity, SensorEntity):
    """PazGas Power Sensor class."""

    def __init__(
        self,
        coordinator: PazGasPowerDataUpdateCoordinator,
        entity_description: PazGasPowerSensorEntityDescription,
        device_info: PazGasPowerEnergyDeviceInfo,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, device_info)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_translation_key = entity_description.key

        attributes = {}
        if self.entity_description.custom_attrs_fn:
            custom_attr = self.entity_description.custom_attrs_fn(self.coordinator.data)
            if custom_attr:
                attributes.update(custom_attr)

        self._attr_extra_state_attributes = attributes

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        if self.coordinator.data:
            return self.entity_description.value_fn(self.coordinator.data)
        return None
