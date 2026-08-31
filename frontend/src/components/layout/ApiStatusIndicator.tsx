import { AlertCircle, Loader2 } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { useApiHealth } from "@/hooks/useApiHealth"

/**
 * Live indicator of whether the React app can reach the FastAPI backend
 * (GET /api/health). Purely a connectivity signal - it does not reflect
 * whether the upstream data source (services/config.py DATA_SOURCE) is
 * itself healthy.
 */
export function ApiStatusIndicator() {
  const { data, error, isInitialLoading } = useApiHealth()

  if (isInitialLoading) {
    return (
      <Badge variant="muted" aria-live="polite">
        <Loader2 className="size-3 animate-spin" aria-hidden="true" />
        Checking API…
      </Badge>
    )
  }

  if (error || !data) {
    return (
      <Badge variant="destructive" role="status" aria-live="polite">
        <AlertCircle className="size-3" aria-hidden="true" />
        API unreachable
      </Badge>
    )
  }

  return (
    <Badge variant="success" role="status" aria-live="polite">
      <span className="relative flex size-2" aria-hidden="true">
        <span className="bg-success-foreground/60 absolute inline-flex size-full animate-ping rounded-full opacity-75" />
        <span className="bg-success-foreground relative inline-flex size-2 rounded-full" />
      </span>
      API connected
    </Badge>
  )
}
