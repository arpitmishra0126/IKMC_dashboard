import { useId, useState } from "react"
import { ChevronDown } from "lucide-react"

import { cn } from "@/lib/utils"

interface CollapsibleProps {
  trigger: React.ReactNode
  children: React.ReactNode
  className?: string
  defaultOpen?: boolean
  onOpenChange?: (open: boolean) => void
}

/**
 * Minimal, dependency-free disclosure widget. Keyboard-accessible (a real
 * <button> toggling aria-expanded/aria-controls) with a smooth height
 * transition via grid-template-rows (no measuring required).
 */
export function Collapsible({
  trigger,
  children,
  className,
  defaultOpen = false,
  onOpenChange,
}: CollapsibleProps) {
  const [open, setOpen] = useState(defaultOpen)
  const contentId = useId()

  function toggle() {
    setOpen((value) => {
      const next = !value
      onOpenChange?.(next)
      return next
    })
  }

  return (
    <div className={className}>
      <button
        type="button"
        aria-expanded={open}
        aria-controls={contentId}
        onClick={toggle}
        className="text-muted-foreground hover:text-foreground focus-visible:ring-ring flex w-full items-center justify-between gap-2 rounded-md text-left text-xs font-medium outline-none focus-visible:ring-2"
      >
        {trigger}
        <ChevronDown
          aria-hidden="true"
          className={cn("size-3.5 shrink-0 transition-transform duration-200", open && "rotate-180")}
        />
      </button>
      <div
        id={contentId}
        className={cn(
          "grid transition-[grid-template-rows] duration-200 ease-out",
          open ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
        )}
      >
        <div className="overflow-hidden">{children}</div>
      </div>
    </div>
  )
}
