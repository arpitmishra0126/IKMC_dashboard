import { useApiQuery } from "@/hooks/useApiQuery"
import { getDataQuality } from "@/services/dashboardService"

export function useDataQuality() {
  return useApiQuery(getDataQuality)
}
