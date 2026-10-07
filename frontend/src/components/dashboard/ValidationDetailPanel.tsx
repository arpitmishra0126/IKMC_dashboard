import { useEffect } from "react"
import { Loader2 } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { Skeleton } from "@/components/ui/skeleton"
import { useValidationDetail } from "@/hooks/useValidationDetail"
import { formatNumber } from "@/lib/format"

const MAX_ROWS_SHOWN = 25

interface ValidationDetailPanelProps {
  check: string
}

interface ColumnSpec {
  header: string
  render: (record: Record<string, unknown>) => string
  /** Extra classes for the body cells (e.g. to emphasise a key column). */
  cellClassName?: string
}

/**
 * Presentation-only column set for the initiation-before-birth check. The
 * API still returns every column (separate date/time fields, numeric gap in
 * hours); this just shows a compact subset with exact datetimes and a
 * human-readable gap.
 */
const INITIATION_COLUMNS: ColumnSpec[] = [
  { header: "Record ID", render: (r) => (r["Record ID"] ? `S${r["Record ID"]}` : "—") },
  { header: "Baby ID", render: (r) => formatCellValue(r["Baby ID"]) },
  { header: "Source", render: (r) => formatCellValue(r["Source"]) },
  { header: "Birth", render: (r) => formatDateTime(r["Birth DateTime"]) },
  { header: "Initiation", render: (r) => formatDateTime(r["Initiation DateTime"]) },
  {
    header: "Gap",
    render: (r) => formatGap(r["Gap (hours)"]),
    cellClassName: "text-warning font-semibold tabular-nums",
  },
]

const CUSTOM_COLUMNS: Record<string, ColumnSpec[]> = {
  "initiation-before-birth": INITIATION_COLUMNS,
}

/**
 * Record table backed by GET /api/validation/{check}, rendered by
 * DataQualitySection below the card grid at the grid's full width. Capped to
 * the first 25 rows for readability (the API response is unmodified;
 * `row_count` always shows the true total). Loads once on mount - the parent
 * remounts it (key=check) when a different card is opened.
 */
export function ValidationDetailPanel({ check }: ValidationDetailPanelProps) {
  const { data, error, isLoading, load } = useValidationDetail(check)

  useEffect(() => {
    load()
  }, [load])

  const columns: ColumnSpec[] =
    CUSTOM_COLUMNS[check] ??
    (data?.columns ?? []).map((column) => ({
      header: column,
      render: (r: Record<string, unknown>) => formatCellValue(r[column]),
    }))

  return (
    <div>
      {isLoading ? (
        <div className="flex items-center gap-2 py-2">
          <Loader2 className="text-muted-foreground size-3.5 animate-spin" aria-hidden="true" />
          <Skeleton className="h-3 w-40" />
        </div>
      ) : null}

      {error ? (
        <ErrorState message={error.detail} title="Couldn't load detail rows" onRetry={load} />
      ) : null}

      {data ? (
        data.row_count === 0 ? (
          <p className="text-muted-foreground text-xs">No records for this check.</p>
        ) : (
          <div>
            <p className="text-muted-foreground mb-2 text-xs">
              Showing {formatNumber(Math.min(data.row_count, MAX_ROWS_SHOWN))} of{" "}
              {formatNumber(data.row_count)} record{data.row_count === 1 ? "" : "s"}
            </p>
            <div className="max-h-80 overflow-auto rounded-md border">
              <table className="w-full text-left text-xs">
                <thead className="bg-muted sticky top-0">
                  <tr>
                    {columns.map((column) => (
                      <th key={column.header} className="whitespace-nowrap px-3 py-2 font-semibold">
                        {column.header}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.records.slice(0, MAX_ROWS_SHOWN).map((record, index) => (
                    <tr key={`${check}-row-${index}`} className="border-border/60 border-t">
                      {columns.map((column) => (
                        <td
                          key={column.header}
                          className={`whitespace-nowrap px-3 py-2 ${column.cellClassName ?? "text-muted-foreground"}`}
                        >
                          {column.render(record)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )
      ) : null}
    </div>
  )
}

function formatCellValue(value: unknown): string {
  if (value === null || value === undefined) return "—"
  return String(value)
}

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

/** "2026-08-11 13:05:00" -> "11 Aug 2026 · 1:05 PM". Display only: parsed from
 * the string, no Date object / timezone conversion. Unparseable input is
 * shown as-is. */
function formatDateTime(value: unknown): string {
  if (typeof value !== "string" || value === "") return "—"
  const match = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})/.exec(value)
  if (!match) return value
  const [, year, month, day, hour, minute] = match
  const h = Number(hour)
  const hour12 = h % 12 === 0 ? 12 : h % 12
  return `${Number(day)} ${MONTHS[Number(month) - 1]} ${year} · ${hour12}:${minute} ${h < 12 ? "AM" : "PM"}`
}

/** Hours (signed) -> "−11h 55m" / "−1d 3h 20m", rounded to the nearest minute.
 * Zero-valued leading units are dropped; a true minus sign (U+2212) is used. */
function formatGap(value: unknown): string {
  if (typeof value !== "number" || Number.isNaN(value)) return "—"
  const totalMinutes = Math.round(Math.abs(value) * 60)
  const days = Math.floor(totalMinutes / 1440)
  const hours = Math.floor((totalMinutes % 1440) / 60)
  const minutes = totalMinutes % 60
  const parts = [days > 0 ? `${days}d` : "", days > 0 || hours > 0 ? `${hours}h` : "", `${minutes}m`]
  const sign = value < 0 && totalMinutes > 0 ? "−" : ""
  return sign + parts.filter(Boolean).join(" ")
}
