{{ config(enabled=target.name == 'history') }}

with raw as (
    select * from {{ source('eia930_history', 'erco_hourly') }}
),
fact as (
    select * from {{ ref('fct_erco_hourly') }}
)
select coalesce(raw.hour_ending_utc, fact.hour_ending_utc) as hour_ending_utc
from raw
full outer join fact using (balancing_authority, hour_ending_utc)
where raw.hour_ending_utc is null
   or fact.hour_ending_utc is null
   or raw.reporting_date is distinct from fact.reporting_date
   or raw.reporting_hour_number is distinct from fact.reporting_hour_number
   or raw.demand_mw is distinct from fact.demand_mw
   or raw.forecast_mw is distinct from fact.forecast_mw
   or raw.net_generation_mw is distinct from fact.net_generation_mw
   or raw.source_file is distinct from fact.source_file
   or fact.paired_hour is distinct from if(raw.demand_mw is null or raw.forecast_mw is null, 0, 1)
   or fact.forecast_error_mw is distinct from (raw.forecast_mw - raw.demand_mw)
   or fact.absolute_error_mw is distinct from abs(raw.forecast_mw - raw.demand_mw)
