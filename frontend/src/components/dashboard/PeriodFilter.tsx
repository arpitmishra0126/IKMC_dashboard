import { CalendarDays } from "lucide-react"
import { useState } from "react"

import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

const OPTIONS: Array<{ value: OverviewPeriod; label: string }> = [
  { value: "all", label: "All Data" },
  { value: "7d", label: "Last 7 Days" },
  { value: "30d", label: "Last 30 Days" },
  { value: "3m", label: "Last 3 Months" },
]

interface PeriodFilterProps {
  value: OverviewPeriod
  onChange: (period: OverviewPeriod) => void
  /** True when a custom From/To range (not one of the preset buttons) is
   * the one currently driving the dashboard - so none of the preset
   * buttons render as active. */
  isCustomActive: boolean
  onApplyCustomRange: (range: OverviewDateRange) => void
}

/**
 * Reporting Period selector for the 3 Overview KPI cards, the 4 discharge
 * outcome counts, and the Total Cases summary (see GET
 * /api/dashboard/overview's `period`/`from_date`/`to_date` query params -
 * both filtered by the STUDY ENROLLMENT DATE, mother.enr_dof). Nothing
 * else on the Overview page or any other route reads this value.
 *
 * Two rows: the existing preset buttons (unchanged, still apply
 * immediately on click - matching the segmented-tray visual language used
 * elsewhere), plus a custom From/To date range below it. The date inputs
 * are local, uncommitted draft state - the dashboard only refetches with
 * the new range once "Apply" is clicked, never as the dates change.
 */
export function PeriodFilter({ value, onChange, isCustomActive, onApplyCustomRange }: PeriodFilterProps) {
  const [fromDate, setFromDate] = useState("")
  const [toDate, setToDate] = useState("")

  const bothDatesGiven = fromDate !== "" && toDate !== ""
  const rangeInvalid = bothDatesGiven && fromDate > toDate
  const canApply = bothDatesGiven && !rangeInvalid

  return (
    <div className="flex flex-col items-end gap-2">
      <div
        role="group"
        aria-label="Data period"
        className="bg-muted/60 border-border/70 inline-flex items-center gap-1 rounded-xl border p-1"
      >
        {OPTIONS.map((option) => {
          const isActive = !isCustomActive && option.value === value
          return (
            <button
              key={option.value}
              type="button"
              aria-pressed={isActive}
              onClick={() => onChange(option.value)}
              className={cn(
                "focus-visible:ring-ring rounded-lg px-3 py-1.5 text-xs font-semibold whitespace-nowrap outline-none transition-all duration-150 focus-visible:ring-2",
                isActive
                  ? "bg-primary text-primary-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-card hover:text-foreground"
              )}
            >
              {option.label}
            </button>
          )
        })}
      </div>

      <div className="flex flex-wrap items-center justify-end gap-2">
        <span className="text-muted-foreground flex items-center gap-1 text-xs font-medium whitespace-nowrap">
          <CalendarDays className="size-3.5 shrink-0" aria-hidden="true" />
          Reporting Period:
        </span>
        <label className="sr-only" htmlFor="reporting-period-from">
          From date
        </label>
        <input
          id="reporting-period-from"
          type="date"
          value={fromDate}
          max={toDate || undefined}
          onChange={(event) => setFromDate(event.target.value)}
          className="bg-card border-border/70 text-foreground focus-visible:ring-ring h-8 rounded-md border px-2 text-xs outline-none focus-visible:ring-2"
        />
        <label className="sr-only" htmlFor="reporting-period-to">
          To date
        </label>
        <input
          id="reporting-period-to"
          type="date"
          value={toDate}
          min={fromDate || undefined}
          onChange={(event) => setToDate(event.target.value)}
          className="bg-card border-border/70 text-foreground focus-visible:ring-ring h-8 rounded-md border px-2 text-xs outline-none focus-visible:ring-2"
        />
        <Button
          type="button"
          size="sm"
          disabled={!canApply}
          onClick={() => onApplyCustomRange({ from: fromDate, to: toDate })}
        >
          Apply
        </Button>
      </div>

      {rangeInvalid ? (
        <p className="text-destructive text-xs font-medium">From Date cannot be after To Date.</p>
      ) : null}
    </div>
  )
}
