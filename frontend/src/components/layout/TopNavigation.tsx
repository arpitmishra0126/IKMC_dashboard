import { useEffect, useState } from "react"
import { Menu, X } from "lucide-react"
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
  { label: "Data Quality", to: "/data-quality", matchPaths: ["/data-quality"] },
]

/**
 * Primary application-level navigation, placed below the Header.
 * - sm and up: a centered, button-like tab group (unchanged). Active item is
 *   indicated by a filled accent background AND `aria-current="page"` (not
 *   color alone).
 * - below sm (mobile): a single "menu" button showing the current section
 *   that toggles a stacked list of touch-sized links (44px rows). It closes
 *   on selection, on Escape, and when the route changes.
 */
export function TopNavigation() {
  const location = useLocation()
  const [open, setOpen] = useState(false)

  useEffect(() => setOpen(false), [location.pathname])

  useEffect(() => {
    if (!open) return
    const onKey = (event: KeyboardEvent) => event.key === "Escape" && setOpen(false)
    window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  }, [open])

  const activeItem = NAV_ITEMS.find((item) => item.matchPaths.includes(location.pathname))

  return (
    <nav aria-label="Dashboard sections">
      <div className="sm:hidden">
        <button
          type="button"
          onClick={() => setOpen((value) => !value)}
          aria-expanded={open}
          aria-controls="mobile-nav-list"
          className="bg-muted/60 border-border/70 focus-visible:ring-ring flex min-h-11 w-full items-center justify-between rounded-xl border px-4 text-sm font-semibold outline-none focus-visible:ring-2"
        >
          <span>{activeItem?.label ?? "Menu"}</span>
          {open ? <X className="size-5" aria-hidden="true" /> : <Menu className="size-5" aria-hidden="true" />}
          <span className="sr-only">{open ? "Close menu" : "Open menu"}</span>
        </button>
        {open ? (
          <ul
            id="mobile-nav-list"
            className="bg-card border-border/70 mt-2 flex flex-col gap-1 rounded-xl border p-1 shadow-md"
          >
            {NAV_ITEMS.map((item) => {
              const isActive = item.matchPaths.includes(location.pathname)
              return (
                <li key={item.to}>
                  <Link
                    to={item.to}
                    aria-current={isActive ? "page" : undefined}
                    className={cn(
                      "focus-visible:ring-ring flex min-h-11 items-center rounded-lg px-4 text-sm font-semibold outline-none focus-visible:ring-2",
                      isActive
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:bg-muted hover:text-foreground"
                    )}
                  >
                    {item.label}
                  </Link>
                </li>
              )
            })}
          </ul>
        ) : null}
      </div>

      <ul className="bg-muted/60 border-border/70 mx-auto hidden w-fit max-w-full items-center gap-1 overflow-x-auto rounded-xl border p-1 sm:flex">
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
