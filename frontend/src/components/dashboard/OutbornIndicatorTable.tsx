import type { LucideIcon } from "lucide-react"

import { MetricComparisonTable } from "@/components/dashboard/MetricComparisonTable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"
import type { OutbornResponse } from "@/types/outborn"

interface OutbornIndicatorTableProps {
  data: OutbornResponse
  icon: LucideIcon
}

/**
 * Reproduces the exact same NVD-vs-C-Section indicator table as
 * InbornUnitCard (Delivery type, SSC<2h, Avg KMC, Exclusive BF, iKMC
 * coverage, Achieved count) - same row set, same MetricComparisonTable
 * structure and formatting, same "% (achieved/denominator)" coverage
 * display - populated from GET /api/dashboard/outborn's nvd/csection
 * coverage fields. Those are backed by get_outborn_{nvd,csection}_coverage()
 * / get_outborn_{nvd,csection}_achieved_count() in services/indicators.py -
 * the exact same pre-existing coverage/achieved-count calculation pattern
 * MSNCU/PNC already use, just not previously wired into this API.
 * outborn_definition_note (already shown once above, in the page header
 * section) is not repeated here to avoid duplicating the same disclosure
 * twice in a row.
 */
export function OutbornIndicatorTable({ data, icon: Icon }: OutbornIndicatorTableProps) {
  const rows = [
    {
      label: "Delivery type",
      nvd: formatNumber(data.nvd.case_count),
      csection: formatNumber(data.csection.case_count),
    },
    {
      label: "SSC < 2h",
      nvd: formatNumber(data.nvd.ssc_under_2h),
      csection: formatNumber(data.csection.ssc_under_2h),
    },
    {
      label: "Avg KMC",
      nvd: `${data.nvd.avg_kmc} hrs/day`,
      csection: `${data.csection.avg_kmc} hrs/day`,
    },
    {
      label: "Exclusive BF",
      nvd: formatNumber(data.nvd.exclusive_bf),
      csection: formatNumber(data.csection.exclusive_bf),
    },
    {
      label: "iKMC coverage",
      nvd: `${data.nvd.coverage.percentage}% (${formatNumber(data.nvd.coverage.achieved_count)}/${formatNumber(data.nvd.case_count)})`,
      csection: `${data.csection.coverage.percentage}% (${formatNumber(data.csection.coverage.achieved_count)}/${formatNumber(data.csection.case_count)})`,
    },
    {
      label: "Achieved count",
      nvd: formatNumber(data.nvd.coverage.achieved_count),
      csection: formatNumber(data.csection.coverage.achieved_count),
    },
  ]

  return (
    <Card>
      <CardHeader>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <CardTitle className="flex items-center gap-2 text-base">
              <span className="bg-muted text-primary rounded-md p-1.5">
                <Icon className="size-4" aria-hidden="true" />
              </span>
              Outborn
            </CardTitle>
            <p className="text-muted-foreground mt-1 text-xs">Delivery-mode indicator summary</p>
          </div>
          <div className="flex items-center gap-5">
            <Stat label="Avg iKMC" value={`${data.overall_avg_kmc} hrs/day`} />
            <Stat label="Cases" value={formatNumber(data.total_cases)} />
          </div>
        </div>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <MetricComparisonTable rows={rows} />
      </CardContent>
    </Card>
  )
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-right">
      <p className="text-muted-foreground text-[11px] font-semibold uppercase tracking-wide">
        {label}
      </p>
      <p className="text-lg font-bold tabular-nums">{value}</p>
    </div>
  )
}

export function OutbornIndicatorTableSkeleton() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Outborn</CardTitle>
        <Skeleton className="h-4 w-48" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-44 w-full" />
      </CardContent>
    </Card>
  )
}
