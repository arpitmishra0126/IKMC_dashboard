import { useApiQuery } from "@/hooks/useApiQuery"
import { getInborn } from "@/services/dashboardService"

export function useInborn() {
  return useApiQuery(getInborn)
}
