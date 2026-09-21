import { useApiQuery } from "@/hooks/useApiQuery"
import { getOutborn } from "@/services/dashboardService"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

export function useOutborn(period: OverviewPeriod = "all", customRange?: OverviewDateRange) {
  return useApiQuery(
    (signal) => getOutborn(period, customRange, signal),
    [period, customRange?.from, customRange?.to]
  )
}
