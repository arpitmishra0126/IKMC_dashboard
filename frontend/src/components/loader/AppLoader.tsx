import { EcgWave } from "@/components/loader/EcgWave"

export type AppLoaderPhase = "please-wait" | "loading" | "error"

interface AppLoaderProps {
  phase: AppLoaderPhase
  onRetry: () => void
}

/**
 * Full-screen pure-black startup loader. Stage 1 ("please-wait") and stage 2
 * ("loading", the ECG waveform) share this one fixed overlay - only its
 * inner content changes - so there is never a gap or mismatched background
 * between stages. Rendering/gating lives in AppInitializer; this component
 * is purely presentational.
 */
export function AppLoader({ phase, onRetry }: AppLoaderProps) {
  return (
    <div className="app-loader" role="status" aria-live="polite">
      {phase === "please-wait" && <p className="app-loader-please-wait">Please Wait</p>}

      {phase === "loading" && (
        <div className="app-loader-content">
          <EcgWave />
          <p className="app-loader-title">Loading iKMC Monitoring System...</p>
          <p className="app-loader-subtitle">Please wait a moment</p>
        </div>
      )}

      {phase === "error" && (
        <div className="app-loader-content">
          <p className="app-loader-title">Unable to connect to the server</p>
          <p className="app-loader-subtitle">
            Please check your connection and try again.
          </p>
          <button type="button" className="app-loader-retry" onClick={onRetry}>
            Retry
          </button>
        </div>
      )}
    </div>
  )
}
