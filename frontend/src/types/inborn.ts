import type { CoverageSplit, DeliverySplitFloat, DeliverySplitInt } from "@/types/common"

/**
 * Mirrors backend/app/schemas/inborn.py exactly (field names verified
 * against the live GET /api/dashboard/inborn response before writing this
 * file - not guessed).
 *
 * `nvd_definition_note` documents a real inconsistency in the existing
 * indicator functions (exclusive_bf.nvd uses scr_del_mode == 11 only,
 * while delivery/ssc/avg_kmc use scr_del_mode.isin([11, 12])) - see
 * docs/MIGRATION_DECISIONS.md #5. The frontend surfaces this note as-is,
 * it does not reconcile or hide it.
 */
export interface InbornUnitDetail {
  avg_kmc: number
  total_cases: number
  delivery: DeliverySplitInt
  ssc_under_2h: DeliverySplitInt
  avg_kmc_by_delivery: DeliverySplitFloat
  exclusive_bf: DeliverySplitInt
  attachment_hours: DeliverySplitFloat
  coverage: CoverageSplit
  nvd_definition_note: string
}

export interface InbornResponse {
  overall_avg_kmc_hours: number
  msncu: InbornUnitDetail
  pnc: InbornUnitDetail
}
