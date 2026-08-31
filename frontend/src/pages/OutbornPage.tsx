import { Ambulance, Scissors, TrendingUp } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { KpiCard, KpiCardSkeleton } from "@/components/dashboard/KpiCard"
import { OutbornDeliveryCard, OutbornDeliveryCardSkeleton } from "@/components/dashboard/OutbornDeliveryCard"
import { Section } from "@/components/layout/Section"
import { useOutborn } from "@/hooks/useOutborn"

/**
 * Reproduces pages/3_Outborn.py via GET /api/dashboard/outborn: overall
 * totals/avg KMC, then NVD and C-Section each as their own card.
 */
export function OutbornPage() {
  const { data, error, isInitialLoading, refetch } = useOutborn()

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
      >
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
    </>
  )
}
