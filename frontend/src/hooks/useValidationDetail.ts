import { useCallback, useRef, useState } from "react"

import { ApiError } from "@/services/apiClient"
import { getValidationDetail } from "@/services/dashboardService"
import type { ValidationDetailResponse } from "@/types/validation"

/**
 * Lazily fetches GET /api/validation/{check} - only called when a data
 * quality card's detail panel is actually expanded, so the ~2,300-row
 * missing-baby-ids table (see docs/MIGRATION_DECISIONS.md #4) is never
 * pulled down unless a user asks to see it.
 */
export function useValidationDetail(check: string) {
  const [data, setData] = useState<ValidationDetailResponse | null>(null)
  const [error, setError] = useState<ApiError | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const hasLoadedRef = useRef(false)

  const load = useCallback(() => {
    if (hasLoadedRef.current) return
    hasLoadedRef.current = true
    setIsLoading(true)
    setError(null)

    getValidationDetail(check)
      .then(setData)
      .catch((err: unknown) => {
        hasLoadedRef.current = false
        setError(err instanceof ApiError ? err : new ApiError(0, "Unexpected error."))
      })
      .finally(() => setIsLoading(false))
  }, [check])

  return { data, error, isLoading, load }
}
