/**
 * Mirrors backend/app/schemas/meta.py.
 *
 * `latest_screening_date` and `api_fetch_timestamp` are deliberately kept
 * as two separate, nullable fields - see docs/MIGRATION_DECISIONS.md #2.
 * `api_fetch_timestamp` is `null` whenever the backend has no reliable
 * fetch timestamp (e.g. DATA_SOURCE="json"); the frontend must not invent
 * a value when it is null.
 */
export interface SyncMetadataResponse {
  latest_screening_date: string | null
  api_fetch_timestamp: string | null
  data_source: string
}

export interface RefreshResponse {
  status: string
  detail: string
}
