/** Mirrors backend/app/schemas/overview.py. */
export interface OverviewResponse {
  pre_screened: number
  screened: number
  eligible_for_enrollment: number
  /** Filtered by dis_inf_dt_outcome (actual infant outcome date), same
   * resolved period boundaries as the 3 fields above (which use scr_dof). */
  discharged: number
  referred: number
  lama: number
  death: number
}

/**
 * Matches the `period` query param accepted by GET /api/dashboard/overview
 * (backend/app/api/dashboard.py). Relative periods are resolved server-side,
 * anchored to the latest scr_dof present in the data - never the browser's
 * clock. Applies to the 3 Overview KPI cards and the 4 discharge outcome
 * counts; nothing else (Still Admitted, Cohort Summary, Data Quality, the
 * dedicated Discharge page).
 */
export type OverviewPeriod = "all" | "7d" | "30d" | "3m"
