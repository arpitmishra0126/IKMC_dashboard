import { Users } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { COHORT_ACCENT_STYLES } from "@/lib/cohortAccent"
import { formatNumber } from "@/lib/format"

interface CohortTotalBannerProps {
  inbornTotal: number
  outbornTotal: number
}

/**
 * Compact horizontal summary sitting directly above the Inborn/Outborn
 * cohort cards: total_cases = inborn.total_cases + outborn.total_cases,
 * computed here purely for display (both numbers already come from the
 * same GET /api/dashboard/cohorts response powering the two cards below -
 * no new calculation is introduced, no backend change needed).
 *
 * Deliberately left without a cohort-colored left border (unlike the two
 * cards below it) since it represents both cohorts combined, not one -
 * the Inborn/Outborn badges carry the same accent colors as the cards
 * below instead, tying the three together without misattributing color.
 */
export function CohortTotalBanner({ inbornTotal, outbornTotal }: CohortTotalBannerProps) {
  const total = inbornTotal + outbornTotal

  return (
    <Card className="flex flex-col gap-3 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-3">
        <span className="bg-primary/10 text-primary rounded-lg p-2">
          <Users className="size-5" aria-hidden="true" />
        </span>
        <div>
          <p className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
            Total Cases
          </p>
          <p className="text-3xl font-bold tabular-nums tracking-tight">{formatNumber(total)}</p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <Badge variant="outline" className={COHORT_ACCENT_STYLES.inborn.badge}>
          {formatNumber(inbornTotal)} Inborn
        </Badge>
        <span className="text-muted-foreground text-sm">+</span>
        <Badge variant="outline" className={COHORT_ACCENT_STYLES.outborn.badge}>
          {formatNumber(outbornTotal)} Outborn
        </Badge>
      </div>
    </Card>
  )
}

export function CohortTotalBannerSkeleton() {
  return (
    <Card className="flex flex-col gap-3 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-3">
        <span className="bg-muted rounded-lg p-2">
          <Users className="text-muted-foreground size-5" aria-hidden="true" />
        </span>
        <div className="flex flex-col gap-2">
          <Skeleton className="h-3 w-20" />
          <Skeleton className="h-8 w-16" />
        </div>
      </div>
      <Skeleton className="h-6 w-40" />
    </Card>
  )
}
