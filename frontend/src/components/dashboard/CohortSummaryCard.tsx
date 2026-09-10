import type { LucideIcon } from "lucide-react"

import { MetricComparisonTable } from "@/components/dashboard/MetricComparisonTable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { type CohortAccent, COHORT_ACCENT_STYLES } from "@/lib/cohortAccent"
import { formatNumber } from "@/lib/format"
import { cn } from "@/lib/utils"
import type { CohortCard } from "@/types/cohorts"

interface CohortSummaryCardProps {
  title: string
  cohort: CohortCard
  accent: CohortAccent
  icon: LucideIcon
}

const METRIC_ROWS: Array<{
  label: string
  read: (cohort: CohortCard) => { nvd: string; csection: string }
}> = [
  {
    label: "Delivery type",
    read: (c) => ({ nvd: formatNumber(c.delivery.nvd), csection: formatNumber(c.delivery.csection) }),
  },
  {
    label: "SSC < 2h",
    read: (c) => ({
      nvd: formatNumber(c.ssc_under_2h.nvd),
      csection: formatNumber(c.ssc_under_2h.csection),
    }),
  },
  {
    label: "Avg KMC",
    read: (c) => ({ nvd: `${c.avg_kmc.nvd} hrs/day`, csection: `${c.avg_kmc.csection} hrs/day` }),
  },
  {
    label: "Exclusive BF",
    read: (c) => ({
      nvd: formatNumber(c.exclusive_bf.nvd),
      csection: formatNumber(c.exclusive_bf.csection),
    }),
  },
]

/**
 * Reproduces components/cohort_summary.py as an NVD vs. C-Section
 * comparison table (total cases + delivery/SSC/KMC/BF rows). Attachment
 * Age lives in its own full-width CohortAttachmentAgeCard below the two
 * Inborn/Outborn cards, not embedded here - it was too cramped alongside
 * this table.
 */
export function CohortSummaryCard({ title, cohort, accent, icon: Icon }: CohortSummaryCardProps) {
  const styles = COHORT_ACCENT_STYLES[accent]

  return (
    <Card className={cn("border-l-4", styles.border)}>
      <CardHeader>
        <div className="flex items-center justify-between gap-3">
          <CardTitle className="flex items-center gap-2 text-base">
            <span className={cn("bg-muted rounded-md p-1.5", styles.icon)}>
              <Icon className="size-4" aria-hidden="true" />
            </span>
            {title}
          </CardTitle>
        </div>
        <p className="text-4xl font-bold tabular-nums tracking-tight">
          {formatNumber(cohort.total_cases)}
        </p>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <MetricComparisonTable rows={METRIC_ROWS.map((row) => ({ label: row.label, ...row.read(cohort) }))} />
      </CardContent>
    </Card>
  )
}

export function CohortSummaryCardSkeleton({ title, accent }: { title: string; accent: CohortAccent }) {
  const styles = COHORT_ACCENT_STYLES[accent]
  return (
    <Card className={cn("border-l-4", styles.border)}>
      <CardHeader>
        <CardTitle className="text-base">{title}</CardTitle>
        <Skeleton className="h-10 w-20" />
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <Skeleton className="h-32 w-full" />
        <Skeleton className="h-16 w-full" />
      </CardContent>
    </Card>
  )
}
