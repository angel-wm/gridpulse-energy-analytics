SELECT
  COUNT(*) AS hours,
  COUNTIF(demand_mw IS NOT NULL AND forecast_mw IS NOT NULL) AS paired_hours,
  MAX(demand_mw) AS peak_demand_mw,
  ROUND(AVG(CAST(ABS(forecast_mw - demand_mw) AS NUMERIC)), 6) AS mae_mw,
  ROUND(AVG(CAST(forecast_mw - demand_mw AS NUMERIC)), 6) AS bias_mw
FROM `RELATION_ID`
WHERE DATE_FILTER;
