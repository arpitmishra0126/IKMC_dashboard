import { useEffect, useRef, useState } from "react"
import { Activity, CheckCircle2, RefreshCw } from "lucide-react"

import { ApiStatusIndicator } from "@/components/layout/ApiStatusIndicator"
import { ThemeToggle } from "@/components/layout/ThemeToggle"
import { SyncMetadataDisplay } from "@/components/dashboard/SyncMetadataDisplay"
import { Button } from "@/components/ui/button"
import { ApiError } from "@/services/apiClient"
import { refreshData } from "@/services/dashboardService"

interface HeaderProps {
  onDataRefreshed: () => void
}

type RefreshState = "idle" | "loading" | "success" | "error"

/**
 * Reproduces components/dashboard_header.py: title, subtitle, sync
 * metadata, and a refresh action. Unlike the Streamlit version (which
 * clears st.cache_data and calls st.rerun()), the refresh button here
 * calls POST /api/meta/refresh (same cache-clear effect on the backend)
 * and then asks the dashboard page to re-fetch its sections.
 */
export function Header({ onDataRefreshed }: HeaderProps) {
  const [refreshState, setRefreshState] = useState<RefreshState>("idle")
  const [refreshErrorMessage, setRefreshErrorMessage] = useState<string | null>(null)
  const successTimeoutRef = useRef<number | undefined>(undefined)

  useEffect(() => () => window.clearTimeout(successTimeoutRef.current), [])

  async function handleRefresh() {
    setRefreshState("loading")
    setRefreshErrorMessage(null)
    try {
      await refreshData()
      onDataRefreshed()
      setRefreshState("success")
      successTimeoutRef.current = window.setTimeout(() => setRefreshState("idle"), 2000)
    } catch (err) {
      setRefreshState("error")
      setRefreshErrorMessage(err instanceof ApiError ? err.detail : "Refresh failed.")
    }
  }

  return (
    <header className="border-border/70 flex flex-col gap-5 border-b pb-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div className="flex items-start gap-3.5">
          <span className="bg-primary/10 text-primary ring-primary/10 mt-0.5 hidden rounded-xl p-2.5 ring-1 sm:flex">
            <Activity className="size-6" aria-hidden="true" />
          </span>
          <div>
            <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
              iKMC Monitoring System
            </h1>
            <p className="text-muted-foreground mt-1.5 max-w-2xl text-sm leading-relaxed">
              Facility-wide monitoring of SSC, KMC, breastfeeding compliance, cohort
              performance, and discharge outcomes.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <ApiStatusIndicator />
          <ThemeToggle />
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={refreshState === "loading"}
            aria-busy={refreshState === "loading"}
          >
            {refreshState === "success" ? (
              <CheckCircle2 className="text-success" aria-hidden="true" />
            ) : (
              <RefreshCw
                className={refreshState === "loading" ? "animate-spin" : ""}
                aria-hidden="true"
              />
            )}
            {refreshState === "success" ? "Refreshed" : "Refresh Dashboard"}
          </Button>
        </div>
      </div>

      <SyncMetadataDisplay />

      {refreshErrorMessage ? (
        <p role="alert" className="text-destructive text-sm">
          {refreshErrorMessage}
        </p>
      ) : null}
    </header>
  )
}
