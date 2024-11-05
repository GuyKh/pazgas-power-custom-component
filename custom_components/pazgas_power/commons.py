"""Common methods for PazGas Power."""

from datetime import date

from pazgas_power import Invoice


def translate_date_to_date_period(date_period: date) -> str:
    """Format date to standard (comparable) date."""
    return date_period.strftime("%Y-%m")


def get_invoice_month(invoice: Invoice) -> str:
    """Get invoice Month string."""
    return f"{invoice.invoice_year}-{invoice.invoice_month:02d}"
