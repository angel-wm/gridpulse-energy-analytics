select
    balancing_authority,
    reporting_date,
    reporting_hour_number,
    hour_ending_utc,
    demand_mw,
    forecast_mw,
    net_generation_mw,
    source_file,
    extract(hour from datetime(timestamp_sub(hour_ending_utc, interval 1 hour), 'America/Chicago')) as local_start_hour,
    if(demand_mw is not null and forecast_mw is not null, 1, 0) as paired_hour,
    forecast_mw - demand_mw as forecast_error_mw,
    abs(forecast_mw - demand_mw) as absolute_error_mw
from {{ ref('stg_eia930_erco_hourly') }}
