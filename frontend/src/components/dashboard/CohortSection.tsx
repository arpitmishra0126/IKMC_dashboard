import { Ambulance, Baby } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { Section } from "@/components/layout/Section"
import { useCohorts } from "@/hooks/useCohorts"

import { CohortSummaryCard, CohortSummaryCardSkeleton } from "./CohortSummaryCard"
import { CohortTotalBanner, CohortTotalBannerSkeleton } from "./CohortTotalBanner"

/**
 * Reproduces the "Cohort Summary" section of app.py (TOTAL INBORN CASES /
 * TOTAL OUTBORN CASES side by side) - backed by GET /api/dashboard/cohorts.
 * Inborn and Outborn are given distinct accent colors/icons purely for
 * visual separation; the underlying data and cohort definitions are
 * unchanged (see docs/MIGRATION_DECISIONS.md #6 for the outborn cohort
 * definition caveat).
 *
 * A combined-total banner sits above the two cards (CohortTotalBanner) -
 * purely a client-side sum of the same two total_cases values already
 * powering the cards below, not a new backend value.
 */
export function CohortSection() {
  const { data, error, isInitialLoading, refetch } = useCohorts()

  return (
    <Section
      title="Cohort Summary"
      description="Delivery-mode comparison of SSC, KMC, and breastfeeding compliance for babies born in vs. referred to the facility."
    >
      {error ? (
        <ErrorState message={error.detail} onRetry={refetch} />
      ) : (
        <div className="flex flex-col gap-3">
          {isInitialLoading || !data ? (
            <CohortTotalBannerSkeleton />
          ) : (
            <CohortTotalBanner
              inbornTotal={data.inborn.total_cases}
              outbornTotal={data.outborn.total_cases}
            />
          )}

          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            {isInitialLoading || !data ? (
              <>
                <CohortSummaryCardSkeleton title="TOTAL INBORN CASES" accent="inborn" />
                <CohortSummaryCardSkeleton title="TOTAL OUTBORN CASES" accent="outborn" />
              </>
            ) : (
              <>
                <CohortSummaryCard
                  title="TOTAL INBORN CASES"
                  cohort={data.inborn}
                  accent="inborn"
                  icon={Baby}
                />
                <CohortSummaryCard
                  title="TOTAL OUTBORN CASES"
                  cohort={data.outborn}
                  accent="outborn"
                  icon={Ambulance}
                />
              </>
            )}
          </div>
        </div>
      )}
    </Section>
  )
}
