import datetime
from dataclasses import dataclass


@dataclass
class SearchAdvertData:
    advert_id: str

    title: str
    short_description: str | None

    price: int | None
    currency: str | None

    scraped_at: datetime.datetime | None
    url: str


@dataclass
class AdvertProcessingData:
    """Advert details from light crawl"""
    advert_id: str

    province: str | None
    city: str | None


@dataclass
class AdvertDetails:
    advert_id: str

    # Add units
    engine_size_cm3: str | None
    engine_power_hp: str | None

    year: int | None
    mileage: str | None
    mileage_unit: str | None

    province: str | None
    city: str | None

    body_type: str | None
    gearbox: str | None
    fuel_type: str | None

    make: str | None
    model: str | None
    version: str | None
    generation: str | None
    drive_type: str | None