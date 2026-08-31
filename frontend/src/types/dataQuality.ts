/**
 * Mirrors backend/app/schemas/data_quality.py.
 *
 * `validation_status` is the raw string returned by
 * services.indicators.get_validation_status() (e.g. "🟢 Healthy" /
 * "🟡 Review Required"). Per docs/MIGRATION_DECISIONS.md #7, that status
 * does not currently factor in missing_baby_ids / duplicate_babies - the
 * frontend renders it as-is, it does not recompute or override it.
 */
export interface DataQualityResponse {
  missing_baby_ids: number
  duplicate_babies: number
  unmatched_records: number
  missing_daily_care: number
  discharge_duplicates: number
  validation_status: string
}
