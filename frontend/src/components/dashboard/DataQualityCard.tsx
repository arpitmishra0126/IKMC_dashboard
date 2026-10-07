import { AlertTriangle, CheckCircle2, ChevronDown } from "lucide-react"

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
  /** Whether this card's record table is currently open below the grid. */
  isOpen?: boolean
  onToggle?: () => void
}

/**
 * Severity is derived purely from whether the count is zero (see
 * lib/severity.ts) - status is always shown with an icon AND text/color
 * together, never color alone. Icon+label+count laid out as a compact
 * horizontal cluster (matching CohortTotalBanner's existing pattern). All
 * six cards sit in one equal-width grid; the record table opens below the
 * grid (see DataQualitySection), so the card itself never changes size.
 */
export function DataQualityCard({
  label,
  value,
  validationCheck,
  isOpen = false,
  onToggle,
}: DataQualityCardProps) {
  const severity = severityFromCount(value)
  const isHealthy = severity === "success"
  const Icon = isHealthy ? CheckCircle2 : AlertTriangle

  return (
    <Card
      className={cn(
        "h-full border-l-4 transition-shadow hover:shadow-md",
        isHealthy ? "border-l-success" : "border-l-warning"
      )}
    >
      <CardContent className="flex h-full flex-col justify-between gap-3 pt-5">
        <div className="flex items-center gap-3">
          <span
            className={cn(
              "shrink-0 rounded-lg p-2",
              isHealthy ? "bg-success/10 text-success" : "bg-warning/10 text-warning"
            )}
          >
            <Icon className="size-5" aria-hidden="true" />
          </span>
          <div>
            <p className="text-muted-foreground text-xs font-semibold uppercase leading-tight tracking-wide">
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

        {validationCheck && onToggle ? (
          <button
            type="button"
            onClick={onToggle}
            aria-expanded={isOpen}
            className="border-border/70 text-muted-foreground hover:text-foreground flex w-full items-center justify-between border-t pt-3 text-left text-xs font-medium"
          >
            <span>View records</span>
            <ChevronDown
              className={cn("size-4 transition-transform", isOpen && "rotate-180")}
              aria-hidden="true"
            />
          </button>
        ) : null}
      </CardContent>
    </Card>
  )
}

export function DataQualityCardSkeleton({ label }: { label: string }) {
  return (
    <Card className="h-full border-l-4 border-l-transparent">
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
