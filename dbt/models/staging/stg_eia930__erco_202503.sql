select
    balancing_authority,
    reporting_date,
    reporting_hour_number,
    hour_ending_utc,
    demand_mw,
    forecast_mw,
    net_generation_mw,
    source_file
from {{ source('eia930', 'erco_202503') }}
