import type { ReactNode } from "react"

interface AppShellProps {
  header: ReactNode
  /** Rendered between the header and page content, e.g. TopNavigation. */
  nav?: ReactNode
  children: ReactNode
}

/** Top-level application shell: responsive container + semantic landmarks. */
export function AppShell({ header, nav, children }: AppShellProps) {
  return (
    <div className="bg-background min-h-svh">
      <div className="mx-auto flex max-w-6xl flex-col px-4 py-6 sm:px-6 lg:px-8">
        {header}
        {nav ? <div className="-mx-4 mt-4 px-4 sm:mx-0 sm:px-0">{nav}</div> : null}
        <main className="mt-6 flex flex-col gap-8">{children}</main>
      </div>
    </div>
  )
}
