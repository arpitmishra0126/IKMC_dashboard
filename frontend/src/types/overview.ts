/** Mirrors backend/app/schemas/overview.py. */
export interface OverviewResponse {
  pre_screened: number
  screened: number
  eligible_for_enrollment: number
}

/**
 * Matches the `period` query param accepted by GET /api/dashboard/overview
 * (backend/app/api/dashboard.py). Relative periods are resolved server-side,
 * anchored to the latest scr_dof present in the data - never the browser's
 * clock. Applies only to the 3 Overview KPI cards; nothing else.
 */
export type OverviewPeriod = "all" | "7d" | "30d" | "3m"
