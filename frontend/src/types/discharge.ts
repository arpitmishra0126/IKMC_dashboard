import type { DischargeBreakdown } from "@/types/common"

/** Mirrors backend/app/schemas/discharge.py exactly. */
export interface DischargeSummary {
  discharged: number
  referred: number
  lama: number
  death: number
  still_admitted: number
}

export interface DischargeResponse {
  summary: DischargeSummary
  inborn: DischargeBreakdown
  outborn: DischargeBreakdown
}
