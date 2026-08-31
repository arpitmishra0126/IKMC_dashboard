import { useApiQuery } from "@/hooks/useApiQuery"
import { getHealth } from "@/services/dashboardService"

/** Backs the API connection indicator in the app shell / header. */
export function useApiHealth() {
  return useApiQuery(getHealth)
}
