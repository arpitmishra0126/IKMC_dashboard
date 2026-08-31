import { useApiQuery } from "@/hooks/useApiQuery"
import { getOverview } from "@/services/dashboardService"

export function useOverview() {
  return useApiQuery(getOverview)
}
