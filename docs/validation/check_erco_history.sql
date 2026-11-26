WITH hourly AS (
  SELECT
    *,
    LAG(hour_ending_utc) OVER (ORDER BY hour_ending_utc) AS previous_hour
  FROM `PROJECT_ID.gridpulse_models.fct_erco_hourly`
)
SELECT
  COUNT(*) AS hours,
  COUNT(DISTINCT hour_ending_utc) AS utc_keys,
  COUNT(DISTINCT reporting_date) AS reporting_dates,
  COUNT(DISTINCT source_file) AS source_files,
  COUNTIF(TIMESTAMP_DIFF(hour_ending_utc, previous_hour, SECOND) != 3600) AS utc_gaps,
  FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', MIN(hour_ending_utc), 'UTC') AS first_utc,
  FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', MAX(hour_ending_utc), 'UTC') AS last_utc,
  SUM(paired_hour) AS paired_hours,
  COUNTIF(demand_mw IS NULL AND forecast_mw IS NOT NULL) AS missing_demand_only,
  COUNTIF(demand_mw IS NOT NULL AND forecast_mw IS NULL) AS missing_forecast_only,
  COUNTIF(demand_mw IS NULL AND forecast_mw IS NULL) AS missing_both,
  COUNTIF(net_generation_mw IS NULL) AS missing_generation,
  COUNTIF(paired_hour = 0 AND (forecast_error_mw IS NOT NULL OR absolute_error_mw IS NOT NULL)) AS invalid_null_errors,
  MAX(demand_mw) AS peak_demand_mw,
  ROUND(SAFE_DIVIDE(SUM(CAST(absolute_error_mw AS NUMERIC)), SUM(paired_hour)), 6) AS mae_mw,
  ROUND(SAFE_DIVIDE(SUM(CAST(forecast_error_mw AS NUMERIC)), SUM(paired_hour)), 6) AS bias_mw,
  SAFE_DIVIDE(
    SUM(IF(paired_hour = 0, CAST(absolute_error_mw AS NUMERIC), NULL)),
    SUM(IF(paired_hour = 0, paired_hour, 0))
  ) AS unpaired_mae,
  SAFE_DIVIDE(
    SUM(IF(paired_hour = 0, CAST(forecast_error_mw AS NUMERIC), NULL)),
    SUM(IF(paired_hour = 0, paired_hour, 0))
  ) AS unpaired_bias
FROM hourly;
