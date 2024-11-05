"""Constants for PazGas Power."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "pazgas_power"
ATTRIBUTION = "Data provided by http://www.pazgas.co.il/hashmal"

CONF_USER_ID = "user_id"
CONF_PHONE = "phone"
CONF_CUSTOMER_ID = "customer_id"
CONF_IS_SMART_METER = "is_smart_meter"
ACTIVATION_DATE_KEY = "activation_date"
LAST_MONTH_INVOICE_KEY = "last_month_invoice"
PAYER_DETAILS_KEY = "payer_details"
MY_PACKAGE_KEY = "my_package"
IS_SMART_METER_KEY = "is_smart_meter"
UNIT_ILS = "₪"
