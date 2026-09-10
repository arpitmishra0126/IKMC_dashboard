import { Clock } from "lucide-react"

import { MetricComparisonTable } from "@/components/dashboard/MetricComparisonTable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"
import type { AttachmentStatSplit } from "@/types/common"

function formatHoursMinutes(totalMinutes: number): string {
  const rounded = Math.round(totalMinutes)
  const hours = Math.floor(rounded / 60)
  const minutes = rounded % 60
  return `${hours}h ${minutes}m`
}

function MinutesCell({ minutes }: { minutes: number }) {
  return (
    <div>
      <p className="text-sm font-bold tabular-nums">{minutes} min</p>
      <p className="text-muted-foreground text-[11px] tabular-nums">{formatHoursMinutes(minutes)}</p>
    </div>
  )
}

interface AttachmentAgeCardProps {
  attachment: AttachmentStatSplit
}

/**
 * Standalone Overview card for Attachment Age (senior feedback: moved out
 * of the Total Cases card into its own card directly below it). NVD vs.
 * C-Section comparison table (Cases / Min / Avg / Max rows) reusing the
 * same MetricComparisonTable component as every other comparison card -
 * values are read as-is from the existing attachment stat, nothing is
 * recalculated here.
 */
export function AttachmentAgeCard({ attachment }: AttachmentAgeCardProps) {
  const rows = [
    {
      label: "Cases",
      nvd: formatNumber(attachment.nvd.case_count),
      csection: formatNumber(attachment.csection.case_count),
    },
    {
      label: "Min",
      nvd: <MinutesCell minutes={attachment.nvd.min_minutes} />,
      csection: <MinutesCell minutes={attachment.csection.min_minutes} />,
    },
    {
      label: "Avg",
      nvd: <MinutesCell minutes={attachment.nvd.minutes} />,
      csection: <MinutesCell minutes={attachment.csection.minutes} />,
    },
    {
      label: "Max",
      nvd: <MinutesCell minutes={attachment.nvd.max_minutes} />,
      csection: <MinutesCell minutes={attachment.csection.max_minutes} />,
    },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <span className="bg-primary/10 text-primary rounded-lg p-2">
            <Clock className="size-5" aria-hidden="true" />
          </span>
          Attachment Age
        </CardTitle>
      </CardHeader>
      <CardContent>
        <MetricComparisonTable rows={rows} rightColumnLabel="C-Section" />
      </CardContent>
    </Card>
  )
}

export function AttachmentAgeCardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-3">
          <Skeleton className="size-9 rounded-lg" />
          <Skeleton className="h-4 w-32" />
        </div>
      </CardHeader>
      <CardContent>
        <Skeleton className="h-40 w-full" />
      </CardContent>
    </Card>
  )
}
