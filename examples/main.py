# examples

import asyncio
from soc_proof import SocProofAPI, DataCache, ServiceNotFound, HTTPRequestError

# Initialize cache
cache = DataCache()

# Your API token, obtained on "https://soc-proof.su/api"
token = "YOUR_API_TOKEN"

api = SocProofAPI(token=token, cache=cache)


async def main():
    # Load all services (cached), default language of details is "en" - English.
    services = await api.load_services()

    # Load all services (uncached)
    services_uncached = await api.load_services(force_reload=True)

    # Load all services with Russian name, description and time (cached)
    services_en = await api.load_services(language="ru")

    # Add an order, returns order_id
    order_id = await api.add_order(
        service=1,
        link="https://example.com",
        quantity=100
    )

    # Get order status, use list to get multiple orders status.
    status_list = await api.get_status(order_id)
    for status in status_list:
        print(f"Order {status.order_id}: {status.status}, Charge: {status.charge}, Remains: {status.remains}")

    # Get single service by ID
    try:
        service_id = services[0].service  # Use first service as example
        service = await api.get_service(service_id, language="en")
        print("Got service:", service)
    except ServiceNotFound:
        print("Service not found")
    except HTTPRequestError as e:
        print("HTTP request failed:", e)


if __name__ == "__main__":
    asyncio.run(main())
