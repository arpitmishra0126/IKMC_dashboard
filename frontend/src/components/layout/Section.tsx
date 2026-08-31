import type { ReactNode } from "react"

interface SectionProps {
  title: string
  description?: string
  children: ReactNode
  /** Rendered top-right of the section header, e.g. a status badge. */
  actions?: ReactNode
}

/** Reusable page-section wrapper: heading + optional description + content. */
export function Section({ title, description, children, actions }: SectionProps) {
  return (
    <section
      aria-labelledby={sectionHeadingId(title)}
      className="animate-fade-in-up flex flex-col gap-4"
    >
      <div className="border-border/70 flex flex-wrap items-end justify-between gap-2 border-b pb-3">
        <div>
          <h2
            id={sectionHeadingId(title)}
            className="text-foreground text-xl font-semibold tracking-tight"
          >
            {title}
          </h2>
          {description ? (
            <p className="text-muted-foreground mt-1 text-sm leading-relaxed">{description}</p>
          ) : null}
        </div>
        {actions}
      </div>
      {children}
    </section>
  )
}

function sectionHeadingId(title: string): string {
  return `section-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`
}
