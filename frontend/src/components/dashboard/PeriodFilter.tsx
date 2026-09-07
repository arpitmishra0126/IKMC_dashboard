import { cn } from "@/lib/utils"
import type { OverviewPeriod } from "@/types/overview"

const OPTIONS: Array<{ value: OverviewPeriod; label: string }> = [
  { value: "all", label: "All Data" },
  { value: "7d", label: "Last 7 Days" },
  { value: "30d", label: "Last 30 Days" },
  { value: "3m", label: "Last 3 Months" },
]

interface PeriodFilterProps {
  value: OverviewPeriod
  onChange: (period: OverviewPeriod) => void
}

/**
 * Compact period selector for the 3 Overview KPI cards only (Pre-Screened /
 * Screened / Eligible for Enrollment - see GET /api/dashboard/overview's
 * `period` query param). Nothing else on the Overview page or any other
 * route reads this value. Visual language matches the existing
 * TopNavigation segmented tray, rather than introducing a new control
 * style.
 */
export function PeriodFilter({ value, onChange }: PeriodFilterProps) {
  return (
    <div
      role="group"
      aria-label="Data period"
      className="bg-muted/60 border-border/70 inline-flex items-center gap-1 rounded-xl border p-1"
    >
      {OPTIONS.map((option) => {
        const isActive = option.value === value
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
  )
}
