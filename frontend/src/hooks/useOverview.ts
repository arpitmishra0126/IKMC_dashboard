import { useApiQuery } from "@/hooks/useApiQuery"
import { getOverview } from "@/services/dashboardService"
import type { OverviewPeriod } from "@/types/overview"

export function useOverview(period: OverviewPeriod = "all") {
  return useApiQuery((signal) => getOverview(period, signal), [period])
}
