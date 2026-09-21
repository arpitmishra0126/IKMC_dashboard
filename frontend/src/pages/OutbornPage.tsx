import { Ambulance, CalendarRange, Scissors, TrendingUp } from "lucide-react"
import { useState } from "react"

import { AttachmentAgeCard, AttachmentAgeCardSkeleton } from "@/components/dashboard/AttachmentAgeCard"
import { ErrorState } from "@/components/common/ErrorState"
import { KpiCard, KpiCardSkeleton } from "@/components/dashboard/KpiCard"
import { OutbornDeliveryCard, OutbornDeliveryCardSkeleton } from "@/components/dashboard/OutbornDeliveryCard"
import {
  OutbornIndicatorTable,
  OutbornIndicatorTableSkeleton,
} from "@/components/dashboard/OutbornIndicatorTable"
import { PeriodFilter } from "@/components/dashboard/PeriodFilter"
import { Section } from "@/components/layout/Section"
import { Skeleton } from "@/components/ui/skeleton"
import { useOutborn } from "@/hooks/useOutborn"
import { formatDateTime } from "@/lib/format"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

/**
 * Reproduces pages/3_Outborn.py via GET /api/dashboard/outborn: overall
 * totals/avg KMC, then NVD and C-Section each as their own card.
 *
 * The Reporting Period selector (same PeriodFilter component/behavior as
 * Overview, independent state - not shared) narrows total_cases/
 * overall_avg_kmc/case_count/ssc_under_2h/avg_kmc/exclusive_bf by the
 * STUDY ENROLLMENT DATE (mother.enr_dof). iKMC coverage/Achieved count
 * and Attachment Age are NOT period-filtered - they keep showing the
 * existing, unfiltered figures regardless of the selected period, per
 * explicit instruction.
 */
export function OutbornPage() {
  const [period, setPeriod] = useState<OverviewPeriod>("all")
  const [customRange, setCustomRange] = useState<OverviewDateRange | undefined>(undefined)
  const { data, error, isInitialLoading, refetch } = useOutborn(period, customRange)

  if (error) {
    return (
      <Section title="Outborn Cohort Compliance Registry">
        <ErrorState message={error.detail} onRetry={refetch} />
      </Section>
    )
  }

  return (
    <>
      <Section
        title="Outborn Cohort Compliance Registry"
        description="Detailed metrics, SSC & KMC progress indexes for outborn admissions."
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

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {isInitialLoading || !data ? (
            <>
              <KpiCardSkeleton label="TOTAL OUTBORN CASES" />
              <KpiCardSkeleton label="OVERALL AVG iKMC" />
            </>
          ) : (
            <>
              <KpiCard label="TOTAL OUTBORN CASES" value={data.total_cases} icon={Ambulance} />
              <KpiCard
                label="OVERALL AVG iKMC"
                value={`${data.overall_avg_kmc} hrs/day`}
                icon={TrendingUp}
              />
            </>
          )}
        </div>
        {data ? (
          <p className="text-muted-foreground text-[11px] italic">{data.outborn_definition_note}</p>
        ) : null}
      </Section>

      {isInitialLoading || !data ? (
        <OutbornIndicatorTableSkeleton />
      ) : (
        <OutbornIndicatorTable data={data} icon={Ambulance} />
      )}

      <Section title="NVD" description="Normal Vaginal Delivery">
        {isInitialLoading || !data ? (
          <OutbornDeliveryCardSkeleton title="NVD" accent="outborn" />
        ) : (
          <OutbornDeliveryCard title="NVD" unit={data.nvd} icon={Ambulance} accent="outborn" />
        )}
      </Section>

      <Section title="C-Section" description="Caesarean delivery">
        {isInitialLoading || !data ? (
          <OutbornDeliveryCardSkeleton title="C-Section" accent="outborn" />
        ) : (
          <OutbornDeliveryCard title="C-Section" unit={data.csection} icon={Scissors} accent="outborn" />
        )}
      </Section>

      {isInitialLoading || !data ? (
        <AttachmentAgeCardSkeleton />
      ) : (
        <AttachmentAgeCard
          attachment={{ nvd: data.nvd.attachment, csection: data.csection.attachment }}
          scopePrefix="outborn"
          contextLabel="Outborn"
        />
      )}
    </>
  )
}
