"""DataUpdateCoordinator for PazGas Power."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import TYPE_CHECKING, Any

import homeassistant.util.dt as dt_util
from dateutil.relativedelta import relativedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from pazgas_power import (
    CustomerData,
    PazGasPowerApi,
    PazGasPowerError,
)

from .commons import get_invoice_month, translate_date_to_date_period
from .const import (
    ACTIVATION_DATE_KEY,
    DOMAIN,
    IS_SMART_METER_KEY,
    LAST_MONTH_INVOICE_KEY,
    LOGGER,
    MY_PACKAGE_KEY,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import PazGasPowerConfigEntry

timezone = dt_util.get_time_zone("Asia/Jerusalem")
_LOGGER = logging.getLogger(__name__)


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class PazGasPowerDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: PazGasPowerConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=1),
        )

    async def _get_data(self):  # noqa: ANN202
        api: PazGasPowerApi = self.config_entry.runtime_data.client
        # is_smart_meter = self.config_entry.runtime_data.device_info.is_smart_meter

        _LOGGER.debug("Logging in to www.pazgas.co.il/hashmal...")
        pazgas_data: CustomerData = await api.login_and_get_customer_data()

        invoices_by_month = {
            get_invoice_month(invoice): invoice for invoice in pazgas_data.invoices
        }

        today = dt_util.now(timezone).date()

        data = {}
        last_month: date = today + relativedelta(months=-1)

        # this_month_invoice = invoices_by_month.get(\
        #         translate_date_to_date_period(today.date()))
        last_month_invoice = invoices_by_month.get(
            translate_date_to_date_period(last_month.date())
        )

        data[MY_PACKAGE_KEY] = pazgas_data.package
        data[ACTIVATION_DATE_KEY] = pazgas_data.activation_date
        data[LAST_MONTH_INVOICE_KEY] = last_month_invoice
        data[IS_SMART_METER_KEY] = (
            self.config_entry.runtime_data.device_info.is_smart_meter
        )

        return data

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self._get_data()
        except PazGasPowerError as exception:
            raise UpdateFailed(exception) from exception
