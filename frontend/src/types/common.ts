/**
 * Mirrors backend/app/schemas/common.py.
 * These types describe API response shapes only - no calculation logic
 * lives here or anywhere else in the frontend.
 */

export interface DeliverySplitInt {
  nvd: number
  csection: number
}

export interface DeliverySplitFloat {
  nvd: number
  csection: number
}

export interface CoverageDetail {
  percentage: number
  achieved_count: number
}

export interface CoverageSplit {
  nvd: CoverageDetail
  csection: CoverageDetail
}

export interface DischargeOutcome {
  discharged: number
  referred: number
  lama: number
  death: number
}

export interface DischargeBreakdown {
  nvd: DischargeOutcome
  csection: DischargeOutcome
}

export interface AttachmentStat {
  minutes: number
  case_count: number
}

export interface AttachmentStatSplit {
  nvd: AttachmentStat
  csection: AttachmentStat
}
