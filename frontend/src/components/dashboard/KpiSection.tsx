import { useState } from "react"
import {
  ArrowRightLeft,
  CalendarRange,
  ClipboardList,
  HeartCrack,
  LogOut,
  Stethoscope,
  UserCheck,
  UserX,
} from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { Section } from "@/components/layout/Section"
import { Skeleton } from "@/components/ui/skeleton"
import { useOverview } from "@/hooks/useOverview"
import { formatDateTime } from "@/lib/format"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

import { AttachmentAgeCard, AttachmentAgeCardSkeleton } from "./AttachmentAgeCard"
import { CompactMetricCard, CompactMetricCardSkeleton } from "./CompactMetricCard"
import { EnrolledKpiCard, EnrolledKpiCardSkeleton } from "./EnrolledKpiCard"
import { KpiCard, KpiCardSkeleton } from "./KpiCard"
import { PeriodFilter } from "./PeriodFilter"
import { TotalCasesSummary, TotalCasesSummarySkeleton } from "./TotalCasesSummary"

const DISCHARGE_LABELS = ["Discharged", "Referred", "LAMA", "Death"] as const

/**
 * Reproduces the "Key Performance Indicators (KPIs)" section of app.py:
 * PRE-SCREENED, SCREENED, ENROLLED - backed by GET /api/dashboard/overview.
 * ENROLLED is one composite card (EnrolledKpiCard, not two separate KPI
 * cards): the Consented population as its main value, with the M-SNCU-
 * requiring / Stable PT/LBW split shown as a compact breakdown beneath it,
 * per the verified ICMR source structure. Icons are purely decorative/
 * contextual and do not add or infer any new metric.
 *
 * The Reporting Period selector controls this 3-card row (filtered by the
 * STUDY ENROLLMENT DATE, mother.enr_dof - not scr_dof), the "Discharge
 * Outcomes" row (dis_inf_dt_outcome-filtered, same resolved boundaries),
 * the displayed period start/end date range, and the "Total Cases"
 * summary below - all from the same GET /api/dashboard/overview response,
 * so there is exactly one fetch per period/range change. Cohort Summary,
 * Data Quality, Still Admitted, and every other page remain unaffected.
 *
 * A custom From/To range (via PeriodFilter's Apply button) takes priority
 * over the preset `period` once applied; clicking a preset button clears
 * it and goes back to that preset immediately, including "All Data".
 */
export function KpiSection() {
  const [period, setPeriod] = useState<OverviewPeriod>("all")
  const [customRange, setCustomRange] = useState<OverviewDateRange | undefined>(undefined)
  const { data, error, isInitialLoading, refetch } = useOverview(period, customRange)

  return (
    <Section
      title="Key Performance Indicators (KPIs)"
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
      {error ? (
        <ErrorState message={error.detail} onRetry={refetch} />
      ) : (
        <>
          {isInitialLoading || !data ? (
            <Skeleton className="h-4 w-56" />
          ) : (
            <p className="text-muted-foreground flex items-center gap-1.5 text-xs font-medium">
              <CalendarRange className="size-3.5 shrink-0" aria-hidden="true" />
              Showing data: {formatDateTime(data.period_start)} – {formatDateTime(data.period_end)}
            </p>
          )}

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {isInitialLoading || !data ? (
              <>
                <KpiCardSkeleton label="PRE-SCREENED" />
                <KpiCardSkeleton label="SCREENED" />
                <EnrolledKpiCardSkeleton />
              </>
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
                <EnrolledKpiCard
                  label="ENROLLED"
                  value={data.enrolled}
                  icon={UserCheck}
                  description="Total enrolled PT/LBW babies"
                  breakdown={[
                    { label: "Enrolled PT/LBW babies requiring M-SNCU admission", value: data.enrolled_msncu },
                    { label: "Enrolled Stable PT/LBW babies", value: data.enrolled_stable },
                  ]}
                />
              </>
            )}
          </div>

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

          {isInitialLoading || !data ? (
            <TotalCasesSummarySkeleton />
          ) : (
            <TotalCasesSummary summary={data.total_cases_summary} />
          )}

          {isInitialLoading || !data ? (
            <AttachmentAgeCardSkeleton />
          ) : (
            <AttachmentAgeCard
              attachment={data.total_cases_summary.attachment}
              scopePrefix="overview"
              contextLabel="Overview"
              avgIsCombined
              period={period}
              customRange={customRange}
            />
          )}
        </>
      )}
    </Section>
  )
}
