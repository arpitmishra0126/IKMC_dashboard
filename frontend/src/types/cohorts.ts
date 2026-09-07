import type { AttachmentStatSplit, DeliverySplitFloat, DeliverySplitInt } from "@/types/common"

/**
 * Mirrors backend/app/schemas/cohorts.py.
 */
export interface CohortCard {
  total_cases: number
  delivery: DeliverySplitInt
  ssc_under_2h: DeliverySplitInt
  avg_kmc: DeliverySplitFloat
  exclusive_bf: DeliverySplitInt
  attachment: AttachmentStatSplit
}

export interface CohortsResponse {
  inborn: CohortCard
  outborn: CohortCard
}
