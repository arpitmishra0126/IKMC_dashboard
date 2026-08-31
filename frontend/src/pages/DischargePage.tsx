import { ArrowRightLeft, BedDouble, HeartCrack, LogOut, UserX } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { DischargeOutcomeCard, DischargeOutcomeCardSkeleton } from "@/components/dashboard/DischargeOutcomeCard"
import { KpiCard, KpiCardSkeleton } from "@/components/dashboard/KpiCard"
import { Section } from "@/components/layout/Section"
import { useDischarge } from "@/hooks/useDischarge"

const SUMMARY_LABELS = ["DISCHARGED", "REFERRED", "LAMA", "DEATH", "STILL ADMITTED"] as const

/**
 * Reproduces pages/6_Discharge.py via GET /api/dashboard/discharge:
 * overall outcome summary, then Inborn and Outborn each broken down by
 * NVD/C-Section - a clearer outcome comparison than duplicating the
 * Overview KPI cards.
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
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3 lg:grid-cols-5">
          {isInitialLoading || !data ? (
            SUMMARY_LABELS.map((label) => <KpiCardSkeleton key={label} label={label} />)
          ) : (
            <>
              <KpiCard label="DISCHARGED" value={data.summary.discharged} icon={LogOut} />
              <KpiCard label="REFERRED" value={data.summary.referred} icon={ArrowRightLeft} />
              <KpiCard label="LAMA" value={data.summary.lama} icon={UserX} />
              <KpiCard label="DEATH" value={data.summary.death} icon={HeartCrack} />
              <KpiCard label="STILL ADMITTED" value={data.summary.still_admitted} icon={BedDouble} />
            </>
          )}
        </div>
      </Section>

      <Section title="Inborn Outcomes">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {isInitialLoading || !data ? (
            <>
              <DischargeOutcomeCardSkeleton title="NVD" accent="inborn" />
              <DischargeOutcomeCardSkeleton title="C-Section" accent="inborn" />
            </>
          ) : (
            <>
              <DischargeOutcomeCard title="NVD" outcome={data.inborn.nvd} accent="inborn" />
              <DischargeOutcomeCard title="C-Section" outcome={data.inborn.csection} accent="inborn" />
            </>
          )}
        </div>
      </Section>

      <Section title="Outborn Outcomes">
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {isInitialLoading || !data ? (
            <>
              <DischargeOutcomeCardSkeleton title="NVD" accent="outborn" />
              <DischargeOutcomeCardSkeleton title="C-Section" accent="outborn" />
            </>
          ) : (
            <>
              <DischargeOutcomeCard title="NVD" outcome={data.outborn.nvd} accent="outborn" />
              <DischargeOutcomeCard title="C-Section" outcome={data.outborn.csection} accent="outborn" />
            </>
          )}
        </div>
      </Section>
    </>
  )
}
