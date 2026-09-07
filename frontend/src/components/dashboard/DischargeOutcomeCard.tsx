import type { LucideIcon } from "lucide-react"

import { MetricComparisonTable } from "@/components/dashboard/MetricComparisonTable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { type CohortAccent, COHORT_ACCENT_STYLES } from "@/lib/cohortAccent"
import { formatNumber } from "@/lib/format"
import { cn } from "@/lib/utils"
import type { DischargeBreakdown } from "@/types/common"

interface DischargeOutcomeCardProps {
  title: string
  breakdown: DischargeBreakdown
  accent: CohortAccent
  icon: LucideIcon
}

/**
 * One cohort's discharge outcomes (Inborn or Outborn) as a single card,
 * with NVD vs C-Section shown as directly comparable table rows - reuses
 * the same MetricComparisonTable and cohort accent styling as the
 * Overview's CohortSummaryCard, so this page shares its visual system
 * instead of inventing a parallel one.
 */
export function DischargeOutcomeCard({ title, breakdown, accent, icon: Icon }: DischargeOutcomeCardProps) {
  const styles = COHORT_ACCENT_STYLES[accent]

  const rows = [
    {
      label: "Discharged",
      nvd: formatNumber(breakdown.nvd.discharged),
      csection: formatNumber(breakdown.csection.discharged),
    },
    {
      label: "Referred",
      nvd: formatNumber(breakdown.nvd.referred),
      csection: formatNumber(breakdown.csection.referred),
    },
    {
      label: "LAMA",
      nvd: formatNumber(breakdown.nvd.lama),
      csection: formatNumber(breakdown.csection.lama),
    },
    {
      label: "Death",
      nvd: formatNumber(breakdown.nvd.death),
      csection: formatNumber(breakdown.csection.death),
    },
  ]

  return (
    <Card className={cn("border-l-4", styles.border)}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <span className={cn("bg-muted rounded-md p-1.5", styles.icon)}>
            <Icon className="size-4" aria-hidden="true" />
          </span>
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <MetricComparisonTable rows={rows} />
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
        <Skeleton className="h-40 w-full" />
      </CardContent>
    </Card>
  )
}
