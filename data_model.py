from dataclasses import dataclass


@dataclass
class SearchAdvertData:
    advert_id: str
    url: str

    title: str
    description: str | None

    price: int | None
    currency: str | None

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
