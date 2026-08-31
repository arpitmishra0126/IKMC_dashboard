import { useApiQuery } from "@/hooks/useApiQuery"
import { getDischarge } from "@/services/dashboardService"

export function useDischarge() {
  return useApiQuery(getDischarge)
}
