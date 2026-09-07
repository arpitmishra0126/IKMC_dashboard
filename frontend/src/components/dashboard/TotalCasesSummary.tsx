import { Users } from "lucide-react"

import { MetricComparisonTable } from "@/components/dashboard/MetricComparisonTable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"
import type { AttachmentStat } from "@/types/common"
import type { TotalCasesSummary as TotalCasesSummaryData } from "@/types/overview"

interface TotalCasesSummaryProps {
  summary: TotalCasesSummaryData
}

function formatAttachment(stat: AttachmentStat): string {
  return `Min ${stat.min_minutes} · Avg ${stat.minutes} · Max ${stat.max_minutes} min · ${formatNumber(stat.case_count)} cases`
}

/**
 * Period-aware "Total Cases" summary (senior feedback): total unique
 * babies across Inborn + Outborn, plus Delivery Type / SSC<2h / Avg KMC /
 * Exclusive BF / Attachment age as one cohesive card - not five/seven
 * separate KPI cards. Same visual pattern as the Overview Cohort Summary's
 * CohortSummaryCard (icon + big total, then an NVD-vs-C-Section table),
 * reusing the same MetricComparisonTable component. Only the computed
 * attachment-age value is shown here (no hardcoded-display string - that
 * distinction only exists for the separate Cohort Summary cards).
 */
export function TotalCasesSummary({ summary }: TotalCasesSummaryProps) {
  const rows = [
    {
      label: "Delivery type",
      nvd: formatNumber(summary.delivery.nvd),
      csection: formatNumber(summary.delivery.csection),
    },
    {
      label: "SSC < 2h",
      nvd: formatNumber(summary.ssc_under_2h.nvd),
      csection: formatNumber(summary.ssc_under_2h.csection),
    },
    {
      label: "Avg KMC",
      nvd: `${summary.avg_kmc.nvd} hrs/day`,
      csection: `${summary.avg_kmc.csection} hrs/day`,
    },
    {
      label: "Exclusive BF",
      nvd: formatNumber(summary.exclusive_bf.nvd),
      csection: formatNumber(summary.exclusive_bf.csection),
    },
    {
      label: "Attachment age",
      nvd: formatAttachment(summary.attachment.nvd),
      csection: formatAttachment(summary.attachment.csection),
    },
  ]

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-3">
          <span className="bg-primary/10 text-primary rounded-lg p-2">
            <Users className="size-5" aria-hidden="true" />
          </span>
          <div>
            <CardTitle className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
              Total Cases
            </CardTitle>
            <p className="text-3xl font-bold tabular-nums tracking-tight">
              {formatNumber(summary.total_cases)}
            </p>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <MetricComparisonTable rows={rows} />
      </CardContent>
    </Card>
  )
}

export function TotalCasesSummarySkeleton() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-3">
          <Skeleton className="size-9 rounded-lg" />
          <div className="flex flex-col gap-2">
            <Skeleton className="h-3 w-20" />
            <Skeleton className="h-8 w-16" />
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Skeleton className="h-40 w-full" />
      </CardContent>
    </Card>
  )
}
