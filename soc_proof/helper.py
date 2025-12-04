from .models import Service


def to_bool(value) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes")


def parse_service(raw: dict) -> Service:
    return Service(
        service=int(raw["service"]),
        name=str(raw["name"]).strip(),
        type=str(raw["type"]).strip(),
        rate=float(raw["rate"]),
        min=int(raw["min"]),
        max=int(raw["max"]),
        refill=to_bool(raw.get("refill", False)),
        cancel=to_bool(raw.get("cancel", False)),
        category=str(raw.get("category", "")).strip(),
        description=str(raw.get("description", "")).strip(),
        time=str(raw.get("time", "")).strip(),
    )
