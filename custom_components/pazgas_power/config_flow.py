"""Adds config flow for PazGas Power."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from pazgas_power import (
    CustomerData,
    PazGasPowerApi,
    PazGasPowerError,
)

from .const import (
    CONF_CUSTOMER_ID,
    CONF_IS_SMART_METER,
    CONF_PHONE,
    CONF_USER_ID,
    DOMAIN,
    LOGGER,
)


class PazGasPowerFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for PazGas."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                customer_data = await self._test_credentials(
                    user_id=user_input[CONF_USER_ID],
                    phone=user_input[CONF_PHONE],
                )
            except PazGasPowerError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                user_input[CONF_CUSTOMER_ID] = customer_data.customer_id
                user_input[
                    CONF_IS_SMART_METER
                ] = not customer_data.need_to_order_smart_meter

                return self.async_create_entry(
                    title=f"PazGas Energy - {customer_data.customer_id}",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_USER_ID,
                        default=(user_input or {}).get(CONF_USER_ID, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(CONF_PHONE): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, user_id: str, phone: str) -> CustomerData:
        """Validate credentials."""
        api = PazGasPowerApi(
            user_id=user_id, phone=phone, session=async_create_clientsession(self.hass)
        )

        return await api.login_and_get_customer_data()
