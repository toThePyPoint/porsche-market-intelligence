CREATE VIEW IF NOT EXISTS vw_listing_lifecycle AS
WITH lifecycle AS (
    SELECT
        advert_id,
        MIN(snapshot_date) AS first_seen_at,
        MAX(snapshot_date) AS last_seen_at,
        COUNT(*) AS snapshots_count,
        MIN(price) AS min_price,
        MAX(price) AS max_price
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