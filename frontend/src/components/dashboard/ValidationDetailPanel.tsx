import { Loader2 } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { Collapsible } from "@/components/ui/collapsible"
import { Skeleton } from "@/components/ui/skeleton"
import { useValidationDetail } from "@/hooks/useValidationDetail"
import { formatNumber } from "@/lib/format"

const MAX_ROWS_SHOWN = 25

interface ValidationDetailPanelProps {
  check: string
  triggerLabel: string
}

/**
 * Expandable disclosure backed by GET /api/validation/{check}. Renders the
 * same record-level data as the Streamlit "View Validation Details"
 * expander, capped to the first 25 rows for a readable in-card table (the
 * API response itself is unmodified/uncapped - `row_count` always shows
 * the true total).
 */
export function ValidationDetailPanel({ check, triggerLabel }: ValidationDetailPanelProps) {
  const { data, error, isLoading, load } = useValidationDetail(check)

  return (
    <Collapsible
      className="border-border/70 mt-3 border-t pt-3"
      trigger={<span>{triggerLabel}</span>}
      onOpenChange={(open) => {
        if (open) load()
      }}
    >
      <div className="pt-2">
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
              <div className="max-h-64 overflow-auto rounded-md border">
                <table className="w-full text-left text-xs">
                  <thead className="bg-muted sticky top-0">
                    <tr>
                      {data.columns.map((column) => (
                        <th key={column} className="whitespace-nowrap px-2 py-1.5 font-semibold">
                          {column}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.records.slice(0, MAX_ROWS_SHOWN).map((record, index) => (
                      <tr key={`${check}-row-${index}`} className="border-border/60 border-t">
                        {data.columns.map((column) => (
                          <td key={column} className="text-muted-foreground whitespace-nowrap px-2 py-1.5">
                            {formatCellValue(record[column])}
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
    </Collapsible>
  )
}

function formatCellValue(value: unknown): string {
  if (value === null || value === undefined) return "—"
  return String(value)
}
