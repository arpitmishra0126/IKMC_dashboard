import { ArrowRightLeft, HeartCrack, LogOut, UserX } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { type CohortAccent, COHORT_ACCENT_STYLES } from "@/lib/cohortAccent"
import { formatNumber } from "@/lib/format"
import { cn } from "@/lib/utils"
import type { DischargeOutcome } from "@/types/common"

interface DischargeOutcomeCardProps {
  title: string
  outcome: DischargeOutcome
  accent: CohortAccent
}

const OUTCOME_META = [
  { key: "discharged", label: "Discharged", icon: LogOut },
  { key: "referred", label: "Referred", icon: ArrowRightLeft },
  { key: "lama", label: "LAMA", icon: UserX },
  { key: "death", label: "Death", icon: HeartCrack },
] as const

/**
 * Reproduces one NVD/C-Section outcome block of pages/6_Discharge.py
 * (discharged / referred / LAMA / death), reused for both Inborn and
 * Outborn sections.
 */
export function DischargeOutcomeCard({ title, outcome, accent }: DischargeOutcomeCardProps) {
  const styles = COHORT_ACCENT_STYLES[accent]

  return (
    <Card className={cn("border-l-4", styles.border)}>
      <CardHeader>
        <CardTitle className="text-base">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <dl className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {OUTCOME_META.map(({ key, label, icon: Icon }) => (
            <div key={key} className="flex flex-col gap-1">
              <dt className="text-muted-foreground flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wide">
                <Icon className="size-3.5" aria-hidden="true" />
                {label}
              </dt>
              <dd className="text-xl font-bold tabular-nums">{formatNumber(outcome[key])}</dd>
            </div>
          ))}
        </dl>
      </CardContent>
    </Card>
  )
}

export function DischargeOutcomeCardSkeleton({ title, accent }: { title: string; accent: CohortAccent }) {
  const styles = COHORT_ACCENT_STYLES[accent]
  return (
    <Card className={cn("border-l-4", styles.border)}>
      <CardHeader>
        <CardTitle className="text-base">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <Skeleton key={`discharge-outcome-skeleton-${index}`} className="h-10 w-14" />
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
