import { useApiQuery } from "@/hooks/useApiQuery"
import { getCohorts } from "@/services/dashboardService"

export function useCohorts() {
  return useApiQuery(getCohorts)
}
