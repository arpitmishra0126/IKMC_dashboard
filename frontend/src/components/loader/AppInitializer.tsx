import { useCallback, useEffect, useRef, useState, type ReactNode } from "react"

import { AppLoader, type AppLoaderPhase } from "@/components/loader/AppLoader"
import { getHealth, getOverview } from "@/services/dashboardService"

/** Minimum time stage 1 ("Please Wait") stays visible before stage 2 takes
 * over, so it reads as a deliberate first screen rather than a one-frame
 * flash. */
const PLEASE_WAIT_MIN_MS = 500

/** How long stage 2 waits for the health check + essential Overview data
 * before treating the backend as unreachable. */
const INIT_TIMEOUT_MS = 20000

type Phase = AppLoaderPhase

/**
 * Gates the dashboard behind the loader: nothing in `children` mounts until
 * the backend health check and the essential Overview/KPI data have both
 * loaded successfully. Does not touch what any dashboard hook/component
 * fetches once revealed - this is initialization gating only.
 */
export function AppInitializer({ children }: { children: ReactNode }) {
  const [phase, setPhase] = useState<Phase>("please-wait")
  const [fadingOut, setFadingOut] = useState(false)
  const [loaderMounted, setLoaderMounted] = useState(true)
  const attemptRef = useRef(0)

  const runInit = useCallback(() => {
    const attempt = ++attemptRef.current
    setPhase("loading")

    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), INIT_TIMEOUT_MS)

    Promise.all([getHealth(controller.signal), getOverview("all", undefined, controller.signal)])
      .then(() => {
        if (attemptRef.current !== attempt) return
        setFadingOut(true)
      })
      .catch(() => {
        if (attemptRef.current !== attempt) return
        setPhase("error")
      })
      .finally(() => clearTimeout(timeout))
  }, [])

  useEffect(() => {
    const t = setTimeout(runInit, PLEASE_WAIT_MIN_MS)
    return () => clearTimeout(t)
  }, [runInit])

  const handleRetry = useCallback(() => {
    setFadingOut(false)
    runInit()
  }, [runInit])

  if (!loaderMounted) {
    return <>{children}</>
  }

  return (
    <>
      <div
        className={fadingOut ? "app-loader app-loader-fade-out" : "app-loader"}
        onAnimationEnd={() => {
          if (fadingOut) setLoaderMounted(false)
        }}
      >
        <AppLoader phase={phase} onRetry={handleRetry} />
      </div>
      {fadingOut ? children : null}
    </>
  )
}
