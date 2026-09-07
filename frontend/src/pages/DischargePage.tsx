import { Ambulance, Baby } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { DischargeOutcomeCard, DischargeOutcomeCardSkeleton } from "@/components/dashboard/DischargeOutcomeCard"
import {
  DischargeOutcomeSummary,
  DischargeOutcomeSummarySkeleton,
} from "@/components/dashboard/DischargeOutcomeSummary"
import { Section } from "@/components/layout/Section"
import { useDischarge } from "@/hooks/useDischarge"

/**
 * Reproduces pages/6_Discharge.py via GET /api/dashboard/discharge - same
 * data, same values, redesigned presentation: one coherent outcome
 * summary (DischargeOutcomeSummary) instead of 5 separate KPI cards, and
 * one card per cohort (DischargeOutcomeCard) with NVD vs C-Section shown
 * as directly comparable table rows, matching the Overview's Cohort
 * Summary visual system.
 */
export function DischargePage() {
  const { data, error, isInitialLoading, refetch } = useDischarge()

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
      >
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
