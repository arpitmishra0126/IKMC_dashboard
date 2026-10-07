import { useState } from "react"

import { SeverityBadge } from "@/components/common/SeverityBadge"
import { ErrorState } from "@/components/common/ErrorState"
import { Section } from "@/components/layout/Section"
import { Skeleton } from "@/components/ui/skeleton"
import { useDataQuality } from "@/hooks/useDataQuality"
import { severityFromStatusText } from "@/lib/severity"
import type { DataQualityResponse } from "@/types/dataQuality"

import { DataQualityCard, DataQualityCardSkeleton } from "./DataQualityCard"
import { ValidationDetailPanel } from "./ValidationDetailPanel"

interface CheckSpec {
  label: string
  check: string
  value: (data: DataQualityResponse) => number
}

/** Row-major order: row 1 = first three, row 2 = last three (3 columns on desktop). */
const CHECKS: CheckSpec[] = [
  { label: "SCREENING RECORDS WITHOUT BABY IDs", check: "missing-baby-ids", value: (d) => d.missing_baby_ids },
  { label: "DUPLICATE BABIES", check: "duplicate-baby-ids", value: (d) => d.duplicate_babies },
  { label: "UNMATCHED RECORDS", check: "merge-mismatches", value: (d) => d.unmatched_records },
  { label: "MISSING DAILY CARE", check: "missing-daily-care", value: (d) => d.missing_daily_care },
  { label: "DISCHARGE DUPLICATES", check: "discharge-duplicates", value: (d) => d.discharge_duplicates },
  {
    label: "INITIATION BEFORE BIRTH (SSC / BREASTFEEDING)",
    check: "initiation-before-birth",
    value: (d) => d.initiation_before_birth,
  },
]

/**
 * Reproduces the "System Validation & Data Quality" section of app.py, with
 * severity-aware styling (icon + color + text, never color alone) and an
 * expandable record table per check backed by the existing
 * GET /api/validation/{check} endpoint. No value shown here is recomputed -
 * see docs/MIGRATION_DECISIONS.md #4 and #7 for the known caveats in how
 * these checks are defined upstream.
 *
 * Layout: all six checks share one equal-width grid (3 / 2 / 1 columns by
 * breakpoint). An opened card's record table renders below the grid, at the
 * grid's full width, so the cards never resize. The overall
 * validation_status is a compact badge in the section header.
 */
export function DataQualitySection() {
  const { data, error, isInitialLoading, refetch } = useDataQuality()
  const [openCheck, setOpenCheck] = useState<string | null>(null)
  const openSpec = CHECKS.find((spec) => spec.check === openCheck)

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
          <div className="grid auto-rows-fr grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {isInitialLoading || !data
              ? CHECKS.map((spec) => <DataQualityCardSkeleton key={spec.check} label={spec.label} />)
              : CHECKS.map((spec) => (
                  <DataQualityCard
                    key={spec.check}
                    label={spec.label}
                    value={spec.value(data)}
                    validationCheck={spec.check}
                    isOpen={openCheck === spec.check}
                    onToggle={() =>
                      setOpenCheck((current) => (current === spec.check ? null : spec.check))
                    }
                  />
                ))}
          </div>

          {openSpec ? (
            <div className="bg-card border-border/70 rounded-xl border p-4">
              <p className="text-muted-foreground mb-3 text-xs font-semibold uppercase tracking-wide">
                {openSpec.label} - records
              </p>
              <ValidationDetailPanel key={openSpec.check} check={openSpec.check} />
            </div>
          ) : null}
        </div>
      )}
    </Section>
  )
}
