import { AlertTriangle, CheckCircle2 } from "lucide-react"

import { ValidationDetailPanel } from "@/components/dashboard/ValidationDetailPanel"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"
import { cn } from "@/lib/utils"
import { severityFromCount } from "@/lib/severity"

interface DataQualityCardProps {
  label: string
  value: number
  /** URL path segment for GET /api/validation/{check}, when a record-level
   * detail table exists for this metric. Omit to render a plain count. */
  validationCheck?: string
}

/**
 * Severity is derived purely from whether the count is zero (see
 * lib/severity.ts) - status is always shown with an icon AND text/color
 * together, never color alone.
 */
export function DataQualityCard({ label, value, validationCheck }: DataQualityCardProps) {
  const severity = severityFromCount(value)
  const isHealthy = severity === "success"

  return (
    <Card
      className={cn(
        "border-l-4 transition-shadow hover:shadow-md",
        isHealthy ? "border-l-success" : "border-l-warning"
      )}
    >
      <CardHeader>
        <CardTitle className="text-muted-foreground flex items-center justify-between gap-2 text-xs font-semibold uppercase tracking-wide">
          <span>{label}</span>
          {isHealthy ? (
            <CheckCircle2 className="text-success size-4 shrink-0" aria-hidden="true" />
          ) : (
            <AlertTriangle className="text-warning size-4 shrink-0" aria-hidden="true" />
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-baseline gap-2">
          <p className="text-3xl font-bold tabular-nums">{formatNumber(value)}</p>
          <span className={cn("text-xs font-medium", isHealthy ? "text-success" : "text-warning")}>
            {isHealthy ? "Clear" : "Needs attention"}
          </span>
        </div>

        {validationCheck ? (
          <ValidationDetailPanel check={validationCheck} triggerLabel="View records" />
        ) : null}
      </CardContent>
    </Card>
  )
}

export function DataQualityCardSkeleton({ label }: { label: string }) {
  return (
    <Card className="border-l-4 border-l-transparent">
      <CardHeader>
        <CardTitle className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
          {label}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Skeleton className="h-9 w-20" />
      </CardContent>
    </Card>
  )
}
