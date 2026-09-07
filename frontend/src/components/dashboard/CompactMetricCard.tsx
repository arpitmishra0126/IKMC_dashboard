import type { LucideIcon } from "lucide-react"

import { Card } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"

interface CompactMetricCardProps {
  label: string
  value: number
  icon: LucideIcon
}

/**
 * Smaller/secondary metric tile, visually distinct from the primary
 * KpiCard row above it (smaller value, tighter padding, inline icon)
 * rather than a second row of oversized KPI cards. Used for the Discharge
 * Outcomes row on the Overview page only.
 */
export function CompactMetricCard({ label, value, icon: Icon }: CompactMetricCardProps) {
  return (
    <Card className="flex flex-row items-center gap-3 px-4 py-3">
      <span className="bg-primary/10 text-primary rounded-md p-1.5">
        <Icon className="size-4" aria-hidden="true" />
      </span>
      <div>
        <p className="text-muted-foreground text-[11px] font-semibold uppercase tracking-wide">
          {label}
        </p>
        <p className="text-xl font-bold tabular-nums">{formatNumber(value)}</p>
      </div>
    </Card>
  )
}

export function CompactMetricCardSkeleton({ label }: { label: string }) {
  return (
    <Card className="flex flex-row items-center gap-3 px-4 py-3">
      <span className="bg-muted rounded-md p-1.5">
        <Skeleton className="size-4" />
      </span>
      <div className="flex flex-col gap-1.5">
        <span className="text-muted-foreground text-[11px] font-semibold uppercase tracking-wide">
          {label}
        </span>
        <Skeleton className="h-6 w-12" />
      </div>
    </Card>
  )
}
