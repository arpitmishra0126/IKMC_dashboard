/**
 * Mirrors backend/app/schemas/attachment_cases.py - the per-case audit
 * list behind the Attachment Age popover.
 */

/**
 * Matches the `scope` query param accepted by
 * GET /api/dashboard/attachment-cases (backend/app/api/dashboard.py).
 * `overview_*` is period-aware (same period/from_date/to_date as the
 * Overview Reporting Period filter); every other scope is not.
 */
export type AttachmentScope =
  | "msncu_nvd"
  | "msncu_csection"
  | "pnc_nvd"
  | "pnc_csection"
  | "outborn_nvd"
  | "outborn_csection"
  | "inborn_nvd"
  | "inborn_csection"
  | "overview_nvd"
  | "overview_csection"

/** The `${prefix}_nvd` / `${prefix}_csection` half of an AttachmentScope -
 * combined with a section in AttachmentAgeCard to build the full scope. */
export type AttachmentScopePrefix = "overview" | "msncu" | "pnc" | "outborn" | "inborn"

export interface AttachmentCaseRecord {
  scr_babyid: string
  recordid: string | null
  minutes: number | null
}

export interface AttachmentCasesResponse {
  scope: AttachmentScope
  cases: AttachmentCaseRecord[]
}
