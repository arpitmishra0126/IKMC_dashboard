import { useApiQuery } from "@/hooks/useApiQuery"
import { getOverview } from "@/services/dashboardService"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

export function useOverview(period: OverviewPeriod = "all", customRange?: OverviewDateRange) {
  return useApiQuery(
    (signal) => getOverview(period, customRange, signal),
    [period, customRange?.from, customRange?.to]
  )
}
