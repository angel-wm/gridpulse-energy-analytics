{{ config(enabled=target.name == 'history') }}

with expected as (
    select * from unnest([
        struct(date '2023-01-01' as period_start, date '2023-07-01' as period_end, 4343 as hours),
        struct(date '2023-07-01', date '2024-01-01', 4417),
        struct(date '2024-01-01', date '2024-07-01', 4367),
        struct(date '2024-07-01', date '2025-01-01', 4417),
        struct(date '2025-01-01', date '2025-07-01', 4343),
        struct(date '2025-07-01', date '2026-01-01', 4417)
    ])
),
expected_sources as (
    select *, concat(
        'EIA930_BALANCE_', cast(extract(year from period_start) as string),
        if(extract(month from period_start) = 1, '_Jan_Jun.csv', '_Jul_Dec.csv')
    ) as source_file
    from expected
),
observed as (
    select
        source_file,
        min(reporting_date) as first_date,
        max(reporting_date) as last_date,
        count(distinct reporting_date) as days,
        count(*) as hours
    from {{ ref('fct_erco_hourly') }}
    group by source_file
)
select coalesce(expected_sources.source_file, observed.source_file) as source_file
from expected_sources
full outer join observed using (source_file)
where observed.hours is distinct from expected_sources.hours
   or observed.first_date is distinct from expected_sources.period_start
   or observed.last_date is distinct from date_sub(expected_sources.period_end, interval 1 day)
   or observed.days is distinct from date_diff(expected_sources.period_end, expected_sources.period_start, day)
