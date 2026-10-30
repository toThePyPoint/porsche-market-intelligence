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
        (last_snapshot.price - first_snapshot.price)
        / first_snapshot.price,
        2
    ) AS price_change
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


CREATE VIEW IF NOT EXISTS vw_monthly_listing_prices AS
WITH ranked_snapshots AS (
    SELECT
        advert_id,
        DATE(snapshot_date, 'start of month') AS month,
        scraped_at,
        price,
        currency,
        ROW_NUMBER() OVER (
            PARTITION BY advert_id, DATE(snapshot_date, 'start of month')
            ORDER BY scraped_at DESC
        ) AS rn
    FROM listings_snapshots
)
SELECT
    s.advert_id,
    s.month,
    DATE(s.scraped_at) AS last_observed_at,
    s.price,
    s.currency,
    d.generation,
    d.damaged
FROM ranked_snapshots AS s
LEFT JOIN listings_details AS d
    ON s.advert_id = d.advert_id
WHERE s.rn = 1;


CREATE VIEW IF NOT EXISTS vw_listing_price_changes AS
WITH price_history AS (
    SELECT
        advert_id,
        snapshot_date,
        price,
        currency,

        FIRST_VALUE(price) OVER (
            PARTITION BY advert_id
            ORDER BY snapshot_date
        ) AS initial_price,

        FIRST_VALUE(currency) OVER (
            PARTITION BY advert_id
            ORDER BY snapshot_date
        ) AS initial_currency

    FROM listings_snapshots
)
SELECT
    advert_id,
    snapshot_date,
    initial_price,
    price AS current_price,
    currency,

    CASE
        WHEN currency != initial_currency THEN 'Currency changed'
        WHEN price < initial_price THEN 'Decreased'
        WHEN price > initial_price THEN 'Increased'
        WHEN price = initial_price THEN 'No change'
    END AS price_change_type

FROM price_history;