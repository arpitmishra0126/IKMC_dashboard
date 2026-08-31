import { AlertTriangle, CheckCircle2 } from "lucide-react"

import { Card, CardContent } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { severityFromStatusText } from "@/lib/severity"
import { cn } from "@/lib/utils"

interface ValidationStatusBannerProps {
  /** Raw string from get_validation_status(), rendered verbatim. */
  status: string
}

/**
 * Prominent, full-width rendering of get_validation_status(). The status
 * TEXT is never altered - only its visual treatment (icon + color) is
 * derived from its existing content. Per docs/MIGRATION_DECISIONS.md #7,
 * this status does not itself factor in missing/duplicate Baby ID counts,
 * even though those are shown as separate cards alongside it.
 */
export function ValidationStatusBanner({ status }: ValidationStatusBannerProps) {
  const severity = severityFromStatusText(status)
  const isHealthy = severity === "success"

  return (
    <Card
      className={cn(
        "border-l-4",
        isHealthy ? "border-l-success bg-success/5" : "border-l-warning bg-warning/5"
      )}
    >
      <CardContent className="flex items-center gap-3 py-5">
        {isHealthy ? (
          <CheckCircle2 className="text-success size-6 shrink-0" aria-hidden="true" />
        ) : (
          <AlertTriangle className="text-warning size-6 shrink-0" aria-hidden="true" />
        )}
        <div>
          <p className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
            Overall Validation Status
          </p>
          <p className="text-xl font-bold">{status}</p>
        </div>
      </CardContent>
    </Card>
  )
}

export function ValidationStatusBannerSkeleton() {
  return (
    <Card className="border-l-4 border-l-transparent">
      <CardContent className="flex items-center gap-3 py-5">
        <Skeleton className="size-6 rounded-full" />
        <div className="flex flex-col gap-2">
          <Skeleton className="h-3 w-40" />
          <Skeleton className="h-5 w-32" />
        </div>
      </CardContent>
    </Card>
  )
}
