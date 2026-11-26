-- Replace PROJECT_ID with the verified unbilled GridPulse project.
WITH hourly AS (
  SELECT
    *,
    LAG(hour_ending_utc) OVER (ORDER BY hour_ending_utc) AS previous_hour
  FROM `PROJECT_ID.gridpulse_raw_pilot.eia930_erco_202503`
)
SELECT
  COUNT(*) AS row_count,
  COUNT(DISTINCT hour_ending_utc) AS distinct_utc_hours,
  COUNTIF(TIMESTAMP_DIFF(hour_ending_utc, previous_hour, SECOND) != 3600) AS non_hourly_steps,
  FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', MIN(hour_ending_utc), 'UTC') AS first_utc,
  FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', MAX(hour_ending_utc), 'UTC') AS last_utc,
  MIN(reporting_date) AS first_reporting_date,
  MAX(reporting_date) AS last_reporting_date,
  COUNT(DISTINCT reporting_date) AS reporting_days,
  COUNTIF(reporting_date = DATE '2025-03-09') AS march_9_hours,
  COUNTIF(balancing_authority != 'ERCO') AS unexpected_authority,
  COUNTIF(source_file != 'EIA930_BALANCE_2025_Jan_Jun.csv') AS unexpected_source,
  COUNTIF(demand_mw IS NULL) AS missing_demand,
  COUNTIF(forecast_mw IS NULL) AS missing_forecast,
  COUNTIF(net_generation_mw IS NULL) AS missing_generation
FROM hourly;
