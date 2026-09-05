import os
from dataclasses import dataclass, field


def _split_env_list(name: str, default: list[str]) -> list[str]:
    raw = os.environ.get(name)
    if not raw:
        return default
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


@dataclass
class Settings:
    cors_allowed_origins: list[str] = field(default_factory=lambda: _split_env_list(
        "CORS_ALLOWED_ORIGINS",
        ["http://127.0.0.1:5005", "http://localhost:5005"],
    ))
    nominatim_base_url: str = os.environ.get("NOMINATIM_BASE_URL", "https://nominatim.openstreetmap.org")
    overpass_base_url: str = os.environ.get("OVERPASS_BASE_URL", "https://overpass-api.de/api/interpreter")
    nominatim_user_agent: str = os.environ.get(
        "NOMINATIM_USER_AGENT", "SahayataAtlas/1.0 (contact: ops@example.org)"
    )
    # Nominatim's public server blanket-blocks many datacenter/cloud IP ranges
    # (Render, Heroku, AWS, etc.) regardless of a correct User-Agent. When
    # LOCATIONIQ_API_KEY is set, location.py uses LocationIQ's hosted
    # geocoder (same OSM data, built for server-to-server traffic) instead.
    # Leave it unset for local development, where the IP block doesn't apply.
    locationiq_api_key: str = os.environ.get("LOCATIONIQ_API_KEY", "")
    locationiq_base_url: str = os.environ.get("LOCATIONIQ_BASE_URL", "https://us1.locationiq.com/v1")
    request_timeout_seconds: float = float(os.environ.get("UPSTREAM_TIMEOUT_SECONDS", "12"))
    hard_deadline_seconds: float = float(os.environ.get("HARD_DEADLINE_SECONDS", "15"))
    rate_limit_per_minute: int = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "60"))
    max_resources: int = 200


settings = Settings()
