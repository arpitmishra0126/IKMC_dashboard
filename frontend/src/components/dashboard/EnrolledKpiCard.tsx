import type { LucideIcon } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"

interface EnrolledBreakdownItem {
  label: string
  value: number
}

interface EnrolledKpiCardProps {
  label: string
  value: number
  description: string
  icon?: LucideIcon
  breakdown: EnrolledBreakdownItem[]
}

/**
 * Same visual language as KpiCard (Card/CardHeader/CardContent, same
 * label/value/description styling), plus a compact secondary breakdown
 * row beneath the main value - one card, not two, per the ICMR source
 * structure where ENROLLED (the Consented population) is the parent of
 * the M-SNCU-requiring / Stable PT/LBW split. The breakdown row adds only
 * one small line of height, so the card stays compact.
 */
export function EnrolledKpiCard({ label, value, description, icon: Icon, breakdown }: EnrolledKpiCardProps) {
  return (
    <Card className="group transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md">
      <CardHeader>
        <CardTitle className="text-muted-foreground flex items-center justify-between gap-2 text-xs font-semibold uppercase tracking-wide">
          <span>{label}</span>
          {Icon ? (
            <Icon
              className="text-primary/70 group-hover:text-primary size-4 shrink-0 transition-colors"
              aria-hidden="true"
            />
          ) : null}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-4xl font-bold tabular-nums tracking-tight">{formatNumber(value)}</p>
        <p className="text-muted-foreground mt-1 text-xs">{description}</p>

        <div className="border-border/70 mt-3 grid grid-cols-2 gap-3 border-t pt-2.5">
          {breakdown.map((item) => (
            <div key={item.label}>
              <p className="text-base font-bold tabular-nums">{formatNumber(item.value)}</p>
              <p className="text-muted-foreground text-[10.5px] leading-tight">{item.label}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

export function EnrolledKpiCardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
          ENROLLED
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Skeleton className="h-10 w-24" />
        <div className="mt-3 grid grid-cols-2 gap-3">
          <Skeleton className="h-8 w-full" />
          <Skeleton className="h-8 w-full" />
        </div>
      </CardContent>
    </Card>
  )
}
