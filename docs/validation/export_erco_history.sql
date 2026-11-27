SELECT
  balancing_authority,
  reporting_date,
  reporting_hour_number,
  FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', hour_ending_utc, 'UTC') AS hour_ending_utc,
  demand_mw,
  forecast_mw,
  net_generation_mw,
  source_file,
  local_start_hour,
  paired_hour,
  forecast_error_mw,
  absolute_error_mw
FROM `PROJECT_ID.gridpulse_models.fct_erco_hourly`
WHERE balancing_authority = 'ERCO'
  AND reporting_date >= DATE '2023-01-01'
  AND reporting_date < DATE '2026-01-01'
ORDER BY hour_ending_utc;
