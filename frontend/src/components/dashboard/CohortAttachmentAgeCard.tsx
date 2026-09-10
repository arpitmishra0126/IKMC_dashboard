import { Clock, Info } from "lucide-react"

import { CohortPanel } from "@/components/dashboard/AttachmentAgeCard"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import type { AttachmentStatSplit } from "@/types/common"

interface CohortAttachmentAgeCardProps {
  inborn: AttachmentStatSplit
  outborn: AttachmentStatSplit
}

function CohortGroup({ label, attachment }: { label: string; attachment: AttachmentStatSplit }) {
  return (
    <div>
      <p className="text-muted-foreground mb-2 text-xs font-semibold uppercase tracking-wide">
        {label}
      </p>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <CohortPanel label="NVD" stat={attachment.nvd} />
        <CohortPanel label="C-Section" stat={attachment.csection} />
      </div>
    </div>
  )
}

/**
 * Full-width Attachment Age card for the Cohort Summary section, shown
 * below the side-by-side Inborn/Outborn cards rather than embedded inside
 * either one (too cramped there for 4 NVD/C-Section panels). Reuses
 * CohortPanel - the exact same NVD/C-Section panel + Min/Avg/Max
 * presentation as the Overview Attachment Age card - for both the Inborn
 * and Outborn groups, so all Attachment Age displays stay visually
 * consistent. Purely presentational: values are read as-is from the
 * existing per-cohort attachment stats, nothing is recalculated here.
 */
export function CohortAttachmentAgeCard({ inborn, outborn }: CohortAttachmentAgeCardProps) {
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
      <CardContent className="flex flex-col gap-5">
        <CohortGroup label="Inborn" attachment={inborn} />
        <CohortGroup label="Outborn" attachment={outborn} />

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

export function CohortAttachmentAgeCardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-3">
          <Skeleton className="size-9 rounded-lg" />
          <Skeleton className="h-4 w-32" />
        </div>
        <Skeleton className="mt-1 h-3 w-72" />
      </CardHeader>
      <CardContent className="flex flex-col gap-5">
        <Skeleton className="h-36 w-full" />
        <Skeleton className="h-36 w-full" />
      </CardContent>
    </Card>
  )
}
