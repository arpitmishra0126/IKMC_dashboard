import { AlertTriangle, CheckCircle2 } from "lucide-react"

import { ValidationDetailPanel } from "@/components/dashboard/ValidationDetailPanel"
import { Card, CardContent } from "@/components/ui/card"
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
 * together, never color alone. Icon+label+count laid out as a compact
 * horizontal cluster (matching CohortTotalBanner's existing pattern)
 * rather than a full-width stacked header, so the card reads the same way
 * whether it's a third of the row or half of it.
 */
export function DataQualityCard({ label, value, validationCheck }: DataQualityCardProps) {
  const severity = severityFromCount(value)
  const isHealthy = severity === "success"
  const Icon = isHealthy ? CheckCircle2 : AlertTriangle

  return (
    <Card
      className={cn(
        "border-l-4 transition-shadow hover:shadow-md",
        isHealthy ? "border-l-success" : "border-l-warning"
      )}
    >
      <CardContent className="pt-5">
        <div className="flex items-center gap-3">
          <span
            className={cn(
              "rounded-lg p-2",
              isHealthy ? "bg-success/10 text-success" : "bg-warning/10 text-warning"
            )}
          >
            <Icon className="size-5" aria-hidden="true" />
          </span>
          <div>
            <p className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
              {label}
            </p>
            <div className="flex items-baseline gap-2">
              <p className="text-3xl font-bold tabular-nums tracking-tight">
                {formatNumber(value)}
              </p>
              <span className={cn("text-xs font-medium", isHealthy ? "text-success" : "text-warning")}>
                {isHealthy ? "Clear" : "Needs attention"}
              </span>
            </div>
          </div>
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
      <CardContent className="pt-5">
        <div className="flex items-center gap-3">
          <Skeleton className="size-9 rounded-lg" />
          <div className="flex flex-col gap-2">
            <p className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
              {label}
            </p>
            <Skeleton className="h-8 w-16" />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
