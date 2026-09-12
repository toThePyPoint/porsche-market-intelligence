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

    engine_size_cm3: int | None
    engine_power_hp: int | None

    # year: int | None
    # mileage: int | None
    #
