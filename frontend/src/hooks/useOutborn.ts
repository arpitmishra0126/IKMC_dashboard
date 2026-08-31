import { useApiQuery } from "@/hooks/useApiQuery"
import { getOutborn } from "@/services/dashboardService"

export function useOutborn() {
  return useApiQuery(getOutborn)
}
