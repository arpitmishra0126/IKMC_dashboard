import { useApiQuery } from "@/hooks/useApiQuery"
import { getDischarge } from "@/services/dashboardService"
import type { OverviewDateRange, OverviewPeriod } from "@/types/overview"

export function useDischarge(period: OverviewPeriod = "all", customRange?: OverviewDateRange) {
  return useApiQuery(
    (signal) => getDischarge(period, customRange, signal),
    [period, customRange?.from, customRange?.to]
  )
}
