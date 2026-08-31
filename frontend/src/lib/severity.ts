/**
 * Presentation-only severity mapping. This does NOT recompute or
 * reinterpret any backend value - it only decides how an already-returned
 * number should be color/icon-coded in the UI (zero => clear, non-zero =>
 * needs attention). No business logic, threshold, or calculation is
 * introduced beyond this purely visual convenience.
 */
export type Severity = "success" | "warning"

export function severityFromCount(value: number): Severity {
  return value > 0 ? "warning" : "success"
}

/**
 * Derives a severity from the raw `validation_status` string returned by
 * get_validation_status() (e.g. "🟢 Healthy" / "🟡 Review Required"). The
 * string itself is never altered - this only maps its existing content to
 * a badge color so the same fact is legible without relying on emoji alone.
 */
export function severityFromStatusText(status: string): Severity {
  return status.includes("🟢") || status.toLowerCase().includes("healthy")
    ? "success"
    : "warning"
}
