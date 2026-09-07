import { ArrowRightLeft, BedDouble, HeartCrack, LogOut, type LucideIcon, UserX } from "lucide-react"

import { Card } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { formatNumber } from "@/lib/format"
import { cn } from "@/lib/utils"
import type { DischargeSummary } from "@/types/discharge"

interface Segment {
  key: keyof DischargeSummary
  label: string
  icon: LucideIcon
  bar: string
  text: string
}

/**
 * Color choices reuse existing semantic tokens only (no new colors
 * introduced): primary for the expected/positive outcome, warning/
 * destructive matching their established meaning from the Data Quality
 * section (LAMA is a compliance concern; death is the most severe
 * outcome), and neutral muted tones for the two non-outcome states
 * (referred elsewhere, still in care). Teal is deliberately avoided here
 * since it already means "Outborn" elsewhere on this page.
 */
const SEGMENTS: Segment[] = [
  { key: "discharged", label: "Discharged", icon: LogOut, bar: "bg-primary", text: "text-primary" },
  {
    key: "referred",
    label: "Referred",
    icon: ArrowRightLeft,
    bar: "bg-muted-foreground/45",
    text: "text-muted-foreground",
  },
  { key: "lama", label: "LAMA", icon: UserX, bar: "bg-warning", text: "text-warning" },
  { key: "death", label: "Death", icon: HeartCrack, bar: "bg-destructive", text: "text-destructive" },
  {
    key: "still_admitted",
    label: "Still Admitted",
    icon: BedDouble,
    bar: "bg-primary/30",
    text: "text-muted-foreground",
  },
]

interface DischargeOutcomeSummaryProps {
  summary: DischargeSummary
}

/**
 * Single coherent outcome summary replacing 5 separate KPI cards:
 * a header total, a proportional distribution bar, and a divided (not
 * boxed) breakdown row - so the discharge/referral/LAMA/death/still-
 * admitted distribution reads as one picture rather than five unrelated
 * numbers. All five values are the same services.indicators-derived
 * counts already served by GET /api/dashboard/discharge; the total shown
 * is a client-side sum of them for display only (same precedent as
 * CohortTotalBanner), not a new backend calculation.
 */
export function DischargeOutcomeSummary({ summary }: DischargeOutcomeSummaryProps) {
  const total =
    summary.discharged + summary.referred + summary.lama + summary.death + summary.still_admitted

  return (
    <Card className="flex flex-col gap-4 px-5 py-5">
      <div>
        <p className="text-muted-foreground text-xs font-semibold uppercase tracking-wide">
          Outcome Summary
        </p>
        <p className="mt-1 text-3xl font-bold tabular-nums tracking-tight">
          {formatNumber(total)}{" "}
          <span className="text-muted-foreground text-sm font-medium">babies tracked</span>
        </p>
      </div>

      <div
        className="bg-muted flex h-2.5 w-full overflow-hidden rounded-full"
        role="img"
        aria-label={SEGMENTS.map((s) => `${s.label}: ${formatNumber(summary[s.key])}`).join(", ")}
      >
        {total > 0
          ? SEGMENTS.map((segment) => {
              const value = summary[segment.key]
              if (value <= 0) return null
              return (
                <div
                  key={segment.key}
                  className={segment.bar}
                  style={{ width: `${(value / total) * 100}%` }}
                />
              )
            })
          : null}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-5">
        {SEGMENTS.map((segment) => (
          <div
            key={segment.key}
            className="border-border/60 flex flex-col gap-1 border-t px-3 py-3 first:pl-0 sm:border-t-0 sm:border-l sm:first:border-l-0 sm:first:pl-0"
          >
            <span
              className={cn(
                "flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wide",
                segment.text
              )}
            >
              <segment.icon className="size-3.5 shrink-0" aria-hidden="true" />
              {segment.label}
            </span>
            <span className="text-2xl font-bold tabular-nums">
              {formatNumber(summary[segment.key])}
            </span>
          </div>
        ))}
      </div>
    </Card>
  )
}

export function DischargeOutcomeSummarySkeleton() {
  return (
    <Card className="flex flex-col gap-4 px-5 py-5">
      <div className="flex flex-col gap-2">
        <Skeleton className="h-3 w-28" />
        <Skeleton className="h-8 w-32" />
      </div>
      <Skeleton className="h-2.5 w-full rounded-full" />
      <div className="grid grid-cols-2 sm:grid-cols-5">
        {Array.from({ length: 5 }).map((_, index) => (
          <div
            key={`discharge-summary-skeleton-${index}`}
            className="border-border/60 flex flex-col gap-2 border-t px-3 py-3 first:pl-0 sm:border-t-0 sm:border-l sm:first:border-l-0 sm:first:pl-0"
          >
            <Skeleton className="h-3 w-16" />
            <Skeleton className="h-7 w-10" />
          </div>
        ))}
      </div>
    </Card>
  )
}
