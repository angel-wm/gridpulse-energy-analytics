{{ config(enabled=target.name == 'history') }}

with expected_clock_changes as (
    select * from unnest([
        struct(date '2023-03-12' as reporting_date, 23 as hours),
        struct(date '2023-11-05', 25),
        struct(date '2024-03-10', 23),
        struct(date '2024-11-03', 25),
        struct(date '2025-03-09', 23),
        struct(date '2025-11-02', 25)
    ])
),
observed as (
    select
        reporting_date,
        count(*) as hours,
        count(distinct hour_ending_utc) as utc_keys,
        count(distinct reporting_hour_number) as reporting_ordinals,
        countif(local_start_hour = 1) as one_am_hours,
        countif(local_start_hour = 2) as two_am_hours,
        countif(date(timestamp_sub(hour_ending_utc, interval 1 hour), 'America/Chicago') != reporting_date) as date_mismatches
    from {{ ref('fct_erco_hourly') }}
    group by reporting_date
)
select coalesce(observed.reporting_date, expected_clock_changes.reporting_date) as reporting_date
from observed
full outer join expected_clock_changes using (reporting_date)
where observed.hours is distinct from coalesce(expected_clock_changes.hours, 24)
   or observed.utc_keys != observed.hours
   or observed.reporting_ordinals != observed.hours
   or observed.one_am_hours != if(expected_clock_changes.hours = 25, 2, 1)
   or observed.two_am_hours != if(expected_clock_changes.hours = 23, 0, 1)
   or observed.date_mismatches != 0
