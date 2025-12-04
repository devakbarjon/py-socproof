import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict

from .cache import DataCache

from .models import Service, OrderStatus, AccountBalance

from .helper import parse_service

from .errors import (
    HTTPRequestError,
    InvalidResponseError,
    ServiceNotFound,
    OrderNotFound,
    OrderStatusError,
)


class SocProofAPI:
    BASE_URL = "https://soc-proof.su/api/v2"
    SERVICES_PAGE_URL = "https://soc-proof.su/services"
    ENG_SERVICES_PAGE_URL = "https://soc-proof.su/en/services"

    def __init__(self, token: str):
        self.token = token
        self.cache = DataCache()
        self.descriptions: Dict[int, dict] = {}

    # Internal HTTP methods

    async def _post(self, data: dict) -> dict:
        """POST request to the API."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.BASE_URL, data=data) as resp:
                    if resp.status != 200:
                        raise HTTPRequestError(resp.status, await resp.text())
                    return await resp.json()
            except Exception as e:
                raise HTTPRequestError(-1, str(e))

    async def _get(self, url: str) -> str:
        """GET request (used for scraping service descriptions)."""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        raise HTTPRequestError(resp.status, await resp.text())
                    return await resp.text()
            except Exception as e:
                raise HTTPRequestError(-1, str(e))

    # Service descriptions

    async def load_descriptions(self, language: str = "en", force_reload: bool = False) -> Dict[int, dict]:
        """
        Load service descriptions (and optionally English names/categories).
        language: "ru" or "en"
        """
        cache_key = f"descriptions_{language}"
        cached = self.cache.get(cache_key)
        if cached and not force_reload:
            return cached

        url = self.SERVICES_PAGE_URL if language == "ru" else self.ENG_SERVICES_PAGE_URL
        html = await self._get(url)
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", id="service-table")
        if not table:
            raise InvalidResponseError(f"Unable to find service table for language: {language}")

        descriptions: Dict[int, dict] = {}
        for tr in table.find("tbody").find_all("tr"):
            if not tr.get("data-filter-table-category-id"):
                continue
            tds = tr.find_all("td")
            if len(tds) != 7:
                continue
            service_id = int(tds[0].text.strip())
            descriptions[service_id] = {
                "description": tds[6].text.strip(),
                "time": tds[5].text.strip(),
                "name": tds[1].text.strip(),
                "category": tds[0].get("data-category-name") or tds[0].text.strip()
            }

        self.cache.set(cache_key, descriptions, timeout=60 * 60 * 24)
        return descriptions

    # Services
    async def load_services(self, language: str = "en", force_reload: bool = False) -> List[Service]:
        """
        Load services with descriptions in selected language.
        Language: "ru" or "en".
        Default: "en".
        """
        cache_key = f"services_{language}"
        cached = self.cache.get(cache_key)
        if cached and not force_reload:
            return cached

        descriptions = await self.load_descriptions(language=language, force_reload=force_reload)

        response = await self._post({"key": self.token, "action": "services"})
        if not isinstance(response, list):
            raise InvalidResponseError("Expected a list of services from API")

        services: List[Service] = []
        allowed_fields = {"service", "name", "type", "rate", "min", "max", "refill", "cancel", "category"}

        for s in response:
            sid = s.get("service")
            desc = descriptions.get(sid, {"description": "", "time": "", "name": "", "category": ""})

            filtered = {k: s[k] for k in allowed_fields if k in s}
            # Overwrite name, description, time with language-specific values

            filtered.update({
                "name": desc["name"],
                "description": desc["description"],
                "time": desc["time"]
            })

            services.append(parse_service(filtered))

        self.cache.set(cache_key, services, timeout=5 * 60)  # 5 min cache for dynamic data
        return services

    async def get_service(self, service_id: int, language: str = "en") -> Service:
        """Return a single service by ID in chosen language."""
        services = await self.load_services(language=language)
        for s in services:
            if s.service == service_id:
                return s
        raise ServiceNotFound(service_id)

    # Orders

    async def add_order(self, service: int, link: str, quantity: int) -> str:
        """Create a new order."""
        response = await self._post({
            "key": self.token,
            "action": "add",
            "service": service,
            "link": link,
            "quantity": quantity,
        })

        order_id = response.get("order")
        if not order_id:
            raise OrderNotFound(-1)
        return str(order_id)

    async def get_status(self, orders: list | str) -> List[OrderStatus]:
        """Get status of one or multiple orders."""
        if isinstance(orders, list):
            orders = ",".join(map(str, orders))

        response = await self._post({
            "key": self.token,
            "action": "status",
            "orders": orders,
        })

        result: List[OrderStatus] = []
        for order_id, data in response.items():
            missing = [k for k in ("charge", "status", "remains") if k not in data]
            if missing:
                raise OrderStatusError(order_id, missing)

            result.append(OrderStatus(
                order_id=order_id,
                charge=float(data["charge"]),
                status=data["status"],
                remains=int(data["remains"]),
            ))

        return result

    async def get_balance(self) -> AccountBalance:
        """Get account balance."""
        response = await self._post({
            "key": self.token,
            "action": "balance",
        })

        return AccountBalance(
            balance=float(response["balance"]),
            currency=response.get("currency", "")
        )