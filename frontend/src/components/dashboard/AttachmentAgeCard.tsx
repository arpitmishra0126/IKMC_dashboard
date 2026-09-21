import { Clock, Info } from "lucide-react"
import { useState } from "react"

import {
  AttachmentCaseDrawer,
  type AttachmentDrawerRequest,
} from "@/components/dashboard/AttachmentCaseDrawer"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"
import type { AttachmentScope, AttachmentScopePrefix } from "@/types/attachmentCases"
import type { AttachmentStat, AttachmentStatSplit } from "@/types/common"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

function formatDaysHoursMinutes(totalMinutes: number): string {
  const rounded = Math.round(totalMinutes)
  const days = Math.floor(rounded / 1440)
  const remainderAfterDays = rounded % 1440
  const hours = Math.floor(remainderAfterDays / 60)
  const minutes = remainderAfterDays % 60
  return `${days}d ${hours}h ${minutes}m`
}

function StatBox({
  label,
  minutes,
  onClick,
}: {
  label: string
  minutes: number
  onClick: () => void
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="border-border/60 bg-card hover:border-primary/50 hover:bg-muted/40 focus-visible:ring-ring rounded-md border p-2.5 text-center outline-none transition-colors focus-visible:ring-2"
    >
      <p className="text-muted-foreground text-[10px] font-semibold uppercase tracking-wide">
        {label}
      </p>
      <p className="text-sm font-bold tabular-nums sm:text-base">{minutes} min</p>
      <p className="text-muted-foreground text-[10px] tabular-nums">
        {formatDaysHoursMinutes(minutes)}
      </p>
    </button>
  )
}

interface CohortPanelProps {
  label: string
  stat: AttachmentStat
  /** Identifies which cohort/delivery-type population this panel's data
   * comes from, e.g. "msncu_nvd" - combined with `label` to build the
   * audit popover's scope and context text. Omit to render the panel
   * read-only (no click handlers) - used only by places that intentionally
   * don't have a scope to audit against. */
  scope?: AttachmentScope
  /** Prefix shown before `label` in the popover's context line, e.g.
   * "Inborn" -> "Inborn → NVD". */
  contextLabel?: string
  /** True when this scope's average is a mean of contributing groups' own
   * averages (Inborn/Overview combined scopes), not a plain mean of the
   * individual cases - see AttachmentCaseDrawer's avg note. */
  avgIsCombined?: boolean
  period?: OverviewPeriod
  customRange?: OverviewDateRange
}

/**
 * One equal-width Min/Avg/Max panel for a single delivery-type group
 * (label + case count, then three stat boxes) - exported so other
 * Attachment Age displays (e.g. the Cohort Summary cards) can reuse the
 * exact same visual structure as this card without duplicating it. The
 * case count and each stat box are clickable (when `scope` is given),
 * opening the read-only case-audit popover - this never recalculates or
 * changes any displayed value, it only shows which underlying cases
 * produced it.
 */
export function CohortPanel({
  label,
  stat,
  scope,
  contextLabel,
  avgIsCombined,
  period,
  customRange,
}: CohortPanelProps) {
  const [drawerRequest, setDrawerRequest] = useState<AttachmentDrawerRequest | null>(null)

  const fullContext = contextLabel ? `${contextLabel} → ${label}` : label

  function open(mode: AttachmentDrawerRequest["mode"]) {
    if (!scope) return
    setDrawerRequest({
      scope,
      mode,
      contextLabel: fullContext,
      targetValue: mode === "min" ? stat.min_minutes : mode === "max" ? stat.max_minutes : undefined,
      avgValue: mode === "avg" ? stat.minutes : undefined,
      avgIsCombined,
      period,
      customRange,
    })
  }

  return (
    <div className="border-border/60 bg-muted/20 rounded-lg border p-3">
      <div className="mb-3">
        <p className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
          {label}
        </p>
        {scope ? (
          <button
            type="button"
            onClick={() => open("all")}
            className="hover:text-primary focus-visible:ring-ring rounded text-lg font-bold tabular-nums outline-none focus-visible:ring-2"
          >
            {formatNumber(stat.case_count)} cases
          </button>
        ) : (
          <p className="text-lg font-bold tabular-nums">{formatNumber(stat.case_count)} cases</p>
        )}
      </div>
      <div className="grid grid-cols-3 gap-2">
        <StatBox label="Min" minutes={stat.min_minutes} onClick={() => open("min")} />
        <StatBox label="Avg" minutes={stat.minutes} onClick={() => open("avg")} />
        <StatBox label="Max" minutes={stat.max_minutes} onClick={() => open("max")} />
      </div>

      {drawerRequest ? (
        <AttachmentCaseDrawer request={drawerRequest} onClose={() => setDrawerRequest(null)} />
      ) : null}
    </div>
  )
}

interface AttachmentAgeCardProps {
  attachment: AttachmentStatSplit
  /** Combined with "_nvd"/"_csection" to build each panel's audit scope,
   * e.g. "msncu" -> "msncu_nvd"/"msncu_csection". */
  scopePrefix: AttachmentScopePrefix
  /** Shown in the popover's context line, e.g. "MSNCU (Inborn)". */
  contextLabel: string
  avgIsCombined?: boolean
  period?: OverviewPeriod
  customRange?: OverviewDateRange
}

/**
 * Standalone Overview card for Attachment Age (senior feedback: moved out
 * of the Total Cases card into its own card directly below it). Two
 * equal-width cohort panels (NVD / C-Section), each with Min/Avg/Max
 * statistic boxes - minutes as the bold primary value, days+hours+minutes
 * as the smaller secondary line. Purely presentational: values are read
 * as-is from the existing attachment stat, nothing is recalculated here.
 * Reused as-is by the Inborn and Outborn pages so every Attachment Age
 * card in the app is visually identical.
 */
export function AttachmentAgeCard({
  attachment,
  scopePrefix,
  contextLabel,
  avgIsCombined,
  period,
  customRange,
}: AttachmentAgeCardProps) {
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
          <CohortPanel
            label="NVD"
            stat={attachment.nvd}
            scope={`${scopePrefix}_nvd` as AttachmentScope}
            contextLabel={contextLabel}
            avgIsCombined={avgIsCombined}
            period={period}
            customRange={customRange}
          />
          <CohortPanel
            label="C-Section"
            stat={attachment.csection}
            scope={`${scopePrefix}_csection` as AttachmentScope}
            contextLabel={contextLabel}
            avgIsCombined={avgIsCombined}
            period={period}
            customRange={customRange}
          />
        </div>

        <div className="bg-muted/40 flex items-start gap-2 rounded-md border p-3">
          <Info className="text-muted-foreground mt-0.5 size-3.5 shrink-0" aria-hidden="true" />
          <p className="text-muted-foreground text-xs">
            Attachment age is calculated from the earliest recorded initiation time in the Daily
            Care Tracking (DCT) form. Click a Min/Avg/Max box or the case count to see the
            underlying cases.
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
