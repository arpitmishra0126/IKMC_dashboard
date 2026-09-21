import { DataQualitySection } from "@/components/dashboard/DataQualitySection"

/**
 * Hosts the "System Validation & Data Quality" section as its own
 * top-level tab (previously rendered inline at the bottom of the Overview
 * page - see DashboardPage.tsx). DataQualitySection itself is unchanged
 * and already self-contained (owns its own Section wrapper, title,
 * description, and severity badge), so this page is just its new home.
 */
export function DataQualityPage() {
  return <DataQualitySection />
}
