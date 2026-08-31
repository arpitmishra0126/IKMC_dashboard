import { AlertTriangle } from "lucide-react"

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"

interface ErrorStateProps {
  title?: string
  message: string
  onRetry?: () => void
}

/** Reusable error state for any section that failed to load from the API. */
export function ErrorState({ title = "Couldn't load this data", message, onRetry }: ErrorStateProps) {
  return (
    <Alert variant="destructive" role="alert">
      <AlertTriangle aria-hidden="true" />
      <AlertTitle>{title}</AlertTitle>
      <AlertDescription>
        <p>{message}</p>
        {onRetry ? (
          <Button variant="outline" size="sm" onClick={onRetry} className="mt-1">
            Retry
          </Button>
        ) : null}
      </AlertDescription>
    </Alert>
  )
}
