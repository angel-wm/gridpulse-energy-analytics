# GridPulse Power BI report specification

**Approved on 2026-11-26.** This specification defines the first Power BI
report build.

## Report identity

| Item | Scope |
| --- | --- |
| Report | GridPulse — ERCO Demand & Forecast Accuracy |
| Audience | Portfolio reviewers and analysts evaluating a reproducible historical energy analysis |
| Purpose | Explore when demand peaked, where day-ahead forecast error was largest, and how much of the selected period has paired data |
| Delivery | Local Power BI Desktop Import using a parameterized CSV and versioned PBIP, PBIR, and TMDL text |
| Reporting window | ERCO (Texas), EIA reporting dates 2023-01-01 through 2025-12-31 |

## Semantic model binding

The planned entry mode is **Local Model**. The final report will bind by path
to `../GridPulse.SemanticModel` from `powerbi/GridPulse.Report`. The
[verified warehouse fact](../dbt/models/history/marts/fct_erco_hourly.sql)
and [export query](../docs/validation/export_erco_history.sql) define the
field inventory. Phase 3 verified a separate local import pilot. The final
historical model will be created after approval.

- **Hourly** imports the curated CSV. It has one ERCO fact per distinct UTC
  hour ending. Keep reporting date, reporting hour, UTC timestamp, demand,
  forecast, generation, source filename, local interval-start hour, paired
  flag, signed error, and absolute error with explicit types.
- **Calendar** contains one row for each of the 1,096 reporting dates.
  Relate `Calendar[Date]` one-to-many, active and single direction, to
  `Hourly[reporting_date]`. Sort `Calendar[YearMonth]` by a numeric
  year-month key and `Hourly[local_start_hour]` numerically.
- Define `CsvPath` as a local Power Query text parameter. Record the
  refresh instructions and exclude personal settings and data caches.

## User decisions and constraints

Use the two pages in the
[approved baseline](../docs/phase-0-design-baseline.md#power-bi-delivery)
and English labels consistent with the repository. Use a native page
navigator and date and local-hour slicers on both pages. Each slicer
filters all analytical visuals on that page. Use titles, units, signed
numbers, and visible counts to explain the metrics. Keep Fabric and paid
sharing outside this phase. Data delivery remains local.

## Narrative and page plan

1. **Demand patterns** answers when observed demand peaked, how paired
   demand and forecast evolved month by month, and how observed demand
   varies by local start hour. The peak card is paired with its EIA
   reporting date. A monthly line chart and hourly chart carry the detail.
2. **Forecast accuracy** answers how large and in which direction forecast
   error was, and how many observations support it. Compact cards show
   MAE, signed bias, paired hours, reporting hours, and coverage. Monthly and hourly charts
   show error magnitude at different time grains.

## Design identity

Use a restrained analytical style with a light canvas, dark type,
consistent metric colors, and a repeated compact context strip. Use Segoe
UI throughout. Use solid/contrasting series styling for the two demand
trends and include alt text and labels with units. The primary chart on
each page uses the larger panel. The hourly chart sits beside it.

## Model requirements

| Measure | Definition |
| --- | --- |
| Peak Demand MW | Maximum reported demand in the current filter context |
| Peak Reporting Date | Earliest EIA reporting date tied for the observed peak in context, blank when peak is blank |
| Mean Paired Demand MW | Mean of demand over paired hours |
| Mean Paired Forecast MW | Mean of forecast over the same paired hours |
| Mean Observed Demand MW | Mean of all non-null observed demand values in context |
| Reporting Hours | Number of rows in the selected date and local-hour context |
| Paired Hours | Sum of the upstream paired flag |
| Paired Coverage | Paired hours divided by reporting hours |
| Forecast MAE MW | Sum of upstream absolute error divided by paired hours |
| Forecast Bias MW | Sum of upstream signed error divided by paired hours |

The error measures return blank when there are zero paired hours. The
paired-hours and reporting-hours cards expose the coverage numerator and
denominator.
Report dates retain the EIA reporting calendar. The local-hour slicer
groups the two repeated autumn intervals while the UTC fact key preserves
both observations.

## Canonical design contract

```yaml
Design Brief:
  generated_by: powerbi-report-cli
  contract_version: 1
  mode: greenfield
  design_identity:
    tone: "Restrained analytical canvas with light slate surfaces and crisp type"
    signature: "A recurring metric strip with explicit units and coverage context"
  archetype: Analytical Canvas
  navigation_model: page_navigator
  color_map:
    - {measure: "Hourly[Peak Demand MW]", color: "#005D71", tint: "#D3EEF3"}
    - {measure: "Hourly[Mean Paired Demand MW]", color: "#005D71", tint: "#D3EEF3"}
    - {measure: "Hourly[Mean Observed Demand MW]", color: "#005D71", tint: "#D3EEF3"}
    - {measure: "Hourly[Mean Paired Forecast MW]", color: "#8A4C14", tint: "#FBE8D2"}
    - {measure: "Hourly[Forecast MAE MW]", color: "#5B4293", tint: "#EEE7F8"}
    - {measure: "Hourly[Forecast Bias MW]", color: "#8A4C14", tint: "#FBE8D2"}
    - {measure: "Hourly[Paired Coverage]", color: "#236238", tint: "#E1F0E4"}
  pages:
    - name: Demand patterns
      role: landing
      archetype: Analytical Canvas
      layout_variant: A
      variant_rationale: "The chronology needs more horizontal space than the 24-hour comparison."
      navigation: [{element: page_navigator, action: PageNavigation, label: "Demand patterns and Forecast accuracy"}]
      page_background: "#F2F5F8"
      layout_summary: "Peak context above a wide monthly trend and an hourly comparison."
      layout_contract:
        canvas: {width: 1920, height: 1080, margin: 32, gutter: 24, snap: 8}
        grid:
          columns: 12
          rows: 12
          regions:
            header: [1, 1, 8, 3]
            filters: [8, 1, 13, 3]
            kpis: [1, 3, 13, 5]
            hero: [1, 5, 8, 12]
            hourly: [8, 5, 13, 12]
            source: [1, 12, 9, 13]
            navigation: [9, 12, 13, 13]
        placements:
          - {id: page_title, region: header, kind: textbox, text: "When does ERCO demand peak?"}
          - {id: date_filter, region: filters, kind: slicer, field_bindings: "Calendar[Date]", slicer_type: between, slot: 1, of: 2, insight_basis: "Compare an arbitrary reporting window, including short peaks."}
          - {id: hour_filter, region: filters, kind: slicer, field_bindings: "Hourly[local_start_hour]", slicer_type: dropdown, slot: 2, of: 2}
          - {id: peak_mw, region: kpis, kind: cardVisual, purpose: "How high was observed demand?", field_bindings: "Hourly[Peak Demand MW]", color_strategy: measure_match, slot: 1, of: 2}
          - {id: peak_date, region: kpis, kind: cardVisual, purpose: "On which reporting date was the selected peak observed?", field_bindings: "Hourly[Peak Reporting Date]", color_strategy: none, slot: 2, of: 2}
          - id: demand_trend
            region: hero
            kind: lineChart
            purpose: "How did demand and forecast move over the reporting months?"
            field_bindings: {Category: "Calendar[YearMonth]", Y: ["Hourly[Mean Paired Demand MW]", "Hourly[Mean Paired Forecast MW]"]}
            color_strategy: measure_match
          - {id: demand_by_hour, region: hourly, kind: columnChart, purpose: "How does observed load vary by local interval-start hour?", field_bindings: {Category: "Hourly[local_start_hour]", Y: "Hourly[Mean Observed Demand MW]"}, sort_policy: category_asc, color_strategy: measure_match}
          - {id: source_note, region: source, kind: textbox, text: "EIA-930 Balance · ERCO · 2023–2025 · Snapshot verified November 25, 2026"}
          - {id: pages, region: navigation, kind: page_navigator}
        space_audit:
          content_cell_count: 120
          placed_cell_count: 120
          empty_cell_pct: 0
          unplaced_regions: []
          largest_region: {name: hero, pct_of_content: 40.83}
          balance_rationale: "The chronology gets 49 cells. The 24-hour chart retains 35 cells and the two peak cards share a compact strip."
    - name: Forecast accuracy
      role: detail
      archetype: Analytical Canvas
      layout_variant: A
      variant_rationale: "Monthly error needs a wider scale while the hourly chart shows all 24 local buckets."
      navigation: [{element: page_navigator, action: PageNavigation, label: "Demand patterns and Forecast accuracy"}]
      page_background: "#F2F5F8"
      layout_summary: "Coverage and errors in a compact strip above monthly and hourly MAE."
      layout_contract:
        canvas: {width: 1920, height: 1080, margin: 32, gutter: 24, snap: 8}
        grid:
          columns: 12
          rows: 12
          regions:
            header: [1, 1, 8, 3]
            filters: [8, 1, 13, 3]
            kpis: [1, 3, 13, 5]
            hero: [1, 5, 8, 12]
            hourly: [8, 5, 13, 12]
            source: [1, 12, 9, 13]
            navigation: [9, 12, 13, 13]
        placements:
          - {id: page_title, region: header, kind: textbox, text: "Where are day-ahead forecast errors largest?"}
          - {id: date_filter, region: filters, kind: slicer, field_bindings: "Calendar[Date]", slicer_type: between, slot: 1, of: 2, insight_basis: "Inspect forecast performance over arbitrary reporting windows."}
          - {id: hour_filter, region: filters, kind: slicer, field_bindings: "Hourly[local_start_hour]", slicer_type: dropdown, slot: 2, of: 2}
          - {id: mae_mw, region: kpis, kind: cardVisual, purpose: "What is the typical error magnitude?", field_bindings: "Hourly[Forecast MAE MW]", color_strategy: measure_match, slot: 1, of: 5}
          - {id: bias_mw, region: kpis, kind: cardVisual, purpose: "Did forecasts run high or low on average?", field_bindings: "Hourly[Forecast Bias MW]", color_strategy: measure_match, slot: 2, of: 5}
          - {id: paired_hours, region: kpis, kind: cardVisual, purpose: "How many hours support the error estimates?", field_bindings: "Hourly[Paired Hours]", color_strategy: none, slot: 3, of: 5}
          - {id: reporting_hours, region: kpis, kind: cardVisual, purpose: "How many reporting hours are in the selected window?", field_bindings: "Hourly[Reporting Hours]", color_strategy: none, slot: 4, of: 5}
          - {id: coverage, region: kpis, kind: cardVisual, purpose: "What fraction of the selected hours have both values?", field_bindings: "Hourly[Paired Coverage]", color_strategy: measure_match, slot: 5, of: 5}
          - {id: monthly_error, region: hero, kind: lineChart, purpose: "How did day-ahead MAE change by month?", field_bindings: {Category: "Calendar[YearMonth]", Y: "Hourly[Forecast MAE MW]", Tooltips: ["Hourly[Paired Hours]", "Hourly[Reporting Hours]"]}, color_strategy: measure_match}
          - {id: hourly_error, region: hourly, kind: columnChart, purpose: "Which local interval-start hours have larger forecast errors?", field_bindings: {Category: "Hourly[local_start_hour]", Y: "Hourly[Forecast MAE MW]", Tooltips: ["Hourly[Paired Hours]", "Hourly[Reporting Hours]"]}, sort_policy: category_asc, color_strategy: measure_match}
          - {id: source_note, region: source, kind: textbox, text: "Positive bias means overforecasting · EIA-930 Balance · ERCO 2023–2025"}
          - {id: pages, region: navigation, kind: page_navigator}
        space_audit:
          content_cell_count: 120
          placed_cell_count: 120
          empty_cell_pct: 0
          unplaced_regions: []
          largest_region: {name: hero, pct_of_content: 40.83}
          balance_rationale: "The two charts show monthly and local-hour patterns. Five compact cards retain the error and coverage context."
  interaction_pattern:
    drill_targets: []
    cross_filter_rules: "Date and local-hour slicers filter every data visual on their page. Chart selections do not change the other charts or cards."
  accessibility:
    alt_text_strategy: "Name the measure, units, time grain, and intended comparison for each chart."
    contrast_notes: "Dark body text on white or light slate. Use labels and series styling as well as color."
  theme:
    base: "Adapt references/design/assets/base.json with Segoe UI, white cards, and the contract palette."
    user_overrides: "Keep the English report labels and EIA source attribution."
```

## Implementation and acceptance

- Bind the project locally and import the curated CSV into the Hourly fact.
- Validate the full period against 26,304 distinct hours, 26,232 paired
  hours, 85,544 MW peak, 1,268.017726 MW MAE, and +374.605558 MW bias.
- Validate March 2025 and a local-hour filter. Check a restricted selection
  with no paired observations and confirm empty MAE and bias.
- Validate both pages in Desktop, including date filtering, sort order,
  coverage, labels, and accessibility. Reopen and refresh the same PBIP,
  then capture both pages for portfolio review.
- Keep the CSV and model cache outside version control. Publish the
  approved repository artifacts within the project release workflow.

## Dependency status

- **Source and schema:** Verified historical BigQuery fact and curated CSV contract.
- **Desktop:** Installed. Phase 3 verified a local import and DAX execution.
  Phase 6 report reopening, refresh, and visual preview remain pending.
- **PBIP/PBIR and TMDL:** The baseline specifies local text project files.
  No historical report or model files exist yet.
- **Modeling MCP:** Available for local validation. Phase 3 used an authorized
  local write session and checked DAX against Desktop.
- **Authoring CLI:** Node and npm are installed. The authoring CLI was
  absent from PATH during the planning check. Verify its supported
  installation and Desktop preview route after approval.
- **Delivery:** Local file-based authoring and repository evidence.
