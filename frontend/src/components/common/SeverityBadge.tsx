import { AlertTriangle, CheckCircle2 } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import type { Severity } from "@/lib/severity"

interface SeverityBadgeProps {
  severity: Severity
  children: React.ReactNode
  className?: string
}

/**
 * Status is always communicated with both an icon AND text/color together,
 * never color alone (WCAG 1.4.1) - the icon shape itself distinguishes
 * "clear" from "needs attention" even without color perception.
 */
export function SeverityBadge({ severity, children, className }: SeverityBadgeProps) {
  const Icon = severity === "success" ? CheckCircle2 : AlertTriangle
  return (
    <Badge
      variant={severity === "success" ? "success" : "warning"}
      className={cn("gap-1.5", className)}
    >
      <Icon className="size-3.5" aria-hidden="true" />
      {children}
    </Badge>
  )
}
