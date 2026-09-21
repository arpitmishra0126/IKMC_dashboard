import { Search, X } from "lucide-react"
import { useEffect, useMemo, useState } from "react"
import { createPortal } from "react-dom"

import { Button } from "@/components/ui/button"
import { useApiQuery } from "@/hooks/useApiQuery"
import { formatNumber } from "@/lib/format"
import { getAttachmentCases } from "@/services/dashboardService"
import type { AttachmentCaseRecord, AttachmentScope } from "@/types/attachmentCases"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

export type AttachmentDrawerMode = "min" | "avg" | "max" | "all"

export interface AttachmentDrawerRequest {
  scope: AttachmentScope
  mode: AttachmentDrawerMode
  /** "Inborn → NVD", "Overview → C-Section", etc. */
  contextLabel: string
  /** Only set for min/max - the exact stat value being drilled into, so
   * the matching case(s) can be highlighted/filtered to. */
  targetValue?: number
  /** Only set for avg - the displayed average, for the explanatory note. */
  avgValue?: number
  /** True when this scope's average is a mean of contributing groups'
   * own averages (Inborn/Overview combined cards), not a plain mean of
   * every individual case below (each leaf group - MSNCU, PNC, Outborn -
   * on its own). The note shown for "avg" mode differs accordingly. */
  avgIsCombined?: boolean
  period?: OverviewPeriod
  customRange?: OverviewDateRange
}

function formatDaysHoursMinutes(totalMinutes: number): string {
  const rounded = Math.round(totalMinutes)
  const days = Math.floor(rounded / 1440)
  const remainderAfterDays = rounded % 1440
  const hours = Math.floor(remainderAfterDays / 60)
  const minutes = remainderAfterDays % 60
  return `${days}d ${hours}h ${minutes}m`
}

const MODE_TITLE: Record<AttachmentDrawerMode, string> = {
  min: "Minimum attachment age",
  avg: "Average attachment age",
  max: "Maximum attachment age",
  all: "All contributing cases",
}

/**
 * Compact audit popover for an Attachment Age stat (Min/Avg/Max box or the
 * case count) - shown as a centered, fixed-height overlay so it never
 * pushes the dashboard layout down. Fetches GET /api/dashboard/
 * attachment-cases, which reads the SAME per-case rows already merged to
 * compute the displayed stat (see services.indicators.get_*_attachment_cases()
 * / services.overview_period_metrics.get_overview_attachment_cases()) -
 * nothing here recalculates or approximates that data.
 */
export function AttachmentCaseDrawer({
  request,
  onClose,
}: {
  request: AttachmentDrawerRequest
  onClose: () => void
}) {
  const [search, setSearch] = useState("")

  const { data, error, isLoading } = useApiQuery(
    (signal) => getAttachmentCases(request.scope, request.period ?? "all", request.customRange, signal),
    [request.scope, request.period, request.customRange?.from, request.customRange?.to]
  )

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") onClose()
    }
    document.addEventListener("keydown", handleKeyDown)
    return () => document.removeEventListener("keydown", handleKeyDown)
  }, [onClose])

  const allCases = useMemo(() => data?.cases ?? [], [data])

  const scopedCases = useMemo(() => {
    if (request.mode === "min" || request.mode === "max") {
      if (request.targetValue === undefined) return []
      return allCases.filter((c) => c.minutes !== null && c.minutes === request.targetValue)
    }
    return allCases
  }, [allCases, request.mode, request.targetValue])

  const visibleCases = useMemo(() => {
    const query = search.trim().toLowerCase()
    if (!query) return scopedCases
    return scopedCases.filter(
      (c) =>
        (c.recordid ?? "").toLowerCase().includes(query) ||
        c.scr_babyid.toLowerCase().includes(query)
    )
  }, [scopedCases, search])

  return createPortal(
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="presentation"
      onClick={onClose}
    >
      <div className="bg-background/70 absolute inset-0" aria-hidden="true" />

      <div
        role="dialog"
        aria-modal="true"
        aria-label={`${MODE_TITLE[request.mode]} - ${request.contextLabel}`}
        onClick={(event) => event.stopPropagation()}
        className="bg-card border-border/70 relative flex max-h-[80vh] w-full max-w-md flex-col overflow-hidden rounded-xl border shadow-lg"
      >
        <div className="border-border/70 flex items-start justify-between gap-3 border-b px-4 py-3">
          <div>
            <p className="text-sm font-semibold">{MODE_TITLE[request.mode]}</p>
            <p className="text-muted-foreground text-xs">{request.contextLabel}</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="text-muted-foreground hover:bg-muted hover:text-foreground focus-visible:ring-ring rounded-md p-1 outline-none focus-visible:ring-2"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </div>

        {request.mode === "avg" ? (
          <div className="bg-muted/40 border-border/70 border-b px-4 py-2.5 text-xs">
            {request.avgIsCombined ? (
              <p className="text-muted-foreground">
                This average ({request.avgValue} min) is the mean of each contributing group's own
                average, not a plain average of the individual cases below. The cases below are
                every case feeding into those group averages.
              </p>
            ) : (
              <p className="text-muted-foreground">
                This average ({request.avgValue} min) is the mean of the {formatNumber(scopedCases.length)}{" "}
                case duration(s) shown below.
              </p>
            )}
          </div>
        ) : null}

        {(request.mode === "min" || request.mode === "max") && request.targetValue !== undefined ? (
          <div className="bg-muted/40 border-border/70 border-b px-4 py-2.5 text-xs">
            <p className="text-muted-foreground">
              Case(s) matching the {request.mode === "min" ? "minimum" : "maximum"} value of{" "}
              <span className="text-foreground font-medium">{request.targetValue} min</span>.
            </p>
          </div>
        ) : null}

        {scopedCases.length > 10 ? (
          <div className="border-border/70 border-b px-4 py-2">
            <div className="relative">
              <Search
                className="text-muted-foreground absolute top-1/2 left-2 size-3.5 -translate-y-1/2"
                aria-hidden="true"
              />
              <input
                type="text"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Filter by Record ID or Baby ID"
                className="bg-muted/40 border-border/70 focus-visible:ring-ring h-8 w-full rounded-md border py-1 pr-2 pl-7 text-xs outline-none focus-visible:ring-2"
              />
            </div>
          </div>
        ) : null}

        <div className="min-h-0 flex-1 overflow-y-auto">
          {isLoading ? (
            <p className="text-muted-foreground px-4 py-6 text-center text-xs">Loading cases…</p>
          ) : error ? (
            <p className="text-destructive px-4 py-6 text-center text-xs">{error.detail}</p>
          ) : visibleCases.length === 0 ? (
            <p className="text-muted-foreground px-4 py-6 text-center text-xs">
              No matching cases.
            </p>
          ) : (
            <ul className="divide-border/60 divide-y">
              {visibleCases.map((caseRecord) => (
                <CaseRow key={`${caseRecord.scr_babyid}-${caseRecord.recordid ?? ""}`} caseRecord={caseRecord} />
              ))}
            </ul>
          )}
        </div>

        <div className="border-border/70 flex items-center justify-between border-t px-4 py-2.5">
          <p className="text-muted-foreground text-[11px]">
            {formatNumber(visibleCases.length)} of {formatNumber(scopedCases.length)} case(s)
          </p>
          <Button type="button" size="sm" variant="outline" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </div>,
    document.body
  )
}

function CaseRow({ caseRecord }: { caseRecord: AttachmentCaseRecord }) {
  return (
    <li className="flex items-center justify-between gap-3 px-4 py-2.5">
      <div className="min-w-0">
        <p className="truncate text-xs font-medium">Record ID: {caseRecord.recordid ?? "—"}</p>
        <p className="text-muted-foreground truncate text-[11px]">
          scr_babyid: {caseRecord.scr_babyid}
        </p>
      </div>
      <div className="shrink-0 text-right">
        {caseRecord.minutes === null ? (
          <p className="text-muted-foreground text-xs">—</p>
        ) : (
          <>
            <p className="text-sm font-bold tabular-nums">{caseRecord.minutes} min</p>
            <p className="text-muted-foreground text-[10px] tabular-nums">
              {formatDaysHoursMinutes(caseRecord.minutes)}
            </p>
          </>
        )}
      </div>
    </li>
  )
}
