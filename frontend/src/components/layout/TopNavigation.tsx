import { Link, useLocation } from "react-router-dom"

import { cn } from "@/lib/utils"

interface NavItem {
  label: string
  to: string
  /** Pathnames that should render this tab as active. */
  matchPaths: string[]
}

const NAV_ITEMS: NavItem[] = [
  { label: "Overview", to: "/", matchPaths: ["/", "/dashboard"] },
  { label: "Inborn", to: "/inborn", matchPaths: ["/inborn"] },
  { label: "Outborn", to: "/outborn", matchPaths: ["/outborn"] },
  { label: "Discharge", to: "/discharge", matchPaths: ["/discharge"] },
]

/**
 * Primary application-level navigation, placed below the Header: a
 * centered, button-like group (not a full-width underlined tab strip, not
 * a sidebar). Active item is indicated by a filled accent background AND
 * an `aria-current="page"` attribute (not color alone). On narrow screens
 * the group stays on one row and scrolls horizontally rather than
 * wrapping.
 */
export function TopNavigation() {
  const location = useLocation()

  return (
    <nav aria-label="Dashboard sections" className="flex justify-center overflow-x-auto">
      <ul className="bg-muted/60 border-border/70 flex items-center gap-1 rounded-xl border p-1">
        {NAV_ITEMS.map((item) => {
          const isActive = item.matchPaths.includes(location.pathname)
          return (
            <li key={item.to}>
              <Link
                to={item.to}
                aria-current={isActive ? "page" : undefined}
                className={cn(
                  "focus-visible:ring-ring inline-flex items-center justify-center whitespace-nowrap rounded-lg border px-4 py-1.5 text-sm font-semibold outline-none transition-all duration-150 focus-visible:ring-2 focus-visible:ring-offset-0",
                  isActive
                    ? "border-primary/20 bg-primary text-primary-foreground shadow-sm"
                    : "text-muted-foreground hover:bg-card hover:text-foreground border-transparent hover:border-border/70 hover:shadow-xs"
                )}
              >
                {item.label}
              </Link>
            </li>
          )
        })}
      </ul>
    </nav>
  )
}
