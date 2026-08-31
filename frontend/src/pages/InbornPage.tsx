import { HeartPulse, ShieldPlus, Stethoscope } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { InbornUnitCard, InbornUnitCardSkeleton } from "@/components/dashboard/InbornUnitCard"
import { KpiCard, KpiCardSkeleton } from "@/components/dashboard/KpiCard"
import { Section } from "@/components/layout/Section"
import { useInborn } from "@/hooks/useInborn"

/**
 * Reproduces pages/2_Inborn.py via GET /api/dashboard/inborn: overall avg
 * iKMC, then MSNCU and PNC each as their own section (rather than one
 * giant card). A single failed fetch shows one retryable error for the
 * whole page - the rest of the app (Header/TopNavigation) keeps working.
 */
export function InbornPage() {
  const { data, error, isInitialLoading, refetch } = useInborn()

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
      >
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
          <InbornUnitCardSkeleton title="MSNCU" />
        ) : (
          <InbornUnitCard
            title="MSNCU"
            description="Mother Sick Newborn Care Unit"
            unit={data.msncu}
            icon={Stethoscope}
          />
        )}
      </Section>

      <Section title="PNC" description="Post Natal Care">
        {isInitialLoading || !data ? (
          <InbornUnitCardSkeleton title="PNC" />
        ) : (
          <InbornUnitCard
            title="PNC"
            description="Post Natal Care"
            unit={data.pnc}
            icon={ShieldPlus}
          />
        )}
      </Section>
    </>
  )
}
