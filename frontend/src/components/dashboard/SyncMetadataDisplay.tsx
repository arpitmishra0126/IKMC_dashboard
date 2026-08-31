import { CalendarClock, RefreshCcw } from "lucide-react"

import { ErrorState } from "@/components/common/ErrorState"
import { Skeleton } from "@/components/ui/skeleton"
import { useSyncMetadata } from "@/hooks/useSyncMetadata"
import { formatDateTime } from "@/lib/format"

/**
 * Displays the two distinct sync-related facts the API exposes, kept
 * deliberately separate per docs/MIGRATION_DECISIONS.md #2:
 *   - latest_screening_date: latest scr_dof present in the data
 *   - api_fetch_timestamp: when the upstream API was actually last called
 *     (null when unavailable, e.g. DATA_SOURCE="json" - never invented)
 */
export function SyncMetadataDisplay() {
  const { data, error, isInitialLoading, refetch } = useSyncMetadata()

  if (isInitialLoading) {
    return (
      <div className="flex flex-wrap gap-4">
        <Skeleton className="h-6 w-56 rounded-full" />
        <Skeleton className="h-6 w-56 rounded-full" />
      </div>
    )
  }

  if (error || !data) {
    return (
      <ErrorState
        title="Sync metadata unavailable"
        message={error?.detail ?? "Unknown error."}
        onRetry={refetch}
      />
    )
  }

  return (
    <dl className="flex flex-wrap gap-2 text-sm">
      <SyncPill
        icon={CalendarClock}
        label="Latest screening date"
        value={formatDateTime(data.latest_screening_date)}
      />
      <SyncPill
        icon={RefreshCcw}
        label="API fetch timestamp"
        value={data.api_fetch_timestamp ? formatDateTime(data.api_fetch_timestamp) : null}
        emptyText="Not available for this data source"
      />
    </dl>
  )
}

function SyncPill({
  icon: Icon,
  label,
  value,
  emptyText,
}: {
  icon: typeof CalendarClock
  label: string
  value: string | null
  emptyText?: string
}) {
  const hasValue = value !== null
  return (
    <div className="bg-muted/60 border-border/70 flex items-center gap-2 rounded-full border px-3 py-1.5">
      <Icon className="text-muted-foreground size-3.5 shrink-0" aria-hidden="true" />
      <dt className="text-muted-foreground text-xs font-medium">{label}:</dt>
      <dd className={hasValue ? "text-foreground text-xs font-semibold" : "text-muted-foreground text-xs italic"}>
        {hasValue ? value : emptyText}
      </dd>
    </div>
  )
}
