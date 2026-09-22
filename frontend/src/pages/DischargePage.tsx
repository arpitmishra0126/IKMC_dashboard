import { Ambulance, Baby, CalendarRange } from "lucide-react"
import { useState } from "react"

import { ErrorState } from "@/components/common/ErrorState"
import { DischargeOutcomeCard, DischargeOutcomeCardSkeleton } from "@/components/dashboard/DischargeOutcomeCard"
import {
  DischargeOutcomeSummary,
  DischargeOutcomeSummarySkeleton,
} from "@/components/dashboard/DischargeOutcomeSummary"
import { PeriodFilter } from "@/components/dashboard/PeriodFilter"
import { Section } from "@/components/layout/Section"
import { Skeleton } from "@/components/ui/skeleton"
import { useDischarge } from "@/hooks/useDischarge"
import { formatDateTime } from "@/lib/format"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

/**
 * Reproduces pages/6_Discharge.py via GET /api/dashboard/discharge - same
 * data, same values, redesigned presentation: one coherent outcome
 * summary (DischargeOutcomeSummary) instead of 5 separate KPI cards, and
 * one card per cohort (DischargeOutcomeCard) with NVD vs C-Section shown
 * as directly comparable table rows, matching the Overview's Cohort
 * Summary visual system.
 *
 * The Reporting Period selector (same PeriodFilter component/behavior as
 * Overview, independent state - not shared) narrows discharged/referred/
 * lama/death (summary and per-cohort) by dis_inf_dt_outcome (actual
 * infant outcome date), same as Overview's own discharge mini-cards.
 * `still_admitted` is a point-in-time census figure, not a discharge
 * event count, so it is NOT period-filtered.
 */
export function DischargePage() {
  const [period, setPeriod] = useState<OverviewPeriod>("all")
  const [customRange, setCustomRange] = useState<OverviewDateRange | undefined>(undefined)
  const { data, error, isInitialLoading, refetch } = useDischarge(period, customRange)

  if (error) {
    return (
      <Section title="Discharge Outcomes & Compliance Registry">
        <ErrorState message={error.detail} onRetry={refetch} />
      </Section>
    )
  }

  return (
    <>
      <Section
        title="Discharge Outcomes & Compliance Registry"
        description="Clinical outcomes, referral patterns, mortality tracking and discharge compliance indicators."
        actions={
          <PeriodFilter
            value={period}
            onChange={(nextPeriod) => {
              setPeriod(nextPeriod)
              setCustomRange(undefined)
            }}
            isCustomActive={customRange !== undefined}
            onApplyCustomRange={setCustomRange}
            onClearCustomRange={() => setCustomRange(undefined)}
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

        {isInitialLoading || !data ? (
          <DischargeOutcomeSummarySkeleton />
        ) : (
          <DischargeOutcomeSummary summary={data.summary} />
        )}
      </Section>

      <Section
        title="Outcomes by Cohort"
        description="Discharge outcome comparison between NVD and C-Section deliveries, for babies born in vs. referred to the facility."
      >
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {isInitialLoading || !data ? (
            <>
              <DischargeOutcomeCardSkeleton title="Inborn" accent="inborn" />
              <DischargeOutcomeCardSkeleton title="Outborn" accent="outborn" />
            </>
          ) : (
            <>
              <DischargeOutcomeCard title="Inborn" breakdown={data.inborn} accent="inborn" icon={Baby} />
              <DischargeOutcomeCard title="Outborn" breakdown={data.outborn} accent="outborn" icon={Ambulance} />
            </>
          )}
        </div>
      </Section>
    </>
  )
}
