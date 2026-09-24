CREATE VIEW IF NOT EXISTS vw_listing_lifecycle AS
WITH lifecycle AS (
    SELECT
        advert_id,
        MIN(snapshot_date) AS first_seen_at,
        MAX(snapshot_date) AS last_seen_at,
        COUNT(*) AS snapshots_count,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        currency
    FROM listings_snapshots
    GROUP BY advert_id
)
SELECT
    l.advert_id,
    l.first_seen_at,
    l.last_seen_at,
    CAST(
        julianday(l.last_seen_at) - julianday(l.first_seen_at)
        AS INTEGER
    ) AS days_on_market,
    l.snapshots_count,
    l.min_price,
    l.max_price,
    first_snapshot.price AS initial_price,
    last_snapshot.price AS current_price,
    last_snapshot.price - first_snapshot.price AS price_change,
    l.currency,
    ROUND(
        (last_snapshot.price - first_snapshot.price) * 100.0
        / first_snapshot.price,
        2
    ) AS price_change_pct
FROM lifecycle l
JOIN listings_snapshots first_snapshot
    ON first_snapshot.advert_id = l.advert_id
    AND first_snapshot.snapshot_date = l.first_seen_at
JOIN listings_snapshots last_snapshot
    ON last_snapshot.advert_id = l.advert_id
    AND last_snapshot.snapshot_date = l.last_seen_at;


CREATE VIEW IF NOT EXISTS vw_active_listings AS
SELECT
    s.advert_id,
    s.title,
    s.price,
    s.currency,
    s.snapshot_date,
    s.scraped_at,
    s.url,

    d.make,
    d.model,
    d.version,
    d.generation,
    d.year,
    d.mileage,
    d.engine_size_cm3,
    d.engine_power_hp,
    d.body_type,
    d.gearbox,
    d.fuel_type,
    d.drive_type,
    d.province,
    d.city,
    d.no_accident,
    d.damaged,
    d.seller_type,
    d.dealer_type,
    d.first_seen_at

FROM listings_snapshots AS s
LEFT JOIN listings_details AS d
    ON s.advert_id = d.advert_id

WHERE s.snapshot_date = (
    SELECT MAX(snapshot_date)
    FROM listings_snapshots
);