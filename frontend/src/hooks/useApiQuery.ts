import { useCallback, useEffect, useRef, useState } from "react"

import { ApiError } from "@/services/apiClient"

export interface UseApiQueryResult<T> {
  data: T | null
  error: ApiError | null
  isLoading: boolean
  /** True only on the very first load (no stale data to show yet). */
  isInitialLoading: boolean
  refetch: () => void
}

/**
 * Minimal fetch-state hook shared by every dashboard section. Deliberately
 * small (no caching/retry library) since the initial React foundation only
 * needs loading / error / data states for a handful of read-only GET
 * endpoints.
 */
export function useApiQuery<T>(
  queryFn: (signal: AbortSignal) => Promise<T>
): UseApiQueryResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<ApiError | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isInitialLoading, setIsInitialLoading] = useState(true)
  const [refetchToken, setRefetchToken] = useState(0)
  const queryFnRef = useRef(queryFn)
  queryFnRef.current = queryFn

  useEffect(() => {
    const controller = new AbortController()
    setIsLoading(true)
    setError(null)

    queryFnRef
      .current(controller.signal)
      .then((result) => {
        if (controller.signal.aborted) return
        setData(result)
      })
      .catch((err: unknown) => {
        if (controller.signal.aborted) return
        setError(err instanceof ApiError ? err : new ApiError(0, "Unexpected error."))
      })
      .finally(() => {
        if (controller.signal.aborted) return
        setIsLoading(false)
        setIsInitialLoading(false)
      })

    return () => controller.abort()
  }, [refetchToken])

  const refetch = useCallback(() => setRefetchToken((token) => token + 1), [])

  return { data, error, isLoading, isInitialLoading, refetch }
}
