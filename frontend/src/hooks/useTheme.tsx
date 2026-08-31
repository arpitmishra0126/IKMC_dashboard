import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react"

/**
 * Global dark/light theme state.
 *
 * - Theme is applied via a `data-theme="light" | "dark"` attribute on
 *   <html>, which index.css keys its color tokens off of - not via
 *   `prefers-color-scheme`.
 * - Dark is the default on first visit (per requirements), not the
 *   system preference. The user's explicit choice is then persisted to
 *   localStorage and restored on future visits.
 * - `index.html` sets the attribute synchronously (see the inline script
 *   there) before React mounts, so there is no flash of the wrong theme.
 *   This provider reads that already-applied attribute as its initial
 *   state rather than re-deciding the theme, so the two stay in sync.
 */

export type Theme = "dark" | "light"

export const THEME_STORAGE_KEY = "ikmc-theme"

interface ThemeContextValue {
  theme: Theme
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextValue | null>(null)

function readInitialTheme(): Theme {
  if (typeof document === "undefined") return "dark"
  const attr = document.documentElement.getAttribute("data-theme")
  return attr === "light" ? "light" : "dark"
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(readInitialTheme)

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme)
    try {
      window.localStorage.setItem(THEME_STORAGE_KEY, theme)
    } catch {
      // localStorage unavailable (private browsing / disabled storage) -
      // theme still works for the current session, just isn't persisted.
    }
  }, [theme])

  const toggleTheme = useCallback(() => {
    setTheme((current) => (current === "dark" ? "light" : "dark"))
  }, [])

  const value = useMemo<ThemeContextValue>(() => ({ theme, toggleTheme }), [theme, toggleTheme])

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}

export function useTheme(): ThemeContextValue {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider")
  }
  return context
}
