import type { LucideIcon } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { type CohortAccent, COHORT_ACCENT_STYLES } from "@/lib/cohortAccent"
import { formatNumber } from "@/lib/format"
import { cn } from "@/lib/utils"
import type { OutbornDeliveryUnit } from "@/types/outborn"

interface OutbornDeliveryCardProps {
  title: string
  unit: OutbornDeliveryUnit
  icon: LucideIcon
  accent: CohortAccent
}

/**
 * Reproduces one delivery-mode block of pages/3_Outborn.py (NVD or
 * C-Section): case count, SSC<2h, avg KMC, exclusive BF - each already a
 * single value per docs/API_MIGRATION_PLAN.md (unlike the Overview cohort
 * cards, there is no further NVD-vs-C-Section split within a single
 * outborn delivery-mode card). Attachment Age lives in its own full-width
 * AttachmentAgeCard below both delivery-mode sections (see
 * OutbornPage.tsx), not embedded in this card - it was too cramped here.
 */
export function OutbornDeliveryCard({ title, unit, icon: Icon, accent }: OutbornDeliveryCardProps) {
  const styles = COHORT_ACCENT_STYLES[accent]

  const metrics = [
    { label: "Case count", value: formatNumber(unit.case_count) },
    { label: "SSC < 2h", value: formatNumber(unit.ssc_under_2h) },
    { label: "Avg KMC", value: `${unit.avg_kmc} hrs/day` },
    { label: "Exclusive BF", value: formatNumber(unit.exclusive_bf) },
  ]

  return (
    <Card className={cn("gap-3 border-l-4", styles.border)}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <span className={cn("bg-muted rounded-md p-1.5", styles.icon)}>
            <Icon className="size-4" aria-hidden="true" />
          </span>
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent className="pb-4">
        <dl className="grid grid-cols-2 gap-x-3 gap-y-3 sm:grid-cols-4 sm:gap-x-4">
          {metrics.map((metric) => (
            <div key={metric.label} className="min-w-0">
              <dt className="text-muted-foreground truncate text-[11px] font-semibold uppercase tracking-wide">
                {metric.label}
              </dt>
              <dd className="text-xl font-bold tabular-nums">{metric.value}</dd>
            </div>
          ))}
        </dl>
      </CardContent>
    </Card>
  )
}

export function OutbornDeliveryCardSkeleton({ title, accent }: { title: string; accent: CohortAccent }) {
  const styles = COHORT_ACCENT_STYLES[accent]
  return (
    <Card className={cn("gap-3 border-l-4", styles.border)}>
      <CardHeader>
        <CardTitle className="text-base">{title}</CardTitle>
      </CardHeader>
      <CardContent className="pb-4">
        <div className="grid grid-cols-2 gap-x-3 gap-y-3 sm:grid-cols-4 sm:gap-x-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <Skeleton key={`outborn-metric-skeleton-${index}`} className="h-10 w-16" />
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
