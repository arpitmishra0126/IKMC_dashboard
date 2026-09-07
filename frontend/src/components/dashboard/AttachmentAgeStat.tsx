import { formatNumber } from "@/lib/format"
import type { AttachmentStat } from "@/types/common"

function formatHoursMinutes(totalMinutes: number): string {
  const rounded = Math.round(totalMinutes)
  const hours = Math.floor(rounded / 60)
  const minutes = rounded % 60
  return `${hours}h ${minutes}m`
}

/**
 * Compact 3-column Min / Avg / Max attachment-age display, minutes as the
 * primary bold value with an hours+minutes secondary line underneath, plus
 * case count below - shared by every place Attachment Age is shown
 * (Overview Total Cases, Cohort Summary, Inborn, Outborn). Purely
 * presentational: values are read as-is, nothing is recalculated here.
 */
export function AttachmentAgeStat({ stat }: { stat: AttachmentStat }) {
  const columns = [
    { label: "Min", minutes: stat.min_minutes },
    { label: "Avg", minutes: stat.minutes },
    { label: "Max", minutes: stat.max_minutes },
  ]

  return (
    <div className="flex flex-col gap-1">
      <div className="grid grid-cols-3 gap-1 text-center">
        {columns.map((col) => (
          <div key={col.label}>
            <p className="text-muted-foreground text-[10px] font-semibold uppercase tracking-wide">
              {col.label}
            </p>
            <p className="text-sm font-bold tabular-nums">{col.minutes} min</p>
            <p className="text-muted-foreground text-[11px] tabular-nums">
              {formatHoursMinutes(col.minutes)}
            </p>
          </div>
        ))}
      </div>
      <p className="text-muted-foreground text-center text-[11px]">
        {formatNumber(stat.case_count)} cases
      </p>
    </div>
  )
}
