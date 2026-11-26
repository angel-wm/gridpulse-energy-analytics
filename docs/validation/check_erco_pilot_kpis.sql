SELECT
  COUNT(*) AS hours,
  COUNT(DISTINCT hour_ending_utc) AS distinct_utc_hours,
  COUNTIF(demand_mw IS NOT NULL AND forecast_mw IS NOT NULL) AS paired_hours,
  MAX(demand_mw) AS peak_demand_mw,
  ROUND(AVG(ABS(forecast_mw - demand_mw)), 3) AS mae_mw,
  ROUND(AVG(forecast_mw - demand_mw), 3) AS bias_mw
FROM `PROJECT_ID.gridpulse_raw_pilot.eia930_erco_202503`
WHERE balancing_authority = 'ERCO'
  AND reporting_date >= DATE '2025-03-01'
  AND reporting_date < DATE '2025-04-01';
