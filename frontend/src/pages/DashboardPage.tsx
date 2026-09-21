import { CohortSection } from "@/components/dashboard/CohortSection"
import { KpiSection } from "@/components/dashboard/KpiSection"

/**
 * Reproduces app.py's structure: KPI cards -> cohort summary. Header +
 * navigation now live in AppLayout (shared across all routes) - this page
 * renders unchanged from before Phase 3, only its former ownership of the
 * header/shell moved up a level. Filters (components/filters.py) are
 * intentionally NOT reproduced yet - see docs/MIGRATION_DECISIONS.md #1
 * (they are decorative in the current Streamlit app and out of scope for
 * this step). Data Quality moved out to its own top-level tab - see
 * DataQualityPage.tsx.
 */
export function DashboardPage() {
  return (
    <>
      <KpiSection />
      <CohortSection />
    </>
  )
}
