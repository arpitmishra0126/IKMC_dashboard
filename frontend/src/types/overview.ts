import type { AttachmentStatSplit, DeliverySplitFloat, DeliverySplitInt } from "@/types/common"

/**
 * Period-aware Total Cases summary (senior feedback), combined across
 * Inborn + Outborn, NVD vs. C-Section. Same field shape as CohortCard's
 * metrics, but computed by an isolated backend calculation path
 * (services/overview_period_metrics.py) rather than the existing Cohort
 * Summary indicator functions - see docs on that module for why. Preserves
 * the exact existing formulas (including the known NVD-definition
 * inconsistency between exclusive_bf and the other metrics - see
 * docs/MIGRATION_DECISIONS.md #5), just period-filtered and combined.
 */
export interface TotalCasesSummary {
  total_cases: number
  delivery: DeliverySplitInt
  ssc_under_2h: DeliverySplitInt
  avg_kmc: DeliverySplitFloat
  exclusive_bf: DeliverySplitInt
  attachment: AttachmentStatSplit
}

/** Mirrors backend/app/schemas/overview.py. */
export interface OverviewResponse {
  pre_screened: number
  screened: number
  /** The project's existing PRE-SCREENED -> SCREENED -> ELIGIBLE ->
   * CONSENTED -> ENROLLED funnel endpoint (scr_mconst == 11 AND
   * scr_bw_ga_stable == 12) - see services/indicators.py get_enrolled_df().
   * Replaces the old eligible_for_enrollment card. */
  enrolled: number
  /** Filtered by dis_inf_dt_outcome (actual infant outcome date), same
   * resolved period boundaries as the 3 fields above (which use the
   * STUDY ENROLLMENT DATE, mother.enr_dof - not scr_dof). */
  discharged: number
  referred: number
  lama: number
  death: number
  /** ISO date strings. For "all", these show the actual earliest/latest
   * enr_dof present in the data (not filter bounds - "all" applies no
   * filtering, so existing values stay exactly as before this feature). */
  period_start: string | null
  period_end: string | null
  total_cases_summary: TotalCasesSummary
}

/**
 * Matches the `period` query param accepted by GET /api/dashboard/overview
 * (backend/app/api/dashboard.py). Relative periods are resolved server-side,
 * anchored to the latest STUDY ENROLLMENT DATE (mother.enr_dof) present in
 * the data - never the browser's clock. Applies to the 3 Overview KPI
 * cards, the 4 discharge outcome counts, and the Total Cases summary;
 * nothing else (Still Admitted, Cohort Summary, Data Quality, the
 * dedicated Discharge page).
 */
export type OverviewPeriod = "all" | "7d" | "30d" | "3m"

/**
 * Custom Reporting Period range (both bounds required, inclusive, ISO
 * "YYYY-MM-DD" date strings) - matches the from_date/to_date query params
 * accepted by GET /api/dashboard/overview. Takes priority over `period`
 * when both are somehow present. Filtered by the same STUDY ENROLLMENT
 * DATE (mother.enr_dof) as the relative periods above.
 */
export interface OverviewDateRange {
  from: string
  to: string
}
