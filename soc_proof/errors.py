class PartnerAPIError(Exception):
    """Base exception for all PartnerAPI-related errors."""
    pass


# ---------------------------
# HTTP + Request
# ---------------------------

class HTTPRequestError(PartnerAPIError):
    """Raised when the HTTP request fails or returns a non-200 status."""
    def __init__(self, status: int, message: str = ""):
        super().__init__(f"HTTP {status}: {message}")
        self.status = status


class InvalidResponseError(PartnerAPIError):
    """Raised when API returns invalid JSON or unexpected format."""
    def __init__(self, message: str = "Invalid or malformed API response"):
        super().__init__(message)


# ---------------------------
# Service / Description Errors
# ---------------------------

class ServiceNotFound(PartnerAPIError):
    """Raised when a service with specified ID does not exist."""
    def __init__(self, service_id: int):
        super().__init__(f"Service ID {service_id} not found")


class DescriptionNotFound(PartnerAPIError):
    """Raised when a service description is missing."""
    def __init__(self, service_id: int):
        super().__init__(f"Description for service ID {service_id} not found")


# ---------------------------
# Order Errors
# ---------------------------

class OrderNotFound(PartnerAPIError):
    """Raised when order details are missing or invalid."""
    def __init__(self, order_id: int):
        super().__init__(f"Order {order_id} not found or returned invalid data")


class OrderStatusError(PartnerAPIError):
    """Raised when an order status response is missing required fields."""
    def __init__(self, order_id: int, missing_fields: list):
        fields = ", ".join(missing_fields)
        super().__init__(f"Order {order_id} missing fields: {fields}")