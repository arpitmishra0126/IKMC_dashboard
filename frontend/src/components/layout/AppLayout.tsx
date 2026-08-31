import { useCallback, useState } from "react"
import { Outlet } from "react-router-dom"

import { AppShell } from "@/components/layout/AppShell"
import { Header } from "@/components/layout/Header"
import { TopNavigation } from "@/components/layout/TopNavigation"

/**
 * Route layout shared by every page (Overview/Inborn/Outborn/Discharge):
 * Header + TopNavigation stay mounted across navigation, only the routed
 * page content (<Outlet/>) changes. "Refresh Dashboard" in the Header
 * remounts the current page's content (via the `refreshSignal` key), so it
 * refetches whichever page is active - the same remount-to-refetch pattern
 * used before this phase, now scoped per-route instead of Overview-only.
 */
export function AppLayout() {
  const [refreshSignal, setRefreshSignal] = useState(0)

  const handleDataRefreshed = useCallback(() => {
    setRefreshSignal((value) => value + 1)
  }, [])

  return (
    <AppShell
      header={<Header onDataRefreshed={handleDataRefreshed} />}
      nav={<TopNavigation />}
    >
      <div key={refreshSignal} className="flex flex-col gap-8">
        <Outlet />
      </div>
    </AppShell>
  )
}
