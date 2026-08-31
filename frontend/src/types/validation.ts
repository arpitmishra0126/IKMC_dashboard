/** Mirrors backend/app/schemas/validation.py. */
export interface ValidationDetailResponse {
  check: string
  row_count: number
  columns: string[]
  records: Array<Record<string, unknown>>
}
