import { Moon, Sun } from "lucide-react"

import { Button } from "@/components/ui/button"
import { useTheme } from "@/hooks/useTheme"

/**
 * Global dark/light toggle. Shows the icon for the mode a click will
 * switch TO (Sun while dark - click for light; Moon while light - click
 * for dark), matching the existing Refresh Dashboard button's style.
 */
export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()
  const isDark = theme === "dark"
  const label = isDark ? "Switch to light mode" : "Switch to dark mode"

  return (
    <Button variant="outline" size="sm" onClick={toggleTheme} title={label} aria-label={label}>
      {isDark ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
    </Button>
  )
}
