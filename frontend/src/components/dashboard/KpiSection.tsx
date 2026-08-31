import { ClipboardList, Stethoscope, UserCheck } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { Section } from "@/components/layout/Section"
import { useOverview } from "@/hooks/useOverview"

import { KpiCard, KpiCardSkeleton } from "./KpiCard"

const KPI_LABELS = ["PRE-SCREENED", "SCREENED", "ELIGIBLE FOR ENROLLMENT"] as const

/**
 * Reproduces the "Key Performance Indicators (KPIs)" section of app.py:
 * PRE-SCREENED, SCREENED, ELIGIBLE FOR ENROLLMENT - backed by
 * GET /api/dashboard/overview. Icons are purely decorative/contextual and
 * do not add or infer any new metric.
 */
export function KpiSection() {
  const { data, error, isInitialLoading, refetch } = useOverview()

  return (
    <Section title="Key Performance Indicators (KPIs)">
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
    </Section>
  )
}
