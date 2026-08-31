/** Presentation-only formatting helpers. No business logic lives here. */

export function formatDateTime(isoString: string | null): string {
  if (!isoString) return "—"
  const date = new Date(isoString)
  if (Number.isNaN(date.getTime())) return isoString
  return new Intl.DateTimeFormat("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date)
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-IN").format(value)
}
