# GridPulse Color report variation

The [original design](report-spec.md) remains available in the original
PBIP. This variant uses an independent report definition over the same
historical semantic model. It retains the two analytical pages, all existing
data bindings, and the same date, local-hour, and navigation controls.

The larger peak tile and monthly demand trend set the demand-page hierarchy.
On the forecast page, MAE and bias get wider tiles than the coverage counts.
Bahnschrift provides the display typography. Teal distinguishes demand,
amber distinguishes forecast and signed bias, and violet identifies MAE.
Lighter versions of those colors distinguish the KPI surfaces from the
midnight-blue canvas.

## Canonical design contract

```yaml
Design Brief:
  generated_by: powerbi-report-cli
  contract_version: 1
  mode: brownfield
  design_identity:
    current_tone: Light slate analytical canvas with Segoe UI throughout
    current_signature: Equal-width KPI strips with restrained accents
    tone: Technical editorial design with a midnight-blue canvas and bright metric
      colors
    signature: Large primary KPI in a tinted panel, with smaller context cards and
      light chart surfaces
  archetype: Analytical Canvas
  navigation_model: page_navigator
  color_map:
  - measure: Hourly[Peak Demand MW]
    color: '#006C67'
    tint: '#D5F5EF'
  - measure: Hourly[Peak Reporting Date]
    color: '#334B80'
    tint: '#E4EDFF'
  - measure: Hourly[Mean Paired Demand MW]
    color: '#006C67'
    tint: '#D5F5EF'
  - measure: Hourly[Mean Observed Demand MW]
    color: '#006C67'
    tint: '#D5F5EF'
  - measure: Hourly[Mean Paired Forecast MW]
    color: '#A3470B'
    tint: '#FFF0DA'
  - measure: Hourly[Forecast MAE MW]
    color: '#5E36A5'
    tint: '#EDE4FF'
  - measure: Hourly[Forecast Bias MW]
    color: '#A3470B'
    tint: '#FFF0DA'
  - measure: Hourly[Paired Hours]
    color: '#006C67'
    tint: '#D5F5EF'
  - measure: Hourly[Reporting Hours]
    color: '#334B80'
    tint: '#E4EDFF'
  - measure: Hourly[Paired Coverage]
    color: '#126042'
    tint: '#D9F5E7'
  pages:
  - name: Demand patterns
    role: landing
    archetype: Analytical Canvas
    layout_variant: B
    variant_rationale: Give the paired monthly trend and primary peak more width,
      retaining all local hours.
    navigation:
    - element: page_navigator
      action: PageNavigation
      label: Demand patterns and Forecast accuracy
    page_background: '#0E1B30'
    layout_summary: Peak context above a wide monthly trend and an hourly comparison.
    layout_contract:
      canvas:
        width: 1920
        height: 1080
        margin: 32
        gutter: 24
        snap: 8
      grid:
        columns: 12
        rows: 12
        regions:
          header:
          - 1
          - 1
          - 8
          - 3
          filters:
          - 8
          - 1
          - 13
          - 3
          hero:
          - 1
          - 5
          - 9
          - 12
          hourly:
          - 9
          - 5
          - 13
          - 12
          source:
          - 1
          - 12
          - 9
          - 13
          navigation:
          - 9
          - 12
          - 13
          - 13
          peak_mw:
          - 1
          - 3
          - 8
          - 5
          peak_date:
          - 8
          - 3
          - 13
          - 5
      placements:
      - id: page_title
        region: header
        kind: textbox
        text: When does ERCO demand peak?
      - id: date_filter
        region: filters
        kind: slicer
        field_bindings: Calendar[Date]
        slicer_type: between
        slot: 1
        of: 2
        insight_basis: Compare an arbitrary reporting window, including short peaks.
      - id: hour_filter
        region: filters
        kind: slicer
        field_bindings: Hourly[local_start_hour]
        slicer_type: dropdown
        slot: 2
        of: 2
      - id: peak_mw
        region: peak_mw
        kind: cardVisual
        purpose: How high was observed demand?
        field_bindings: Hourly[Peak Demand MW]
        color_strategy: measure_match
        value_size: 60
      - id: peak_date
        region: peak_date
        kind: cardVisual
        purpose: On which reporting date was the selected peak observed?
        field_bindings: Hourly[Peak Reporting Date]
        color_strategy: measure_match
        value_size: 39
      - id: demand_trend
        region: hero
        kind: lineChart
        purpose: How did demand and forecast move over the reporting months?
        field_bindings:
          Category: Calendar[YearMonth]
          Y:
          - Hourly[Mean Paired Demand MW]
          - Hourly[Mean Paired Forecast MW]
        color_strategy: measure_match
      - id: demand_by_hour
        region: hourly
        kind: columnChart
        purpose: How does observed load vary by local interval-start hour?
        field_bindings:
          Category: Hourly[local_start_hour]
          Y: Hourly[Mean Observed Demand MW]
        sort_policy: category_asc
        color_strategy: measure_match
      - id: source_note
        region: source
        kind: textbox
        text: EIA-930 Balance · ERCO · 2023–2025 · Snapshot verified November 25,
          2026
      - id: pages
        region: navigation
        kind: page_navigator
      space_audit:
        content_cell_count: 120
        placed_cell_count: 120
        empty_cell_pct: 0
        unplaced_regions: []
        largest_region:
          name: hero
          pct_of_content: 46.67
        balance_rationale: Two charts retain the primary reading area, with card widths
          assigned by KPI importance.
  - name: Forecast accuracy
    role: detail
    archetype: Analytical Canvas
    layout_variant: A
    variant_rationale: Balance the month and local-hour error views while emphasizing
      MAE and bias over counts.
    navigation:
    - element: page_navigator
      action: PageNavigation
      label: Demand patterns and Forecast accuracy
    page_background: '#0E1B30'
    layout_summary: Coverage and errors in a compact strip above monthly and hourly
      MAE.
    layout_contract:
      canvas:
        width: 1920
        height: 1080
        margin: 32
        gutter: 24
        snap: 8
      grid:
        columns: 12
        rows: 12
        regions:
          header:
          - 1
          - 1
          - 8
          - 3
          filters:
          - 8
          - 1
          - 13
          - 3
          hero:
          - 1
          - 5
          - 8
          - 12
          hourly:
          - 8
          - 5
          - 13
          - 12
          source:
          - 1
          - 12
          - 9
          - 13
          navigation:
          - 9
          - 12
          - 13
          - 13
          mae_mw:
          - 1
          - 3
          - 4
          - 5
          bias_mw:
          - 4
          - 3
          - 7
          - 5
          paired_hours:
          - 7
          - 3
          - 9
          - 5
          reporting_hours:
          - 9
          - 3
          - 11
          - 5
          coverage:
          - 11
          - 3
          - 13
          - 5
      placements:
      - id: page_title
        region: header
        kind: textbox
        text: Where are day-ahead forecast errors largest?
      - id: date_filter
        region: filters
        kind: slicer
        field_bindings: Calendar[Date]
        slicer_type: between
        slot: 1
        of: 2
        insight_basis: Inspect forecast performance over arbitrary reporting windows.
      - id: hour_filter
        region: filters
        kind: slicer
        field_bindings: Hourly[local_start_hour]
        slicer_type: dropdown
        slot: 2
        of: 2
      - id: mae_mw
        region: mae_mw
        kind: cardVisual
        purpose: What is the typical error magnitude?
        field_bindings: Hourly[Forecast MAE MW]
        color_strategy: measure_match
        value_size: 50
      - id: bias_mw
        region: bias_mw
        kind: cardVisual
        purpose: Did forecasts run high or low on average?
        field_bindings: Hourly[Forecast Bias MW]
        color_strategy: measure_match
        value_size: 46
      - id: paired_hours
        region: paired_hours
        kind: cardVisual
        purpose: How many hours support the error estimates?
        field_bindings: Hourly[Paired Hours]
        color_strategy: measure_match
        value_size: 35
      - id: reporting_hours
        region: reporting_hours
        kind: cardVisual
        purpose: How many reporting hours are in the selected window?
        field_bindings: Hourly[Reporting Hours]
        color_strategy: measure_match
        value_size: 35
      - id: coverage
        region: coverage
        kind: cardVisual
        purpose: What fraction of the selected hours have both values?
        field_bindings: Hourly[Paired Coverage]
        color_strategy: measure_match
        value_size: 43
      - id: monthly_error
        region: hero
        kind: lineChart
        purpose: How did day-ahead MAE change by month?
        field_bindings:
          Category: Calendar[YearMonth]
          Y: Hourly[Forecast MAE MW]
          Tooltips:
          - Hourly[Paired Hours]
          - Hourly[Reporting Hours]
        color_strategy: measure_match
      - id: hourly_error
        region: hourly
        kind: columnChart
        purpose: Which local interval-start hours have larger forecast errors?
        field_bindings:
          Category: Hourly[local_start_hour]
          Y: Hourly[Forecast MAE MW]
          Tooltips:
          - Hourly[Paired Hours]
          - Hourly[Reporting Hours]
        sort_policy: category_asc
        color_strategy: measure_match
      - id: source_note
        region: source
        kind: textbox
        text: Positive bias means overforecasting · EIA-930 Balance · ERCO 2023–2025
      - id: pages
        region: navigation
        kind: page_navigator
      space_audit:
        content_cell_count: 120
        placed_cell_count: 120
        empty_cell_pct: 0
        unplaced_regions: []
        largest_region:
          name: hero
          pct_of_content: 40.83
        balance_rationale: Two charts retain the primary reading area, with card widths
          assigned by KPI importance.
  interaction_pattern:
    drill_targets: []
    cross_filter_rules: Date and local-hour slicers filter every data visual on their
      page. Chart selections do not change the other charts or cards.
  accessibility:
    alt_text_strategy: Name the measure, units, time grain, and intended comparison
      for each chart.
    contrast_notes: Light title and source text on navy; dark metric colors on pale
      tinted tiles and light charts.
  theme:
    base: A sibling of GridPulseLight using the same visual safeguards
    user_overrides: Bahnschrift for headlines and values; Segoe UI for filters, charts,
      and labels
```
