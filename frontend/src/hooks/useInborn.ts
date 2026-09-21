import { useApiQuery } from "@/hooks/useApiQuery"
import { getInborn } from "@/services/dashboardService"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

export function useInborn(period: OverviewPeriod = "all", customRange?: OverviewDateRange) {
  return useApiQuery(
    (signal) => getInborn(period, customRange, signal),
    [period, customRange?.from, customRange?.to]
  )
}
