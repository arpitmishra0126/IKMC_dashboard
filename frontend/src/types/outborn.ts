/**
 * Mirrors backend/app/schemas/outborn.py exactly (field names verified
 * against the live GET /api/dashboard/outborn response).
 *
 * `outborn_definition_note` documents that every field here uses
 * scr_pob.isin([12, 13, 14]) in the existing indicator functions, which
 * differs from KPI_FORMULA_DEFINITIONS.txt (scr_pob == 12 only) - see
 * docs/MIGRATION_DECISIONS.md #6. Shown as-is, not reconciled here.
 */
export interface OutbornDeliveryUnit {
  case_count: number
  ssc_under_2h: number
  avg_kmc: number
  exclusive_bf: number
  attachment_hours: number
}

export interface OutbornResponse {
  total_cases: number
  overall_avg_kmc: number
  nvd: OutbornDeliveryUnit
  csection: OutbornDeliveryUnit
  outborn_definition_note: string
}
