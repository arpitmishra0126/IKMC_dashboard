import type { LucideIcon } from "lucide-react"

import { MetricComparisonTable } from "@/components/dashboard/MetricComparisonTable"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"
import type { AttachmentStat } from "@/types/common"
import type { InbornUnitDetail } from "@/types/inborn"

interface InbornUnitCardProps {
  title: string
  description: string
  unit: InbornUnitDetail
  icon: LucideIcon
}

function formatAttachment(stat: AttachmentStat): string {
  return `Min ${stat.min_minutes} · Avg ${stat.minutes} · Max ${stat.max_minutes} min · ${formatNumber(stat.case_count)} cases`
}

/**
 * Reproduces one MSNCU/PNC section of pages/2_Inborn.py: unit-level avg
 * iKMC + case count, then the full NVD-vs-C-Section metric set (delivery,
 * SSC<2h, avg KMC, exclusive BF, attachment, coverage %, achieved count).
 * `nvd_definition_note` (from the API - see docs/MIGRATION_DECISIONS.md #5)
 * is shown as-is rather than hidden, since exclusive_bf.nvd uses a
 * narrower NVD definition than the other rows in this same table.
 */
export function InbornUnitCard({ title, description, unit, icon: Icon }: InbornUnitCardProps) {
  const rows = [
    {
      label: "Delivery type",
      nvd: formatNumber(unit.delivery.nvd),
      csection: formatNumber(unit.delivery.csection),
    },
    {
      label: "SSC < 2h",
      nvd: formatNumber(unit.ssc_under_2h.nvd),
      csection: formatNumber(unit.ssc_under_2h.csection),
    },
    {
      label: "Avg KMC",
      nvd: `${unit.avg_kmc_by_delivery.nvd} hrs/day`,
      csection: `${unit.avg_kmc_by_delivery.csection} hrs/day`,
    },
    {
      label: "Exclusive BF",
      nvd: formatNumber(unit.exclusive_bf.nvd),
      csection: formatNumber(unit.exclusive_bf.csection),
    },
    {
      label: "Attachment age",
      nvd: formatAttachment(unit.attachment.nvd),
      csection: formatAttachment(unit.attachment.csection),
    },
    {
      label: "iKMC coverage",
      nvd: `${unit.coverage.nvd.percentage}% (${formatNumber(unit.coverage.nvd.achieved_count)}/${formatNumber(unit.delivery.nvd)})`,
      csection: `${unit.coverage.csection.percentage}% (${formatNumber(unit.coverage.csection.achieved_count)}/${formatNumber(unit.delivery.csection)})`,
    },
    {
      label: "Achieved count",
      nvd: formatNumber(unit.coverage.nvd.achieved_count),
      csection: formatNumber(unit.coverage.csection.achieved_count),
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
              {title}
            </CardTitle>
            <p className="text-muted-foreground mt-1 text-xs">{description}</p>
          </div>
          <div className="flex items-center gap-5">
            <Stat label="Avg iKMC" value={`${unit.avg_kmc} hrs/day`} />
            <Stat label="Cases" value={formatNumber(unit.total_cases)} />
          </div>
        </div>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <MetricComparisonTable rows={rows} />
        <p className="text-muted-foreground text-[11px] italic">{unit.nvd_definition_note}</p>
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

export function InbornUnitCardSkeleton({ title }: { title: string }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">{title}</CardTitle>
        <Skeleton className="h-4 w-48" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-44 w-full" />
      </CardContent>
    </Card>
  )
}
