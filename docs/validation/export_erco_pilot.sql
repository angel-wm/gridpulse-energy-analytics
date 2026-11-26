SELECT
  balancing_authority,
  reporting_date,
  reporting_hour_number,
  FORMAT_TIMESTAMP('%Y-%m-%dT%H:%M:%SZ', hour_ending_utc, 'UTC') AS hour_ending_utc,
  demand_mw,
  forecast_mw,
  net_generation_mw,
  source_file,
  forecast_mw - demand_mw AS forecast_error_mw,
  ABS(forecast_mw - demand_mw) AS absolute_forecast_error_mw
FROM `PROJECT_ID.gridpulse_models_pilot.stg_eia930__erco_202503`
WHERE balancing_authority = 'ERCO'
  AND reporting_date >= DATE '2025-03-01'
  AND reporting_date < DATE '2025-04-01'
ORDER BY hour_ending_utc;
