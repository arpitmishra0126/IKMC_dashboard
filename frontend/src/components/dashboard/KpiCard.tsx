import type { LucideIcon } from "lucide-react"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"

interface KpiCardProps {
  label: string
  value: number | string
  icon?: LucideIcon
  description?: string
}

/** Reusable KPI tile - equivalent to components/kpi_cards.py::kpi_card in the Streamlit app. */
export function KpiCard({ label, value, icon: Icon, description }: KpiCardProps) {
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
        <p className="text-4xl font-bold tabular-nums tracking-tight">
          {typeof value === "number" ? formatNumber(value) : value}
        </p>
        {description ? <p className="text-muted-foreground mt-1 text-xs">{description}</p> : null}
      </CardContent>
    </Card>
  )
}

export function KpiCardSkeleton({ label }: { label: string }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
          {label}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Skeleton className="h-10 w-24" />
      </CardContent>
    </Card>
  )
}
