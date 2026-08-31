import type { DeliverySplitFloat, DeliverySplitInt } from "@/types/common"

/**
 * Mirrors backend/app/schemas/cohorts.py.
 *
 * `displayed_*` are the exact hardcoded attachment-time strings currently
 * shown in the Streamlit app.py (e.g. "1h 45m"). `computed_*_hours` are the
 * real values from get_*_attachment_hours(). `is_hardcoded` flags that the
 * displayed values do not come from computed data.
 * See docs/MIGRATION_DECISIONS.md #3 - the frontend must show this
 * distinction, not silently pick one value.
 */
export interface AttachmentDisplay {
  displayed_nvd: string
  displayed_csection: string
  is_hardcoded: boolean
  computed_nvd_hours: number
  computed_csection_hours: number
}

export interface CohortCard {
  total_cases: number
  delivery: DeliverySplitInt
  ssc_under_2h: DeliverySplitInt
  avg_kmc: DeliverySplitFloat
  exclusive_bf: DeliverySplitInt
  attachment: AttachmentDisplay
}

export interface CohortsResponse {
  inborn: CohortCard
  outborn: CohortCard
}
