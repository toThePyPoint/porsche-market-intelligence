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
    engine_size_cm3: int | None
    engine_power_hp: int | None

    year: int | None
    mileage: int | None
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
    color: str | None

    no_accident: bool | None
    country_origin: str | None
    service_record: bool | None
    new_used: str | None
    registered_pl: bool | None

    damaged: bool | None
    historical_vehicle: bool | None
    has_registration: bool | None
    registration_number: str | None
    tuning: bool | None
    original_owner: bool | None
    long_description: str | None
    seller_type: str | None
    dealer_type: str | None

    first_seen_at: datetime.date | None
