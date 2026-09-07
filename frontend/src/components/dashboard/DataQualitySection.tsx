import { SeverityBadge } from "@/components/common/SeverityBadge"
import { ErrorState } from "@/components/common/ErrorState"
import { Section } from "@/components/layout/Section"
import { Skeleton } from "@/components/ui/skeleton"
import { useDataQuality } from "@/hooks/useDataQuality"
import { severityFromStatusText } from "@/lib/severity"

import { DataQualityCard, DataQualityCardSkeleton } from "./DataQualityCard"

const ROW_1_LABELS = [
  "SCREENING RECORDS WITHOUT BABY IDs",
  "DUPLICATE BABIES",
  "UNMATCHED RECORDS",
] as const

const ROW_2_LABELS = ["MISSING DAILY CARE", "DISCHARGE DUPLICATES"] as const

/**
 * Reproduces the "System Validation & Data Quality" section of app.py, with
 * severity-aware styling (icon + color + text, never color alone) and an
 * expandable detail table per check backed by the existing
 * GET /api/validation/{check} endpoint. No value shown here is recomputed -
 * see docs/MIGRATION_DECISIONS.md #4 and #7 for the known caveats in how
 * these checks are defined upstream.
 *
 * Layout: the overall validation_status (formerly a full standalone banner
 * card) is now a compact badge in the section header, so it reads as a
 * section-level status rather than a sixth card. The 5 checks are arranged
 * as 3 cards + 2 wider cards, matching how naturally related they are
 * (screening/registry checks vs. downstream linkage checks) and giving the
 * last two more room instead of a large empty area.
 */
export function DataQualitySection() {
  const { data, error, isInitialLoading, refetch } = useDataQuality()

  return (
    <Section
      title="System Validation & Data Quality"
      description="Summary of data completeness and integrity checks performed across source datasets."
      actions={
        isInitialLoading || !data ? (
          <Skeleton className="h-6 w-36 rounded-md" />
        ) : (
          <SeverityBadge severity={severityFromStatusText(data.validation_status)}>
            {data.validation_status}
          </SeverityBadge>
        )
      }
    >
      {error ? (
        <ErrorState message={error.detail} onRetry={refetch} />
      ) : (
        <div className="flex flex-col gap-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {isInitialLoading || !data ? (
              ROW_1_LABELS.map((label) => <DataQualityCardSkeleton key={label} label={label} />)
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
              </>
            )}
          </div>

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            {isInitialLoading || !data ? (
              ROW_2_LABELS.map((label) => <DataQualityCardSkeleton key={label} label={label} />)
            ) : (
              <>
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
