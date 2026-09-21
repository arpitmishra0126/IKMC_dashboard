import { CalendarRange, HeartPulse, ShieldPlus, Stethoscope } from "lucide-react"
import { useState } from "react"

import { AttachmentAgeCard, AttachmentAgeCardSkeleton } from "@/components/dashboard/AttachmentAgeCard"
import { ErrorState } from "@/components/common/ErrorState"
import { InbornUnitCard, InbornUnitCardSkeleton } from "@/components/dashboard/InbornUnitCard"
import { KpiCard, KpiCardSkeleton } from "@/components/dashboard/KpiCard"
import { PeriodFilter } from "@/components/dashboard/PeriodFilter"
import { Section } from "@/components/layout/Section"
import { Skeleton } from "@/components/ui/skeleton"
import { useInborn } from "@/hooks/useInborn"
import { formatDateTime } from "@/lib/format"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

/**
 * Reproduces pages/2_Inborn.py via GET /api/dashboard/inborn: overall avg
 * iKMC, then MSNCU and PNC each as their own section (rather than one
 * giant card). A single failed fetch shows one retryable error for the
 * whole page - the rest of the app (Header/TopNavigation) keeps working.
 *
 * The Reporting Period selector (same PeriodFilter component/behavior as
 * Overview, independent state - not shared) narrows total_cases/avg_kmc/
 * delivery/ssc_under_2h/avg_kmc_by_delivery/exclusive_bf on both MSNCU and
 * PNC by the STUDY ENROLLMENT DATE (mother.enr_dof). iKMC coverage/
 * Achieved count and Attachment Age are NOT period-filtered - they keep
 * showing the existing, unfiltered figures regardless of the selected
 * period, per explicit instruction.
 */
export function InbornPage() {
  const [period, setPeriod] = useState<OverviewPeriod>("all")
  const [customRange, setCustomRange] = useState<OverviewDateRange | undefined>(undefined)
  const { data, error, isInitialLoading, refetch } = useInborn(period, customRange)

  if (error) {
    return (
      <Section title="Inborn Cohort Compliance Registry">
        <ErrorState message={error.detail} onRetry={refetch} />
      </Section>
    )
  }

  return (
    <>
      <Section
        title="Inborn Cohort Compliance Registry"
        description="Detailed metrics, SSC & KMC progress indexes for births completed within facility."
        actions={
          <PeriodFilter
            value={period}
            onChange={(nextPeriod) => {
              setPeriod(nextPeriod)
              setCustomRange(undefined)
            }}
            isCustomActive={customRange !== undefined}
            onApplyCustomRange={setCustomRange}
          />
        }
      >
        {isInitialLoading || !data ? (
          <Skeleton className="h-4 w-56" />
        ) : (
          <p className="text-muted-foreground flex items-center gap-1.5 text-xs font-medium">
            <CalendarRange className="size-3.5 shrink-0" aria-hidden="true" />
            Showing data: {formatDateTime(data.period_start)} – {formatDateTime(data.period_end)}
          </p>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-3">
          {isInitialLoading || !data ? (
            <KpiCardSkeleton label="OVERALL AVG iKMC" />
          ) : (
            <KpiCard
              label="OVERALL AVG iKMC"
              value={`${data.overall_avg_kmc_hours} hrs/day`}
              icon={HeartPulse}
            />
          )}
        </div>
      </Section>

      <Section title="MSNCU" description="Mother Sick Newborn Care Unit">
        {isInitialLoading || !data ? (
          <>
            <InbornUnitCardSkeleton title="MSNCU" />
            <AttachmentAgeCardSkeleton />
          </>
        ) : (
          <>
            <InbornUnitCard
              title="MSNCU"
              description="Mother Sick Newborn Care Unit"
              unit={data.msncu}
              icon={Stethoscope}
            />
            <AttachmentAgeCard
              attachment={data.msncu.attachment}
              scopePrefix="msncu"
              contextLabel="MSNCU (Inborn)"
            />
          </>
        )}
      </Section>

      <Section title="PNC" description="Post Natal Care">
        {isInitialLoading || !data ? (
          <>
            <InbornUnitCardSkeleton title="PNC" />
            <AttachmentAgeCardSkeleton />
          </>
        ) : (
          <>
            <InbornUnitCard
              title="PNC"
              description="Post Natal Care"
              unit={data.pnc}
              icon={ShieldPlus}
            />
            <AttachmentAgeCard
              attachment={data.pnc.attachment}
              scopePrefix="pnc"
              contextLabel="PNC (Inborn)"
            />
          </>
        )}
      </Section>
    </>
  )
}
