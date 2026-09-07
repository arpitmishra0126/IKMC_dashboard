import { useState } from "react"
import { ArrowRightLeft, ClipboardList, HeartCrack, LogOut, Stethoscope, UserCheck, UserX } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { Section } from "@/components/layout/Section"
import { useOverview } from "@/hooks/useOverview"
import type { OverviewPeriod } from "@/types/overview"

import { CompactMetricCard, CompactMetricCardSkeleton } from "./CompactMetricCard"
import { KpiCard, KpiCardSkeleton } from "./KpiCard"
import { PeriodFilter } from "./PeriodFilter"

const KPI_LABELS = ["PRE-SCREENED", "SCREENED", "ELIGIBLE FOR ENROLLMENT"] as const
const DISCHARGE_LABELS = ["Discharged", "Referred", "LAMA", "Death"] as const

/**
 * Reproduces the "Key Performance Indicators (KPIs)" section of app.py:
 * PRE-SCREENED, SCREENED, ELIGIBLE FOR ENROLLMENT - backed by
 * GET /api/dashboard/overview. Icons are purely decorative/contextual and
 * do not add or infer any new metric.
 *
 * The period selector (PeriodFilter) controls both this 3-card row (scr_dof-
 * filtered) and the compact "Discharge Outcomes" row below it
 * (dis_inf_dt_outcome-filtered, same resolved period boundaries) - Cohort
 * Summary, Data Quality, Still Admitted, and every other page are
 * unaffected, since only this section's fetch passes a `period` to
 * useOverview().
 */
export function KpiSection() {
  const [period, setPeriod] = useState<OverviewPeriod>("all")
  const { data, error, isInitialLoading, refetch } = useOverview(period)

  return (
    <Section
      title="Key Performance Indicators (KPIs)"
      actions={<PeriodFilter value={period} onChange={setPeriod} />}
    >
      {error ? (
        <ErrorState message={error.detail} onRetry={refetch} />
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {isInitialLoading || !data ? (
            KPI_LABELS.map((label) => <KpiCardSkeleton key={label} label={label} />)
          ) : (
            <>
              <KpiCard
                label="PRE-SCREENED"
                value={data.pre_screened}
                icon={ClipboardList}
                description="Total screening records"
              />
              <KpiCard
                label="SCREENED"
                value={data.screened}
                icon={Stethoscope}
                description="Preterm / low-birth-weight"
              />
              <KpiCard
                label="ELIGIBLE FOR ENROLLMENT"
                value={data.eligible_for_enrollment}
                icon={UserCheck}
                description="Meeting enrollment criteria"
              />
            </>
          )}
        </div>
      )}

      {error ? null : (
        <div className="flex flex-col gap-3">
          <h3 className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
            Discharge Outcomes
          </h3>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {isInitialLoading || !data ? (
              DISCHARGE_LABELS.map((label) => (
                <CompactMetricCardSkeleton key={label} label={label} />
              ))
            ) : (
              <>
                <CompactMetricCard label="Discharged" value={data.discharged} icon={LogOut} />
                <CompactMetricCard label="Referred" value={data.referred} icon={ArrowRightLeft} />
                <CompactMetricCard label="LAMA" value={data.lama} icon={UserX} />
                <CompactMetricCard label="Death" value={data.death} icon={HeartCrack} />
              </>
            )}
          </div>
        </div>
      )}
    </Section>
  )
}
