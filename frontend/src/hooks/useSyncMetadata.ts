import { useApiQuery } from "@/hooks/useApiQuery"
import { getSyncMetadata } from "@/services/dashboardService"

export function useSyncMetadata() {
  return useApiQuery(getSyncMetadata)
}
