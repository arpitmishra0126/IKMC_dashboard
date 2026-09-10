import { Clock, Info } from "lucide-react"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"
import type { AttachmentStat, AttachmentStatSplit } from "@/types/common"

function formatDaysHoursMinutes(totalMinutes: number): string {
  const rounded = Math.round(totalMinutes)
  const days = Math.floor(rounded / 1440)
  const remainderAfterDays = rounded % 1440
  const hours = Math.floor(remainderAfterDays / 60)
  const minutes = remainderAfterDays % 60
  return `${days}d ${hours}h ${minutes}m`
}

function StatBox({ label, minutes }: { label: string; minutes: number }) {
  return (
    <div className="border-border/60 bg-card rounded-md border p-2.5 text-center">
      <p className="text-muted-foreground text-[10px] font-semibold uppercase tracking-wide">
        {label}
      </p>
      <p className="text-sm font-bold tabular-nums sm:text-base">{minutes} min</p>
      <p className="text-muted-foreground text-[10px] tabular-nums">
        {formatDaysHoursMinutes(minutes)}
      </p>
    </div>
  )
}

/**
 * One equal-width Min/Avg/Max panel for a single delivery-type group
 * (label + case count, then three stat boxes) - exported so other
 * Attachment Age displays (e.g. the Cohort Summary cards) can reuse the
 * exact same visual structure as this card without duplicating it.
 */
export function CohortPanel({ label, stat }: { label: string; stat: AttachmentStat }) {
  return (
    <div className="border-border/60 bg-muted/20 rounded-lg border p-3">
      <div className="mb-3">
        <p className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
          {label}
        </p>
        <p className="text-lg font-bold tabular-nums">{formatNumber(stat.case_count)} cases</p>
      </div>
      <div className="grid grid-cols-3 gap-2">
        <StatBox label="Min" minutes={stat.min_minutes} />
        <StatBox label="Avg" minutes={stat.minutes} />
        <StatBox label="Max" minutes={stat.max_minutes} />
      </div>
    </div>
  )
}

interface AttachmentAgeCardProps {
  attachment: AttachmentStatSplit
}

/**
 * Standalone Overview card for Attachment Age (senior feedback: moved out
 * of the Total Cases card into its own card directly below it). Two
 * equal-width cohort panels (NVD / C-Section), each with Min/Avg/Max
 * statistic boxes - minutes as the bold primary value, days+hours+minutes
 * as the smaller secondary line. Purely presentational: values are read
 * as-is from the existing attachment stat, nothing is recalculated here.
 */
export function AttachmentAgeCard({ attachment }: AttachmentAgeCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-base">
          <span className="bg-primary/10 text-primary rounded-lg p-2">
            <Clock className="size-5" aria-hidden="true" />
          </span>
          Attachment Age
        </CardTitle>
        <CardDescription>
          Time from birth to first breast milk attachment (early initiation)
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <CohortPanel label="NVD" stat={attachment.nvd} />
          <CohortPanel label="C-Section" stat={attachment.csection} />
        </div>

        <div className="bg-muted/40 flex items-start gap-2 rounded-md border p-3">
          <Info className="text-muted-foreground mt-0.5 size-3.5 shrink-0" aria-hidden="true" />
          <p className="text-muted-foreground text-xs">
            Attachment age is calculated from the earliest recorded initiation time in the Daily
            Care Tracking (DCT) form.
          </p>
        </div>
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
        <Skeleton className="mt-1 h-3 w-72" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-40 w-full" />
      </CardContent>
    </Card>
  )
}
