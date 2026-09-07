import type { ReactNode } from "react"

export interface MetricComparisonRow {
  label: string
  nvd: ReactNode
  csection: ReactNode
}

interface MetricComparisonTableProps {
  rows: MetricComparisonRow[]
  /** Defaults to "NVD" / "C-Section" - override for e.g. coverage-only tables. */
  leftColumnLabel?: string
  rightColumnLabel?: string
}

/**
 * Reusable NVD-vs-C-Section metric table shared by the cohort summary
 * cards (Overview) and the Inborn/Outborn detail pages, so the same
 * comparison layout/markup isn't duplicated per page. Purely presentational
 * - callers supply already-formatted, already-computed values (no
 * calculation happens here).
 */
export function MetricComparisonTable({
  rows,
  leftColumnLabel = "NVD",
  rightColumnLabel = "C-Section",
}: MetricComparisonTableProps) {
  return (
    <div className="overflow-x-auto rounded-md border">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="bg-muted/60 text-muted-foreground text-xs uppercase tracking-wide">
            <th className="px-3 py-2 font-semibold">Metric</th>
            <th className="px-3 py-2 font-semibold">{leftColumnLabel}</th>
            <th className="px-3 py-2 font-semibold">{rightColumnLabel}</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.label} className="border-border/60 border-t">
              <td className="text-muted-foreground px-3 py-2 font-medium">{row.label}</td>
              <td className="px-3 py-2 tabular-nums">{row.nvd}</td>
              <td className="px-3 py-2 tabular-nums">{row.csection}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
