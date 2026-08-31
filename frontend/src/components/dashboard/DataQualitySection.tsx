import { ErrorState } from "@/components/common/ErrorState"
import { Section } from "@/components/layout/Section"
import { useDataQuality } from "@/hooks/useDataQuality"

import { DataQualityCard, DataQualityCardSkeleton } from "./DataQualityCard"
import { ValidationStatusBanner, ValidationStatusBannerSkeleton } from "./ValidationStatusBanner"

const DATA_QUALITY_LABELS = [
  "SCREENING RECORDS WITHOUT BABY IDs",
  "DUPLICATE BABIES",
  "UNMATCHED RECORDS",
  "MISSING DAILY CARE",
  "DISCHARGE DUPLICATES",
] as const

/**
 * Reproduces the "System Validation & Data Quality" section of app.py, with
 * severity-aware styling (icon + color + text, never color alone) and an
 * expandable detail table per check backed by the existing
 * GET /api/validation/{check} endpoint. No value shown here is recomputed -
 * see docs/MIGRATION_DECISIONS.md #4 and #7 for the known caveats in how
 * these checks are defined upstream.
 */
export function DataQualitySection() {
  const { data, error, isInitialLoading, refetch } = useDataQuality()

  return (
    <Section
      title="System Validation & Data Quality"
      description="Summary of data completeness and integrity checks performed across source datasets."
    >
      {error ? (
        <ErrorState message={error.detail} onRetry={refetch} />
      ) : (
        <div className="flex flex-col gap-4">
          {isInitialLoading || !data ? (
            <ValidationStatusBannerSkeleton />
          ) : (
            <ValidationStatusBanner status={data.validation_status} />
          )}

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {isInitialLoading || !data ? (
              DATA_QUALITY_LABELS.map((label) => (
                <DataQualityCardSkeleton key={label} label={label} />
              ))
            ) : (
              <>
                <DataQualityCard
                  label="SCREENING RECORDS WITHOUT BABY IDs"
                  value={data.missing_baby_ids}
                  validationCheck="missing-baby-ids"
                />
                <DataQualityCard
                  label="DUPLICATE BABIES"
                  value={data.duplicate_babies}
                  validationCheck="duplicate-baby-ids"
                />
                <DataQualityCard
                  label="UNMATCHED RECORDS"
                  value={data.unmatched_records}
                  validationCheck="merge-mismatches"
                />
                <DataQualityCard
                  label="MISSING DAILY CARE"
                  value={data.missing_daily_care}
                  validationCheck="missing-daily-care"
                />
                <DataQualityCard
                  label="DISCHARGE DUPLICATES"
                  value={data.discharge_duplicates}
                  validationCheck="discharge-duplicates"
                />
              </>
            )}
          </div>
        </div>
      )}
    </Section>
  )
}
