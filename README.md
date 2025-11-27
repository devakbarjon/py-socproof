# Soc-proof

Async Python client for the Partner API (https://soc-proof.su).  
Easily interact with services, orders, and statuses.

---

## Installation

```bash
pip install soc-proof
```

## Examples

You can find example scripts demonstrating how to use `soc-proof` in the [`examples`](examples/) folder.

## Language Support for Services
```
The API client supports fetching service details in multiple languages.

language="en" — English (default)

language="ru" — Russian 
```

## Features

*  Async requests with aiohttp

* Simple in-memory caching with TTL

* Fetch all services, get service by ID

* Create orders and check their status

* Automatically merges service descriptions

* Easy to use and extend

## Models

**Service**: Represents a service with all fields from the API (name, category, rate, min, max, dripfeed, refill, cancel, description, time, admin_cost)

**OrderStatus**: Represents an order’s current status, charge, and remaining quantity.

# Cache

* AsyncCache stores services and descriptions in memory with optional TTL.

* You can force reload services if API data changes:

```python
services = await api.load_services(force_reload=True)
```

## Error Handling

```python
from py_partner_api import PartnerAPIAsync, HTTPRequestError, InvalidResponseError, APIError

try:
    services = await api.load_services()
except HTTPRequestError as e:
    print(f"HTTP error: {e}")
except APIError as e:
    print(f"API returned error: {e}")
except InvalidResponseError as e:
    print(f"Invalid response: {e}")
```